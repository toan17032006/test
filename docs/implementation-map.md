# Source implementation map

> Generated from the checked-in source map. The original inline annotations were moved to the README; this map keeps their symbol-level locations. A reference shows where a behavior is declared or implemented; it does not prove runtime reachability. Check `test_status` and the linked runtime/audit evidence separately.

Annotated vulnerability IDs: **122 / 661**.

| ID | Vulnerability | Annotated source locations |
|---:|---|---|
| 7 | Server Version Disclosure | `backend/config.py::INTERNAL_ADMIN_URL`, `backend/main.py::http_exception_handler` |
| 8 | Technology Stack Disclosure | `backend/config.py::INTERNAL_ADMIN_URL`, `backend/main.py::root` |
| 9 | Framework Fingerprinting | `backend/main.py::phpinfo` |
| 10 | Debug Information Exposure | `backend/config.py::STRIPE_WEBHOOK_SECRET`, `backend/main.py::debug_info` |
| 15 | Backup File Exposure | `backend/main.py::db_backup` |
| 17 | Environment File Exposure | `backend/main.py::env_file` |
| 19 | Swagger Exposure | `backend/main.py::module`, `backend/main.py::swagger_json` |
| 20 | GraphQL Introspection Exposure | `backend/main.py::graphql_info`, `services/graphql/src/index.js::module`, `services/graphql/src/index.js::server`, `services/graphql/src/schema.js::module` |
| 24 | Error Message Information Leakage | `backend/routes/products.py::list_products` |
| 25 | Stack Trace Disclosure | `backend/main.py::global_exception_handler`, `backend/main.py::graphql_info` |
| 26 | Internal IP Disclosure | `backend/main.py::debug_info`, `backend/main.py::health` |
| 31 | Weak Password Policy | `backend/routes/auth.py::register`, `backend/routes/auth.py::reset_password` |
| 33 | Default Admin Account | `backend/config.py::JWT_EXPIRE_MINUTES` |
| 34 | Username Enumeration | `backend/routes/auth.py::login`, `backend/routes/auth.py::register`, `frontend/routes/index.js::status` |
| 35 | Email Enumeration | `backend/routes/auth.py::forgot_password`, `backend/routes/auth.py::register` |
| 38 | Brute Force | `backend/routes/auth.py::login` |
| 41 | Missing Login Rate Limiting | `backend/config.py::RATE_LIMIT_ENABLED`, `backend/routes/auth.py::login` |
| 43 | CAPTCHA Bypass | `backend/routes/auth.py::login` |
| 44 | MFA Bypass | `backend/routes/auth.py::mfa_verify` |
| 46 | OTP Brute Force | `backend/routes/auth.py::mfa_verify` |
| 47 | OTP Replay | `backend/routes/auth.py::mfa_verify` |
| 48 | OTP Predictability | `backend/config.py::RATE_LIMIT_WINDOW`, `backend/routes/auth.py::mfa_setup`, `backend/routes/auth.py::mfa_verify` |
| 49 | OTP Expiration Bypass | `backend/config.py::OTP_EXPIRE_SECONDS` |
| 51 | Password Reset Token Leakage | `backend/routes/auth.py::forgot_password`, `backend/routes/auth.py::register`, `services/graphql/src/schema.js::typeDefs`, `services/worker/worker.py::module`, `services/worker/worker.py::send_password_reset_email`, `services/worker/worker.py::send_verification_email` |
| 52 | Password Reset Token Prediction | `backend/config.py::OTP_SECRET`, `backend/routes/auth.py::forgot_password`, `backend/routes/auth.py::register`, `backend/routes/auth.py::weak_token`, `services/worker/worker.py::module`, `services/worker/worker.py::send_password_reset_email`, `services/worker/worker.py::send_verification_email` |
| 53 | Password Reset Token Reuse | `backend/routes/auth.py::reset_password` |
| 54 | Password Reset Token Not Expiring | `backend/config.py::PASSWORD_RESET_TOKEN_EXPIRE`, `backend/routes/auth.py::forgot_password`, `backend/routes/auth.py::reset_password` |
| 56 | Password Reset Host Header Injection | `backend/routes/auth.py::forgot_password` |
| 57 | Insecure Email Verification | `backend/routes/auth.py::verify_email` |
| 58 | Email Verification Token Reuse | `backend/routes/auth.py::verify_email`, `services/worker/worker.py::module`, `services/worker/worker.py::send_verification_email` |
| 59 | Email Verification Bypass | `backend/routes/auth.py::verify_email_bypass` |
| 61 | Authentication Bypass | `backend/routes/auth.py::auth_bypass` |
| 62 | Insecure Remember Me | `backend/routes/auth.py::login` |
| 64 | Authentication Logic Flaws | `backend/routes/auth.py::login` |
| 65 | Session Fixation | `backend/routes/auth.py::login` |
| 66 | Session Hijacking | `backend/routes/auth.py::login` |
| 68 | Session Not Invalidated After Logout | `backend/routes/auth.py::login`, `backend/routes/auth.py::logout`, `services/worker/worker.py::cleanup_sessions`, `services/worker/worker.py::module` |
| 69 | Session Not Invalidated After Password Change | `backend/routes/auth.py::reset_password` |
| 70 | Concurrent Session Abuse | `backend/routes/auth.py::login` |
| 71 | Insecure Session Cookie | `backend/config.py::SESSION_COOKIE_HTTPONLY`, `backend/config.py::SESSION_COOKIE_SECURE`, `backend/routes/auth.py::login` |
| 72 | JWT None Algorithm | `backend/routes/auth.py::get_me`, `services/graphql/src/auth.js::REFRESH_SECRET`, `services/graphql/src/auth.js::module` |
| 73 | JWT Algorithm Confusion | `backend/routes/auth.py::get_me` |
| 74 | JWT Signature Validation Bypass | `backend/routes/auth.py::get_me`, `services/graphql/src/auth.js::REFRESH_SECRET`, `services/graphql/src/auth.js::module` |
| 75 | JWT Weak Secret | `backend/config.py::INFLUXDB_TOKEN`, `services/graphql/src/auth.js::jwt`, `services/graphql/src/auth.js::module` |
| 77 | JWT Expiration Validation Bypass | `backend/config.py::JWT_EXPIRE_MINUTES`, `backend/routes/auth.py::create_jwt`, `backend/routes/auth.py::get_me`, `services/graphql/src/auth.js::REFRESH_SECRET`, `services/graphql/src/auth.js::module` |
| 81 | JWT Sensitive Data Exposure | `backend/routes/auth.py::create_jwt`, `backend/routes/auth.py::login` |
| 82 | Refresh Token Reuse | `backend/routes/auth.py::login`, `backend/routes/auth.py::refresh_token` |
| 83 | Refresh Token Rotation Failure | `backend/routes/auth.py::refresh_token` |
| 84 | OAuth Account Takeover | `backend/routes/auth.py::social_login_google` |
| 85 | OAuth Redirect URI Manipulation | `backend/routes/auth.py::social_login_google` |
| 86 | OAuth State Parameter CSRF | `backend/routes/auth.py::social_login_google` |
| 94 | Social Login Account Linking Abuse | `backend/routes/auth.py::social_login_google` |
| 95 | Insecure Account Linking | `backend/routes/auth.py::social_login_google` |
| 97 | IDOR | `backend/routes/products.py::get_product`, `backend/routes/products.py::module`, `backend/routes/products.py::update_product`, `services/graphql/src/resolvers.js::if`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 102 | Role Escalation | `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::rows`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 103 | Privilege Escalation Through Mass Assignment | `backend/routes/auth.py::RegisterRequest`, `backend/routes/auth.py::register` |
| 104 | Missing Function-Level Authorization | `backend/routes/auth.py::list_all_users`, `backend/routes/products.py::create_product`, `backend/routes/products.py::delete_product`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::resolvers`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 108 | Admin Endpoint Exposure | `services/graphql/src/auth.js::if`, `services/graphql/src/resolvers.js::deleteUser`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::rows`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 113 | Unauthorized Order Access | `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::productsByCategory`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 115 | Unauthorized Payment Access | `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::rows`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 125 | HTTP Method-Based Authorization Bypass | `backend/routes/products.py::update_product` |
| 128 | SQL Injection | `backend/routes/auth.py::login`, `backend/routes/products.py::list_products`, `backend/routes/products.py::module` |
| 136 | NoSQL Injection | `backend/routes/products.py::module` |
| 161 | SMTP Injection | `backend/routes/auth.py::send_email_smtp`, `services/worker/worker.py::module`, `services/worker/worker.py::send_bulk_email`, `services/worker/worker.py::send_email`, `services/worker/worker.py::send_password_reset_email`, `services/worker/worker.py::send_smtp` |
| 168 | CSV Injection | `backend/routes/products.py::export_products_csv` |
| 170 | Reflected XSS | `backend/routes/products.py::get_qna` |
| 171 | Stored XSS | `backend/routes/products.py::add_review`, `backend/routes/products.py::create_product`, `backend/routes/products.py::get_reviews`, `backend/routes/products.py::module` |
| 177 | HTML Injection | `backend/routes/products.py::add_review` |
| 184 | SameSite Cookie Misconfiguration | `backend/config.py::SESSION_COOKIE_SAMESITE` |
| 187 | CORS Misconfiguration | `backend/config.py::EMAIL_VERIFY_TOKEN_EXPIRE`, `backend/main.py::module`, `services/graphql/src/index.js::app`, `services/graphql/src/index.js::module` |
| 189 | CORS Credential Exposure | `backend/config.py::CORS_CREDENTIALS`, `backend/main.py::module` |
| 198 | SSRF | `backend/routes/products.py::get_recommendations` |
| 203 | SSRF Through Image Processing | `backend/routes/products.py::get_recommendations` |
| 204 | SSRF Through PDF Generation | `services/worker/worker.py::generate_invoice`, `services/worker/worker.py::module` |
| 230 | Race Condition | `services/worker/worker.py::module`, `services/worker/worker.py::process_payment_async` |
| 239 | Regular Expression DoS (ReDoS) | `backend/routes/products.py::list_products` |
| 250 | API Mass Assignment | `backend/routes/products.py::ProductCreate`, `backend/routes/products.py::create_product`, `backend/routes/products.py::module`, `backend/routes/products.py::update_product`, `services/graphql/src/resolvers.js::logout`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::register`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 251 | API Excessive Data Exposure | `backend/routes/products.py::get_product`, `backend/routes/products.py::list_products`, `services/graphql/src/schema.js::typeDefs` |
| 253 | API Versioning Bypass | `backend/main.py::module` |
| 259 | API Sorting Injection | `backend/routes/products.py::list_products` |
| 260 | API GraphQL Introspection Abuse | `services/graphql/src/index.js::module`, `services/graphql/src/index.js::server`, `services/graphql/src/schema.js::module` |
| 264 | GraphQL Query Depth Abuse | `services/graphql/src/index.js::module`, `services/graphql/src/index.js::server`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/schema.js::module` |
| 265 | GraphQL Query Complexity Abuse | `services/graphql/src/index.js::module`, `services/graphql/src/index.js::server`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/schema.js::module` |
| 266 | GraphQL Batching Abuse | `services/graphql/src/index.js::module`, `services/graphql/src/index.js::server`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/schema.js::module` |
| 267 | GraphQL Subscription Authorization Bypass | `services/graphql/src/index.js::httpServer`, `services/graphql/src/index.js::module`, `services/graphql/src/index.js::serverCleanup`, `services/graphql/src/resolvers.js::resetAllPasswords`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs` |
| 268 | GraphQL Federation Trust Abuse | `services/graphql/src/index.js::app`, `services/graphql/src/index.js::module`, `services/graphql/src/schema.js::module` |
| 271 | WebSocket Authentication Bypass | `backend/main.py::admin_ws`, `backend/main.py::websocket_endpoint`, `frontend/server.js::server` |
| 272 | WebSocket Authorization Bypass | `backend/main.py::websocket_endpoint` |
| 278 | Webhook Signature Validation Bypass | `backend/config.py::WEBHOOK_VERIFY_SIGNATURES`, `frontend/routes/webhook.js::API_URL` |
| 280 | Webhook SSRF | `frontend/routes/webhook.js::payload` |
| 281 | Webhook Secret Leakage | `backend/config.py::WEBHOOK_SECRET` |
| 283 | Product Price Manipulation | `frontend/routes/index.js::route /cart/add`, `frontend/routes/index.js::route /checkout` |
| 300 | Flash Sale Race Condition | `backend/routes/products.py::flash_sale` |
| 305 | Concurrent Purchase Race Condition | `backend/routes/products.py::flash_sale` |
| 309 | Payment Amount Manipulation | `services/graphql/src/resolvers.js::deleteProduct`, `services/graphql/src/resolvers.js::module`, `services/graphql/src/resolvers.js::rows`, `services/graphql/src/schema.js::module`, `services/graphql/src/schema.js::typeDefs`, `services/worker/worker.py::process_payment_async` |
| 345 | Unrestricted File Upload | `backend/config.py::ALLOWED_EXTENSIONS` |
| 355 | ImageMagick Vulnerability | `services/worker/worker.py::module`, `services/worker/worker.py::process_image` |
| 369 | Path Traversal Through File Names | `services/worker/worker.py::export_user_data`, `services/worker/worker.py::generate_invoice`, `services/worker/worker.py::module`, `services/worker/worker.py::process_image` |
| 372 | MD5 Password Storage | `backend/routes/auth.py::login`, `backend/routes/auth.py::module`, `backend/routes/auth.py::register` |
| 376 | Hardcoded Secrets | `backend/config.py::INFLUXDB_TOKEN`, `backend/config.py::JWT_EXPIRE_MINUTES`, `backend/routes/auth.py::mfa_setup` |
| 378 | Predictable Token Generation | `backend/config.py::OTP_SECRET`, `backend/routes/auth.py::weak_token` |
| 393 | Sensitive Data in URL | `backend/routes/auth.py::register` |
| 401 | Database Public Exposure | `backend/main.py::internal_db_query` |
| 406 | Database SQL Injection | `backend/main.py::internal_db_query` |
| 410 | Database Backup Exposure | `backend/main.py::db_backup`, `services/worker/worker.py::BACKUP_DIR`, `services/worker/worker.py::backup_database`, `services/worker/worker.py::module` |
| 435 | Cloud Access Key Leakage | `backend/config.py::EMAIL_FROM`, `backend/main.py::debug_info` |
| 480 | HTTP Security Header Misconfiguration | `backend/main.py::log_requests` |
| 558 | Password Logging | `backend/main.py::http_exception_handler`, `backend/main.py::log_requests`, `backend/routes/auth.py::login`, `backend/routes/auth.py::register`, `backend/routes/auth.py::reset_password` |
| 559 | Token Logging | `backend/main.py::log_requests`, `backend/routes/auth.py::send_email_smtp`, `services/graphql/src/resolvers.js::rawQuery`, `services/worker/worker.py::backup_database`, `services/worker/worker.py::db_query`, `services/worker/worker.py::export_user_data`, `services/worker/worker.py::generate_invoice`, `services/worker/worker.py::module`, `services/worker/worker.py::process_payment_async`, `services/worker/worker.py::send_email`, `services/worker/worker.py::send_order_confirmation`, `services/worker/worker.py::send_password_reset_email`, `services/worker/worker.py::send_smtp`, `services/worker/worker.py::send_verification_email` |
| 560 | PII Logging | `backend/main.py::log_requests` |
| 562 | CRLF Log Injection | `backend/main.py::log_requests` |
| 570 | Metrics Endpoint Exposure | `backend/main.py::metrics` |
| 587 | Regex DoS | `backend/routes/products.py::list_products` |
| 589 | File Upload DoS | `backend/config.py::MAX_UPLOAD_SIZE` |
| 603 | Unbounded Pagination | `backend/routes/products.py::list_products` |
| 608 | Hardcoded API Keys | `frontend/views/layout.ejs::template` |
| 609 | Exposed Source Maps | `frontend/views/layout.ejs::template` |
| 631 | Payment Provider Integration Flaws | `backend/config.py::S3_BUCKET` |
| 643 | Customer PII Exposure | `backend/routes/auth.py::list_all_users`, `services/graphql/src/schema.js::typeDefs` |
| 648 | Payment Information Exposure | `services/graphql/src/schema.js::typeDefs` |
| 651 | Internal Business Data Exposure | `backend/routes/products.py::get_product`, `backend/routes/products.py::list_products`, `backend/routes/products.py::module` |
| 657 | Personal Data Export Authorization Bypass | `services/worker/worker.py::export_user_data`, `services/worker/worker.py::module` |
