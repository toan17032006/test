$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$logDir = Join-Path $env:TEMP ("vulnshop-smoke-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $logDir | Out-Null

function Get-FreeLoopbackPort {
  $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
  $listener.Start()
  try { return ([System.Net.IPEndPoint]$listener.LocalEndpoint).Port }
  finally { $listener.Stop() }
}

function Assert-Equal($actual, $expected, $label) {
  if ($actual -ne $expected) { throw "$label expected '$expected', got '$actual'." }
}

function ConvertTo-Base64Url([string]$value) {
  return [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($value)).TrimEnd('=').Replace('+','-').Replace('/','_')
}

function New-UnsignedTestJwt($payload) {
  $header = ConvertTo-Base64Url '{"alg":"none","typ":"JWT"}'
  $body = ConvertTo-Base64Url ($payload | ConvertTo-Json -Compress)
  return "$header.$body."
}

function New-SignedTestJwt($payload, [string]$secret) {
  $header = ConvertTo-Base64Url '{"alg":"HS256","typ":"JWT"}'
  $body = ConvertTo-Base64Url ($payload | ConvertTo-Json -Compress)
  $message = [Text.Encoding]::UTF8.GetBytes("$header.$body")
  $hmac = [System.Security.Cryptography.HMACSHA256]::new([Text.Encoding]::UTF8.GetBytes($secret))
  try { $signature = [Convert]::ToBase64String($hmac.ComputeHash($message)).TrimEnd('=').Replace('+','-').Replace('/','_') }
  finally { $hmac.Dispose() }
  return "$header.$body.$signature"
}

function Get-ApiErrorMessage([string]$uri, [string]$body) {
  try {
    $null = Invoke-RestMethod -Uri $uri -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 5
    return ''
  } catch {
    $responseBody = $_.ErrorDetails.Message
    if ($responseBody) {
      try {
        $parsed = $responseBody | ConvertFrom-Json
        if ($parsed.detail) { return [string]$parsed.detail }
        if ($parsed.error) { return [string]$parsed.error }
        return $responseBody
      }
      catch { return $responseBody }
    }
    return $_.Exception.Message
  }
}

do { $apiPort = Get-FreeLoopbackPort } while ($apiPort -in @($webPort,$graphqlPort))
do { $webPort = Get-FreeLoopbackPort } while ($webPort -eq $apiPort)
do { $graphqlPort = Get-FreeLoopbackPort } while ($graphqlPort -in @($apiPort,$webPort))
$api = $null
$web = $null
$graphql = $null
$oldEnvironment = @{}
foreach ($name in @('UPLOAD_DIR','API_URL','HOST','PORT','VULNDB_DIR','NODE_ENV','SESSION_SECRET','SECRET_KEY','JWT_SECRET','ADMIN_PASSWORD','AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','SMTP_HOST','SMTP_PORT','DATABASE_URL','MYSQL_URL','MONGODB_URL','REDIS_URL','PYTHONUNBUFFERED')) {
  $oldEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

try {
  $env:UPLOAD_DIR = Join-Path $repoRoot 'uploads'
  $env:SECRET_KEY = 'local-smoke-secret'
  $env:JWT_SECRET = 'local-smoke-jwt'
  $env:PYTHONUNBUFFERED = '1'
  $env:ADMIN_PASSWORD = 'admin123'
  $env:AWS_ACCESS_KEY_ID = 'LAB_ONLY_NOT_A_CREDENTIAL'
  $env:AWS_SECRET_ACCESS_KEY = 'LAB_ONLY_NOT_A_CREDENTIAL'
  $env:SMTP_HOST = '127.0.0.1'
  $env:SMTP_PORT = '1'
  $env:DATABASE_URL = 'postgresql://lab:lab@127.0.0.1:1/vulnshop'
  $env:MYSQL_URL = 'mysql://lab:lab@127.0.0.1:1/vulnshop'
  $env:MONGODB_URL = 'mongodb://127.0.0.1:1/vulnshop'
  $env:REDIS_URL = 'redis://127.0.0.1:1/0'
  $api = Start-Process -FilePath 'python' -ArgumentList @('-m','uvicorn','main:app','--host','127.0.0.1','--port',"$apiPort") -WorkingDirectory (Join-Path $repoRoot 'backend') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logDir 'api.out') -RedirectStandardError (Join-Path $logDir 'api.err')

  $env:API_URL = "http://127.0.0.1:$apiPort"
  $env:HOST = '127.0.0.1'
  $env:PORT = "$webPort"
  $env:SESSION_SECRET = 'local-smoke-session'
  $env:VULNDB_DIR = Join-Path $repoRoot 'vulndb'
  $web = Start-Process -FilePath 'node' -ArgumentList @('server.js') -WorkingDirectory (Join-Path $repoRoot 'frontend') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logDir 'web.out') -RedirectStandardError (Join-Path $logDir 'web.err')

  $env:PORT = "$graphqlPort"
  $graphql = Start-Process -FilePath 'node' -ArgumentList @('src/index.js') -WorkingDirectory (Join-Path $repoRoot 'services/graphql') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logDir 'graphql.out') -RedirectStandardError (Join-Path $logDir 'graphql.err')

  $apiBase = "http://127.0.0.1:$apiPort"
  $webBase = "http://127.0.0.1:$webPort"
  $graphqlBase = "http://127.0.0.1:$graphqlPort"

  $ready = $false
  for ($i = 0; $i -lt 30; $i++) {
    try {
      $null = Invoke-RestMethod -Uri "$apiBase/health" -TimeoutSec 2
      $null = Invoke-WebRequest -Uri "$webBase/admin/vulns" -TimeoutSec 2
      $null = Invoke-RestMethod -Uri "$webBase/api/vuln-catalog" -TimeoutSec 2
      $query = Invoke-RestMethod -Uri "$graphqlBase/graphql" -Method Post -ContentType 'application/json' -Body '{"query":"{ __schema { queryType { name } } }"}' -TimeoutSec 2
      if ($query.data.__schema.queryType.name -eq 'Query') { $ready = $true; break }
    } catch { Start-Sleep -Milliseconds 300 }
  }
  if (-not $ready) { throw 'The local services did not become ready.' }

  $paths = @('/','/products','/products/1','/cart','/checkout','/login','/register','/profile','/admin/vulns')
  foreach ($path in $paths) {
    $response = Invoke-WebRequest -Uri "$webBase$path" -TimeoutSec 8
    Assert-Equal $response.StatusCode 200 "GET $path"
  }

  $catalog = Invoke-RestMethod -Uri "$webBase/api/vuln-catalog" -TimeoutSec 8
  Assert-Equal $catalog.counts.components 275 'Component inventory count'
  Assert-Equal $catalog.counts.vulnerabilities 661 'Vulnerability inventory count'
  Assert-Equal $catalog.counts.attack_chains 29 'Attack-chain inventory count'
  Assert-Equal $catalog.counts.test_matrix_fields 36 'Test-matrix inventory count'

  $docsResponse = Invoke-WebRequest -Uri "$apiBase/docs" -TimeoutSec 5
  Assert-Equal $docsResponse.StatusCode 200 'Unauthenticated API documentation'
  $envResponse = Invoke-WebRequest -Uri "$apiBase/.env" -TimeoutSec 5
  if ($envResponse.Content -notmatch 'AWS_ACCESS_KEY_ID=LAB_ONLY_NOT_A_CREDENTIAL') { throw 'The synthetic environment marker was not exposed by the lab env endpoint.' }

  $bypassBody = '{"admin":true}'
  $bypass = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/bypass" -Method Post -ContentType 'application/json' -Body $bypassBody -TimeoutSec 5
  Assert-Equal $bypass.bypass $true 'Authentication bypass endpoint'
  Assert-Equal $bypass.user.role 'admin' 'Authentication bypass administrator role'

  $defaultLoginBody = @{ email = 'admin@vulnshop.com'; password = 'admin123' } | ConvertTo-Json -Compress
  $defaultLogin = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/login" -Method Post -ContentType 'application/json' -Body $defaultLoginBody -TimeoutSec 5
  Assert-Equal $defaultLogin.user.role 'admin' 'Weak default admin credentials'
  Assert-Equal $defaultLogin.user.password_plain 'admin123' 'Sensitive fields in JWT login response'
  $missingAccountBody = @{ email = "missing-$([guid]::NewGuid().ToString('N'))@example.test"; password = 'wrong' } | ConvertTo-Json -Compress
  $missingAccountMessage = Get-ApiErrorMessage "$apiBase/api/v1/auth/login" $missingAccountBody
  $wrongPasswordBody = @{ email = 'admin@vulnshop.com'; password = 'wrong' } | ConvertTo-Json -Compress
  $wrongPasswordMessage = Get-ApiErrorMessage "$apiBase/api/v1/auth/login" $wrongPasswordBody
  Assert-Equal $missingAccountMessage 'User not found' 'Username enumeration error response'
  Assert-Equal $wrongPasswordMessage 'Invalid password' 'Existing-account enumeration error response'
  for ($attempt = 0; $attempt -lt 5; $attempt++) {
    $rateProbe = Get-ApiErrorMessage "$apiBase/api/v1/auth/login" $wrongPasswordBody
    Assert-Equal $rateProbe 'Invalid password' 'Missing login rate limit'
  }

  $productRecord = Invoke-RestMethod -Uri "$apiBase/api/v1/products/1" -TimeoutSec 5
  Assert-Equal $productRecord.product.price 29990000 'Synthetic product catalog price'
  Assert-Equal $productRecord.internal_data.cost 15000000 'Unauthenticated internal cost disclosure'
  Assert-Equal $productRecord.internal_data.admin_note 'Profit margin 40%' 'Unauthenticated internal business data disclosure'
  $reviewBody = @{ content = 'Synthetic smoke review'; rating = 5; user_name = 'Unauthenticated Reviewer' } | ConvertTo-Json -Compress
  $fakeReview = Invoke-RestMethod -Uri "$apiBase/api/v1/products/1/review" -Method Post -ContentType 'application/json' -Body $reviewBody -TimeoutSec 5
  Assert-Equal $fakeReview.review.user_name 'Unauthenticated Reviewer' 'Fake product review injection'
  $reviewList = Invoke-RestMethod -Uri "$apiBase/api/v1/products/1/reviews" -TimeoutSec 5
  Assert-Equal $reviewList.reviews[0].content 'Synthetic smoke review' 'Unauthenticated review ownership bypass'

  $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
  $null = Invoke-WebRequest -Uri "$webBase/cart" -WebSession $session -TimeoutSec 5
  $added = Invoke-RestMethod -Uri "$webBase/cart/add" -Method Post -WebSession $session -ContentType 'application/json' -Body '{"productId":1,"name":"Lab phone","price":100,"qty":2,"image":"/img/lab.png"}' -TimeoutSec 5
  Assert-Equal $added.cartCount 1 'Storefront cart item count'
  $formBody = 'shipping_name=Lab+User&shipping_address=Synthetic+address&shipping_phone=0900000000&payment_method=cod&total_amount=200&shipping_fee=0&coupon_code='
  $checkout = Invoke-WebRequest -Uri "$webBase/checkout" -Method Post -WebSession $session -ContentType 'application/x-www-form-urlencoded' -Body $formBody -TimeoutSec 8
  Assert-Equal $checkout.StatusCode 200 'Storefront checkout'
  $emptyCart = Invoke-WebRequest -Uri "$webBase/cart" -WebSession $session -TimeoutSec 5
  if ($emptyCart.Content -notmatch 'Giỏ hàng đang trống') { throw 'Checkout did not clear the session cart.' }

  $email = "smoke-$([guid]::NewGuid().ToString('N'))@example.test"
  $registerBody = @{ email = $email; name = 'Lab Smoke User'; password = 'x'; role = 'admin'; is_admin = $true } | ConvertTo-Json -Compress
  $registered = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/register" -Method Post -ContentType 'application/json' -Body $registerBody -TimeoutSec 8
  Assert-Equal $registered.role 'admin' 'Synthetic account registration'
  $registeredProfile = Invoke-RestMethod -Uri "$apiBase/api/v1/users/$($registered.user_id)" -TimeoutSec 5
  Assert-Equal $registeredProfile.password_plain 'x' 'Unauthenticated profile password exposure'
  if ($registeredProfile.password_hash.Length -ne 32) { throw 'The lab password hash was not the expected MD5-sized value.' }
  $md5 = [System.Security.Cryptography.MD5]::Create()
  try { $expectedMd5 = [Convert]::ToHexString($md5.ComputeHash([Text.Encoding]::UTF8.GetBytes('x'))).ToLowerInvariant() }
  finally { $md5.Dispose() }
  Assert-Equal $registeredProfile.password_hash $expectedMd5 'Weak MD5 password storage'
  Assert-Equal $registeredProfile.role 'admin' 'Signup privilege escalation by mass assignment'
  $duplicateRegistrationBody = @{ email = $email; name = 'Duplicate User'; password = 'different' } | ConvertTo-Json -Compress
  $duplicateRegistrationMessage = Get-ApiErrorMessage "$apiBase/api/v1/auth/register" $duplicateRegistrationBody
  if ($duplicateRegistrationMessage -notmatch 'already registered') { throw 'Registration did not distinguish an existing email address.' }
  $verifyBypass = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/verify-email-bypass?email=$email" -TimeoutSec 5
  Assert-Equal $verifyBypass.bypass $true 'Email verification without a token'
  $verifyUrl = "$apiBase/api/v1/auth/verify-email?token=$($registered.verify_token)&email=$email"
  $verifyFirst = Invoke-RestMethod -Uri $verifyUrl -TimeoutSec 5
  $verifyReplay = Invoke-RestMethod -Uri $verifyUrl -TimeoutSec 5
  Assert-Equal $verifyFirst.email $email 'Email verification token use'
  Assert-Equal $verifyReplay.email $email 'Email verification token replay'
  $userHeaders = @{ 'x-user-id' = '2' }
  $unprotectedAdminList = Invoke-RestMethod -Uri "$apiBase/api/v1/admin/users" -TimeoutSec 5
  if ($unprotectedAdminList.total -lt 4) { throw 'The admin user list was not available to an unauthenticated caller.' }
  Assert-Equal $unprotectedAdminList.items[0].password_plain 'admin123' 'Unauthenticated admin PII and credential exposure'
  Assert-Equal $unprotectedAdminList.items[0].email 'admin@vulnshop.com' 'Unauthenticated customer email exposure'
  Assert-Equal $unprotectedAdminList.items[0].phone '0901234567' 'Unauthenticated customer phone exposure'
  if (-not $unprotectedAdminList.items[0].credit_card -or -not $unprotectedAdminList.items[0].ssn) { throw 'The admin list did not expose synthetic PII fields.' }
  $roleChangeBody = '{"role":"admin"}'
  $unauthorizedRoleChange = Invoke-RestMethod -Uri "$apiBase/api/v1/admin/users/2/role" -Method Patch -ContentType 'application/json' -Body $roleChangeBody -TimeoutSec 5
  Assert-Equal $unauthorizedRoleChange.user.role 'admin' 'Unauthenticated user role modification'
  $unprotectedBackup = Invoke-RestMethod -Uri "$apiBase/api/v1/admin/backup" -TimeoutSec 5
  if ($unprotectedBackup.users.Count -lt 3 -or $unprotectedBackup.orders.Count -lt 2) { throw 'The unauthenticated backup endpoint did not return synthetic records.' }
  $couponList = Invoke-RestMethod -Uri "$apiBase/api/v1/coupons" -TimeoutSec 5
  if (-not ($couponList.items | Where-Object { $_.code -eq 'ADMIN' })) { throw 'The unauthenticated coupon list did not expose the synthetic ADMIN coupon.' }
  $otherUserOrder = Invoke-RestMethod -Uri "$apiBase/api/v1/orders/1002" -Headers $userHeaders -TimeoutSec 5
  Assert-Equal $otherUserOrder.user_id '3' 'Unauthenticated cross-user order read'
  $otherUserAddress = Invoke-RestMethod -Uri "$apiBase/api/v1/users/3/addresses" -Headers $userHeaders -TimeoutSec 5
  if ($otherUserAddress.addresses[0].phone -ne '0923456789') { throw 'Cross-user address/phone read did not return the synthetic record.' }
  $loginBody = @{ email = $email; password = 'x' } | ConvertTo-Json -Compress
  $login = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/login" -Method Post -ContentType 'application/json' -Body $loginBody -TimeoutSec 8
  if (-not $login.access_token) { throw 'Login did not return an access token.' }
  $me = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $($login.access_token)" } -TimeoutSec 5
  Assert-Equal $me.user.role 'admin' 'Authenticated profile role'
  Assert-Equal $me.token_payload.password_plain 'x' 'Sensitive password data in JWT claims'

  $rememberBody = @{ email = $email; password = 'x'; remember_me = $true } | ConvertTo-Json -Compress
  $rememberResponse = Invoke-WebRequest -Uri "$apiBase/api/v1/auth/login" -Method Post -ContentType 'application/json' -Body $rememberBody -TimeoutSec 5
  $cookieHeader = [string]::Join('; ', $rememberResponse.Headers['Set-Cookie'])
  if ($cookieHeader -notmatch 'remember_me=') { throw 'The remember-me cookie was not issued.' }
  if ($cookieHeader -notmatch 'Max-Age=99999999') { throw 'The remember-me cookie did not use the lab persistent lifetime.' }
  if ($cookieHeader -notmatch 'SameSite=none') { throw 'The session cookie did not expose its permissive SameSite setting.' }
  if ($cookieHeader -match 'HttpOnly|Secure') { throw 'The test expected session/auth cookies without HttpOnly or Secure flags.' }

  $mfaSetup = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/mfa/setup?email=$email" -Method Post -TimeoutSec 5
  Assert-Equal $mfaSetup.current_otp '123456' 'Predictable MFA one-time password'
  $invalidOtpBody = @{ email = $email; otp = '999999' } | ConvertTo-Json -Compress
  for ($attempt = 0; $attempt -lt 3; $attempt++) {
    $otpError = Get-ApiErrorMessage "$apiBase/api/v1/auth/mfa/verify" $invalidOtpBody
    Assert-Equal $otpError 'Invalid OTP code' 'Missing OTP attempt limit'
  }
  $validOtpBody = @{ email = $email; otp = '123456' } | ConvertTo-Json -Compress
  $validOtpFirst = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/mfa/verify" -Method Post -ContentType 'application/json' -Body $validOtpBody -TimeoutSec 5
  $validOtpReplay = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/mfa/verify" -Method Post -ContentType 'application/json' -Body $validOtpBody -TimeoutSec 5
  if (-not $validOtpFirst.token -or -not $validOtpReplay.token) { throw 'The lab did not accept repeated valid OTP input.' }
  $mfaBody = @{ email = $email; otp = '000000' } | ConvertTo-Json -Compress
  $mfaBypass = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/mfa/verify" -Method Post -ContentType 'application/json' -Body $mfaBody -TimeoutSec 5
  if (-not $mfaBypass.token) { throw 'The MFA backdoor did not return a token.' }
  $mfaReplay = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/mfa/verify" -Method Post -ContentType 'application/json' -Body $mfaBody -TimeoutSec 5
  if (-not $mfaReplay.token) { throw 'The lab did not accept replayed OTP input.' }

  $refreshBody = @{ refresh_token = $login.refresh_token } | ConvertTo-Json -Compress
  $refreshOne = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/refresh" -Method Post -ContentType 'application/json' -Body $refreshBody -TimeoutSec 5
  $refreshTwo = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/refresh" -Method Post -ContentType 'application/json' -Body $refreshBody -TimeoutSec 5
  Assert-Equal $refreshOne.refresh_token $login.refresh_token 'Refresh token reuse'
  Assert-Equal $refreshTwo.refresh_token $login.refresh_token 'Refresh token rotation failure'

  $fixedHeaders = @{ 'X-Session-Id' = 'fixed-lab-session' }
  $fixedLogin = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/login" -Method Post -Headers $fixedHeaders -ContentType 'application/json' -Body $loginBody -TimeoutSec 5
  Assert-Equal $fixedLogin.session_id 'fixed-lab-session' 'Session fixation'
  $null = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/logout" -Method Post -Headers @{ Authorization = "Bearer $($login.access_token)" } -TimeoutSec 5
  $afterLogout = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $($login.access_token)" } -TimeoutSec 5
  Assert-Equal $afterLogout.user.email $email 'Session remained valid after logout'

  $unknownResetBody = @{ email = "unknown-$([guid]::NewGuid().ToString('N'))@example.test" } | ConvertTo-Json -Compress
  $unknownResetMessage = Get-ApiErrorMessage "$apiBase/api/v1/auth/forgot-password" $unknownResetBody
  if ($unknownResetMessage -notmatch 'not found') { throw 'Password reset did not reveal whether the email address exists.' }
  $forgotStart = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $resetEmail = 'admin@vulnshop.com'
  $forgotBody = @{ email = $resetEmail } | ConvertTo-Json -Compress
  $forgotHeaders = @{ Host = 'attacker.invalid'; 'X-Forwarded-Proto' = 'https' }
  $forgot = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/forgot-password" -Method Post -Headers $forgotHeaders -ContentType 'application/json' -Body $forgotBody -TimeoutSec 8
  if (-not $forgot.token) { throw 'The password reset endpoint did not disclose its token.' }
  if ($forgot.reset_url -notmatch '^https://attacker\.invalid/') { throw 'The reset URL did not trust the attacker-controlled Host header.' }
  $forgotEnd = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $tokenPredicted = $false
  $tokenHasher = [System.Security.Cryptography.MD5]::Create()
  try {
    for ($second = $forgotStart - 5; $second -le $forgotEnd + 5; $second++) {
      $candidateRaw = [Text.Encoding]::UTF8.GetBytes(('{0}:{1}:reset' -f $resetEmail, $second))
      $candidate = [Convert]::ToHexString($tokenHasher.ComputeHash($candidateRaw)).ToLowerInvariant().Substring(0,16)
      if ($candidate -eq $forgot.token) { $tokenPredicted = $true; break }
    }
  } finally { $tokenHasher.Dispose() }
  if (-not $tokenPredicted) { throw 'The reset token did not match the timestamp-derived prediction.' }
  $resetBodyOne = @{ token = $forgot.token; new_password = 'reset-one' } | ConvertTo-Json -Compress
  $resetOne = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/reset-password" -Method Post -ContentType 'application/json' -Body $resetBodyOne -TimeoutSec 5
  Assert-Equal $resetOne.new_password 'reset-one' 'Password reset response exposure'
  $resetBodyTwo = @{ token = $forgot.token; new_password = 'reset-two' } | ConvertTo-Json -Compress
  $resetTwo = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/reset-password" -Method Post -ContentType 'application/json' -Body $resetBodyTwo -TimeoutSec 5
  Assert-Equal $resetTwo.new_password 'reset-two' 'Password reset token reuse'
  $newPasswordLoginBody = @{ email = $resetEmail; password = 'reset-two' } | ConvertTo-Json -Compress
  $resetLogin = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/login" -Method Post -ContentType 'application/json' -Body $newPasswordLoginBody -TimeoutSec 5
  if (-not $resetLogin.access_token) { throw 'The unauthenticated reset flow did not change the synthetic account password.' }
  $oldTokenAfterReset = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $($defaultLogin.access_token)" } -TimeoutSec 5
  Assert-Equal $oldTokenAfterReset.user.email $resetEmail 'Session remained valid after password reset'

  $nonePayload = @{ sub = $email; role = 'admin'; exp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 3600 }
  $noneToken = New-UnsignedTestJwt $nonePayload
  $noneAccepted = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $noneToken" } -TimeoutSec 5
  Assert-Equal $noneAccepted.user.email $email 'Unsigned JWT acceptance'
  $expiredPayload = @{ sub = $email; role = 'admin'; exp = 1 }
  $expiredToken = New-SignedTestJwt $expiredPayload 'local-smoke-jwt'
  $expiredAccepted = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $expiredToken" } -TimeoutSec 5
  Assert-Equal $expiredAccepted.expired_token $true 'Expired JWT acceptance'
  $unvalidatedClaims = @{ sub = $email; aud = 'attacker.invalid'; iss = 'https://attacker.invalid'; exp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + 3600 }
  $claimsToken = New-SignedTestJwt $unvalidatedClaims 'local-smoke-jwt'
  $claimsAccepted = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/me" -Headers @{ Authorization = "Bearer $claimsToken" } -TimeoutSec 5
  Assert-Equal $claimsAccepted.user.email $email 'JWT audience and issuer validation'

  $oauthBody = @{ code = 'LAB_FAKE_CODE'; redirect_uri = 'https://attacker.invalid/callback'; state = 'unvalidated-state' } | ConvertTo-Json -Compress
  $oauth = Invoke-RestMethod -Uri "$apiBase/api/v1/auth/social/google" -Method Post -ContentType 'application/json' -Body $oauthBody -TimeoutSec 5
  Assert-Equal $oauth.redirect_uri 'https://attacker.invalid/callback' 'OAuth redirect URI manipulation'
  Assert-Equal $oauth.state 'unvalidated-state' 'OAuth state parameter not validated'
  if (-not $oauth.token) { throw 'The fake OAuth flow did not return its synthetic token.' }

  $addedApiItem = Invoke-RestMethod -Uri "$apiBase/api/v1/cart/items" -Method Post -Headers $userHeaders -ContentType 'application/json' -Body '{"product_id":1,"quantity":2,"unit_price":10}' -TimeoutSec 5
  Assert-Equal $addedApiItem.total 20 'API cart subtotal'
  if ($addedApiItem.item.unit_price -ge $productRecord.product.price) { throw 'The API did not accept the client-supplied below-catalog unit price.' }
  $negativePriceCart = Invoke-RestMethod -Uri "$apiBase/api/v1/cart/items" -Method Post -Headers @{ 'x-user-id' = '4' } -ContentType 'application/json' -Body '{"product_id":4,"quantity":1,"unit_price":-1}' -TimeoutSec 5
  Assert-Equal $negativePriceCart.total -1 'Negative cart price'
  $zeroPriceCart = Invoke-RestMethod -Uri "$apiBase/api/v1/cart/items" -Method Post -Headers @{ 'x-user-id' = '5' } -ContentType 'application/json' -Body '{"product_id":4,"quantity":1,"unit_price":0}' -TimeoutSec 5
  Assert-Equal $zeroPriceCart.total 0 'Zero cart price'
  $negativeQuantityCart = Invoke-RestMethod -Uri "$apiBase/api/v1/cart/items" -Method Post -Headers @{ 'x-user-id' = '6' } -ContentType 'application/json' -Body '{"product_id":4,"quantity":-1,"unit_price":100}' -TimeoutSec 5
  Assert-Equal $negativeQuantityCart.total -100 'Negative cart quantity'
  $victimCart = Invoke-RestMethod -Uri "$apiBase/api/v1/cart/items" -Method Post -Headers @{ 'x-user-id' = '3' } -ContentType 'application/json' -Body '{"product_id":1,"quantity":1,"unit_price":10}' -TimeoutSec 5
  $cartBypass = Invoke-RestMethod -Uri "$apiBase/api/v1/cart?user_id=3" -TimeoutSec 5
  Assert-Equal $cartBypass.items[0].product_id 1 'Unauthenticated cart ownership bypass'
  $couponBody = '{"code":"SALE10","total":100}'
  $couponUseOne = Invoke-RestMethod -Uri "$apiBase/api/v1/coupons/validate" -Method Post -ContentType 'application/json' -Body $couponBody -TimeoutSec 5
  $couponUseTwo = Invoke-RestMethod -Uri "$apiBase/api/v1/coupons/validate" -Method Post -ContentType 'application/json' -Body $couponBody -TimeoutSec 5
  Assert-Equal $couponUseOne.valid $true 'First coupon use'
  Assert-Equal $couponUseTwo.valid $true 'Coupon reuse without a use limit'
  $orderBody = '{"user_id":"3","items":[{"product_id":1,"quantity":1,"unit_price":17}],"total":17}'
  $order = Invoke-RestMethod -Uri "$apiBase/api/v1/orders" -Method Post -Headers $userHeaders -ContentType 'application/json' -Body $orderBody -TimeoutSec 5
  $orderId = $order.order_id
  Assert-Equal $order.order.total 17 'API accepted order total'
  Assert-Equal $order.order.user_id '3' 'Client-controlled order ownership'
  $canceledOrder = Invoke-RestMethod -Uri "$apiBase/api/v1/orders/$orderId/cancel" -Method Post -TimeoutSec 5
  Assert-Equal $canceledOrder.order.status 'cancelled' 'Unauthenticated cross-user order cancellation'
  $payment = Invoke-RestMethod -Uri "$apiBase/api/v1/payment/process" -Method Post -ContentType 'application/json' -Body ("{`"order_id`":$orderId,`"amount`":0}") -TimeoutSec 5
  Assert-Equal $payment.payment.amount 0 'Mock payment accepted a zero amount'
  Assert-Equal $payment.order.payment_status 'paid' 'Mock payment status'
  $duplicatePayment = Invoke-RestMethod -Uri "$apiBase/api/v1/payment/process" -Method Post -ContentType 'application/json' -Body ("{`"order_id`":$orderId,`"amount`":0}") -TimeoutSec 5
  if ($duplicatePayment.payment.id -eq $payment.payment.id) { throw 'Repeated mock payment processing did not create a duplicate payment.' }
  $paymentHistory = Invoke-RestMethod -Uri "$apiBase/api/v1/payment/$orderId" -TimeoutSec 5
  Assert-Equal $paymentHistory.payments.Count 2 'Payment idempotency failure'
  $event = '{"order_id":1002,"status":"paid"}'
  $first = Invoke-RestMethod -Uri "$apiBase/api/v1/webhooks/payment" -Method Post -ContentType 'application/json' -Body $event -TimeoutSec 5
  $replay = Invoke-RestMethod -Uri "$apiBase/api/v1/webhooks/payment" -Method Post -ContentType 'application/json' -Body $event -TimeoutSec 5
  Assert-Equal $first.duplicate_count 1 'First payment callback count'
  Assert-Equal $replay.duplicate_count 2 'Repeated payment callback count'
  $forgedOrder = Invoke-RestMethod -Uri "$apiBase/api/v1/orders/1002" -TimeoutSec 5
  Assert-Equal $forgedOrder.payment_status 'paid' 'Unsigned payment callback state change'
  $refundBody = '{"amount":1}'
  $unauthorizedRefund = Invoke-RestMethod -Uri "$apiBase/api/v1/payment/1002/refund" -Method Post -ContentType 'application/json' -Body $refundBody -TimeoutSec 5
  Assert-Equal $unauthorizedRefund.amount 1 'Unauthenticated refund amount manipulation'
  $refundedOrder = Invoke-RestMethod -Uri "$apiBase/api/v1/orders/1002" -TimeoutSec 5
  Assert-Equal $refundedOrder.payment_status 'refunded' 'Unauthenticated order refund'

  $apiLog = Get-Content -Raw -LiteralPath (Join-Path $logDir 'api.out')
  if ($apiLog -notmatch [regex]::Escape("email=$email password=x role=admin")) { throw 'The synthetic signup password was not present in the lab API log.' }

  Write-Output 'Loopback smoke passed: storefront/catalog, docs/env/backup exposure, coupon discovery/reuse, auth bypass/default credentials/enumeration/rate limits, email/OTP/reset flows, refresh/session/JWT/OAuth flaws, product/customer data exposure and fake reviews, role/order ownership changes, cart price/quantity tampering, duplicate payments, unauthorized cancellation/refunds, payment webhook forgery/replay, and GraphQL introspection.'
}
catch {
  foreach ($name in @('api.err','web.err','graphql.err')) {
    $path = Join-Path $logDir $name
    if (Test-Path $path) {
      $content = Get-Content -Raw -LiteralPath $path
      if ($content) { Write-Output "$name`:`n$content" }
    }
  }
  throw
}
finally {
  foreach ($process in @($web,$api,$graphql)) {
    if ($process -and -not $process.HasExited) { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue }
  }
  foreach ($file in Get-ChildItem -LiteralPath $logDir -File -ErrorAction SilentlyContinue) { Remove-Item -LiteralPath $file.FullName -Force }
  Remove-Item -LiteralPath $logDir -Force -ErrorAction SilentlyContinue
  foreach ($name in $oldEnvironment.Keys) { [Environment]::SetEnvironmentVariable($name, $oldEnvironment[$name], 'Process') }
}
