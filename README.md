# VulnShop

VulnShop is an intentionally vulnerable e-commerce training lab for authorized testing. Use synthetic data and run it only on a machine and network you control. Do not expose it to the public internet or use production data. The externally reachable storefront port is intended for a trusted lab network only.

The shopping site is a complete storefront: catalog, search, product detail, reviews, cart, checkout, order history, tracking, profile, password reset, login, and registration. The vulnerability inventory is documentation only and no longer appears as hints in the application source or storefront UI.

## Inventory and evidence

The supplied brief has 275 store and architecture components plus a numbered 1–726 catalog. Those 726 entries comprise 661 vulnerability topics, 29 attack-chain scenarios, and 36 test-matrix fields. All 275 components and all 726 numbered entries are reproduced in the [complete inventory](#complete-inventory) below and remain searchable in [vulndb/checklist.md](vulndb/checklist.md). The storefront itself no longer exposes an inventory route.

Coverage is recorded honestly:

- Evidence verifies 165 vulnerability topics (162 from loopback smoke and route tests, three from the dependency audit) and nine attack chains.
- The source map covers 122 vulnerability IDs at symbol level. A source reference shows where behavior is declared or implemented; it does not prove runtime reachability.
- Component smoke evidence covers 102 of the 275 component/workflow rows at route or flow level. The remaining 173 are still marked `unverified` / `not_tested`.
- All inline vulnerability comments and docstrings were moved out of the source and are reproduced in the [moved annotations](#implementation-notes-moved-out-of-source) section. [vulndb/source-annotations.json](vulndb/source-annotations.json) keeps the machine-readable symbol map.

Evidence is documented in [docs/smoke-findings.md](docs/smoke-findings.md), [docs/component-smoke.md](docs/component-smoke.md), [docs/dependency-audit.md](docs/dependency-audit.md), and [docs/implementation-map.md](docs/implementation-map.md). The checklist is regenerated with `python scripts/render_checklist.py`.

## Docker deployment and one-command startup

Requirements: Docker Desktop or Docker Engine with Compose v2. The launchers build every image and start the full stack: storefront, backend API, GraphQL, worker, nginx, and the seeded databases.

```powershell
# Windows: build all images, start the stack, wait until it is ready
scripts\start-app.ps1
```

```bash
# Linux, macOS, or Git Bash
./scripts/start-app.sh
```

`start-app` uses Docker by default. The available modes:

| Command | Purpose |
|---|---|
| `scripts/start-app.ps1 -NoBuild` / `scripts/start-app.sh --no-build` | reuse existing images |
| `scripts/start-app.ps1 -Local` / `scripts/start-app.sh --local` | run backend and frontend natively, without Docker |
| `scripts/start-app.ps1 -Foreground` / `scripts/start-app.sh --foreground` | stream Compose logs in the terminal |
| `scripts/start-app.ps1 -Stop` / `scripts/start-app.sh --stop` | stop the Docker stack and native processes |

Individual launchers: `scripts/docker-up.ps1` / `scripts/docker-up.sh` build and start only the Docker stack; `scripts/dev-up.ps1` / `scripts/dev-up.sh` run the backend and storefront natively. Both wait for the API health check and storefront before printing URLs, and `dev-up` writes logs and PID files under `.run/`.

### Externally reachable storefront

The storefront is published on host port **13000** and nginx on **9080**, both on every host interface. Open `http://<host-lan-ip>:13000` from another machine on the same network; the launchers print the address they detect. Every published host port is above 9000:

| Service | Host port | Binding | URL from another machine |
|---|---:|---|---|
| Storefront (direct) | 13000 | all interfaces | `http://<host-lan-ip>:13000` |
| Nginx entry point | 9080 | all interfaces | `http://<host-lan-ip>:9080` |
| Backend API | 18000 | loopback | `http://127.0.0.1:18000/health` |
| GraphQL | 14000 | loopback | `http://127.0.0.1:14000/graphql` |
| MailHog UI | 18025 | loopback | `http://127.0.0.1:18025` |
| MailHog SMTP | 11025 | loopback | `127.0.0.1:11025` |
| PostgreSQL | 15432 | loopback | — |
| MySQL | 13306 | loopback | — |
| MongoDB | 27017 | loopback | — |
| Redis | 16379 | loopback | — |
| Elasticsearch | 19200 / 19300 | loopback | — |
| Neo4j | 17474 / 17687 | loopback | — |
| InfluxDB | 18086 | loopback | — |

Containers keep their normal internal ports (8000 API, 3000 storefront, 80 nginx); only the host side is remapped. The default Docker network remains `internal: true`, so containers have no outbound internet access, and no Docker socket or privileged container is used. When started natively, `dev-up` serves the same addresses: backend on 18000 and storefront on 13000, both bound to `0.0.0.0`.

**Trusted lab network only.** Ports 13000 and 9080 are intentionally reachable from other hosts, so anyone on the network can reach an intentionally vulnerable application. Run the lab on an isolated or trusted network, never on the public internet, and never with production data. Accounts, products, payments, and emails are synthetic; payments are mock-only and never contact a real provider.

### Verification performed here

- `docker-compose.yml` parses with PyYAML; every published host port is above 9000; frontend and nginx are non-loopback; every database, API, GraphQL, and mail service is loopback-only.
- `bash -n` and the PowerShell parser accept all six launchers.
- The native path (`scripts/dev-up.sh`) was started on this machine: `http://127.0.0.1:13000` and `http://192.168.1.103:13000` both returned HTTP 200, `http://127.0.0.1:18000/health` returned `"status": "healthy"`, and the robots/sitemap and WebSocket URLs follow the browser host.
- The Docker CLI is not installed on this machine, so `docker compose build` and `docker compose up` could not be executed here. The Compose file, Dockerfiles, and scripts passed static validation; `scripts/start-app.ps1` performs the first image build on a machine with Docker Desktop.

The vulnerability inventory remains documentation only: [vulndb/checklist.md](vulndb/checklist.md) and [vulndb/catalog.json](vulndb/catalog.json).

## Accounts and customer flows

Registration and login are available at `/register` and `/login`; logout is `/logout`. A successful registration signs the new account in and redirects to the storefront. Profile, order history, wishlist, password reset, and order tracking are linked from the customer menu.

Seeded demo accounts are synthetic and intentionally weak: `admin@vulnshop.com` / `admin123` and `user@vulnshop.com` / `password`.

## Test and verification

```powershell
python -m unittest discover -s tests -v
```

The unit tests cover inventory completeness, README and checklist synchronization, source-map consistency, the absence of removed hint comments, rendered view/build-file references, Compose containment, JWT helper behavior, SMTP header handling, reset-token expiry, and an in-memory cart → order → mock-payment → webhook workflow.

For a loopback HTTP smoke test of the storefront, API, and GraphQL service, run `./tests/smoke-local.ps1` in PowerShell. It uses synthetic credentials/data, binds only to `127.0.0.1`, exercises login, registration, cart, checkout, order history, tracking, profile, and logout, and stops the processes when it finishes. GitHub Actions runs the unit and template checks on pushes and pull requests.

## Main areas

- `frontend/` — Vietnamese e-commerce storefront and customer flows
- `backend/` — FastAPI routes for authentication, catalog, cart, orders, payments, users, admin, files, search, coupons, notifications, and webhooks
- `services/graphql/` — GraphQL API
- `services/worker/` — background job examples
- `docker-compose.yml` — lab services with the storefront exposed on 13000 and synthetic database seeds
- `scripts/` — Docker, native, and one-command launchers for Windows and Bash
- `vulndb/` — complete source inventory, searchable checklist, and symbol-level annotation map

High-impact topics such as denial of service, host escape, cloud metadata access, arbitrary command execution, and third-party attack chains must be tested only in disposable, isolated lab infrastructure. Never run tests against systems outside your authorization.

<!-- BEGIN COMPLETE INVENTORY -->
## Complete inventory

> Generated from `vulndb/catalog.json`. Every component and every numbered entry from the brief is listed here; the searchable version remains at `vulndb/index.html` and `vulndb/checklist.md`.

### Application components

All **275** components, with implementation and test status.

| ID | Component | Group | Type | Implementation | Test |
|---:|---|---|---|---|---|
| 1 | DNS | Hạ tầng và Cloud | component | unverified | not_tested |
| 2 | CDN | Hạ tầng và Cloud | component | unverified | not_tested |
| 3 | WAF | Hạ tầng và Cloud | component | unverified | not_tested |
| 4 | Cloud Infrastructure | Hạ tầng và Cloud | component | unverified | not_tested |
| 5 | Cloud Storage (S3, Blob Storage) | Hạ tầng và Cloud | component | unverified | not_tested |
| 6 | Load Balancer | Hạ tầng và Cloud | component | unverified | not_tested |
| 7 | Reverse Proxy | Hạ tầng và Cloud | component | unverified | not_tested |
| 8 | API Gateway | Hạ tầng và Cloud | component | unverified | not_tested |
| 9 | Web Server (Nginx, Apache, IIS) | Hạ tầng và Cloud | component | unverified | not_tested |
| 10 | Application Server | Hạ tầng và Cloud | component | unverified | not_tested |
| 11 | Containerization (Docker) | Hạ tầng và Cloud | component | unverified | not_tested |
| 12 | Container Orchestration (Kubernetes) | Hạ tầng và Cloud | component | unverified | not_tested |
| 13 | Virtual Machines | Hạ tầng và Cloud | component | unverified | not_tested |
| 14 | Serverless Functions | Hạ tầng và Cloud | component | unverified | not_tested |
| 15 | Edge Computing | Hạ tầng và Cloud | component | unverified | not_tested |
| 16 | Multi-Region Deployment | Hạ tầng và Cloud | component | unverified | not_tested |
| 17 | Network Infrastructure | Hạ tầng và Cloud | component | unverified | not_tested |
| 18 | Firewall | Hạ tầng và Cloud | component | unverified | not_tested |
| 19 | VPN | Hạ tầng và Cloud | component | unverified | not_tested |
| 20 | SSH | Hạ tầng và Cloud | component | unverified | not_tested |
| 21 | Homepage | Frontend và Browser | component | observed | verified |
| 22 | Product Listing | Frontend và Browser | component | observed | verified |
| 23 | Product Detail | Frontend và Browser | component | observed | verified |
| 24 | Product Search | Frontend và Browser | component | observed | verified |
| 25 | Product Filtering | Frontend và Browser | component | observed | verified |
| 26 | Product Sorting | Frontend và Browser | component | unverified | not_tested |
| 27 | Category Navigation | Frontend và Browser | component | unverified | not_tested |
| 28 | Shopping Cart | Frontend và Browser | component | observed | verified |
| 29 | Wishlist | Frontend và Browser | component | unverified | not_tested |
| 30 | Checkout | Frontend và Browser | component | observed | verified |
| 31 | Order Tracking | Frontend và Browser | component | observed | verified |
| 32 | User Profile | Frontend và Browser | component | observed | verified |
| 33 | Address Book | Frontend và Browser | component | observed | verified |
| 34 | Login | Frontend và Browser | component | observed | verified |
| 35 | Sign Up | Frontend và Browser | component | observed | verified |
| 36 | Logout | Frontend và Browser | component | observed | verified |
| 37 | Forgot Password | Frontend và Browser | component | unverified | not_tested |
| 38 | Reset Password | Frontend và Browser | component | unverified | not_tested |
| 39 | Email Verification | Frontend và Browser | component | unverified | not_tested |
| 40 | Phone Verification | Frontend và Browser | component | unverified | not_tested |
| 41 | Multi-Factor Authentication | Frontend và Browser | component | observed | verified |
| 42 | Social Login | Frontend và Browser | component | observed | verified |
| 43 | OAuth2 / OIDC | Frontend và Browser | component | observed | verified |
| 44 | SSO | Frontend và Browser | component | unverified | not_tested |
| 45 | Session Management | Frontend và Browser | component | observed | verified |
| 46 | Cookies | Frontend và Browser | component | observed | verified |
| 47 | LocalStorage | Frontend và Browser | component | unverified | not_tested |
| 48 | SessionStorage | Frontend và Browser | component | unverified | not_tested |
| 49 | IndexedDB | Frontend và Browser | component | unverified | not_tested |
| 50 | Service Workers | Frontend và Browser | component | unverified | not_tested |
| 51 | Browser Cache | Frontend và Browser | component | unverified | not_tested |
| 52 | CORS | Frontend và Browser | component | observed | verified |
| 53 | CSP | Frontend và Browser | component | observed | verified |
| 54 | HTTP Security Headers | Frontend và Browser | component | observed | verified |
| 55 | Responsive Design | Frontend và Browser | component | unverified | not_tested |
| 56 | Admin Dashboard | Frontend và Browser | component | observed | verified |
| 57 | User Dashboard | Frontend và Browser | component | unverified | not_tested |
| 58 | REST API | Backend và API | component | observed | verified |
| 59 | GraphQL | Backend và API | component | observed | verified |
| 60 | GraphQL Federation | Backend và API | component | unverified | not_tested |
| 61 | gRPC | Backend và API | component | unverified | not_tested |
| 62 | WebSocket | Backend và API | component | observed | verified |
| 63 | Webhook | Backend và API | component | observed | verified |
| 64 | Microservices | Backend và API | component | unverified | not_tested |
| 65 | Monolithic Architecture | Backend và API | component | unverified | not_tested |
| 66 | API Versioning | Backend và API | component | unverified | not_tested |
| 67 | Rate Limiting | Backend và API | component | observed | verified |
| 68 | Input Validation | Backend và API | component | observed | verified |
| 69 | Output Encoding | Backend và API | component | unverified | not_tested |
| 70 | Authentication | Backend và API | component | observed | verified |
| 71 | Authorization | Backend và API | component | observed | verified |
| 72 | RBAC | Backend và API | component | observed | verified |
| 73 | ABAC | Backend và API | component | unverified | not_tested |
| 74 | Multi-Tenancy | Backend và API | component | unverified | not_tested |
| 75 | Business Logic | Backend và API | component | observed | verified |
| 76 | Background Jobs | Backend và API | component | unverified | not_tested |
| 77 | Workflow Engine | Backend và API | component | unverified | not_tested |
| 78 | Event-Driven Architecture | Backend và API | component | unverified | not_tested |
| 79 | Message Queue | Backend và API | component | unverified | not_tested |
| 80 | Event Streaming | Backend và API | component | unverified | not_tested |
| 81 | Product Management | Chức năng thương mại điện tử | component | observed | verified |
| 82 | Product Variants | Chức năng thương mại điện tử | component | unverified | not_tested |
| 83 | Product Attributes | Chức năng thương mại điện tử | component | unverified | not_tested |
| 84 | Product Categories | Chức năng thương mại điện tử | component | unverified | not_tested |
| 85 | Product Brands | Chức năng thương mại điện tử | component | unverified | not_tested |
| 86 | Product Pricing | Chức năng thương mại điện tử | component | observed | verified |
| 87 | Discount Management | Chức năng thương mại điện tử | component | unverified | not_tested |
| 88 | Coupon Management | Chức năng thương mại điện tử | component | observed | verified |
| 89 | Flash Sale | Chức năng thương mại điện tử | component | observed | verified |
| 90 | Inventory Management | Chức năng thương mại điện tử | component | unverified | not_tested |
| 91 | Stock Reservation | Chức năng thương mại điện tử | component | unverified | not_tested |
| 92 | Shopping Cart | Chức năng thương mại điện tử | component | observed | verified |
| 93 | Cart Synchronization | Chức năng thương mại điện tử | component | unverified | not_tested |
| 94 | Guest Checkout | Chức năng thương mại điện tử | component | observed | verified |
| 95 | Customer Checkout | Chức năng thương mại điện tử | component | observed | verified |
| 96 | Shipping Management | Chức năng thương mại điện tử | component | observed | verified |
| 97 | Shipping Fee Calculation | Chức năng thương mại điện tử | component | unverified | not_tested |
| 98 | Shipping Address | Chức năng thương mại điện tử | component | unverified | not_tested |
| 99 | Billing Address | Chức năng thương mại điện tử | component | unverified | not_tested |
| 100 | Payment Gateway | Chức năng thương mại điện tử | component | observed | verified |
| 101 | Cash on Delivery (COD) | Chức năng thương mại điện tử | component | observed | verified |
| 102 | Payment Refund | Chức năng thương mại điện tử | component | observed | verified |
| 103 | Payment Callback | Chức năng thương mại điện tử | component | observed | verified |
| 104 | Payment Webhook | Chức năng thương mại điện tử | component | observed | verified |
| 105 | Order Management | Chức năng thương mại điện tử | component | observed | verified |
| 106 | Order History | Chức năng thương mại điện tử | component | observed | verified |
| 107 | Order Cancellation | Chức năng thương mại điện tử | component | observed | verified |
| 108 | Order Return | Chức năng thương mại điện tử | component | unverified | not_tested |
| 109 | Order Exchange | Chức năng thương mại điện tử | component | unverified | not_tested |
| 110 | Invoice Generation | Chức năng thương mại điện tử | component | unverified | not_tested |
| 111 | Tax Calculation | Chức năng thương mại điện tử | component | unverified | not_tested |
| 112 | Review & Rating | Chức năng thương mại điện tử | component | observed | verified |
| 113 | Product Q&A | Chức năng thương mại điện tử | component | observed | verified |
| 114 | Wishlist | Chức năng thương mại điện tử | component | unverified | not_tested |
| 115 | Recently Viewed Products | Chức năng thương mại điện tử | component | unverified | not_tested |
| 116 | Recommendation System | Chức năng thương mại điện tử | component | observed | verified |
| 117 | Loyalty Points | Chức năng thương mại điện tử | component | unverified | not_tested |
| 118 | Gift Cards | Chức năng thương mại điện tử | component | unverified | not_tested |
| 119 | Affiliate System | Chức năng thương mại điện tử | component | unverified | not_tested |
| 120 | Subscription Products | Chức năng thương mại điện tử | component | unverified | not_tested |
| 121 | Notification System | Chức năng thương mại điện tử | component | observed | verified |
| 122 | Email Notification | Chức năng thương mại điện tử | component | unverified | not_tested |
| 123 | SMS Notification | Chức năng thương mại điện tử | component | unverified | not_tested |
| 124 | Push Notification | Chức năng thương mại điện tử | component | unverified | not_tested |
| 125 | SQL Database (PostgreSQL, MySQL) | Database và Data Storage | component | unverified | not_tested |
| 126 | NoSQL Database (MongoDB) | Database và Data Storage | component | unverified | not_tested |
| 127 | Graph Database (Neo4j) | Database và Data Storage | component | unverified | not_tested |
| 128 | In-Memory Database (Redis) | Database và Data Storage | component | unverified | not_tested |
| 129 | Search Engine (Elasticsearch, OpenSearch) | Database và Data Storage | component | unverified | not_tested |
| 130 | Time-Series Database | Database và Data Storage | component | unverified | not_tested |
| 131 | Object Storage | Database và Data Storage | component | unverified | not_tested |
| 132 | File System | Database và Data Storage | component | unverified | not_tested |
| 133 | Data Replication | Database và Data Storage | component | unverified | not_tested |
| 134 | Database Sharding | Database và Data Storage | component | unverified | not_tested |
| 135 | Database Backup & Recovery | Database và Data Storage | component | unverified | not_tested |
| 136 | Database Migration | Database và Data Storage | component | unverified | not_tested |
| 137 | Database Encryption | Database và Data Storage | component | unverified | not_tested |
| 138 | Data Masking | Database và Data Storage | component | unverified | not_tested |
| 139 | Admin Dashboard | Quản trị hệ thống | component | unverified | not_tested |
| 140 | User Management | Quản trị hệ thống | component | observed | verified |
| 141 | Product Management | Quản trị hệ thống | component | unverified | not_tested |
| 142 | Category Management | Quản trị hệ thống | component | unverified | not_tested |
| 143 | Order Management | Quản trị hệ thống | component | unverified | not_tested |
| 144 | Inventory Management | Quản trị hệ thống | component | unverified | not_tested |
| 145 | Payment Management | Quản trị hệ thống | component | observed | verified |
| 146 | Refund Management | Quản trị hệ thống | component | unverified | not_tested |
| 147 | Coupon Management | Quản trị hệ thống | component | unverified | not_tested |
| 148 | Promotion Management | Quản trị hệ thống | component | unverified | not_tested |
| 149 | Role & Permission Management | Quản trị hệ thống | component | observed | verified |
| 150 | Audit Log | Quản trị hệ thống | component | unverified | not_tested |
| 151 | System Configuration | Quản trị hệ thống | component | unverified | not_tested |
| 152 | Feature Flags | Quản trị hệ thống | component | unverified | not_tested |
| 153 | Tenant Management | Quản trị hệ thống | component | unverified | not_tested |
| 154 | CMS | Quản trị hệ thống | component | unverified | not_tested |
| 155 | Analytics & Reporting | Quản trị hệ thống | component | unverified | not_tested |
| 156 | External APIs | Tích hợp bên thứ ba | component | unverified | not_tested |
| 157 | Payment Providers | Tích hợp bên thứ ba | component | unverified | not_tested |
| 158 | Shipping Providers | Tích hợp bên thứ ba | component | unverified | not_tested |
| 159 | Email Service (SMTP) | Tích hợp bên thứ ba | component | unverified | not_tested |
| 160 | SMS Service | Tích hợp bên thứ ba | component | unverified | not_tested |
| 161 | OAuth Providers | Tích hợp bên thứ ba | component | unverified | not_tested |
| 162 | CAPTCHA | Tích hợp bên thứ ba | component | unverified | not_tested |
| 163 | Maps & Geolocation | Tích hợp bên thứ ba | component | unverified | not_tested |
| 164 | Analytics Services | Tích hợp bên thứ ba | component | unverified | not_tested |
| 165 | CRM | Tích hợp bên thứ ba | component | unverified | not_tested |
| 166 | ERP | Tích hợp bên thứ ba | component | unverified | not_tested |
| 167 | Search Services | Tích hợp bên thứ ba | component | observed | verified |
| 168 | AI Integration | Tích hợp bên thứ ba | component | unverified | not_tested |
| 169 | CI/CD Pipeline | DevOps và vận hành | component | unverified | not_tested |
| 170 | Source Code Repository | DevOps và vận hành | component | unverified | not_tested |
| 171 | Dependency Management | DevOps và vận hành | component | observed | verified |
| 172 | Package Registry | DevOps và vận hành | component | unverified | not_tested |
| 173 | Infrastructure as Code (Terraform, Ansible) | DevOps và vận hành | component | unverified | not_tested |
| 174 | Docker Compose | DevOps và vận hành | component | unverified | not_tested |
| 175 | Kubernetes | DevOps và vận hành | component | unverified | not_tested |
| 176 | Secrets Management | DevOps và vận hành | component | unverified | not_tested |
| 177 | Configuration Management | DevOps và vận hành | component | unverified | not_tested |
| 178 | Monitoring | DevOps và vận hành | component | unverified | not_tested |
| 179 | Logging | DevOps và vận hành | component | observed | verified |
| 180 | Distributed Tracing | DevOps và vận hành | component | unverified | not_tested |
| 181 | Error Tracking | DevOps và vận hành | component | unverified | not_tested |
| 182 | Metrics & Alerting | DevOps và vận hành | component | unverified | not_tested |
| 183 | Backup & Recovery | DevOps và vận hành | component | unverified | not_tested |
| 184 | Disaster Recovery | DevOps và vận hành | component | unverified | not_tested |
| 185 | Multi-Region Deployment | DevOps và vận hành | component | unverified | not_tested |
| 186 | SQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 187 | NoSQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 188 | GraphQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 189 | XSS | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 190 | CSRF | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 191 | SSRF | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 192 | IDOR / BOLA | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 193 | Broken Authentication | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 194 | Broken Authorization | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 195 | Privilege Escalation | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 196 | Session Hijacking | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 197 | Session Fixation | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 198 | JWT Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 199 | OAuth Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 200 | SAML Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 201 | Password Reset Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 202 | Account Enumeration | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 203 | Brute Force | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 204 | Credential Stuffing | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 205 | Rate Limit Bypass | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 206 | Business Logic Abuse | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 207 | Price Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 208 | Coupon Abuse | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 209 | Cart Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 210 | Payment Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 211 | Race Conditions | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 212 | Inventory Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 213 | Checkout Bypass | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 214 | Payment Replay | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 215 | Webhook Forgery | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 216 | File Upload Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 217 | Path Traversal | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 218 | Local File Inclusion (LFI) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 219 | Remote File Inclusion (RFI) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 220 | Remote Code Execution (RCE) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 221 | Server-Side Template Injection (SSTI) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 222 | XXE | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 223 | Deserialization Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 224 | CORS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 225 | CSP Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 226 | TLS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 227 | Security Header Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 228 | DNS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 229 | Subdomain Takeover | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 230 | Open Redirect | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 231 | Clickjacking | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 232 | Host Header Injection | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 233 | HTTP Request Smuggling | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 234 | Cache Poisoning | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 235 | Cache Deception | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 236 | API Mass Assignment | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 237 | API Excessive Data Exposure | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 238 | GraphQL Introspection Abuse | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 239 | GraphQL DoS | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 240 | WebSocket Authorization Bypass | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 241 | Webhook SSRF | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 242 | Cloud Storage Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 243 | IAM Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 244 | Container Escape | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 245 | Kubernetes Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 246 | Secrets Exposure | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 247 | CI/CD Pipeline Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 248 | Dependency / Supply Chain Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 249 | Logging & Monitoring Weaknesses | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 250 | Backup Exposure | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 251 | Information Disclosure | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 252 | Sensitive Data Exposure | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 253 | PII Leakage | Các chức năng và bề mặt kiểm thử bảo mật | component | observed | verified |
| 254 | Business Email Compromise Scenarios | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 255 | Denial of Service (DoS) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 256 | Distributed Denial of Service (DDoS) | Các chức năng và bề mặt kiểm thử bảo mật | component | unverified | not_tested |
| 257 | Đăng ký → Xác minh email → Đăng nhập | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 258 | Đăng nhập → Quản lý hồ sơ → Đổi mật khẩu | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 259 | Tìm kiếm → Xem sản phẩm → Thêm giỏ hàng | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 260 | Giỏ hàng → Áp mã giảm giá → Checkout | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 261 | Checkout → Thanh toán → Xác nhận đơn hàng | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 262 | Thanh toán thất bại → Thử lại thanh toán | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 263 | Đặt hàng → Hủy đơn → Hoàn tiền | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 264 | Đặt hàng → Theo dõi vận chuyển → Nhận hàng | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 265 | Yêu cầu đổi trả → Duyệt yêu cầu → Hoàn tiền | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 266 | Admin → Quản lý người dùng → Phân quyền | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 267 | Admin → Quản lý sản phẩm → Quản lý kho | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 268 | Admin → Quản lý đơn hàng → Quản lý thanh toán | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 269 | User A → Truy cập dữ liệu User B (kiểm thử IDOR/BOLA) | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 270 | User thường → Truy cập chức năng Admin (kiểm thử phân quyền) | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 271 | Guest → Truy cập tài nguyên yêu cầu đăng nhập | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 272 | Nhiều người dùng đồng thời mua sản phẩm giới hạn tồn kho | Các kịch bản nghiệp vụ end-to-end | component | unverified | not_tested |
| 273 | Gửi lại payment callback/webhook | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 274 | Thay đổi giá, số lượng, coupon trong quá trình checkout | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |
| 275 | Truy cập API trực tiếp bỏ qua giao diện frontend | Các kịch bản nghiệp vụ end-to-end | component | observed | verified |

### Numbered catalog

All **726** entries: 661 vulnerability topics, 29 attack chains, and 36 test-matrix fields.

| ID | Name | Type | Group | Implementation | Test |
|---:|---|---|---|---|---|
| 1 | Subdomain Enumeration Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 2 | Subdomain Takeover | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 3 | DNS Zone Transfer | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 4 | DNS Misconfiguration | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 5 | DNS Cache Poisoning | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 6 | Virtual Host Misconfiguration | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 7 | Server Version Disclosure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 8 | Technology Stack Disclosure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 9 | Framework Fingerprinting | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 10 | Debug Information Exposure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 11 | Source Code Disclosure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 12 | Source Map Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 13 | Git Repository Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 14 | SVN Repository Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 15 | Backup File Exposure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 16 | Configuration File Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 17 | Environment File Exposure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 18 | API Documentation Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 19 | Swagger Exposure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 20 | GraphQL Introspection Exposure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 21 | Directory Listing | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 22 | Hidden Endpoint Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 23 | Sensitive Metadata Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 24 | Error Message Information Leakage | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 25 | Stack Trace Disclosure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 26 | Internal IP Disclosure | vulnerability | Reconnaissance & Information Disclosure | observed | verified |
| 27 | Cloud Metadata Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 28 | Public Cloud Storage Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 29 | PII Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 30 | Sensitive Business Data Exposure | vulnerability | Reconnaissance & Information Disclosure | unverified | not_tested |
| 31 | Weak Password Policy | vulnerability | Authentication Vulnerabilities | observed | verified |
| 32 | Weak Default Credentials | vulnerability | Authentication Vulnerabilities | observed | verified |
| 33 | Default Admin Account | vulnerability | Authentication Vulnerabilities | observed | verified |
| 34 | Username Enumeration | vulnerability | Authentication Vulnerabilities | observed | verified |
| 35 | Email Enumeration | vulnerability | Authentication Vulnerabilities | observed | verified |
| 36 | Phone Number Enumeration | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 37 | Account Enumeration | vulnerability | Authentication Vulnerabilities | observed | verified |
| 38 | Brute Force | vulnerability | Authentication Vulnerabilities | observed | verified |
| 39 | Password Spraying | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 40 | Credential Stuffing | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 41 | Missing Login Rate Limiting | vulnerability | Authentication Vulnerabilities | observed | verified |
| 42 | Rate Limit Bypass | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 43 | CAPTCHA Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 44 | MFA Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 45 | MFA Fatigue | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 46 | OTP Brute Force | vulnerability | Authentication Vulnerabilities | observed | verified |
| 47 | OTP Replay | vulnerability | Authentication Vulnerabilities | observed | verified |
| 48 | OTP Predictability | vulnerability | Authentication Vulnerabilities | observed | verified |
| 49 | OTP Expiration Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 50 | OTP Race Condition | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 51 | Password Reset Token Leakage | vulnerability | Authentication Vulnerabilities | observed | verified |
| 52 | Password Reset Token Prediction | vulnerability | Authentication Vulnerabilities | observed | verified |
| 53 | Password Reset Token Reuse | vulnerability | Authentication Vulnerabilities | observed | verified |
| 54 | Password Reset Token Not Expiring | vulnerability | Authentication Vulnerabilities | observed | verified |
| 55 | Password Reset Account Takeover | vulnerability | Authentication Vulnerabilities | observed | verified |
| 56 | Password Reset Host Header Injection | vulnerability | Authentication Vulnerabilities | observed | verified |
| 57 | Insecure Email Verification | vulnerability | Authentication Vulnerabilities | observed | verified |
| 58 | Email Verification Token Reuse | vulnerability | Authentication Vulnerabilities | observed | verified |
| 59 | Email Verification Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 60 | Phone Verification Bypass | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 61 | Authentication Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 62 | Insecure Remember Me | vulnerability | Authentication Vulnerabilities | observed | verified |
| 63 | Broken Authentication | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 64 | Authentication Logic Flaws | vulnerability | Authentication Vulnerabilities | observed | verified |
| 65 | Session Fixation | vulnerability | Authentication Vulnerabilities | observed | verified |
| 66 | Session Hijacking | vulnerability | Authentication Vulnerabilities | observed | verified |
| 67 | Session Replay | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 68 | Session Not Invalidated After Logout | vulnerability | Authentication Vulnerabilities | observed | verified |
| 69 | Session Not Invalidated After Password Change | vulnerability | Authentication Vulnerabilities | observed | verified |
| 70 | Concurrent Session Abuse | vulnerability | Authentication Vulnerabilities | observed | verified |
| 71 | Insecure Session Cookie | vulnerability | Authentication Vulnerabilities | observed | verified |
| 72 | JWT None Algorithm | vulnerability | Authentication Vulnerabilities | observed | verified |
| 73 | JWT Algorithm Confusion | vulnerability | Authentication Vulnerabilities | observed | verified |
| 74 | JWT Signature Validation Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 75 | JWT Weak Secret | vulnerability | Authentication Vulnerabilities | observed | verified |
| 76 | JWT Key Confusion | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 77 | JWT Expiration Validation Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 78 | JWT Audience Validation Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 79 | JWT Issuer Validation Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 80 | JWT Token Replay | vulnerability | Authentication Vulnerabilities | observed | verified |
| 81 | JWT Sensitive Data Exposure | vulnerability | Authentication Vulnerabilities | observed | verified |
| 82 | Refresh Token Reuse | vulnerability | Authentication Vulnerabilities | observed | verified |
| 83 | Refresh Token Rotation Failure | vulnerability | Authentication Vulnerabilities | observed | verified |
| 84 | OAuth Account Takeover | vulnerability | Authentication Vulnerabilities | observed | verified |
| 85 | OAuth Redirect URI Manipulation | vulnerability | Authentication Vulnerabilities | observed | verified |
| 86 | OAuth State Parameter CSRF | vulnerability | Authentication Vulnerabilities | observed | verified |
| 87 | OAuth PKCE Bypass | vulnerability | Authentication Vulnerabilities | observed | verified |
| 88 | OAuth Token Leakage | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 89 | OAuth Scope Escalation | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 90 | OpenID Connect Misconfiguration | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 91 | SAML Signature Validation Bypass | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 92 | SAML XML Signature Wrapping | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 93 | SSO Authentication Bypass | vulnerability | Authentication Vulnerabilities | unverified | not_tested |
| 94 | Social Login Account Linking Abuse | vulnerability | Authentication Vulnerabilities | observed | verified |
| 95 | Insecure Account Linking | vulnerability | Authentication Vulnerabilities | observed | verified |
| 96 | Broken Access Control | vulnerability | Authorization & Access Control | unverified | not_tested |
| 97 | IDOR | vulnerability | Authorization & Access Control | observed | verified |
| 98 | BOLA | vulnerability | Authorization & Access Control | observed | verified |
| 99 | BFLA | vulnerability | Authorization & Access Control | unverified | not_tested |
| 100 | Horizontal Privilege Escalation | vulnerability | Authorization & Access Control | unverified | not_tested |
| 101 | Vertical Privilege Escalation | vulnerability | Authorization & Access Control | unverified | not_tested |
| 102 | Role Escalation | vulnerability | Authorization & Access Control | observed | verified |
| 103 | Privilege Escalation Through Mass Assignment | vulnerability | Authorization & Access Control | observed | verified |
| 104 | Missing Function-Level Authorization | vulnerability | Authorization & Access Control | observed | verified |
| 105 | Missing Object-Level Authorization | vulnerability | Authorization & Access Control | unverified | not_tested |
| 106 | Missing Property-Level Authorization | vulnerability | Authorization & Access Control | unverified | not_tested |
| 107 | Insecure Direct Object Reference | vulnerability | Authorization & Access Control | unverified | not_tested |
| 108 | Admin Endpoint Exposure | vulnerability | Authorization & Access Control | observed | verified |
| 109 | Admin Panel Authorization Bypass | vulnerability | Authorization & Access Control | unverified | not_tested |
| 110 | Tenant Isolation Bypass | vulnerability | Authorization & Access Control | unverified | not_tested |
| 111 | Cross-Tenant Data Access | vulnerability | Authorization & Access Control | unverified | not_tested |
| 112 | User Data Access Violation | vulnerability | Authorization & Access Control | unverified | not_tested |
| 113 | Unauthorized Order Access | vulnerability | Authorization & Access Control | observed | verified |
| 114 | Unauthorized Invoice Access | vulnerability | Authorization & Access Control | unverified | not_tested |
| 115 | Unauthorized Payment Access | vulnerability | Authorization & Access Control | observed | verified |
| 116 | Unauthorized Address Access | vulnerability | Authorization & Access Control | observed | verified |
| 117 | Unauthorized File Access | vulnerability | Authorization & Access Control | unverified | not_tested |
| 118 | Unauthorized Refund | vulnerability | Authorization & Access Control | unverified | not_tested |
| 119 | Unauthorized Coupon Management | vulnerability | Authorization & Access Control | unverified | not_tested |
| 120 | Unauthorized Inventory Modification | vulnerability | Authorization & Access Control | unverified | not_tested |
| 121 | Unauthorized Role Modification | vulnerability | Authorization & Access Control | observed | verified |
| 122 | Unauthorized User Management | vulnerability | Authorization & Access Control | observed | verified |
| 123 | Forced Browsing | vulnerability | Authorization & Access Control | unverified | not_tested |
| 124 | Parameter-Based Authorization Bypass | vulnerability | Authorization & Access Control | unverified | not_tested |
| 125 | HTTP Method-Based Authorization Bypass | vulnerability | Authorization & Access Control | observed | verified |
| 126 | Inconsistent Authorization Across APIs | vulnerability | Authorization & Access Control | unverified | not_tested |
| 127 | Insecure Resource Ownership Validation | vulnerability | Authorization & Access Control | unverified | not_tested |
| 128 | SQL Injection | vulnerability | Injection Vulnerabilities | observed | verified |
| 129 | Blind SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 130 | Boolean-Based SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 131 | Time-Based SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 132 | Error-Based SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 133 | Union-Based SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 134 | Second-Order SQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 135 | Stored Procedure Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 136 | NoSQL Injection | vulnerability | Injection Vulnerabilities | observed | not_tested |
| 137 | MongoDB Operator Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 138 | GraphQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 139 | LDAP Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 140 | XPath Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 141 | XML Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 142 | XXE | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 143 | Blind XXE | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 144 | SSRF Through XML | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 145 | OS Command Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 146 | Blind OS Command Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 147 | Argument Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 148 | Code Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 149 | PHP Code Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 150 | Java Expression Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 151 | JavaScript Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 152 | Python Code Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 153 | Template Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 154 | Server-Side Template Injection (SSTI) | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 155 | Client-Side Template Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 156 | Expression Language Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 157 | ORM Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 158 | HQL Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 159 | Header Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 160 | CRLF Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 161 | SMTP Injection | vulnerability | Injection Vulnerabilities | observed | verified |
| 162 | IMAP Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 163 | Redis Command Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 164 | Elasticsearch Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 165 | Search Query Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 166 | JSON Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 167 | YAML Deserialization Injection | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 168 | CSV Injection | vulnerability | Injection Vulnerabilities | observed | verified |
| 169 | HTTP Parameter Pollution | vulnerability | Injection Vulnerabilities | unverified | not_tested |
| 170 | Reflected XSS | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 171 | Stored XSS | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 172 | DOM-Based XSS | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 173 | Blind XSS | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 174 | Mutation XSS | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 175 | Self-XSS | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 176 | Context-Specific XSS | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 177 | HTML Injection | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 178 | CSS Injection | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 179 | JavaScript Context Injection | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 180 | CSRF | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 181 | Login CSRF | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 182 | Logout CSRF | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 183 | Stored CSRF | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 184 | SameSite Cookie Misconfiguration | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 185 | Clickjacking | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 186 | UI Redressing | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 187 | CORS Misconfiguration | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 188 | CORS Origin Reflection | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 189 | CORS Credential Exposure | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 190 | CSP Misconfiguration | vulnerability | Cross-Site Vulnerabilities | observed | verified |
| 191 | CSP Bypass | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 192 | PostMessage Origin Validation Bypass | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 193 | Cross-Origin Data Leakage | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 194 | XS-Leaks | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 195 | DOM Clobbering | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 196 | Open Redirect | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 197 | Tabnabbing | vulnerability | Cross-Site Vulnerabilities | unverified | not_tested |
| 198 | SSRF | vulnerability | Server-Side Vulnerabilities | observed | verified |
| 199 | Blind SSRF | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 200 | SSRF to Internal Services | vulnerability | Server-Side Vulnerabilities | observed | verified |
| 201 | SSRF to Cloud Metadata | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 202 | SSRF Through Webhooks | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 203 | SSRF Through Image Processing | vulnerability | Server-Side Vulnerabilities | observed | verified |
| 204 | SSRF Through PDF Generation | vulnerability | Server-Side Vulnerabilities | observed | not_tested |
| 205 | SSRF Through URL Preview | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 206 | SSRF Through Import Functions | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 207 | Local File Inclusion (LFI) | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 208 | Remote File Inclusion (RFI) | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 209 | Path Traversal | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 210 | Directory Traversal | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 211 | Arbitrary File Read | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 212 | Arbitrary File Write | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 213 | Arbitrary File Deletion | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 214 | Remote Code Execution (RCE) | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 215 | Local Code Execution | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 216 | Unsafe Deserialization | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 217 | Insecure Object Deserialization | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 218 | Java Deserialization | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 219 | PHP Deserialization | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 220 | Python Pickle Deserialization | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 221 | Prototype Pollution | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 222 | Server-Side Prototype Pollution | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 223 | HTTP Request Smuggling | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 224 | HTTP Response Splitting | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 225 | Host Header Injection | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 226 | Host Header Poisoning | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 227 | Web Cache Poisoning | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 228 | Web Cache Deception | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 229 | DNS Rebinding | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 230 | Race Condition | vulnerability | Server-Side Vulnerabilities | observed | not_tested |
| 231 | TOCTOU Vulnerability | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 232 | Integer Overflow | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 233 | Integer Underflow | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 234 | Buffer Overflow | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 235 | Memory Corruption | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 236 | Format String Vulnerability | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 237 | Resource Exhaustion | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 238 | Denial of Service (DoS) | vulnerability | Server-Side Vulnerabilities | unverified | not_tested |
| 239 | Regular Expression DoS (ReDoS) | vulnerability | Server-Side Vulnerabilities | observed | not_tested |
| 240 | API1 - Broken Object Level Authorization | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 241 | API2 - Broken Authentication | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 242 | API3 - Broken Object Property Level Authorization | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 243 | API4 - Unrestricted Resource Consumption | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 244 | API5 - Broken Function Level Authorization | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 245 | API6 - Unrestricted Access to Sensitive Business Flows | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 246 | API7 - Server Side Request Forgery | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 247 | API8 - Security Misconfiguration | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 248 | API9 - Improper Inventory Management | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 249 | API10 - Unsafe Consumption of APIs | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 250 | API Mass Assignment | vulnerability | API Security Vulnerabilities | observed | verified |
| 251 | API Excessive Data Exposure | vulnerability | API Security Vulnerabilities | observed | verified |
| 252 | API Parameter Tampering | vulnerability | API Security Vulnerabilities | observed | verified |
| 253 | API Versioning Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 254 | API Authentication Inconsistency | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 255 | API Authorization Inconsistency | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 256 | API Rate Limit Bypass | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 257 | API Pagination Abuse | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 258 | API Filtering Bypass | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 259 | API Sorting Injection | vulnerability | API Security Vulnerabilities | observed | verified |
| 260 | API GraphQL Introspection Abuse | vulnerability | API Security Vulnerabilities | observed | verified |
| 261 | GraphQL Authorization Bypass | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 262 | GraphQL Field-Level Authorization Bypass | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 263 | GraphQL Alias-Based DoS | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 264 | GraphQL Query Depth Abuse | vulnerability | API Security Vulnerabilities | observed | verified |
| 265 | GraphQL Query Complexity Abuse | vulnerability | API Security Vulnerabilities | observed | verified |
| 266 | GraphQL Batching Abuse | vulnerability | API Security Vulnerabilities | observed | verified |
| 267 | GraphQL Subscription Authorization Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 268 | GraphQL Federation Trust Abuse | vulnerability | API Security Vulnerabilities | observed | not_tested |
| 269 | gRPC Authorization Bypass | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 270 | gRPC Reflection Exposure | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 271 | WebSocket Authentication Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 272 | WebSocket Authorization Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 273 | WebSocket Origin Validation Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 274 | WebSocket Message Injection | vulnerability | API Security Vulnerabilities | observed | verified |
| 275 | WebSocket Replay | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 276 | WebSocket Resource Exhaustion | vulnerability | API Security Vulnerabilities | unverified | not_tested |
| 277 | Webhook Forgery | vulnerability | API Security Vulnerabilities | observed | verified |
| 278 | Webhook Signature Validation Bypass | vulnerability | API Security Vulnerabilities | observed | verified |
| 279 | Webhook Replay | vulnerability | API Security Vulnerabilities | observed | verified |
| 280 | Webhook SSRF | vulnerability | API Security Vulnerabilities | observed | verified |
| 281 | Webhook Secret Leakage | vulnerability | API Security Vulnerabilities | observed | verified |
| 282 | Webhook Event Injection | vulnerability | API Security Vulnerabilities | observed | verified |
| 283 | Product Price Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 284 | Negative Price Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 285 | Zero Price Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 286 | Quantity Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 287 | Negative Quantity Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 288 | Cart Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 289 | Cart Ownership Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 290 | Cart Price Desynchronization | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 291 | Cart Item Substitution | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 292 | Coupon Code Brute Force | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 293 | Coupon Enumeration | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 294 | Coupon Reuse | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 295 | Coupon Stacking Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 296 | Coupon Expiration Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 297 | Coupon Scope Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 298 | Discount Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 299 | Promotion Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 300 | Flash Sale Race Condition | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 301 | Inventory Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 302 | Negative Inventory | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 303 | Stock Reservation Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 304 | Overselling | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 305 | Concurrent Purchase Race Condition | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 306 | Checkout Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 307 | Payment Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 308 | Payment Status Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 309 | Payment Amount Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 310 | Payment Currency Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 311 | Payment Callback Forgery | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 312 | Payment Webhook Forgery | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 313 | Payment Replay | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 314 | Duplicate Payment Processing | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 315 | Payment Idempotency Failure | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 316 | Refund Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 317 | Unauthorized Refund | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 318 | Partial Refund Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 319 | Refund Race Condition | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 320 | Order Ownership Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 321 | Order Status Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 322 | Order Cancellation Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 323 | Order Reuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 324 | Shipping Fee Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 325 | Shipping Address Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 326 | Tax Calculation Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 327 | Gift Card Enumeration | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 328 | Gift Card Balance Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 329 | Loyalty Points Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 330 | Affiliate Commission Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 331 | Referral Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 332 | Review Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 333 | Fake Review Injection | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 334 | Review Ownership Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | observed | verified |
| 335 | Wishlist Authorization Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 336 | Subscription Billing Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 337 | Subscription Plan Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 338 | Trial Period Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 339 | Return Policy Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 340 | Exchange Workflow Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 341 | Invoice Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 342 | Business Workflow Bypass | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 343 | Time-of-Check to Time-of-Use Abuse | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 344 | State Machine Manipulation | vulnerability | E-commerce Business Logic Vulnerabilities | unverified | not_tested |
| 345 | Unrestricted File Upload | vulnerability | File Upload & File Processing | observed | verified |
| 346 | Arbitrary File Upload | vulnerability | File Upload & File Processing | unverified | not_tested |
| 347 | Malicious MIME Type | vulnerability | File Upload & File Processing | unverified | not_tested |
| 348 | Extension Validation Bypass | vulnerability | File Upload & File Processing | unverified | not_tested |
| 349 | Double Extension Upload | vulnerability | File Upload & File Processing | unverified | not_tested |
| 350 | Null Byte Extension Bypass | vulnerability | File Upload & File Processing | unverified | not_tested |
| 351 | Polyglot File Upload | vulnerability | File Upload & File Processing | unverified | not_tested |
| 352 | SVG XSS | vulnerability | File Upload & File Processing | unverified | not_tested |
| 353 | HTML File XSS | vulnerability | File Upload & File Processing | unverified | not_tested |
| 354 | Image Processing RCE | vulnerability | File Upload & File Processing | unverified | not_tested |
| 355 | ImageMagick Vulnerability | vulnerability | File Upload & File Processing | observed | not_tested |
| 356 | EXIF Metadata Leakage | vulnerability | File Upload & File Processing | unverified | not_tested |
| 357 | ZIP Slip | vulnerability | File Upload & File Processing | unverified | not_tested |
| 358 | Archive Extraction Traversal | vulnerability | File Upload & File Processing | unverified | not_tested |
| 359 | ZIP Bomb | vulnerability | File Upload & File Processing | unverified | not_tested |
| 360 | XML Bomb | vulnerability | File Upload & File Processing | unverified | not_tested |
| 361 | PDF Processing Vulnerability | vulnerability | File Upload & File Processing | unverified | not_tested |
| 362 | Office Document Macro Abuse | vulnerability | File Upload & File Processing | unverified | not_tested |
| 363 | Malicious File Preview | vulnerability | File Upload & File Processing | unverified | not_tested |
| 364 | Insecure File Download | vulnerability | File Upload & File Processing | unverified | not_tested |
| 365 | Insecure File Sharing | vulnerability | File Upload & File Processing | unverified | not_tested |
| 366 | Public File Storage Exposure | vulnerability | File Upload & File Processing | unverified | not_tested |
| 367 | File Access Control Bypass | vulnerability | File Upload & File Processing | unverified | not_tested |
| 368 | Temporary File Exposure | vulnerability | File Upload & File Processing | unverified | not_tested |
| 369 | Path Traversal Through File Names | vulnerability | File Upload & File Processing | observed | verified |
| 370 | Weak Cryptographic Algorithms | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 371 | Weak Hashing Algorithm | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 372 | MD5 Password Storage | vulnerability | Cryptography & Data Protection | observed | verified |
| 373 | SHA1 Password Storage | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 374 | Weak Password Hashing | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 375 | Hardcoded Encryption Keys | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 376 | Hardcoded Secrets | vulnerability | Cryptography & Data Protection | observed | verified |
| 377 | Weak Random Number Generator | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 378 | Predictable Token Generation | vulnerability | Cryptography & Data Protection | observed | verified |
| 379 | Weak Encryption | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 380 | Improper Encryption Mode | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 381 | ECB Mode Usage | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 382 | IV Reuse | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 383 | Nonce Reuse | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 384 | Padding Oracle | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 385 | Timing Attack | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 386 | Insecure Key Management | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 387 | Private Key Exposure | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 388 | Certificate Validation Bypass | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 389 | TLS Misconfiguration | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 390 | Weak TLS Protocol | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 391 | Weak Cipher Suites | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 392 | Missing HSTS | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 393 | Sensitive Data in URL | vulnerability | Cryptography & Data Protection | observed | verified |
| 394 | Sensitive Data in Logs | vulnerability | Cryptography & Data Protection | observed | verified |
| 395 | Sensitive Data in Browser Storage | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 396 | Sensitive Data in Cache | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 397 | PII Exposure | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 398 | Insecure Data Retention | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 399 | Missing Data Encryption at Rest | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 400 | Missing Data Encryption in Transit | vulnerability | Cryptography & Data Protection | unverified | not_tested |
| 401 | Database Public Exposure | vulnerability | Database Security | observed | verified |
| 402 | Database Default Credentials | vulnerability | Database Security | unverified | not_tested |
| 403 | Weak Database Authentication | vulnerability | Database Security | unverified | not_tested |
| 404 | Database Privilege Escalation | vulnerability | Database Security | unverified | not_tested |
| 405 | Excessive Database Permissions | vulnerability | Database Security | unverified | not_tested |
| 406 | Database SQL Injection | vulnerability | Database Security | observed | verified |
| 407 | Database NoSQL Injection | vulnerability | Database Security | unverified | not_tested |
| 408 | Database Command Injection | vulnerability | Database Security | unverified | not_tested |
| 409 | Database Information Disclosure | vulnerability | Database Security | unverified | not_tested |
| 410 | Database Backup Exposure | vulnerability | Database Security | observed | verified |
| 411 | Database Snapshot Exposure | vulnerability | Database Security | unverified | not_tested |
| 412 | Database Replication Exposure | vulnerability | Database Security | unverified | not_tested |
| 413 | Database Misconfiguration | vulnerability | Database Security | unverified | not_tested |
| 414 | Database Audit Log Disabled | vulnerability | Database Security | unverified | not_tested |
| 415 | Database Encryption Disabled | vulnerability | Database Security | unverified | not_tested |
| 416 | Database Connection String Exposure | vulnerability | Database Security | unverified | not_tested |
| 417 | Database Credential Leakage | vulnerability | Database Security | unverified | not_tested |
| 418 | Database DoS | vulnerability | Database Security | unverified | not_tested |
| 419 | Database Resource Exhaustion | vulnerability | Database Security | unverified | not_tested |
| 420 | Cross-Tenant Database Access | vulnerability | Database Security | unverified | not_tested |
| 421 | Row-Level Security Bypass | vulnerability | Database Security | unverified | not_tested |
| 422 | Database Migration Security Flaws | vulnerability | Database Security | unverified | not_tested |
| 423 | Unsafe Stored Procedures | vulnerability | Database Security | unverified | not_tested |
| 424 | Redis Unauthorized Access | vulnerability | Database Security | unverified | not_tested |
| 425 | MongoDB Unauthorized Access | vulnerability | Database Security | unverified | not_tested |
| 426 | Elasticsearch Unauthorized Access | vulnerability | Database Security | unverified | not_tested |
| 427 | Neo4j Unauthorized Access | vulnerability | Database Security | unverified | not_tested |
| 428 | Graph Database Query Injection | vulnerability | Database Security | unverified | not_tested |
| 429 | Public Cloud Storage Bucket | vulnerability | Cloud Security | unverified | not_tested |
| 430 | Cloud IAM Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 431 | Excessive Cloud Permissions | vulnerability | Cloud Security | unverified | not_tested |
| 432 | Cloud Privilege Escalation | vulnerability | Cloud Security | unverified | not_tested |
| 433 | Cloud Metadata SSRF | vulnerability | Cloud Security | unverified | not_tested |
| 434 | Cloud Credential Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 435 | Cloud Access Key Leakage | vulnerability | Cloud Security | observed | verified |
| 436 | Cloud Secret Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 437 | Cloud Storage ACL Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 438 | Cloud Snapshot Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 439 | Cloud Backup Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 440 | Cloud Database Public Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 441 | Cloud Network Security Group Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 442 | Cloud Firewall Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 443 | Cloud Logging Disabled | vulnerability | Cloud Security | unverified | not_tested |
| 444 | Cloud Audit Trail Disabled | vulnerability | Cloud Security | unverified | not_tested |
| 445 | Cloud KMS Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 446 | Cloud Encryption Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 447 | Cloud Function Misconfiguration | vulnerability | Cloud Security | unverified | not_tested |
| 448 | Serverless Function Authorization Bypass | vulnerability | Cloud Security | unverified | not_tested |
| 449 | Serverless Event Injection | vulnerability | Cloud Security | unverified | not_tested |
| 450 | Serverless Secret Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 451 | Cross-Account Access | vulnerability | Cloud Security | unverified | not_tested |
| 452 | Cross-Region Data Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 453 | Container Registry Exposure | vulnerability | Cloud Security | unverified | not_tested |
| 454 | Public Artifact Repository | vulnerability | Cloud Security | unverified | not_tested |
| 455 | Cloud Resource Enumeration | vulnerability | Cloud Security | unverified | not_tested |
| 456 | Cloud Resource Takeover | vulnerability | Cloud Security | unverified | not_tested |
| 457 | Insecure Cloud API | vulnerability | Cloud Security | unverified | not_tested |
| 458 | Open Ports | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 459 | Unnecessary Network Services | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 460 | Insecure Network Protocols | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 461 | Plaintext HTTP | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 462 | FTP Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 463 | Telnet Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 464 | SSH Weak Authentication | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 465 | SSH Weak Configuration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 466 | SMB Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 467 | NFS Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 468 | SNMP Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 469 | Firewall Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 470 | Network Segmentation Failure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 471 | Internal Service Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 472 | Internal Network Access | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 473 | VPN Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 474 | Reverse Proxy Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 475 | Load Balancer Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 476 | API Gateway Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 477 | TLS Certificate Expiration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 478 | Certificate Hostname Mismatch | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 479 | Certificate Chain Validation Failure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 480 | HTTP Security Header Misconfiguration | vulnerability | Network & Infrastructure Security | observed | verified |
| 481 | HTTP/2 Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 482 | HTTP/3 Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 483 | QUIC Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 484 | IPv6 Security Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 485 | IP Spoofing Trust Issues | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 486 | Proxy Trust Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 487 | Rate Limiting Misconfiguration | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 488 | Network DoS | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 489 | DNS Cache Poisoning | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 490 | ARP Spoofing Exposure | vulnerability | Network & Infrastructure Security | unverified | not_tested |
| 491 | Privileged Container | vulnerability | Docker & Container Security | unverified | not_tested |
| 492 | Container Running as Root | vulnerability | Docker & Container Security | unverified | not_tested |
| 493 | Docker Socket Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 494 | Container Escape | vulnerability | Docker & Container Security | unverified | not_tested |
| 495 | Host Filesystem Mount Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 496 | Sensitive Environment Variable Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 497 | Container Capability Misconfiguration | vulnerability | Docker & Container Security | unverified | not_tested |
| 498 | Insecure Container Image | vulnerability | Docker & Container Security | unverified | not_tested |
| 499 | Vulnerable Base Image | vulnerability | Docker & Container Security | unverified | not_tested |
| 500 | Untrusted Image Usage | vulnerability | Docker & Container Security | unverified | not_tested |
| 501 | Image Signature Validation Missing | vulnerability | Docker & Container Security | unverified | not_tested |
| 502 | Container Registry Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 503 | Docker API Unauthorized Access | vulnerability | Docker & Container Security | unverified | not_tested |
| 504 | Container Network Misconfiguration | vulnerability | Docker & Container Security | unverified | not_tested |
| 505 | Container Secret Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 506 | Container Resource Limit Missing | vulnerability | Docker & Container Security | unverified | not_tested |
| 507 | Container Runtime Vulnerability | vulnerability | Docker & Container Security | unverified | not_tested |
| 508 | Insecure Docker Compose Configuration | vulnerability | Docker & Container Security | unverified | not_tested |
| 509 | Container Log Sensitive Data Exposure | vulnerability | Docker & Container Security | unverified | not_tested |
| 510 | Container Supply Chain Vulnerability | vulnerability | Docker & Container Security | unverified | not_tested |
| 511 | Kubernetes API Server Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 512 | Kubernetes Dashboard Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 513 | Anonymous API Access | vulnerability | Kubernetes Security | unverified | not_tested |
| 514 | RBAC Misconfiguration | vulnerability | Kubernetes Security | unverified | not_tested |
| 515 | Excessive Service Account Permissions | vulnerability | Kubernetes Security | unverified | not_tested |
| 516 | Service Account Token Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 517 | Pod Privilege Escalation | vulnerability | Kubernetes Security | unverified | not_tested |
| 518 | Privileged Pod | vulnerability | Kubernetes Security | unverified | not_tested |
| 519 | HostPath Mount Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 520 | HostNetwork Misconfiguration | vulnerability | Kubernetes Security | unverified | not_tested |
| 521 | HostPID Misconfiguration | vulnerability | Kubernetes Security | unverified | not_tested |
| 522 | Container Escape | vulnerability | Kubernetes Security | unverified | not_tested |
| 523 | Insecure Network Policies | vulnerability | Kubernetes Security | unverified | not_tested |
| 524 | Namespace Isolation Failure | vulnerability | Kubernetes Security | unverified | not_tested |
| 525 | Secrets Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 526 | ConfigMap Sensitive Data Exposure | vulnerability | Kubernetes Security | unverified | not_tested |
| 527 | etcd Unauthorized Access | vulnerability | Kubernetes Security | unverified | not_tested |
| 528 | Admission Controller Misconfiguration | vulnerability | Kubernetes Security | unverified | not_tested |
| 529 | Insecure Ingress Configuration | vulnerability | Kubernetes Security | unverified | not_tested |
| 530 | Kubernetes Audit Logging Disabled | vulnerability | Kubernetes Security | unverified | not_tested |
| 531 | Resource Quota Missing | vulnerability | Kubernetes Security | unverified | not_tested |
| 532 | Kubernetes Supply Chain Vulnerability | vulnerability | Kubernetes Security | unverified | not_tested |
| 533 | Git Repository Secret Exposure | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 534 | Hardcoded Credentials | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 535 | CI/CD Secret Leakage | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 536 | Pipeline Permission Misconfiguration | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 537 | Pipeline Injection | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 538 | Build Script Injection | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 539 | Dependency Confusion | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 540 | Dependency Hijacking | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 541 | Typosquatting | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 542 | Malicious Package Installation | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 543 | Vulnerable Dependencies | vulnerability | CI/CD & Supply Chain Security | observed | verified |
| 544 | Outdated Dependencies | vulnerability | CI/CD & Supply Chain Security | observed | verified |
| 545 | Insecure Package Registry | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 546 | Artifact Tampering | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 547 | Build Artifact Exposure | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 548 | Insecure Deployment Credentials | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 549 | Unprotected Deployment Branch | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 550 | Pull Request Workflow Abuse | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 551 | Insecure GitHub Actions | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 552 | Insecure GitLab CI | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 553 | Software Bill of Materials Missing | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 554 | Missing Dependency Integrity Verification | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 555 | Unsigned Container Images | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 556 | Compromised Build Pipeline | vulnerability | CI/CD & Supply Chain Security | unverified | not_tested |
| 557 | Sensitive Data Logging | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 558 | Password Logging | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 559 | Token Logging | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 560 | PII Logging | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 561 | Log Injection | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 562 | CRLF Log Injection | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 563 | Audit Log Tampering | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 564 | Audit Log Deletion | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 565 | Missing Security Audit Trail | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 566 | Missing Authentication Monitoring | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 567 | Missing Authorization Monitoring | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 568 | Missing Alerting | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 569 | Monitoring Dashboard Exposure | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 570 | Metrics Endpoint Exposure | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 571 | Debug Endpoint Exposure | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 572 | Health Check Information Leakage | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 573 | Trace Data Exposure | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 574 | Distributed Tracing Data Leakage | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 575 | Error Tracking Data Leakage | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 576 | Backup Data Exposure | vulnerability | Logging, Monitoring & Operational Security | observed | verified |
| 577 | Disaster Recovery Misconfiguration | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 578 | Insecure Log Storage | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 579 | Log Retention Misconfiguration | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 580 | Monitoring Access Control Bypass | vulnerability | Logging, Monitoring & Operational Security | unverified | not_tested |
| 581 | HTTP Flood | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 582 | Slow HTTP Attack | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 583 | Slowloris | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 584 | Application Layer DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 585 | API Resource Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 586 | GraphQL Query DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 587 | Regex DoS | vulnerability | DoS & Resource Exhaustion | observed | not_tested |
| 588 | Large Payload DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 589 | File Upload DoS | vulnerability | DoS & Resource Exhaustion | observed | not_tested |
| 590 | Image Processing DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 591 | PDF Processing DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 592 | ZIP Bomb DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 593 | Database Query DoS | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 594 | Connection Pool Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 595 | Thread Pool Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 596 | Memory Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 597 | CPU Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 598 | Queue Flooding | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 599 | Message Queue Poisoning | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 600 | WebSocket Connection Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 601 | Rate Limit Bypass | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 602 | Cache Exhaustion | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 603 | Unbounded Pagination | vulnerability | DoS & Resource Exhaustion | observed | verified |
| 604 | Unbounded Search Query | vulnerability | DoS & Resource Exhaustion | unverified | not_tested |
| 605 | DOM-Based XSS | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 606 | Client-Side Validation Bypass | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 607 | Sensitive Data in JavaScript | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 608 | Hardcoded API Keys | vulnerability | Frontend & Client-Side Security | observed | not_tested |
| 609 | Exposed Source Maps | vulnerability | Frontend & Client-Side Security | observed | not_tested |
| 610 | Insecure LocalStorage | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 611 | Insecure SessionStorage | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 612 | IndexedDB Data Exposure | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 613 | Insecure Cookie Configuration | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 614 | Service Worker Cache Poisoning | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 615 | Service Worker Scope Abuse | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 616 | PostMessage Vulnerability | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 617 | Third-Party JavaScript Risk | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 618 | JavaScript Dependency Vulnerability | vulnerability | Frontend & Client-Side Security | observed | verified |
| 619 | Prototype Pollution | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 620 | Client-Side Access Control | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 621 | Hidden UI Authorization | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 622 | Payment Data Exposure | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 623 | Browser Cache Sensitive Data Exposure | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 624 | DOM Clobbering | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 625 | Clickjacking | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 626 | Tabnabbing | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 627 | Client-Side Open Redirect | vulnerability | Frontend & Client-Side Security | unverified | not_tested |
| 628 | Insecure Third-Party API Consumption | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 629 | Third-Party API Authentication Bypass | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 630 | Third-Party API Token Leakage | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 631 | Payment Provider Integration Flaws | vulnerability | Third-Party Integration Security | observed | verified |
| 632 | Shipping Provider Integration Flaws | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 633 | OAuth Provider Misconfiguration | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 634 | Email Service Credential Exposure | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 635 | SMTP Injection | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 636 | SMS OTP Abuse | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 637 | CAPTCHA Provider Bypass | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 638 | Webhook Trust Validation Failure | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 639 | Third-Party Data Injection | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 640 | Third-Party Response Deserialization | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 641 | Insecure API Response Validation | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 642 | Third-Party Dependency Compromise | vulnerability | Third-Party Integration Security | unverified | not_tested |
| 643 | Customer PII Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 644 | Customer Address Exposure | vulnerability | Business Data & Privacy | unverified | not_tested |
| 645 | Customer Phone Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 646 | Customer Email Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 647 | Order History Exposure | vulnerability | Business Data & Privacy | unverified | not_tested |
| 648 | Payment Information Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 649 | Invoice Exposure | vulnerability | Business Data & Privacy | unverified | not_tested |
| 650 | Admin Data Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 651 | Internal Business Data Exposure | vulnerability | Business Data & Privacy | observed | verified |
| 652 | Cross-Customer Data Leakage | vulnerability | Business Data & Privacy | observed | verified |
| 653 | Cross-Tenant Data Leakage | vulnerability | Business Data & Privacy | unverified | not_tested |
| 654 | Data Retention Violation | vulnerability | Business Data & Privacy | unverified | not_tested |
| 655 | Data Deletion Failure | vulnerability | Business Data & Privacy | unverified | not_tested |
| 656 | Account Deletion Bypass | vulnerability | Business Data & Privacy | unverified | not_tested |
| 657 | Personal Data Export Authorization Bypass | vulnerability | Business Data & Privacy | observed | verified |
| 658 | Privacy Settings Bypass | vulnerability | Business Data & Privacy | unverified | not_tested |
| 659 | Consent Management Bypass | vulnerability | Business Data & Privacy | unverified | not_tested |
| 660 | Sensitive Data in Analytics | vulnerability | Business Data & Privacy | unverified | not_tested |
| 661 | Sensitive Data in Third-Party Services | vulnerability | Business Data & Privacy | unverified | not_tested |
| 662 | Reconnaissance → Information Disclosure → Credential Discovery → Account Takeover | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 663 | XSS → Session Theft → Account Takeover | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 664 | CSRF → Privileged Action → Account Compromise | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 665 | IDOR → PII Disclosure → Account Targeting | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 666 | SSRF → Cloud Metadata → IAM Credentials → Cloud Access | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 667 | SQL Injection → Database Access → Data Exfiltration | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 668 | SQL Injection → Privilege Escalation → RCE | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 669 | File Upload → File Execution → RCE | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 670 | Path Traversal → Configuration Disclosure → Credential Theft | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 671 | XXE → Local File Read → Credential Exposure | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 672 | SSTI → Server-Side Code Execution | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 673 | JWT Forgery → Authorization Bypass → Privilege Escalation | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 674 | OAuth Misconfiguration → Account Linking Abuse → Account Takeover | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 675 | API BOLA → Cross-Customer Data Access → Data Exfiltration | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 676 | GraphQL Introspection → Sensitive Field Discovery → Authorization Bypass | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 677 | Webhook SSRF → Internal Service Access | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 678 | Payment Callback Forgery → Fake Payment → Order Fraud | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 679 | Coupon Abuse → Price Manipulation → Financial Loss | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 680 | Race Condition → Overselling → Inventory Inconsistency | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 681 | Refund Abuse → Unauthorized Financial Transaction | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 682 | Container Misconfiguration → Container Escape → Host Access | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 683 | Kubernetes RBAC Abuse → Cluster Privilege Escalation | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 684 | CI/CD Secret Exposure → Pipeline Compromise → Production Access | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 685 | Dependency Compromise → Supply Chain Attack → RCE | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 686 | Cloud Storage Exposure → Sensitive Data Exfiltration | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 687 | Admin Panel Exposure → Credential Compromise → Full Application Access | attack_chain | Các chuỗi khai thác Attack Chain | observed | verified |
| 688 | Weak Network Segmentation → Internal Service Compromise | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 689 | Redis Exposure → Data Manipulation → Application Compromise | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 690 | Database Credential Leakage → Database Compromise → Customer Data Exfiltration | attack_chain | Các chuỗi khai thác Attack Chain | unverified | not_tested |
| 691 | Vulnerability ID | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 692 | Vulnerability Name | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 693 | Vulnerability Category | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 694 | CWE Mapping | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 695 | OWASP Mapping | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 696 | WSTG Mapping | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 697 | OWASP API Top 10 Mapping | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 698 | CVSS v4.0 Scoring | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 699 | Severity Classification | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 700 | Affected Component | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 701 | Affected Endpoint | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 702 | HTTP Method | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 703 | Required Authentication | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 704 | Required User Role | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 705 | Test Account | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 706 | Test Credentials | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 707 | Test Data | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 708 | Preconditions | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 709 | Vulnerability Trigger | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 710 | Reproduction Steps | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 711 | Expected Vulnerable Behavior | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 712 | Expected Secure Behavior | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 713 | Proof of Concept | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 714 | Evidence Collection | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 715 | Detection Indicators | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 716 | False Positive Conditions | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 717 | Exploitation Impact | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 718 | Remediation Guidance | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 719 | Regression Test | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 720 | Automated Verification | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 721 | Manual Verification | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 722 | Attack Chain Mapping | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 723 | Vulnerability Dependencies | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 724 | Lab Reset Mechanism | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 725 | Test Isolation | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
| 726 | Vulnerability Enable/Disable Configuration | test_matrix_field | Ma trận kiểm thử và dữ liệu phục vụ Agent | schema_field | not_applicable |
<!-- END COMPLETE INVENTORY -->

<!-- BEGIN MOVED ANNOTATIONS -->
## Implementation notes moved out of source

> The lab source no longer contains inline vulnerability hints. The following notes were moved here from source comments and docstrings, with the symbol that implements each behavior. Line-level evidence lives in `vulndb/source-annotations.json`; `docs/implementation-map.md` maps IDs to symbols.

**713** notes covering **122** vulnerability IDs.

| File | Symbol | IDs | Original note |
|---|---|---|---|
| backend/config.py | module | — | VulnShop Configuration |
| backend/config.py | module | — | INTENTIONALLY INSECURE - FOR PENTEST LAB ONLY |
| backend/config.py | INFLUXDB_TOKEN | 75, 376 | Hardcoded weak JWT and application secrets (vuln #75, #376) |
| backend/config.py | JWT_EXPIRE_MINUTES | 77 | Never expires (vuln #77) |
| backend/config.py | JWT_EXPIRE_MINUTES | 33, 376 | Admin credentials (hardcoded - vuln #33, #376) |
| backend/config.py | EMAIL_FROM | 435 | AWS Keys (intentionally exposed - vuln #435) |
| backend/config.py | S3_BUCKET | 631 | Payment (Stripe - fake keys exposed - vuln #631) |
| backend/config.py | STRIPE_WEBHOOK_SECRET | — | Hardcoded |
| backend/config.py | STRIPE_WEBHOOK_SECRET | 10 | Debug mode (intentional - vuln #10) |
| backend/config.py | MAX_UPLOAD_SIZE | 589 | 999MB - intentionally huge (vuln #589) |
| backend/config.py | ALLOWED_EXTENSIONS | 345 | Empty = all allowed (vuln #345) |
| backend/config.py | ALLOWED_EXTENSIONS | — | Rate limiting (intentionally off) |
| backend/config.py | RATE_LIMIT_ENABLED | 41 | vuln #41 |
| backend/config.py | RATE_LIMIT_WINDOW | 48 | OTP Settings (predictable - vuln #48) |
| backend/config.py | OTP_EXPIRE_SECONDS | 49 | Never expires (vuln #49) |
| backend/config.py | OTP_SECRET | — | Hardcoded OTP secret |
| backend/config.py | OTP_SECRET | 52, 378 | Token settings (weak - vuln #52, #378) |
| backend/config.py | PASSWORD_RESET_TOKEN_EXPIRE | 54 | Never expires (vuln #54) |
| backend/config.py | EMAIL_VERIFY_TOKEN_EXPIRE | 187 | CORS (intentional misconfiguration - vuln #187) |
| backend/config.py | CORS_CREDENTIALS | 189 | vuln #189 |
| backend/config.py | SESSION_COOKIE_SECURE | 71 | vuln #71 |
| backend/config.py | SESSION_COOKIE_HTTPONLY | 71 | vuln #71 |
| backend/config.py | SESSION_COOKIE_SAMESITE | 184 | vuln #184 |
| backend/config.py | WEBHOOK_VERIFY_SIGNATURES | 278 | vuln #278 |
| backend/config.py | WEBHOOK_SECRET | 281 | Hardcoded (vuln #281) |
| backend/config.py | WEBHOOK_SECRET | — | Internal services (for SSRF demos) |
| backend/config.py | INTERNAL_ADMIN_URL | 7, 8 | Version info (exposed - vuln #7, #8) |
| backend/main.py | module | — | VulnShop FastAPI Main Application INTENTIONALLY VULNERABLE E-COMMERCE PLATFORM FOR PENTESTING |
| backend/main.py | module | 19 | Swagger UI - no auth (vuln #19) |
| backend/main.py | module | — | ReDoc - no auth |
| backend/main.py | module | 187 | ─── CORS Middleware (intentionally misconfigured - vuln #187) ─────────────── |
| backend/main.py | module | 187 | vuln #187 - CORS Origin Reflection |
| backend/main.py | module | 189 | vuln #189 - with credentials=True + *origins = dangerous |
| backend/main.py | module | 253 | API versioning bypass (vuln #253) |
| backend/main.py | websocket_endpoint | 271, 272 | WebSocket - no auth check (vuln #271, #272) |
| backend/main.py | websocket_endpoint | — | No authentication or authorization |
| backend/main.py | websocket_endpoint | — | Reflect data back (potential XSS via WebSocket) |
| backend/main.py | websocket_endpoint | 272 | Broadcast to ALL connected clients (no isolation - vuln #272) |
| backend/main.py | admin_ws | 271 | Admin WebSocket - no auth check (vuln #271) |
| backend/main.py | admin_ws | — | Intentional exposure |
| backend/main.py | root | 8 | Root endpoint - technology stack disclosure (vuln #8) |
| backend/main.py | health | 26 | Health check - internal IP disclosure (vuln #26) |
| backend/main.py | health | — | Credential exposure |
| backend/main.py | debug_info | 10, 26 | Debug endpoint - full system info disclosure (vuln #10, #26) |
| backend/main.py | debug_info | — | All env vars exposed |
| backend/main.py | debug_info | 435 | Cloud credential exposure (vuln #435) |
| backend/main.py | metrics | 570 | Prometheus-style metrics - no auth (vuln #570) |
| backend/main.py | metrics | — | Intentional exposure |
| backend/main.py | phpinfo | 9 | Fake phpinfo for fingerprinting (vuln #9) |
| backend/main.py | env_file | 17 | Exposed .env file (vuln #17) |
| backend/main.py | db_backup | 15, 410 | Database backup exposure (vuln #15, #410) |
| backend/main.py | internal_db_query | 401, 406 | Internal DB query endpoint - no auth (vuln #401, #406) |
| backend/main.py | swagger_json | 19 | Swagger exposure (vuln #19) |
| backend/main.py | graphql_info | 20 | GraphQL introspection info (vuln #20) |
| backend/main.py | graphql_info | 25 | ─── Error Handlers (stack trace disclosure - vuln #25) ───────────────────── |
| backend/main.py | global_exception_handler | 25 | Return full stack trace (vuln #25) |
| backend/main.py | global_exception_handler | — | Full stack trace exposed |
| backend/main.py | http_exception_handler | 7 | Server version disclosure in error (vuln #7) |
| backend/main.py | http_exception_handler | 7 | vuln #7 |
| backend/main.py | http_exception_handler | 558 | ─── Request Logging Middleware (logs passwords - vuln #558) ───────────────── |
| backend/main.py | log_requests | 558, 559, 560 | Log all requests including sensitive data (vuln #558, #559, #560) |
| backend/main.py | log_requests | 562 | CRLF injection in logs (vuln #562) |
| backend/main.py | log_requests | 480 | No security headers added (vuln #480) |
| backend/routes/auth.py | module | — | Authentication Routes - Intentionally Vulnerable Covers vulns: #31-95 (Authentication Vulnerabilities) |
| backend/routes/auth.py | module | 372 | vuln #372 MD5 |
| backend/routes/auth.py | module | 372 | Plaintext stored! vuln #372 |
| backend/routes/auth.py | RegisterRequest | 103 | Mass assignment - anyone can set role (vuln #103) |
| backend/routes/auth.py | RegisterRequest | — | Mass assignment vuln |
| backend/routes/auth.py | weak_token | 52, 378 | Predictable token generation (vuln #52, #378) |
| backend/routes/auth.py | weak_token | — | Token based on email + timestamp truncated to seconds = predictable |
| backend/routes/auth.py | weak_token | — | Short MD5 = predictable |
| backend/routes/auth.py | create_jwt | 81 | Create JWT - stores sensitive data in payload (vuln #81) |
| backend/routes/auth.py | create_jwt | 81 | PII in token (vuln #81) |
| backend/routes/auth.py | create_jwt | 81 | PII in token (vuln #81) |
| backend/routes/auth.py | create_jwt | 81 | PII in token (vuln #81) |
| backend/routes/auth.py | create_jwt | 77 | No exp = never expires (vuln #77) |
| backend/routes/auth.py | send_email_smtp | 161 | Send email via MailHog - SMTP injection possible (vuln #161) |
| backend/routes/auth.py | send_email_smtp | 161 | SMTP injection via subject (vuln #161) |
| backend/routes/auth.py | send_email_smtp | — | Not sanitized |
| backend/routes/auth.py | send_email_smtp | — | Not sanitized - SMTP injection |
| backend/routes/auth.py | send_email_smtp | 559 | Log email including content (vuln #559) |
| backend/routes/auth.py | register | 31, 34, 35 | Register - weak password policy, email enumeration (vuln #31, #34, #35) |
| backend/routes/auth.py | register | 558 | Log registration data including password (vuln #558) |
| backend/routes/auth.py | register | 31 | Weak password policy - no length/complexity check (vuln #31) |
| backend/routes/auth.py | register | 35 | Email enumeration - different error messages (vuln #35) |
| backend/routes/auth.py | register | 103 | Mass assignment - role can be set by user (vuln #103) |
| backend/routes/auth.py | register | — | Privilege escalation via mass assignment |
| backend/routes/auth.py | register | 372 | MD5! vuln #372 |
| backend/routes/auth.py | register | 372 | Store plaintext vuln #372 |
| backend/routes/auth.py | register | 52 | Generate predictable token (vuln #52) |
| backend/routes/auth.py | register | 393 | Token in email URL (sensitive data in URL - vuln #393) |
| backend/routes/auth.py | register | 51 | Token in response (vuln #51) |
| backend/routes/auth.py | login | 38, 64, 65, 66 | Login - SQL injection sim, timing attack, brute force possible (vuln #38, #64, #65, #66) |
| backend/routes/auth.py | login | 558 | Log credentials (vuln #558) |
| backend/routes/auth.py | login | 38, 41 | No rate limiting (vuln #38, #41) |
| backend/routes/auth.py | login | 43 | No CAPTCHA (vuln #43) |
| backend/routes/auth.py | login | 65 | Session fixation - use existing session ID if provided (vuln #65) |
| backend/routes/auth.py | login | 128 | SQL injection simulation in login (vuln #128) |
| backend/routes/auth.py | login | — | With: email = "admin@vulnshop.com' OR '1'='1'--" → bypasses auth |
| backend/routes/auth.py | login | — | Simulate SQLi bypass |
| backend/routes/auth.py | login | — | vuln: should block but doesn't |
| backend/routes/auth.py | login | 34 | Username enumeration via timing (vuln #34) |
| backend/routes/auth.py | login | — | Faster for non-existent (timing attack) |
| backend/routes/auth.py | login | 372 | Password check using MD5 (vuln #372) |
| backend/routes/auth.py | login | — | Different msg = enumeration |
| backend/routes/auth.py | login | 81 | Create JWT with sensitive data (vuln #81) |
| backend/routes/auth.py | login | 82 | Refresh token - never expires, can be reused (vuln #82) |
| backend/routes/auth.py | login | 68, 70 | Session management - session NOT invalidated if exists (vuln #68, #70) |
| backend/routes/auth.py | login | 70 | Concurrent sessions allowed (vuln #70) |
| backend/routes/auth.py | login | 62 | Remember me - insecure persistent cookie (vuln #62) |
| backend/routes/auth.py | login | 71 | Insecure cookie (vuln #71) - no Secure, no HttpOnly, SameSite=None |
| backend/routes/auth.py | login | 62 | Insecure remember me (vuln #62) |
| backend/routes/auth.py | logout | 68 | Logout - session NOT invalidated (vuln #68) |
| backend/routes/auth.py | logout | 68 | Session NOT removed from server (vuln #68) |
| backend/routes/auth.py | logout | — | sessions_db.pop(session_id, None)  <-- intentionally commented out |
| backend/routes/auth.py | forgot_password | 51, 56 | Forgot password - host header injection (vuln #56), token exposure (vuln #51) |
| backend/routes/auth.py | forgot_password | 35 | Email enumeration - confirm if email exists (vuln #35) |
| backend/routes/auth.py | forgot_password | — | Enumeration |
| backend/routes/auth.py | forgot_password | 52 | Predictable token (vuln #52) |
| backend/routes/auth.py | forgot_password | 54 | No expiry set (vuln #54) |
| backend/routes/auth.py | forgot_password | 56 | Host Header Injection (vuln #56) - use Host header for reset URL |
| backend/routes/auth.py | forgot_password | — | Attacker controls this |
| backend/routes/auth.py | forgot_password | 51 | Token leaked in response (vuln #51) |
| backend/routes/auth.py | forgot_password | 51 | Token in response body (vuln #51) |
| backend/routes/auth.py | forgot_password | — | URL exposed in response |
| backend/routes/auth.py | reset_password | 53, 54 | Reset password - token reuse, never expires (vuln #53, #54) |
| backend/routes/auth.py | reset_password | 54 | No expiry check (vuln #54) - tokens never expire |
| backend/routes/auth.py | reset_password | 53 | Token NOT deleted after use (vuln #53) - can be reused |
| backend/routes/auth.py | reset_password | 31 | Weak new password accepted (vuln #31) |
| backend/routes/auth.py | reset_password | 69 | Sessions NOT invalidated after password change (vuln #69) |
| backend/routes/auth.py | reset_password | 558 | Log password change (vuln #558) |
| backend/routes/auth.py | verify_email | 57, 58 | Email verification - token reuse (vuln #57, #58) |
| backend/routes/auth.py | verify_email | 58 | Token NOT deleted = can be reused (vuln #58) |
| backend/routes/auth.py | verify_email_bypass | 59 | Email verification bypass (vuln #59) - no token needed |
| backend/routes/auth.py | mfa_verify | 44, 46, 47, 48 | MFA verify - OTP brute force, replay (vuln #44, #46, #47, #48) |
| backend/routes/auth.py | mfa_verify | 46 | No rate limiting on OTP (vuln #46) |
| backend/routes/auth.py | mfa_verify | 48 | Predictable OTP (vuln #48) |
| backend/routes/auth.py | mfa_verify | — | Default OTP = "123456" (predictable) |
| backend/routes/auth.py | mfa_verify | 47 | OTP not deleted after use (vuln #47 - replay) |
| backend/routes/auth.py | mfa_verify | 44 | Backdoor OTP (vuln #44) |
| backend/routes/auth.py | mfa_verify | — | Different error for wrong OTP vs expired (enumeration) |
| backend/routes/auth.py | mfa_setup | 376 | MFA setup - hardcoded secret (vuln #376) |
| backend/routes/auth.py | mfa_setup | 48 | Predictable OTP (vuln #48) |
| backend/routes/auth.py | mfa_setup | — | Hardcoded secret exposed |
| backend/routes/auth.py | mfa_setup | — | Weak backup codes |
| backend/routes/auth.py | refresh_token | 82, 83 | Refresh token - reuse allowed, rotation failure (vuln #82, #83) |
| backend/routes/auth.py | refresh_token | 83 | Token NOT rotated (vuln #83) - same token works forever |
| backend/routes/auth.py | refresh_token | 82 | Same refresh token returned (vuln #82) |
| backend/routes/auth.py | get_me | 72 | Get current user - JWT none algorithm accepted (vuln #72) |
| backend/routes/auth.py | get_me | 72 | Accept none algorithm (vuln #72) |
| backend/routes/auth.py | get_me | 73 | Accept any algorithm (vuln #73) |
| backend/routes/auth.py | get_me | 74 | Try without algorithm check (vuln #74) |
| backend/routes/auth.py | get_me | 77 | No expiry check bypass (vuln #77) |
| backend/routes/auth.py | social_login_google | 84, 85 | OAuth Google login - redirect URI manipulation (vuln #84, #85) |
| backend/routes/auth.py | social_login_google | 86 | No state validation (vuln #86) |
| backend/routes/auth.py | social_login_google | 85 | No redirect_uri validation (vuln #85) |
| backend/routes/auth.py | social_login_google | — | Attacker can set redirect_uri to their server |
| backend/routes/auth.py | social_login_google | 86 | No state parameter CSRF check (vuln #86) |
| backend/routes/auth.py | social_login_google | 94, 95 | Create account linking - no verification (vuln #94, #95) |
| backend/routes/auth.py | list_all_users | 104, 643 | List all users - no auth required (vuln #104, #643) |
| backend/routes/auth.py | auth_bypass | 61 | Authentication bypass endpoint (vuln #61) |
| backend/routes/auth.py | auth_bypass | — | Logic flaw - any request with admin=true bypasses auth |
| backend/routes/products.py | module | 97, 128, 136, 171, 250 | Product Routes - Intentionally Vulnerable Covers vulns: SQLi (#128), NoSQL Injection (#136), XSS (#171), IDOR (#97), Mass Assignment (#250) |
| backend/routes/products.py | module | 651 | Internal cost exposed (vuln #651) |
| backend/routes/products.py | module | 651 | Sensitive business data (vuln #651) |
| backend/routes/products.py | ProductCreate | 250 | Mass assignment fields - all accepted (vuln #250) |
| backend/routes/products.py | ReviewCreate | — | No XSS sanitization |
| backend/routes/products.py | list_products | 603 | No limit = unbounded (vuln #603) |
| backend/routes/products.py | list_products | 603 | Unbounded pagination (vuln #603) |
| backend/routes/products.py | list_products | 128, 603 | List products - SQL injection in search, unbounded pagination (vuln #128, #603) |
| backend/routes/products.py | list_products | 128 | SQL injection simulation in search (vuln #128) |
| backend/routes/products.py | list_products | 239, 587 | ReDoS vulnerability (vuln #239, #587) - catastrophic backtracking |
| backend/routes/products.py | list_products | — | Vulnerable regex pattern |
| backend/routes/products.py | list_products | 128, 259 | SQL injection in sort parameter (vuln #128, #259) |
| backend/routes/products.py | list_products | 24 | Injection reflected back (vuln #24) |
| backend/routes/products.py | list_products | 251 | Return ALL fields including sensitive ones (vuln #251) |
| backend/routes/products.py | list_products | 651 | Including cost, admin_note, supplier_cost (vuln #651) |
| backend/routes/products.py | list_products | — | Reflected back (potential XSS context) |
| backend/routes/products.py | export_products_csv | 168 | Export products - CSV injection (vuln #168) |
| backend/routes/products.py | export_products_csv | 168 | CSV injection - name or admin_note can contain formulas (vuln #168) |
| backend/routes/products.py | export_products_csv | — | Sensitive data exposed |
| backend/routes/products.py | export_products_csv | — | Sensitive data exposed |
| backend/routes/products.py | flash_sale | 300, 305 | Flash sale - race condition vulnerability (vuln #300, #305) |
| backend/routes/products.py | get_product | 97, 251 | Get product - IDOR, returns ALL fields including sensitive (vuln #97, #251) |
| backend/routes/products.py | get_product | 251, 651 | Return ALL fields including internal data (vuln #251, #651) |
| backend/routes/products.py | create_product | 104, 250 | Create product - mass assignment, no auth check (vuln #250, #104) |
| backend/routes/products.py | create_product | 104 | No authentication check (vuln #104) |
| backend/routes/products.py | create_product | 250 | Mass assignment - all fields accepted including privileged ones (vuln #250) |
| backend/routes/products.py | create_product | 171 | XSS in description not sanitized (vuln #171) |
| backend/routes/products.py | create_product | — | Mass assignment |
| backend/routes/products.py | create_product | — | Mass assignment |
| backend/routes/products.py | update_product | 97, 125 | Update product - no ownership check, IDOR (vuln #97, #125) |
| backend/routes/products.py | update_product | — | No auth check |
| backend/routes/products.py | update_product | — | No ownership validation |
| backend/routes/products.py | update_product | — | HTTP method bypass - PUT works for anyone |
| backend/routes/products.py | update_product | 250 | Mass assignment - update any field (vuln #250) |
| backend/routes/products.py | delete_product | 104 | Delete product - no auth (vuln #104) |
| backend/routes/products.py | get_recommendations | 198, 203 | Get recommendations - SSRF via external URL (vuln #198, #203) |
| backend/routes/products.py | get_recommendations | 198 | SSRF - fetch any URL including internal services (vuln #198) |
| backend/routes/products.py | get_recommendations | — | Fetch attacker-controlled URL |
| backend/routes/products.py | add_review | 171, 177 | Add review - stored XSS (vuln #171, #177) |
| backend/routes/products.py | add_review | 171 | Stored without sanitization - XSS (vuln #171) |
| backend/routes/products.py | add_review | — | Also unsanitized |
| backend/routes/products.py | get_reviews | 171 | Get reviews - returns XSS payloads unsanitized (vuln #171) |
| backend/routes/products.py | get_qna | 170 | Q&A - reflected XSS in question (vuln #170) |
| backend/routes/products.py | get_qna | 170 | Reflected without sanitization (vuln #170) |
| frontend/routes/api.js | API_URL | — | VULN: SSRF - target URL controlled by user input |
| frontend/routes/index.js | r | — | GET /products — Product listing (XSS in search query) |
| frontend/routes/index.js | query | — | VULN: used unescaped in template |
| frontend/routes/index.js | r | — | VULN: passed to template, rendered unescaped |
| frontend/routes/index.js | r | — | GET /products/:id — Product detail (stored XSS in description/reviews) |
| frontend/routes/index.js | reviews | — | VULN: Review comment rendered unescaped (stored XSS possible) |
| frontend/routes/index.js | route /cart/add | 283 | VULN: Price taken from request body - price manipulation #283 |
| frontend/routes/index.js | if | — | VULN: price from client |
| frontend/routes/index.js | if | — | VULN: price manipulation |
| frontend/routes/index.js | route /checkout | 283 | VULN: Total price taken from form (client-side) - vuln #283 |
| frontend/routes/index.js | order | — | VULN: from form |
| frontend/routes/index.js | order | — | VULN: from form |
| frontend/routes/index.js | order | — | GET /orders — Order history (IDOR - no session check) |
| frontend/routes/index.js | route /orders | — | VULN: IDOR - user_id from query param, no ownership check |
| frontend/routes/index.js | r | — | GET /profile — User profile (mass assignment, no current password) |
| frontend/routes/index.js | route /profile | — | Update profile (mass assignment) |
| frontend/routes/index.js | route /profile | — | VULN: Mass assignment - user can set role, loyalty_points, etc. |
| frontend/routes/index.js | if | — | VULN: mass assignment |
| frontend/routes/index.js | route /profile/change-password | — | VULN: No current password required - logic flaw |
| frontend/routes/index.js | route /profile/change-password | — | VULN: No token/CSRF check |
| frontend/routes/index.js | wishlist | — | GET /login — Login page (no CSRF, user enumeration) |
| frontend/routes/index.js | route /login | — | VULN: No CSRF token |
| frontend/routes/index.js | userData | — | VULN: Remember me stores credentials in cookie without encryption |
| frontend/routes/index.js | status | 34 | VULN: Different error messages leak user existence (enumeration #34) |
| frontend/routes/index.js | error | — | VULN: user enumeration |
| frontend/routes/index.js | error | — | VULN: confirms user exists |
| frontend/routes/index.js | if | — | GET /register — Registration (no CSRF, weak validation) |
| frontend/routes/index.js | route /forgot-password | — | Always return success (no enumeration protection but demo) |
| frontend/routes/index.js | route /forgot-password | — | GET /reset-password — Token in URL (sensitive data exposure) |
| frontend/routes/index.js | route /reset-password | — | VULN: Token in URL - logged in server logs, browser history, referrer |
| frontend/routes/index.js | route /reset-password | — | VULN: token exposed in URL |
| frontend/routes/index.js | route /reset-password | — | No token expiry check, no rate limiting |
| frontend/routes/index.js | route /reset-password | — | GET /track/:orderId — Order tracking (IDOR) |
| frontend/routes/index.js | route /track/:orderId | — | VULN: IDOR - no ownership check, anyone can track any order |
| frontend/routes/index.js | r | — | GET /addresses/:userId — Address book (IDOR) |
| frontend/routes/index.js | route /addresses/:userId | — | VULN: IDOR - no ownership check |
| frontend/routes/webhook.js | API_URL | — | POST /webhook/payment — Payment webhook (no signature validation) |
| frontend/routes/webhook.js | API_URL | 278 | vuln #278: No HMAC/signature check |
| frontend/routes/webhook.js | route /payment | — | VULN: No signature validation |
| frontend/routes/webhook.js | payload | — | VULN: Webhook SSRF - callback_url from payload |
| frontend/routes/webhook.js | payload | 280 | vuln #280 |
| frontend/routes/webhook.js | if | — | VULN: SSRF via callback_url |
| frontend/routes/webhook.js | if | — | POST /webhook/shipping — Shipping webhook (no validation) |
| frontend/routes/webhook.js | route /shipping | — | VULN: No authentication, no signature |
| frontend/routes/webhook.js | route /shipping | — | VULN: SSRF via callback_url |
| frontend/routes/webhook.js | route /inventory | — | VULN: SSRF, no auth |
| frontend/routes/webhook.js | route /test | — | VULN: exposes all env vars |
| frontend/server.js | server | — | INTENTIONAL VULN: Socket.io with NO authentication |
| frontend/server.js | server | 271 | vuln #271 - WebSocket without auth |
| frontend/server.js | io | — | No auth check at all |
| frontend/server.js | io | — | No validation, anyone can join any room |
| frontend/server.js | io | — | No admin check - anyone can broadcast |
| frontend/server.js | io | — | IDOR - returns any user data without auth |
| frontend/server.js | io | — | INTENTIONAL VULN: CORS allows all origins |
| frontend/server.js | io | — | INTENTIONAL: Helmet DISABLED |
| frontend/server.js | io | — | app.use(helmet()); // Disabled intentionally - no security headers |
| frontend/server.js | io | — | INTENTIONAL VULN: Session with weak config |
| frontend/server.js | io | — | Weak secret |
| frontend/server.js | io | — | No sameSite (CSRF possible) |
| frontend/server.js | io | — | VULN: works over HTTP |
| frontend/server.js | io | — | VULN: JS can read session cookie |
| frontend/server.js | io | — | VULN: CSRF possible |
| frontend/server.js | io | — | No file type validation - intentional |
| frontend/server.js | io | — | INTENTIONAL VULN: Request logging with sensitive data |
| frontend/server.js | io | — | INTENTIONAL VULN: Static file serving |
| frontend/server.js | io | — | Exposes source maps |
| frontend/server.js | io | — | Exposes .env |
| frontend/server.js | io | — | Exposes .git |
| frontend/server.js | route /robots.txt | — | Debug endpoint (intentional) |
| frontend/server.js | route /debug | — | Source map (intentional exposure) |
| frontend/server.js | route /webhook | — | Admin redirect (no auth) |
| frontend/server.js | route /admin | — | INTENTIONAL: No auth check before redirect |
| frontend/server.js | route /admin/dashboard | — | INTENTIONAL VULN: Error handler exposes stack traces |
| frontend/server.js | route /admin/dashboard | — | VULN: stack trace exposed |
| frontend/views/home.ejs | template | — | VULN: XSS - email value echoed back without escaping |
| frontend/views/home.ejs | template | — | Newsletter - VULN: DOM XSS |
| frontend/views/home.ejs | template | — | VULN: innerHTML with user input = DOM XSS |
| frontend/views/layout.ejs | template | 608 | INTENTIONAL VULN #608: Hardcoded API keys |
| frontend/views/layout.ejs | template | — | jQuery 1.x (old - for DOM XSS vulns) |
| frontend/views/layout.ejs | template | 609 | sourceMappingURL intentional exposure (vuln #609) |
| frontend/views/layout.ejs | template | — | Newsletter subscription (XSS in email) |
| frontend/views/layout.ejs | template | — | VULN: XSS - email rendered via innerHTML |
| frontend/views/layout.ejs | template | — | DOM XSS |
| frontend/views/products.ejs | template | — | VULN: XSS - search query rendered unescaped with <%- |
| frontend/views/products.ejs | template | — | ^^^ INTENTIONAL XSS VULNERABILITY - unescaped output |
| services/graphql/src/auth.js | module | — | VulnShop GraphQL Auth Middleware |
| services/graphql/src/auth.js | module | — | INTENTIONALLY VULNERABLE - weak JWT validation |
| services/graphql/src/auth.js | module | 72, 74, 75, 77 | Vulnerabilities: #75 (weak secret), #77 (expiry bypass), #74 (signature bypass), #72 (alg:none acceptance) |
| services/graphql/src/auth.js | jwt | 75 | VULN #75: Hardcoded, weak JWT secret |
| services/graphql/src/auth.js | REFRESH_SECRET | 77 | VULN #77: Expired tokens can pass through the unverified decode fallback |
| services/graphql/src/auth.js | REFRESH_SECRET | 72, 74 | VULN #74, #72: The unverified decode fallback bypasses signatures, including for alg:none tokens |
| services/graphql/src/auth.js | verifyToken | — | VULN: No algorithm restriction - accepts HS256 or 'none' |
| services/graphql/src/auth.js | verifyToken | — | An attacker can forge tokens with alg:none |
| services/graphql/src/auth.js | decoded | — | VULN: Multiple algorithms accepted |
| services/graphql/src/auth.js | decoded | — | VULN: Try to decode without verification as fallback |
| services/graphql/src/auth.js | decoded | — | VULN: Decoded without verification |
| services/graphql/src/auth.js | if | — | VULN: Returns unverified payload! |
| services/graphql/src/auth.js | if | — | VULN: Weak token generation |
| services/graphql/src/auth.js | generateToken | — | VULN: No jti (JWT ID) for revocation |
| services/graphql/src/auth.js | generateToken | — | VULN: No iss or aud claims |
| services/graphql/src/auth.js | generateToken | — | VULN: Long expiry |
| services/graphql/src/auth.js | generateRefreshToken | — | VULN: Very long refresh token expiry |
| services/graphql/src/auth.js | generateRefreshToken | — | VULN: Auth middleware that can be bypassed |
| services/graphql/src/auth.js | authHeader | — | VULN: Accept token from multiple insecure sources |
| services/graphql/src/auth.js | token | — | VULN: Custom insecure header |
| services/graphql/src/auth.js | token | — | VULN: Token in URL query string |
| services/graphql/src/auth.js | token | — | VULN: Token in request body |
| services/graphql/src/auth.js | user | — | VULN: X-User-ID header bypass - if no token, trust this header |
| services/graphql/src/auth.js | if | — | VULN: Role from header |
| services/graphql/src/auth.js | if | 108 | VULN #108: isAdmin check that can be bypassed |
| services/graphql/src/auth.js | isAdmin | — | VULN: Check role from JWT which can be forged |
| services/graphql/src/index.js | module | — | VulnShop GraphQL Service - Main Entry Point |
| services/graphql/src/index.js | module | — | INTENTIONALLY VULNERABLE - For educational/pentesting purposes only |
| services/graphql/src/index.js | module | 20, 187, 260, 264, 265, 266, 267, 268 | Vulnerabilities: #20, #187, #260, #264, #265, #266, #267, #268 |
| services/graphql/src/index.js | app | 187 | VULN #187: CORS allows ALL origins - no restriction |
| services/graphql/src/index.js | app | — | VULN: Wildcard CORS |
| services/graphql/src/index.js | app | — | VULN: All headers allowed |
| services/graphql/src/index.js | app | — | VULN: Large payload limit (DoS risk) |
| services/graphql/src/index.js | app | 268 | Build schema - using buildSubgraphSchema for federation (vuln #268) |
| services/graphql/src/index.js | app | 268 | VULN #268: Federation enabled - exposes _service, _entities, _sdl |
| services/graphql/src/index.js | httpServer | 267 | VULN #267: WebSocket server for subscriptions - NO AUTH |
| services/graphql/src/index.js | wsServer | — | Setup GraphQL over WebSocket (subscriptions) - no auth |
| services/graphql/src/index.js | serverCleanup | 267 | VULN #267: No authentication on websocket connection |
| services/graphql/src/index.js | onConnect | — | VULN: Accept all connections, log params (may contain tokens) |
| services/graphql/src/index.js | onSubscribe | — | VULN: No auth check on subscriptions |
| services/graphql/src/index.js | context | — | VULN: Extract user from connection params without validation |
| services/graphql/src/index.js | context | — | VULN: Trust user role from client |
| services/graphql/src/index.js | server | 20, 260 | VULN #20, #260: Introspection ALWAYS enabled regardless of environment |
| services/graphql/src/index.js | server | 264 | VULN #264: Effectively no depth limit (1000 is functionally unlimited) |
| services/graphql/src/index.js | server | 265 | VULN #265: No query complexity limit configured |
| services/graphql/src/index.js | server | 266 | VULN #266: Batching enabled (allows batch GraphQL attacks) |
| services/graphql/src/index.js | server | — | VULN: Inline tracing exposes query execution details |
| services/graphql/src/index.js | server | — | Custom plugin to log all queries (may log sensitive data) |
| services/graphql/src/index.js | didEncounterErrors | — | VULN: Full error details including stack traces |
| services/graphql/src/index.js | didEncounterErrors | — | VULN: Detailed error formatting - exposes stack traces |
| services/graphql/src/index.js | formatError | — | VULN: Expose internal error details |
| services/graphql/src/index.js | formatError | — | VULN: Echo the query back |
| services/graphql/src/index.js | stacktrace | — | VULN: Include suggestions in errors (helps attackers enumerate schema) |
| services/graphql/src/index.js | context | — | VULN: User extracted from token without strict validation |
| services/graphql/src/index.js | user | — | VULN: Pass raw headers to context (accessible in resolvers) |
| services/graphql/src/index.js | user | — | VULN: Health check endpoint leaks environment info |
| services/graphql/src/index.js | route /health | — | VULN: DB info in health check |
| services/graphql/src/index.js | route /health | — | VULN: SDL/Schema endpoint exposed (federation) |
| services/graphql/src/index.js | route /schema | — | VULN: Debug endpoint exposes all env vars |
| services/graphql/src/index.js | route /debug | — | VULN: Metrics endpoint without auth |
| services/graphql/src/resolvers.js | module | — | VulnShop GraphQL Resolvers |
| services/graphql/src/resolvers.js | module | — | INTENTIONALLY VULNERABLE - For educational/pentesting purposes only |
| services/graphql/src/resolvers.js | module | 97, 102, 104, 108, 113, 115, 250, 264, 265, 266, 309 | Vulnerabilities: #97, #102, #104, #108, #113, #115, #250, #264, #265, #266, #309 |
| services/graphql/src/resolvers.js | pool | — | VULN: Helper that runs raw SQL without parameterization (SQL Injection) |
| services/graphql/src/resolvers.js | rawQuery | 559 | VULN #559: SQL logged |
| services/graphql/src/resolvers.js | result | — | N+1 query helper - intentionally not batched |
| services/graphql/src/resolvers.js | getUserById | — | VULN: No caching, N+1 problem |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | resolvers | 104 | VULN #104: Returns all users including passwords, no auth check |
| services/graphql/src/resolvers.js | sql | — | VULN: Returns password column |
| services/graphql/src/resolvers.js | if | — | VULN: SQL injection via role param |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi via limit/offset |
| services/graphql/src/resolvers.js | if | 97 | VULN #97: IDOR - returns any user's data including password |
| services/graphql/src/resolvers.js | user | — | VULN: No auth check, no ownership verification |
| services/graphql/src/resolvers.js | user | — | VULN: User enumeration |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: Returns current user including sensitive fields |
| services/graphql/src/resolvers.js | me | — | VULN: SQL injectable search returning PII |
| services/graphql/src/resolvers.js | searchUsers | — | VULN: Direct SQL injection |
| services/graphql/src/resolvers.js | sql | — | VULN: Filter with SQL injectable fields |
| services/graphql/src/resolvers.js | if | — | VULN: SQL injection via search |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: SQL injection via ORDER BY field name |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | productsByCategory | — | VULN: SQLi |
| services/graphql/src/resolvers.js | productsByCategory | 113 | VULN #113: Returns ALL orders regardless of auth or ownership |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: No auth check - returns all orders |
| services/graphql/src/resolvers.js | if | — | VULN: IDOR on order |
| services/graphql/src/resolvers.js | order | — | VULN: No auth check, no ownership check |
| services/graphql/src/resolvers.js | ordersByUser | — | VULN: IDOR - no check if current user owns these orders |
| services/graphql/src/resolvers.js | ordersByUser | — | VULN: SQLi |
| services/graphql/src/resolvers.js | ordersByUser | — | VULN: IDOR on cart |
| services/graphql/src/resolvers.js | targetUserId | — | VULN: No ownership check |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | 115 | VULN #115: Payment data accessible without auth |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | if | — | VULN: No auth check - returns card numbers, CVVs |
| services/graphql/src/resolvers.js | payment | — | VULN: IDOR - returns payment with card details |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: All coupons exposed |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | 108 | VULN #108: Admin data without auth check |
| services/graphql/src/resolvers.js | adminUsers | — | VULN: Expose sensitive system configuration |
| services/graphql/src/resolvers.js | adminUsers | — | VULN: System info exposed |
| services/graphql/src/resolvers.js | databaseVersion | — | VULN: ALL env vars exposed |
| services/graphql/src/resolvers.js | databaseVersion | — | VULN (EXTREME): Direct database dump endpoint |
| services/graphql/src/resolvers.js | for | — | VULN: Error details exposed |
| services/graphql/src/resolvers.js | users | — | VULN: SQL injectable search |
| services/graphql/src/resolvers.js | search | — | VULN: Direct SQL injection in query |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: Debug endpoint |
| services/graphql/src/resolvers.js | debugInfo | — | VULN: DB connection details in debug |
| services/graphql/src/resolvers.js | debugInfo | — | VULN (EXTREME): Direct SQL execution |
| services/graphql/src/resolvers.js | result | — | VULN: DB error messages exposed |
| services/graphql/src/resolvers.js | result | — | Register with mass assignment |
| services/graphql/src/resolvers.js | register | 250 | VULN #250: role directly from input - privilege escalation |
| services/graphql/src/resolvers.js | userRole | — | VULN: Password stored in plaintext if no hashing |
| services/graphql/src/resolvers.js | userRole | — | VULN: SQL injection in registration |
| services/graphql/src/resolvers.js | refreshToken | — | VULN: Store refresh token in DB |
| services/graphql/src/resolvers.js | login | — | VULN: SQL injection in login |
| services/graphql/src/resolvers.js | if | — | VULN: Timing-based user enumeration possible |
| services/graphql/src/resolvers.js | refreshToken | — | VULN: Logging password |
| services/graphql/src/resolvers.js | logout | — | VULN: Tokens not actually invalidated server-side |
| services/graphql/src/resolvers.js | logout | 250 | VULN #250: Mass assignment - all fields settable including role |
| services/graphql/src/resolvers.js | values | — | VULN: SQL injection via field names and values |
| services/graphql/src/resolvers.js | rows | — | VULN: No ownership check - can update any user |
| services/graphql/src/resolvers.js | updateUser | — | VULN: No auth check, no ownership verification |
| services/graphql/src/resolvers.js | setClauses | — | VULN: SQL injection in key names and values |
| services/graphql/src/resolvers.js | rows | 102 | VULN #102: Privilege escalation - change any user's role |
| services/graphql/src/resolvers.js | updateUserRole | — | VULN: No auth check - any user can escalate any other user's role |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: Delete any user without auth |
| services/graphql/src/resolvers.js | deleteUser | — | VULN: SQLi, no auth |
| services/graphql/src/resolvers.js | deleteUser | 108 | VULN #108: Admin update without admin check |
| services/graphql/src/resolvers.js | adminUpdateUser | — | VULN: Same as updateUser but labeled "admin" - no actual check |
| services/graphql/src/resolvers.js | createProduct | — | VULN: No auth check - anyone can create products |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | updateProduct | — | VULN: No auth check |
| services/graphql/src/resolvers.js | deleteProduct | 309 | VULN #309: Price/total injectable by client |
| services/graphql/src/resolvers.js | createOrder | — | VULN: Total comes from client - no server-side calculation |
| services/graphql/src/resolvers.js | createOrder | — | VULN: Status settable on creation |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | for | — | VULN: SQLi, price injectable |
| services/graphql/src/resolvers.js | for | — | VULN: No auth on status change |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | cancelOrder | — | VULN: No ownership check |
| services/graphql/src/resolvers.js | rows | 309 | VULN #309: Payment amount injectable |
| services/graphql/src/resolvers.js | processPayment | — | VULN: Amount comes from client - no validation against order total |
| services/graphql/src/resolvers.js | processPayment | — | VULN: Arbitrary amount can be passed (send $0.01 for a $1000 order) |
| services/graphql/src/resolvers.js | processPayment | — | VULN: Logging PCI data |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi; CVV stored (PCI violation) |
| services/graphql/src/resolvers.js | rows | — | VULN: Update order without validating amount |
| services/graphql/src/resolvers.js | rows | — | VULN: Refund amount injectable |
| services/graphql/src/resolvers.js | refundPayment | — | VULN: No check if refund amount <= original payment amount |
| services/graphql/src/resolvers.js | rows | — | VULN: Price injectable; can add to any user's cart |
| services/graphql/src/resolvers.js | addToCart | — | VULN: price comes from client |
| services/graphql/src/resolvers.js | if | — | VULN: SQLi |
| services/graphql/src/resolvers.js | removeFromCart | — | VULN: SQLi, no auth |
| services/graphql/src/resolvers.js | clearCart | — | VULN: Can clear any user's cart - no ownership check |
| services/graphql/src/resolvers.js | clearCart | — | VULN: Discount amount injected by client |
| services/graphql/src/resolvers.js | applyDiscount | — | VULN: discount value comes from client - no validation against coupon table |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi |
| services/graphql/src/resolvers.js | rows | — | VULN: Create coupon without auth |
| services/graphql/src/resolvers.js | rows | — | VULN: SQLi, no auth |
| services/graphql/src/resolvers.js | rows | — | VULN (EXTREME): Direct SQL execution - no auth |
| services/graphql/src/resolvers.js | result | — | VULN: Arbitrary SQL execution |
| services/graphql/src/resolvers.js | result | — | VULN: Error + query in response |
| services/graphql/src/resolvers.js | result | — | VULN: System config update without auth |
| services/graphql/src/resolvers.js | cfg | — | VULN: Directly modifying process environment |
| services/graphql/src/resolvers.js | cfg | — | VULN: Reset ALL passwords without auth |
| services/graphql/src/resolvers.js | resetAllPasswords | — | VULN: No auth check on destructive admin operation |
| services/graphql/src/resolvers.js | resetAllPasswords | 267 | VULN #267: Subscriptions without auth |
| services/graphql/src/resolvers.js | subscribe | — | VULN: No auth check - anyone can subscribe to any user's order updates |
| services/graphql/src/resolvers.js | resolve | — | VULN: ALL payment events broadcast to all subscribers |
| services/graphql/src/resolvers.js | resolve | — | VULN: Admin alerts accessible to any subscriber |
| services/graphql/src/resolvers.js | resolve | — | Type resolvers for relations (N+1 problem - vuln for DoS) |
| services/graphql/src/resolvers.js | orders | — | VULN: N+1 query - no DataLoader |
| services/graphql/src/resolvers.js | user | — | VULN: Accessing any user via order - IDOR |
| services/graphql/src/resolvers.js | items | — | VULN: N+1 |
| services/graphql/src/resolvers.js | rows | — | VULN: Returns card number, CVV |
| services/graphql/src/resolvers.js | reviews | — | VULN: N+1 - no batching |
| services/graphql/src/resolvers.js | rows | — | VULN: Returns contract terms and sensitive supplier data |
| services/graphql/src/schema.js | module | — | VulnShop GraphQL Schema |
| services/graphql/src/schema.js | module | — | INTENTIONALLY VULNERABLE - For educational/pentesting purposes only |
| services/graphql/src/schema.js | module | 20, 97, 102, 104, 108, 113, 115, 250, 260, 264, 265, 266, 267, 268, 309 | Vulnerabilities: #20, #97, #102, #104, #108, #113, #115, #250, #260, #264, #265, #266, #267, #268, #309 |
| services/graphql/src/schema.js | typeDefs | 251 | VULN #251: Password field exposed in schema - excessive data exposure |
| services/graphql/src/schema.js | typeDefs | 643, 648 | VULN #643, #648: PII and payment fields exposed in schema |
| services/graphql/src/schema.js | typeDefs | — | VULN: Password hash directly accessible |
| services/graphql/src/schema.js | typeDefs | 648 | VULN #648: Payment data exposed |
| services/graphql/src/schema.js | typeDefs | 643 | VULN #643: SSN directly in schema |
| services/graphql/src/schema.js | typeDefs | 643 | VULN #643: Bank info exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Token exposed in schema |
| services/graphql/src/schema.js | typeDefs | 51 | VULN #51: Password reset token exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal admin notes accessible |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal cost/margin data exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Supplier info exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Business-sensitive pricing |
| services/graphql/src/schema.js | typeDefs | — | VULN: Sensitive contract data exposed |
| services/graphql/src/schema.js | typeDefs | 97, 113 | VULN #97, #113: Order accessible without ownership check (IDOR) |
| services/graphql/src/schema.js | typeDefs | — | VULN: Can access any user's data via order |
| services/graphql/src/schema.js | typeDefs | — | VULN: Sensitive payment data returned |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal order notes |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal fulfillment status |
| services/graphql/src/schema.js | typeDefs | 648 | VULN #648: Payment card data exposed in API responses |
| services/graphql/src/schema.js | typeDefs | — | VULN: Full card number exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: CVV exposed (PCI DSS violation) |
| services/graphql/src/schema.js | typeDefs | — | VULN: Raw gateway response with internals |
| services/graphql/src/schema.js | typeDefs | — | VULN: Full card data |
| services/graphql/src/schema.js | typeDefs | — | VULN: CVV stored and exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Discount percentage exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Admin notes exposed to all |
| services/graphql/src/schema.js | typeDefs | 108 | VULN #108: Admin data accessible without auth |
| services/graphql/src/schema.js | typeDefs | — | VULN: System config exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: API keys and secrets in response |
| services/graphql/src/schema.js | typeDefs | — | VULN: DB connection string exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Log data exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: All active user data |
| services/graphql/src/schema.js | typeDefs | — | VULN: Admin accounts exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Version fingerprinting |
| services/graphql/src/schema.js | typeDefs | — | VULN: OS info exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: DB version exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Environment variables exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Memory stats exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Package list exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Raw metadata in alerts |
| services/graphql/src/schema.js | typeDefs | — | VULN: User data in search results |
| services/graphql/src/schema.js | typeDefs | 250 | VULN #250: Permissive input types allow mass assignment |
| services/graphql/src/schema.js | typeDefs | 102 | VULN #102: Role directly settable in input |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal field settable by users |
| services/graphql/src/schema.js | typeDefs | — | VULN: Token settable by users |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal cost field settable |
| services/graphql/src/schema.js | typeDefs | — | VULN: Business data settable |
| services/graphql/src/schema.js | typeDefs | — | VULN: User ID settable = IDOR |
| services/graphql/src/schema.js | typeDefs | 309 | VULN #309: Total price settable by client |
| services/graphql/src/schema.js | typeDefs | — | VULN: Discount settable directly |
| services/graphql/src/schema.js | typeDefs | — | VULN: Status settable on creation |
| services/graphql/src/schema.js | typeDefs | 309 | VULN #309: Price settable by client |
| services/graphql/src/schema.js | typeDefs | — | VULN: Discount settable per item |
| services/graphql/src/schema.js | typeDefs | 309 | VULN #309: Amount client-controlled |
| services/graphql/src/schema.js | typeDefs | — | VULN: SQL injectable via raw query |
| services/graphql/src/schema.js | typeDefs | — | VULN: SQL injectable field name |
| services/graphql/src/schema.js | typeDefs | — | VULN: SQL injectable order direction |
| services/graphql/src/schema.js | typeDefs | — | VULN: Soft-deleted items accessible |
| services/graphql/src/schema.js | typeDefs | 104, 108, 113, 115 | VULN #104, #108, #113, #115: Many queries lack auth checks |
| services/graphql/src/schema.js | typeDefs | 104 | VULN #104: Admin only but no check |
| services/graphql/src/schema.js | typeDefs | 97 | VULN #97: IDOR - any user data |
| services/graphql/src/schema.js | typeDefs | — | VULN: User enumeration |
| services/graphql/src/schema.js | typeDefs | — | VULN: User enumeration |
| services/graphql/src/schema.js | typeDefs | — | VULN: SQL injectable, returns PII |
| services/graphql/src/schema.js | typeDefs | 113 | VULN #113: Returns ALL orders |
| services/graphql/src/schema.js | typeDefs | — | VULN: IDOR |
| services/graphql/src/schema.js | typeDefs | — | VULN: IDOR |
| services/graphql/src/schema.js | typeDefs | — | VULN: Access any user's cart |
| services/graphql/src/schema.js | typeDefs | 115 | VULN #115: Payment data, no auth |
| services/graphql/src/schema.js | typeDefs | — | VULN: IDOR on payments |
| services/graphql/src/schema.js | typeDefs | — | VULN: All coupon codes exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN: Coupon detail including discount |
| services/graphql/src/schema.js | typeDefs | 108 | VULN #108: No auth |
| services/graphql/src/schema.js | typeDefs | — | VULN: Internal system info exposed |
| services/graphql/src/schema.js | typeDefs | — | VULN (extreme): Full DB dump |
| services/graphql/src/schema.js | typeDefs | — | VULN: All user PII exported |
| services/graphql/src/schema.js | typeDefs | — | VULN: SQL/NoSQL injectable |
| services/graphql/src/schema.js | typeDefs | — | VULN: Debug info |
| services/graphql/src/schema.js | typeDefs | — | VULN (extreme): Direct SQL execution |
| services/graphql/src/schema.js | typeDefs | 102, 250, 309 | VULN #102, #250, #309: Mutations without auth or input validation |
| services/graphql/src/schema.js | typeDefs | 250 | VULN #250: Mass assignment |
| services/graphql/src/schema.js | typeDefs | — | VULN: No ownership check; mass assign |
| services/graphql/src/schema.js | typeDefs | 102 | VULN #102: Privilege escalation |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth check |
| services/graphql/src/schema.js | typeDefs | 108 | VULN #108: No admin check |
| services/graphql/src/schema.js | typeDefs | — | VULN: No admin check |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth |
| services/graphql/src/schema.js | typeDefs | 309 | VULN #309: Total/price injectable |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth check |
| services/graphql/src/schema.js | typeDefs | — | VULN: Can cancel anyone's order |
| services/graphql/src/schema.js | typeDefs | 309 | VULN #309: Amount client-controlled |
| services/graphql/src/schema.js | typeDefs | — | VULN: Refund amount client-controlled |
| services/graphql/src/schema.js | typeDefs | — | VULN: Price injectable |
| services/graphql/src/schema.js | typeDefs | — | VULN: Can clear anyone's cart |
| services/graphql/src/schema.js | typeDefs | — | VULN: Discount injectable |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth |
| services/graphql/src/schema.js | typeDefs | — | VULN (extreme): Direct SQL execution |
| services/graphql/src/schema.js | typeDefs | — | VULN: No auth |
| services/graphql/src/schema.js | typeDefs | — | VULN: Extreme admin action no check |
| services/graphql/src/schema.js | typeDefs | 267 | VULN #267: Subscriptions without authentication |
| services/graphql/src/schema.js | typeDefs | — | VULN: Anyone can subscribe to any user's orders |
| services/graphql/src/schema.js | typeDefs | — | VULN: Leaks all payment events globally |
| services/graphql/src/schema.js | typeDefs | — | VULN: Admin alerts exposed to all subscribers |
| services/graphql/src/schema.js | typeDefs | — | VULN: Login events expose user data |
| services/graphql/src/schema.js | typeDefs | — | VULN: All new orders visible |
| services/worker/worker.py | module | — | VulnShop Celery Worker |
| services/worker/worker.py | module | — | INTENTIONALLY VULNERABLE - For educational/pentesting purposes only |
| services/worker/worker.py | module | 51, 52, 58, 68, 161, 204, 230, 355, 369, 410, 559, 657 | Vulnerabilities: #51, #52, #58, #68, #161, #204, #230, #355, #369, #410, #559, #657 |
| services/worker/worker.py | module | 559 | Logging setup - VULN #559: Logs may capture sensitive data |
| services/worker/worker.py | module | — | VULN: DEBUG level logs everything |
| services/worker/worker.py | module | — | VULN: Logs to world-readable tmp |
| services/worker/worker.py | BACKUP_DIR | 410 | VULN #410: Web-accessible backup dir |
| services/worker/worker.py | UPLOAD_DIR | — | VULN: Long task result expiry |
| services/worker/worker.py | UPLOAD_DIR | — | VULN: No rate limiting on tasks |
| services/worker/worker.py | UPLOAD_DIR | — | VULN: autoescape disabled - XSS in email templates possible |
| services/worker/worker.py | db_query | — | Execute a query - VULN: Some callers build SQL via string formatting. |
| services/worker/worker.py | db_query | 559 | VULN #559: SQL logged |
| services/worker/worker.py | send_smtp | 161 | Send email via SMTP (MailHog in dev).     VULN #161: SMTP injection in `to_addr` and `subject` - no sanitization. |
| services/worker/worker.py | send_smtp | 161 | VULN #161: No validation/sanitization on to_addr or subject |
| services/worker/worker.py | send_smtp | — | Attacker can inject headers: |
| services/worker/worker.py | send_smtp | — | to_addr = "victim@example.com\r\nBcc: attacker@evil.com" |
| services/worker/worker.py | send_smtp | 559 | VULN #559 |
| services/worker/worker.py | send_smtp | 161 | VULN #161: Direct assignment without sanitization |
| services/worker/worker.py | send_smtp | — | VULN: Header injection point |
| services/worker/worker.py | send_smtp | 161 | VULN #161: to_addr passed directly - can contain injected recipients |
| services/worker/worker.py | send_email | 161, 559 | Send a generic email.     VULN #161: SMTP header injection via `to` and `subject`.     VULN #559: Full email content logged including sensitive body. |
| services/worker/worker.py | send_email | 559 | VULN #559: Log entire email content |
| services/worker/worker.py | send_email | — | VULN: Body may contain PII/tokens |
| services/worker/worker.py | send_email | — | VULN: Template rendering with user-supplied data (SSTI possible) |
| services/worker/worker.py | send_email | 161 | VULN #161: to and subject passed without sanitization |
| services/worker/worker.py | send_password_reset_email | 51, 52, 559 | Send password reset email.     VULN #51: Reset token logged.     VULN #52: Predictable token generation.     VULN #559: Sensitive data in logs. |
| services/worker/worker.py | send_password_reset_email | 52 | VULN #52: Predictable token - uses timestamp + simple hash |
| services/worker/worker.py | send_password_reset_email | — | VULN: Predictable - only based on timestamp |
| services/worker/worker.py | send_password_reset_email | 51, 559 | VULN #51, #559: Token logged in plaintext |
| services/worker/worker.py | send_password_reset_email | — | VULN: Store token in DB without expiry check (or very long expiry) |
| services/worker/worker.py | send_password_reset_email | — | VULN: SQLi |
| services/worker/worker.py | send_password_reset_email | — | VULN: Token in template context (may render it) |
| services/worker/worker.py | send_password_reset_email | 52 | VULN #52: Long expiry |
| services/worker/worker.py | send_password_reset_email | 161 | VULN #161: user_email not sanitized |
| services/worker/worker.py | send_password_reset_email | — | VULN: Token in return value |
| services/worker/worker.py | send_order_confirmation | — | VULN: SQLi via order_id if not integer |
| services/worker/worker.py | send_order_confirmation | — | VULN: SQLi |
| services/worker/worker.py | send_order_confirmation | — | VULN: SQLi |
| services/worker/worker.py | send_order_confirmation | 559 | VULN #559: PII logged |
| services/worker/worker.py | send_verification_email | 51, 58 | Send email verification.     VULN #51: Token logged.     VULN #58: Token reusable indefinitely (no single-use enforcement). |
| services/worker/worker.py | send_verification_email | — | VULN: SQLi |
| services/worker/worker.py | send_verification_email | 58 | VULN #58: Token reusable - generated once, never invalidated after use |
| services/worker/worker.py | send_verification_email | 52 | VULN #52: Predictable |
| services/worker/worker.py | send_verification_email | 51, 559 | VULN #51, #559: Token logged |
| services/worker/worker.py | send_verification_email | 58 | VULN #58: Token stored permanently, never marked as used after verification |
| services/worker/worker.py | send_verification_email | — | VULN: Token in return |
| services/worker/worker.py | process_payment_async | 230, 309, 559 | Async payment processing.     VULN #230: Race condition - no distributed locking.     VULN #309: Amount from client not re-validated.     VULN #559: Payment data with card info logged. |
| services/worker/worker.py | process_payment_async | 559 | VULN #559: Logging full payment data including card details |
| services/worker/worker.py | process_payment_async | 309 | VULN #309: Amount from client |
| services/worker/worker.py | process_payment_async | 230 | VULN #230: Race condition - no lock acquired before reading order |
| services/worker/worker.py | process_payment_async | 230 | VULN #230: Time-of-check / time-of-use gap |
| services/worker/worker.py | process_payment_async | 230 | VULN #230: This check can fail under concurrent requests |
| services/worker/worker.py | process_payment_async | — | Should return error but intentionally continues |
| services/worker/worker.py | process_payment_async | 309 | VULN #309: No re-validation that amount == order total |
| services/worker/worker.py | process_payment_async | — | VULN: SQLi + CVV stored in plaintext (PCI violation) |
| services/worker/worker.py | process_payment_async | 230 | VULN #230: Update order status without atomic lock |
| services/worker/worker.py | generate_invoice | 204, 369, 559 | Generate PDF invoice for an order.     VULN #204: SSRF via logo_url - no URL validation.     VULN #369: Path traversal in output filename.     VULN #559: Order data with PII logged. |
| services/worker/worker.py | generate_invoice | — | VULN: SQLi |
| services/worker/worker.py | generate_invoice | 559 | VULN #559 |
| services/worker/worker.py | generate_invoice | 369 | VULN #369: Path traversal in filename |
| services/worker/worker.py | generate_invoice | — | Attacker can write to arbitrary locations |
| services/worker/worker.py | generate_invoice | 369 | VULN #369: filename constructed from user-controllable data without sanitization |
| services/worker/worker.py | generate_invoice | 204 | VULN #204: SSRF - logo_url fetched without validation |
| services/worker/worker.py | generate_invoice | — | Attacker can supply: logo_url = "http://169.254.169.254/latest/meta-data/" |
| services/worker/worker.py | generate_invoice | — | VULN: logs SSRF target |
| services/worker/worker.py | generate_invoice | 204 | VULN #204: No URL scheme check, no IP validation, no redirect protection |
| services/worker/worker.py | generate_invoice | — | VULN: Follows redirects (open redirect to SSRF) |
| services/worker/worker.py | generate_invoice | — | VULN: TLS verification disabled |
| services/worker/worker.py | generate_invoice | — | VULN: Response content returned to PDF (data exfiltration) |
| services/worker/worker.py | generate_invoice | — | VULN: Even if not an image, response body goes into error log |
| services/worker/worker.py | export_user_data | 657 | GDPR data export.     VULN #657: Returns ALL user data including sensitive PII fields.     No access control - any user_id can be exported. |
| services/worker/worker.py | export_user_data | 657 | VULN #657: Returns ALL columns including password, cvv, ssn, credit_card |
| services/worker/worker.py | export_user_data | — | VULN: SQLi |
| services/worker/worker.py | export_user_data | 657 | VULN #657: ALL PII included |
| services/worker/worker.py | export_user_data | 657 | VULN #657: Includes password, ssn, credit_card |
| services/worker/worker.py | export_user_data | 657 | VULN #657: Includes card_number, cvv |
| services/worker/worker.py | export_user_data | 369 | VULN #369: Path traversal in export filename |
| services/worker/worker.py | export_user_data | — | VULN: user_id could be path traversal |
| services/worker/worker.py | export_user_data | 559 | VULN #559: Logs full user data |
| services/worker/worker.py | export_user_data | 657 | VULN #657: Full PII data in task result |
| services/worker/worker.py | cleanup_sessions | 68 | Cleanup expired sessions.     VULN #68: Does NOT actually clean up expired sessions.     Old/expired sessions remain valid indefinitely. |
| services/worker/worker.py | cleanup_sessions | 68 | VULN #68: Query shows expired sessions but does NOT delete them |
| services/worker/worker.py | cleanup_sessions | 68 | VULN #68: Intentionally skip the actual cleanup |
| services/worker/worker.py | cleanup_sessions | 68 | VULN #68: Always 0 |
| services/worker/worker.py | backup_database | 410, 559 | Create a database backup.     VULN #410: Backup stored in web-accessible public directory.     Backup filename is predictable.     VULN #559: DB credentials logged. |
| services/worker/worker.py | backup_database | 410 | VULN #410: Backup stored in BACKUP_DIR which is web-accessible (/var/www/html/backups) |
| services/worker/worker.py | backup_database | — | Anyone can download: http://victim.com/backups/vulnshop_backup_20240101_120000.sql |
| services/worker/worker.py | backup_database | 559 | VULN #559: DB credentials logged |
| services/worker/worker.py | backup_database | — | VULN: DB password in environment / command line (visible in /proc) |
| services/worker/worker.py | backup_database | — | VULN: Error output may contain sensitive info |
| services/worker/worker.py | backup_database | 410 | VULN #410: Set world-readable permissions on backup |
| services/worker/worker.py | backup_database | 410 | VULN #410: Return public URL to backup |
| services/worker/worker.py | backup_database | 410 | VULN #410: Backup accessible publicly |
| services/worker/worker.py | backup_database | 410 | VULN #410: World-readable |
| services/worker/worker.py | backup_database | — | VULN: Full DB dump in task result |
| services/worker/worker.py | process_image | 355, 369 | Process an uploaded image.     VULN #355: ImageMagick vulnerabilities (ImageTragick / command injection).     VULN #369: Path traversal via image_path. |
| services/worker/worker.py | process_image | 369 | VULN #369: No path traversal check |
| services/worker/worker.py | process_image | 369 | VULN #369: Path traversal - read arbitrary files |
| services/worker/worker.py | process_image | 355 | VULN #355: Using convert (ImageMagick) with user-supplied path |
| services/worker/worker.py | process_image | 355 | VULN #355: Shell injection via image_path |
| services/worker/worker.py | process_image | — | VULN: subprocess with shell=True and user input |
| services/worker/worker.py | process_image | — | VULN: shell=True with user input |
| services/worker/worker.py | process_image | — | VULN: Error output returned (may contain path info) |
| services/worker/worker.py | process_image | 355 | VULN #355: Operation parameters not sanitized |
| services/worker/worker.py | process_image | — | VULN: Injected args go directly to convert |
| services/worker/worker.py | process_image | — | VULN: injection |
| services/worker/worker.py | process_image | — | VULN: PIL/Pillow also used - ReDoS via crafted image metadata |
| services/worker/worker.py | process_image | — | VULN: No size check - decompression bomb if huge image |
| services/worker/worker.py | process_image | — | VULN: Raw EXIF data returned |
| services/worker/worker.py | send_bulk_email | 161 | Send bulk email to multiple users.     VULN #161: SMTP injection in subject.     VULN: No rate limiting on bulk sending. |
| services/worker/worker.py | send_bulk_email | — | VULN: SQLi, N+1 |
| services/worker/worker.py | send_bulk_email | — | VULN: User-controlled context can cause SSTI |
| services/worker/worker.py | send_bulk_email | 161 | VULN #161: subject not sanitized |
| services/worker/worker.py | run_report | — | Run internal reports.     VULN: SQL injectable report type and params.     VULN: No auth check - any worker message can trigger. |
| services/worker/worker.py | run_report | — | VULN: report_type directly interpolated into SQL |
| services/worker/worker.py | run_report | — | VULN: Table name from user input (SQLi) |
| services/worker/worker.py | run_report | — | VULN: Direct SQLi |
| services/worker/worker.py | run_report | — | VULN: SQLi |
| services/worker/worker.py | run_report | — | VULN: DB error message returned |
| services/worker/worker.py | parse_yaml_config | — | Parse YAML configuration.     VULN: Unsafe YAML loading allows arbitrary code execution. |
| services/worker/worker.py | parse_yaml_config | — | VULN: yaml.load without Loader=SafeLoader allows deserialization attacks |
| services/worker/worker.py | parse_yaml_config | — | Attacker payload: "!!python/object/apply:os.system ['rm -rf /']" |
| services/worker/worker.py | parse_yaml_config | — | VULN: Unsafe loader |
<!-- END MOVED ANNOTATIONS -->
