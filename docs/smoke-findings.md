# Loopback smoke findings

Captured on **2026-11-05** by `tests/smoke-local.ps1`. The test starts the FastAPI, storefront, and GraphQL processes on dynamically selected `127.0.0.1` ports. It uses synthetic accounts, marker credentials, fake SMTP/database endpoints, and in-memory order/payment data. No real payment provider or external target is contacted; the script stops the processes and removes its temporary logs.

The automated smoke reproduced the following behaviors and records them as `observed` / `verified` in `vulndb/catalog.json`:

| IDs | Finding | Direct evidence |
|---|---|---|
| 17, 19, 20 | Exposed environment configuration, API docs, and GraphQL introspection | Unauthenticated `/.env` returned only a test marker; `/docs` returned 200; GraphQL `__schema` returned the `Query` root. |
| 31, 61 | Weak password policy and authentication bypass | Registration accepted a one-character password; `/auth/bypass` returned an admin principal for `{"admin":true}`. |
| 97, 98, 102, 103, 104, 108, 113, 116 | Object-level access failures, role escalation, and exposed admin routes | A caller identifying as user 2 read user 3's order and address; unauthenticated signup set the new account's role to admin; the admin user list returned without authentication. |
| 251, 252, 260 | Excessive API data, parameter tampering, and GraphQL introspection | Product responses included internal cost/admin notes; cart and order requests set below-catalog prices and totals; schema introspection succeeded. |
| 277, 278, 279, 283, 288, 290, 307, 308, 309, 311, 312, 313 | Forged/replayed payment events and client-controlled pricing | A below-catalog cart price and altered order total were accepted; a zero-amount mock payment set an order to paid; an unsigned payment webhook changed another synthetic order to paid and accepted the same event twice. |
| 372, 394, 435, 558 | Weak password storage, sensitive logging, and exposed environment credentials | The returned password hash matched MD5 of the synthetic one-character password; the isolated API log contained that password; `/.env` returned a deliberately fake AWS marker. |
| 543, 544, 618 | Vulnerable/outdated JavaScript dependencies | See the dated `npm audit` summary in [dependency-audit.md](dependency-audit.md). |
| 643, 645, 646, 650, 651, 652 | Customer PII, admin data, business information, and cross-customer leakage | The unauthenticated admin list exposed synthetic email, phone, card/SSN and password fields; product detail exposed cost/admin note; user 2 received user 3's order and address. |
| 675, 678 | API BOLA data access and forged payment attack chains | The cross-customer read returned user 3's order; the unsigned webhook changed a pending order to paid/processing. |

These results cover only the listed findings. The other vulnerability entries, attack chains, components, and environment-dependent infrastructure checks remain `unverified` / `not_tested`; catalog completeness does not imply complete implementation.
