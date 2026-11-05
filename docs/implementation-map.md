# Source implementation map

> Generated from explicit vulnerability annotations in the lab source. A source reference shows where a behavior is declared or implemented; it does not prove runtime reachability. Check `test_status` and the linked runtime/audit evidence separately.

Annotated vulnerability IDs: **120 / 661**.

| ID | Vulnerability | Annotated source locations |
|---:|---|---|
| 7 | Server Version Disclosure | `backend/config.py:91`, `backend/main.py:270`, `backend/main.py:274` |
| 8 | Technology Stack Disclosure | `backend/config.py:91`, `backend/main.py:115` |
| 9 | Framework Fingerprinting | `backend/main.py:190` |
| 10 | Debug Information Exposure | `backend/config.py:48`, `backend/main.py:147` |
| 15 | Backup File Exposure | `backend/main.py:218` |
| 17 | Environment File Exposure | `backend/main.py:205` |
| 19 | Swagger Exposure | `backend/main.py:229`, `backend/main.py:27` |
| 20 | GraphQL Introspection Exposure | `backend/main.py:234`, `services/graphql/src/index.js:223`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:88`, `services/graphql/src/schema.js:3` |
| 24 | Error Message Information Leakage | `backend/routes/products.py:138` |
| 25 | Stack Trace Disclosure | `backend/main.py:241`, `backend/main.py:245` |
| 26 | Internal IP Disclosure | `backend/main.py:131`, `backend/main.py:147` |
| 31 | Weak Password Policy | `backend/routes/auth.py:134`, `backend/routes/auth.py:138`, `backend/routes/auth.py:322` |
| 33 | Default Admin Account | `backend/config.py:26` |
| 34 | Username Enumeration | `backend/routes/auth.py:134`, `backend/routes/auth.py:208`, `frontend/routes/index.js:323` |
| 35 | Email Enumeration | `backend/routes/auth.py:134`, `backend/routes/auth.py:141`, `backend/routes/auth.py:274` |
| 38 | Brute Force | `backend/routes/auth.py:187`, `backend/routes/auth.py:191` |
| 41 | Missing Login Rate Limiting | `backend/config.py:58`, `backend/routes/auth.py:191` |
| 43 | CAPTCHA Bypass | `backend/routes/auth.py:192` |
| 44 | MFA Bypass | `backend/routes/auth.py:360`, `backend/routes/auth.py:366` |
| 46 | OTP Brute Force | `backend/routes/auth.py:360`, `backend/routes/auth.py:361` |
| 47 | OTP Replay | `backend/routes/auth.py:360`, `backend/routes/auth.py:365` |
| 48 | OTP Predictability | `backend/config.py:62`, `backend/routes/auth.py:360`, `backend/routes/auth.py:362`, `backend/routes/auth.py:379` |
| 49 | OTP Expiration Bypass | `backend/config.py:64` |
| 51 | Password Reset Token Leakage | `backend/routes/auth.py:180`, `backend/routes/auth.py:273`, `backend/routes/auth.py:292`, `backend/routes/auth.py:301`, `services/graphql/src/schema.js:26`, `services/worker/worker.py:186`, `services/worker/worker.py:196`, `services/worker/worker.py:266`, `services/worker/worker.py:280`, `services/worker/worker.py:3` |
| 52 | Password Reset Token Prediction | `backend/config.py:67`, `backend/routes/auth.py:165`, `backend/routes/auth.py:279`, `backend/routes/auth.py:93`, `services/worker/worker.py:187`, `services/worker/worker.py:190`, `services/worker/worker.py:214`, `services/worker/worker.py:277`, `services/worker/worker.py:3` |
| 53 | Password Reset Token Reuse | `backend/routes/auth.py:309`, `backend/routes/auth.py:315` |
| 54 | Password Reset Token Not Expiring | `backend/config.py:68`, `backend/routes/auth.py:284`, `backend/routes/auth.py:309`, `backend/routes/auth.py:314` |
| 56 | Password Reset Host Header Injection | `backend/routes/auth.py:273`, `backend/routes/auth.py:287` |
| 57 | Insecure Email Verification | `backend/routes/auth.py:337` |
| 58 | Email Verification Token Reuse | `backend/routes/auth.py:337`, `backend/routes/auth.py:342`, `services/worker/worker.py:267`, `services/worker/worker.py:276`, `services/worker/worker.py:283`, `services/worker/worker.py:3` |
| 59 | Email Verification Bypass | `backend/routes/auth.py:351` |
| 61 | Authentication Bypass | `backend/routes/auth.py:480` |
| 62 | Insecure Remember Me | `backend/routes/auth.py:236`, `backend/routes/auth.py:254` |
| 64 | Authentication Logic Flaws | `backend/routes/auth.py:187` |
| 65 | Session Fixation | `backend/routes/auth.py:187`, `backend/routes/auth.py:194` |
| 66 | Session Hijacking | `backend/routes/auth.py:187` |
| 68 | Session Not Invalidated After Logout | `backend/routes/auth.py:226`, `backend/routes/auth.py:262`, `backend/routes/auth.py:265`, `services/worker/worker.py:3`, `services/worker/worker.py:490`, `services/worker/worker.py:495`, `services/worker/worker.py:499`, `services/worker/worker.py:501`, `services/worker/worker.py:514`, `services/worker/worker.py:515` |
| 69 | Session Not Invalidated After Password Change | `backend/routes/auth.py:326` |
| 70 | Concurrent Session Abuse | `backend/routes/auth.py:226`, `backend/routes/auth.py:231` |
| 71 | Insecure Session Cookie | `backend/config.py:78`, `backend/config.py:79`, `backend/routes/auth.py:248` |
| 72 | JWT None Algorithm | `backend/routes/auth.py:407`, `backend/routes/auth.py:415`, `services/graphql/src/auth.js:12`, `services/graphql/src/auth.js:3` |
| 73 | JWT Algorithm Confusion | `backend/routes/auth.py:416` |
| 74 | JWT Signature Validation Bypass | `backend/routes/auth.py:420`, `services/graphql/src/auth.js:12`, `services/graphql/src/auth.js:3` |
| 75 | JWT Weak Secret | `backend/config.py:20`, `services/graphql/src/auth.js:3`, `services/graphql/src/auth.js:7` |
| 77 | JWT Expiration Validation Bypass | `backend/config.py:24`, `backend/routes/auth.py:111`, `backend/routes/auth.py:427`, `services/graphql/src/auth.js:11`, `services/graphql/src/auth.js:3` |
| 81 | JWT Sensitive Data Exposure | `backend/routes/auth.py:100`, `backend/routes/auth.py:106`, `backend/routes/auth.py:107`, `backend/routes/auth.py:108`, `backend/routes/auth.py:220` |
| 82 | Refresh Token Reuse | `backend/routes/auth.py:222`, `backend/routes/auth.py:389`, `backend/routes/auth.py:401` |
| 83 | Refresh Token Rotation Failure | `backend/routes/auth.py:389`, `backend/routes/auth.py:394` |
| 84 | OAuth Account Takeover | `backend/routes/auth.py:436` |
| 85 | OAuth Redirect URI Manipulation | `backend/routes/auth.py:436`, `backend/routes/auth.py:442` |
| 86 | OAuth State Parameter CSRF | `backend/routes/auth.py:439`, `backend/routes/auth.py:445` |
| 94 | Social Login Account Linking Abuse | `backend/routes/auth.py:450` |
| 95 | Insecure Account Linking | `backend/routes/auth.py:450` |
| 97 | IDOR | `backend/routes/products.py:185`, `backend/routes/products.py:230`, `backend/routes/products.py:3`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:54`, `services/graphql/src/schema.js:279`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:80` |
| 102 | Role Escalation | `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:390`, `services/graphql/src/schema.js:218`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:328`, `services/graphql/src/schema.js:337` |
| 103 | Privilege Escalation Through Mass Assignment | `backend/routes/auth.py:145`, `backend/routes/auth.py:73` |
| 104 | Missing Function-Level Authorization | `backend/routes/auth.py:473`, `backend/routes/products.py:203`, `backend/routes/products.py:204`, `backend/routes/products.py:245`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:44`, `services/graphql/src/schema.js:275`, `services/graphql/src/schema.js:278`, `services/graphql/src/schema.js:3` |
| 108 | Admin Endpoint Exposure | `services/graphql/src/auth.js:92`, `services/graphql/src/resolvers.js:191`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:405`, `services/graphql/src/schema.js:171`, `services/graphql/src/schema.js:275`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:308`, `services/graphql/src/schema.js:339` |
| 113 | Unauthorized Order Access | `services/graphql/src/resolvers.js:128`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/schema.js:275`, `services/graphql/src/schema.js:292`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:80` |
| 115 | Unauthorized Payment Access | `services/graphql/src/resolvers.js:164`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/schema.js:275`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:300` |
| 125 | HTTP Method-Based Authorization Bypass | `backend/routes/products.py:230` |
| 128 | SQL Injection | `backend/routes/auth.py:197`, `backend/routes/products.py:112`, `backend/routes/products.py:115`, `backend/routes/products.py:135`, `backend/routes/products.py:3` |
| 136 | NoSQL Injection | `backend/routes/products.py:3` |
| 161 | SMTP Injection | `backend/routes/auth.py:116`, `backend/routes/auth.py:119`, `services/worker/worker.py:125`, `services/worker/worker.py:127`, `services/worker/worker.py:134`, `services/worker/worker.py:144`, `services/worker/worker.py:154`, `services/worker/worker.py:173`, `services/worker/worker.py:219`, `services/worker/worker.py:3`, `services/worker/worker.py:685`, `services/worker/worker.py:702` |
| 168 | CSV Injection | `backend/routes/products.py:152`, `backend/routes/products.py:158` |
| 170 | Reflected XSS | `backend/routes/products.py:300`, `backend/routes/products.py:303` |
| 171 | Stored XSS | `backend/routes/products.py:210`, `backend/routes/products.py:274`, `backend/routes/products.py:283`, `backend/routes/products.py:294`, `backend/routes/products.py:3` |
| 177 | HTML Injection | `backend/routes/products.py:274` |
| 184 | SameSite Cookie Misconfiguration | `backend/config.py:80` |
| 187 | CORS Misconfiguration | `backend/config.py:71`, `backend/main.py:32`, `backend/main.py:35`, `services/graphql/src/index.js:229`, `services/graphql/src/index.js:28`, `services/graphql/src/index.js:3` |
| 189 | CORS Credential Exposure | `backend/config.py:73`, `backend/main.py:36` |
| 198 | SSRF | `backend/routes/products.py:254`, `backend/routes/products.py:258` |
| 203 | SSRF Through Image Processing | `backend/routes/products.py:254` |
| 204 | SSRF Through PDF Generation | `services/worker/worker.py:3`, `services/worker/worker.py:360`, `services/worker/worker.py:390`, `services/worker/worker.py:396` |
| 230 | Race Condition | `services/worker/worker.py:3`, `services/worker/worker.py:306`, `services/worker/worker.py:319`, `services/worker/worker.py:327`, `services/worker/worker.py:331`, `services/worker/worker.py:345` |
| 239 | Regular Expression DoS (ReDoS) | `backend/routes/products.py:118` |
| 250 | API Mass Assignment | `backend/routes/products.py:203`, `backend/routes/products.py:205`, `backend/routes/products.py:238`, `backend/routes/products.py:3`, `backend/routes/products.py:85`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:316`, `services/graphql/src/resolvers.js:363`, `services/graphql/src/schema.js:211`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:328`, `services/graphql/src/schema.js:335` |
| 251 | API Excessive Data Exposure | `backend/routes/products.py:141`, `backend/routes/products.py:185`, `backend/routes/products.py:190`, `services/graphql/src/schema.js:8` |
| 253 | API Versioning Bypass | `backend/main.py:61` |
| 259 | API Sorting Injection | `backend/routes/products.py:135` |
| 260 | API GraphQL Introspection Abuse | `services/graphql/src/index.js:223`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:88`, `services/graphql/src/schema.js:3` |
| 264 | GraphQL Query Depth Abuse | `services/graphql/src/index.js:224`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:91`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/schema.js:3` |
| 265 | GraphQL Query Complexity Abuse | `services/graphql/src/index.js:225`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:95`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/schema.js:3` |
| 266 | GraphQL Batching Abuse | `services/graphql/src/index.js:226`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:98`, `services/graphql/src/resolvers.js:3`, `services/graphql/src/schema.js:3` |
| 267 | GraphQL Subscription Authorization Bypass | `services/graphql/src/index.js:227`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:52`, `services/graphql/src/index.js:62`, `services/graphql/src/resolvers.js:589`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:370` |
| 268 | GraphQL Federation Trust Abuse | `services/graphql/src/index.js:228`, `services/graphql/src/index.js:3`, `services/graphql/src/index.js:40`, `services/graphql/src/index.js:43`, `services/graphql/src/schema.js:3` |
| 271 | WebSocket Authentication Bypass | `backend/main.py:100`, `backend/main.py:79`, `frontend/server.js:18` |
| 272 | WebSocket Authorization Bypass | `backend/main.py:79`, `backend/main.py:88` |
| 278 | Webhook Signature Validation Bypass | `backend/config.py:83`, `frontend/routes/webhook.js:9` |
| 280 | Webhook SSRF | `frontend/routes/webhook.js:31` |
| 281 | Webhook Secret Leakage | `backend/config.py:84` |
| 283 | Product Price Manipulation | `frontend/routes/index.js:135`, `frontend/routes/index.js:192` |
| 300 | Flash Sale Race Condition | `backend/routes/products.py:179` |
| 305 | Concurrent Purchase Race Condition | `backend/routes/products.py:179` |
| 309 | Payment Amount Manipulation | `services/graphql/src/resolvers.js:3`, `services/graphql/src/resolvers.js:440`, `services/graphql/src/resolvers.js:483`, `services/graphql/src/schema.js:242`, `services/graphql/src/schema.js:253`, `services/graphql/src/schema.js:262`, `services/graphql/src/schema.js:3`, `services/graphql/src/schema.js:328`, `services/graphql/src/schema.js:347`, `services/graphql/src/schema.js:352`, `services/worker/worker.py:307`, `services/worker/worker.py:314`, `services/worker/worker.py:335` |
| 345 | Unrestricted File Upload | `backend/config.py:55` |
| 355 | ImageMagick Vulnerability | `services/worker/worker.py:3`, `services/worker/worker.py:598`, `services/worker/worker.py:619`, `services/worker/worker.py:628`, `services/worker/worker.py:650` |
| 369 | Path Traversal Through File Names | `services/worker/worker.py:3`, `services/worker/worker.py:361`, `services/worker/worker.py:376`, `services/worker/worker.py:382`, `services/worker/worker.py:466`, `services/worker/worker.py:599`, `services/worker/worker.py:601`, `services/worker/worker.py:605` |
| 372 | MD5 Password Storage | `backend/routes/auth.py:154`, `backend/routes/auth.py:155`, `backend/routes/auth.py:214`, `backend/routes/auth.py:31`, `backend/routes/auth.py:32` |
| 376 | Hardcoded Secrets | `backend/config.py:20`, `backend/config.py:26`, `backend/routes/auth.py:378` |
| 378 | Predictable Token Generation | `backend/config.py:67`, `backend/routes/auth.py:93` |
| 393 | Sensitive Data in URL | `backend/routes/auth.py:169` |
| 401 | Database Public Exposure | `backend/main.py:223` |
| 406 | Database SQL Injection | `backend/main.py:223` |
| 410 | Database Backup Exposure | `backend/main.py:218`, `services/worker/worker.py:3`, `services/worker/worker.py:523`, `services/worker/worker.py:528`, `services/worker/worker.py:555`, `services/worker/worker.py:561`, `services/worker/worker.py:567`, `services/worker/worker.py:585`, `services/worker/worker.py:61` |
| 435 | Cloud Access Key Leakage | `backend/config.py:38`, `backend/main.py:161` |
| 480 | HTTP Security Header Misconfiguration | `backend/main.py:311` |
| 558 | Password Logging | `backend/main.py:280`, `backend/main.py:284`, `backend/routes/auth.py:135`, `backend/routes/auth.py:188`, `backend/routes/auth.py:329` |
| 559 | Token Logging | `backend/main.py:284`, `backend/routes/auth.py:123`, `services/graphql/src/resolvers.js:20`, `services/worker/worker.py:102`, `services/worker/worker.py:131`, `services/worker/worker.py:155`, `services/worker/worker.py:157`, `services/worker/worker.py:188`, `services/worker/worker.py:196`, `services/worker/worker.py:242`, `services/worker/worker.py:280`, `services/worker/worker.py:3`, `services/worker/worker.py:308`, `services/worker/worker.py:310`, `services/worker/worker.py:362`, `services/worker/worker.py:37`, `services/worker/worker.py:372`, `services/worker/worker.py:475`, `services/worker/worker.py:525`, `services/worker/worker.py:534` |
| 560 | PII Logging | `backend/main.py:284` |
| 562 | CRLF Log Injection | `backend/main.py:301` |
| 570 | Metrics Endpoint Exposure | `backend/main.py:171` |
| 587 | Regex DoS | `backend/routes/products.py:118` |
| 589 | File Upload DoS | `backend/config.py:54` |
| 603 | Unbounded Pagination | `backend/routes/products.py:108`, `backend/routes/products.py:110`, `backend/routes/products.py:112` |
| 631 | Payment Provider Integration Flaws | `backend/config.py:44` |
| 643 | Customer PII Exposure | `backend/routes/auth.py:473`, `services/graphql/src/schema.js:19`, `services/graphql/src/schema.js:20`, `services/graphql/src/schema.js:9` |
| 648 | Payment Information Exposure | `services/graphql/src/schema.js:105`, `services/graphql/src/schema.js:18`, `services/graphql/src/schema.js:9` |
| 651 | Internal Business Data Exposure | `backend/routes/products.py:143`, `backend/routes/products.py:190`, `backend/routes/products.py:20`, `backend/routes/products.py:26` |
| 657 | Personal Data Export Authorization Bypass | `services/worker/worker.py:3`, `services/worker/worker.py:442`, `services/worker/worker.py:447`, `services/worker/worker.py:453`, `services/worker/worker.py:459`, `services/worker/worker.py:461`, `services/worker/worker.py:482` |
