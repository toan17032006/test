# VulnShop

VulnShop is an intentionally vulnerable e-commerce training lab for authorized testing. Use synthetic data and run it only on a machine and network you control. Do not expose it to the public internet or use production data.

## Brief coverage

The supplied brief has 275 store and architecture components plus a numbered 1–726 catalog. Those 726 entries comprise 661 vulnerability topics, 29 attack-chain scenarios, and 36 test-matrix fields. The complete inventory is preserved in [vulndb/catalog.json](vulndb/catalog.json) and [vulndb/checklist.md](vulndb/checklist.md).

The complete inventory is preserved. The source map records annotated locations for 120 vulnerability IDs; those references show where behavior is declared or implemented, not that it is reachable at runtime. Loopback smoke evidence verifies 145 vulnerability topics and nine attack chains; a route-handler regression verifies that a reset token timestamped ten years in the past is still accepted; the dependency audit verifies three additional dependency topics. Component smoke evidence covers 102 of the 275 component/workflow rows at route or flow level; the other 173 remain `unverified` / `not_tested`. Evidence is linked in the checklist and documented in [docs/implementation-map.md](docs/implementation-map.md), [docs/component-smoke.md](docs/component-smoke.md), [docs/smoke-findings.md](docs/smoke-findings.md), and [docs/dependency-audit.md](docs/dependency-audit.md). Many source-mapped vulnerability entries also remain `not_tested`.

## Local run

Requirements: Docker Engine with Compose, or Node.js 20+ for the storefront and Python 3.12+ for the API.

```powershell
docker compose up --build
```

Local endpoints:

- Storefront and admin checklist: `http://127.0.0.1:3000` and `http://127.0.0.1:3000/admin/vulns`
- API and OpenAPI: `http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs`
- GraphQL: `http://127.0.0.1:4000/graphql`
- Nginx entry point: `http://127.0.0.1`
- MailHog: `http://127.0.0.1:8025`

Demo accounts are synthetic and intentionally weak: `admin@vulnshop.com` / `admin123` and `user@vulnshop.com` / `password`.

The Compose topology binds host ports to loopback and uses an internal Docker network without outbound internet access. Keep these defaults. Do not change them to `0.0.0.0` or add host networking. Payments are mock-only and do not contact a real provider. The API's cart, order, and notification routes use in-memory state; database containers are seeded with synthetic sample rows.

For the storefront without Docker, run `npm install` and `npm start` from `frontend/`. It listens on `127.0.0.1` by default. To run the API, install `backend/requirements.txt` and start Uvicorn from `backend/`.

## Test and verification

```powershell
python -m unittest discover -s tests -v
```

The tests cover inventory completeness, rendered checklist synchronization, view/build-file references, Compose containment, JWT helper behavior, and an in-memory cart → order → mock-payment → webhook workflow. The loopback smoke test reproduces the findings listed in its evidence report. It does not prove that all 661 vulnerability topics are implemented. Docker Compose could not be run in the current environment because Docker is unavailable.

For a loopback HTTP smoke test of the storefront, API, and GraphQL service, run `./tests/smoke-local.ps1` in PowerShell. It uses synthetic credentials/data, binds only to `127.0.0.1`, and stops the processes when it finishes. GitHub Actions runs the unit and template checks on pushes and pull requests.

## Main areas

- `frontend/` — Vietnamese e-commerce storefront, customer flows, and checklist page
- `backend/` — FastAPI routes for authentication, catalog, cart, orders, payments, users, admin, files, search, coupons, notifications, and webhooks
- `services/graphql/` — GraphQL API
- `services/worker/` — background job examples
- `docker-compose.yml` — local-only services and synthetic database seeds
- `vulndb/` — complete source inventory and searchable checklist interface

High-impact topics such as denial of service, host escape, cloud metadata access, arbitrary command execution, and third-party attack chains must be tested only in disposable, isolated lab infrastructure. Never run tests against systems outside your authorization.
