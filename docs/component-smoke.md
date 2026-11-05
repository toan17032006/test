# Component smoke coverage

This report maps checks in `tests/smoke-local.ps1` and `docs/dependency-audit.md` to the supplied component/workflow inventory. A verified component means the named local route or lab behavior was exercised. It does not mean every part of a broad component is implemented, backed by a real provider, or production-ready.

| IDs | Component area | What was exercised |
|---|---|---|
| 21, 22, 23, 24, 25 | Storefront browsing | Home, listing, product detail, search, and category filter routes; the detail/search pages rendered the matching synthetic product. |
| 28, 30, 94, 101 | Cart and guest checkout | Added a synthetic item to a session cart, submitted guest checkout with COD, and confirmed the cart cleared. |
| 34, 35, 257 | Login, signup, and verification flow | Loaded login/signup pages; registered a synthetic user, replayed the verification token, and logged in. |
| 41, 42, 43, 45, 46, 197, 198, 199, 201, 202 | Authentication and browser session | Exercised MFA setup/verification, fake Google OAuth, session fixation/logout behavior, cookie flags, JWT acceptance, password reset, and account enumeration. |
| 52, 54, 224, 227 | Browser security configuration | Checked credentialed CORS origin reflection and absent CSP, HSTS, frame, and content-type headers. |
| 58, 59, 63, 67, 68, 70, 71, 72, 75 | API and access control | Exercised REST requests, GraphQL introspection, webhook handlers, login throttling behavior, weak input validation, authentication, authorization, role changes, and business logic. |
| 88, 95, 96, 100, 102, 103, 104, 105, 107, 112, 145 | Commerce, shipping, and payment operations | Exercised coupons, synthetic order creation, shipping status/tracking, mock payment, refund, payment callback replay, order cancellation, review creation, and payment history. |
| 121, 140, 149, 171, 179 | Notifications, administration, and operations | Created/read a synthetic notification, exercised user listing/role changes, ran the dependency audit, and confirmed synthetic credential logging. |
| 192, 193, 194, 195, 206, 207, 208, 209, 210, 214, 215, 236, 237, 238, 246, 249, 250, 251, 252, 253 | Security test surfaces | Reproduced the listed local access-control, auth, business-logic, webhook, data-exposure, backup, and GraphQL behaviors with synthetic records. |
| 259, 261, 264, 269, 270, 273, 274, 275 | End-to-end lab scenarios | Exercised search-to-product/cart steps, order-to-payment processing, shipping-to-delivery updates, cross-user access, user-to-admin access, webhook replay, price/quantity/coupon manipulation, and direct API calls. |

The SSRF recommendation route was not exercised because `httpx` is absent from the current Python runtime; vulnerability catalog entries #198 (SSRF) and #200 (SSRF to Internal Services) remain `not_tested`. This is separate from component ID 198 (JWT Vulnerabilities) in the table above. Docker/Compose, database containers, external providers, background workers, and infrastructure components were not started in this environment.
