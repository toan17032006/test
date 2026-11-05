# Component smoke coverage

This report maps checks in `tests/smoke-local.ps1` and `docs/dependency-audit.md` to the supplied component/workflow inventory. A verified component means the named local route or lab behavior was exercised. It does not mean every part of a broad component is implemented, backed by a real provider, or production-ready.

| IDs | Component area | What was exercised |
|---|---|---|
| 21, 22, 23, 24, 25 | Storefront browsing | Home, listing, product detail, search, and category filter routes; the detail/search pages rendered the matching synthetic product. |
| 28, 30, 92, 94, 101 | Cart and guest checkout | Added and removed a synthetic item through the REST cart, submitted guest checkout with COD, and confirmed the session cart cleared. |
| 31, 106 | Order history and tracking | The storefront rendered a synthetic user's order history and an order tracking page from the local API. |
| 32, 33 | Profile and address book | Loaded the profile page and retrieved the synthetic user's address book through the API. |
| 34, 35, 257 | Login, signup, and verification flow | Loaded login/signup pages; registered a synthetic user, replayed the verification token, and logged in. |
| 36, 41, 42, 43, 45, 46, 197, 198, 199, 201, 202 | Authentication and browser session | Exercised storefront logout, MFA setup/verification, fake Google OAuth, session fixation/logout behavior, cookie flags, JWT acceptance, password reset, and account enumeration. |
| 52, 53, 54, 224, 227 | Browser security configuration | Checked credentialed CORS origin reflection and absent CSP, HSTS, frame, and content-type headers. |
| 58, 59, 62, 63, 67, 68, 70, 71, 72, 75 | API and access control | Exercised REST requests, GraphQL HTTP and subscription protocols, unauthenticated Socket.IO events, introspection, webhook handlers, login throttling behavior, weak input validation, authentication, authorization, role changes, and business logic. |
| 81, 86, 88, 89, 95, 96, 100, 102, 103, 104, 105, 107, 112, 113, 116, 145 | Commerce, shipping, and payment operations | Exercised product management/pricing, flash-sale listing, coupons, product Q&A, local recommendations, synthetic order creation, shipping status/tracking, mock payment, refund, payment callback replay, order cancellation, review creation, and payment history. |
| 56, 121, 140, 149, 167, 171, 179 | Notifications, administration, and operations | Followed the unauthenticated admin dashboard redirect, created/read a synthetic notification, exercised user listing/role changes and local search suggestions, ran the dependency audit, and confirmed synthetic credential logging. |
| 189, 190, 192, 193, 194, 195, 206, 207, 208, 209, 210, 214, 215, 231, 232, 236, 237, 238, 240, 246, 248, 249, 250, 251, 252, 253 | Security test surfaces | Reproduced raw reflected/stored HTML markers, cross-origin profile role escalation, and the listed local access-control, auth, WebSocket, host-header, business-logic, webhook, data-exposure, backup, dependency, clickjacking-header, and GraphQL behaviors with synthetic records. |
| 259, 261, 264, 266, 269, 270, 271, 273, 274, 275 | End-to-end lab scenarios | Exercised search-to-product/cart steps, order-to-payment processing, shipping-to-delivery updates, admin role assignment, guest access to admin data, cross-user access, user-to-admin access, webhook replay, price/quantity/coupon manipulation, bounded GraphQL depth/batch probes, and direct API calls. |

The XSS probes returned the synthetic `onerror` marker as raw HTML; the test client did not execute it. The Socket.IO probe used a fake token for seeded lab user 3 and an attacker origin. The GraphQL admin-alert subscription was accepted without authentication, but the stub pub/sub emitted no data.

The SSRF recommendation route was exercised only against the lab's own loopback health endpoint after temporarily installing the declared `httpx` dependency; vulnerability catalog entries #198 and #200 are verified for that local target. This is separate from component ID 198 (JWT Vulnerabilities) in the table above. Docker/Compose, database containers, external providers, background workers, and infrastructure components were not started in this environment.
