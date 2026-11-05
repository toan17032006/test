# Loopback smoke findings

Captured on **2026-11-05** by `tests/smoke-local.ps1`. The test starts the FastAPI, storefront, and GraphQL processes on dynamically selected `127.0.0.1` ports. It uses synthetic accounts, marker credentials, fake SMTP/database endpoints, and in-memory order/payment data. No real payment provider or external target is contacted; the script stops the processes and removes its temporary logs.

The automated smoke reproduced the following behaviors and records them as `observed` / `verified` in `vulndb/catalog.json`:

| IDs | Finding | Direct evidence |
|---|---|---|
| 8, 9, 26, 570 | Service fingerprinting, internal health information, and metrics disclosure | The root returned its framework version, the synthetic phpinfo page disclosed fixed service markers, health returned the synthetic database URL and internal IP, and unauthenticated metrics returned a lab secret marker and internal routes. |
| 184, 187, 189, 480 | SameSite cookie and CORS misconfiguration; missing security headers | The synthetic login cookie used `SameSite=None` without `Secure`; a request with `Origin: https://attacker.invalid` and a fake cookie received the reflected origin plus `Access-Control-Allow-Credentials: true`; the API root lacked CSP, HSTS, frame, and content-type protections. |
| 282 | Webhook event injection | An unauthenticated shipping webhook advanced a synthetic order from pending to shipped to delivered and set a lab tracking number without a signature. |
| 17, 19, 20 | Exposed environment configuration, API docs, and GraphQL introspection | Unauthenticated `/.env` returned deliberately fake environment values; `/docs` returned 200; GraphQL `__schema` returned the `Query` root. |
| 128 | SQL injection training simulation | A synthetic login payload matching the route's explicit SQLi exercise branch authenticated as the seeded lab admin. This demonstrates the route simulation, not SQL execution against a database. |
| 168, 250, 603 | CSV formula injection, product mass assignment, and unbounded pagination | An unauthenticated product create accepted admin-only fields; its synthetic `=1+1` name was exported without formula neutralization; requesting `limit=1` still returned multiple catalog rows. |
| 293, 576 | Coupon enumeration and backup data exposure | Unauthenticated coupon listing revealed the synthetic `ADMIN` coupon; the admin backup endpoint returned synthetic user and order records. |
| 284, 285, 286, 287, 289 | Negative/zero price, quantity, and cart ownership abuse | The API accepted negative and zero unit prices, a negative quantity, and returned user 3's cart through a caller-selected user ID. |
| 294 | Coupon reuse | The same synthetic coupon validated successfully twice without a use limit. |
| 32, 33 | Weak default credentials and default admin account | The seeded synthetic admin account accepted `admin123` without CAPTCHA. |
| 31, 61 | Weak password policy and authentication bypass | Registration accepted a one-character password; `/auth/bypass` returned an admin principal for `{"admin":true}`. |
| 34, 35, 37, 38, 41, 43 | Account enumeration, missing login throttling, and CAPTCHA bypass | Unknown and known usernames returned different errors; duplicate registration and password reset distinguished known emails; five invalid logins did not lock out the account; a valid login required no CAPTCHA. |
| 44, 46, 47, 48 | MFA bypass and weak OTP controls | MFA setup returned the fixed `123456`; invalid attempts were not throttled; the OTP and `000000` backdoor both succeeded repeatedly. |
| 51, 52, 53, 55, 56 | Password-reset token exposure/prediction/reuse and account takeover | The unauthenticated reset endpoint returned a timestamp-derived token, which was reproduced and reused to change the synthetic admin password; an attacker-controlled `Host` header appeared in the reset URL. |
| 57, 58, 59 | Email verification weaknesses | Registration returned the verification token, the same token verified twice, and a separate endpoint verified the account without a token. |
| 97, 98, 102, 103, 104, 108, 113, 116, 121, 122 | Object-level access failures, role escalation, and exposed admin routes | A caller identifying as user 2 read user 3's order and address; unauthenticated signup and an admin role endpoint changed user roles without authentication; the admin user list returned without authentication. |
| 251, 252, 260 | Excessive API data, parameter tampering, and GraphQL introspection | Product responses included internal cost/admin notes; cart and order requests set below-catalog prices and totals; schema introspection succeeded. |
| 277, 278, 279, 283, 288, 290, 307, 308, 309, 311, 312, 313 | Forged/replayed payment events and client-controlled pricing | A below-catalog cart price and altered order total were accepted; a zero-amount mock payment set an order to paid; an unsigned payment webhook changed another synthetic order to paid and accepted the same event twice. |
| 316, 317 | Refund manipulation and unauthorized refund | An unauthenticated request refunded a synthetic paid order for an amount of one. |
| 314, 315 | Duplicate payment processing and idempotency failure | Repeating the same mock payment request created two distinct payment records for one order. |
| 320, 322 | Order ownership manipulation and cancellation abuse | User 2 created an order for user 3 through a client-supplied owner ID, then cancelled that order without authentication. |
| 332, 333, 334 | Review manipulation, fake review injection, and ownership bypass | An unauthenticated caller created and retrieved a synthetic review under an arbitrary display name. |
| 62, 65, 68, 69, 71 | Insecure remember-me and session controls | A long-lived cookie lacked `HttpOnly`/`Secure`, a caller-supplied session ID was retained, and access tokens stayed valid after logout and password reset. |
| 72, 74, 77, 78, 79, 80, 81, 82, 83 | JWT and refresh-token weaknesses | An unsigned token and an expired token were accepted; incorrect audience/issuer claims were not checked; access and refresh tokens were reusable; login responses/claims contained password data. |
| 85, 86, 87 | OAuth redirect, state, and PKCE weaknesses | The fake OAuth flow accepted a code without PKCE and echoed an attacker redirect URI and unvalidated state. |
| 372, 394, 435, 558 | Weak password storage, sensitive logging, and exposed environment credentials | The returned password hash matched MD5 of the synthetic one-character password; the isolated API log contained that password; `/.env` returned a deliberately fake AWS marker. |
| 643, 645, 646, 650, 651, 652 | Customer PII, admin data, business information, and cross-customer leakage | The unauthenticated admin list exposed synthetic email, phone, card/SSN and password fields; product detail exposed cost/admin note; user 2 received user 3's order and address. |
| 675, 678 | API BOLA data access and forged payment attack chains | The cross-customer read returned user 3's order; the unsigned webhook changed a pending order to paid/processing. |

Dependency findings **#543 Vulnerable Dependencies**, **#544 Outdated Dependencies**, and **#618 JavaScript Dependency Vulnerability** are recorded separately in [dependency-audit.md](dependency-audit.md).

These results cover only the listed findings. The recommendation SSRF check for #198 and #200 was skipped because `httpx` is declared in `backend/requirements.txt` but is not installed in this Python runtime. The other vulnerability entries, attack chains, components, and environment-dependent infrastructure checks remain `unverified` / `not_tested`; catalog completeness does not imply complete implementation.
