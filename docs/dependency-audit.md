# Dependency audit evidence

Captured on **2026-11-05** with `npm audit` against the generated lockfiles. These results confirm dependency findings for the local lab; they do not prove that every advisory is reachable through an application endpoint.

| Package tree | Audit total | Moderate | High | Critical | Direct examples |
|---|---:|---:|---:|---:|---|
| `frontend/` | 4 | 1 | 2 | 1 | `nodemailer@6.10.1`, `uuid@9.0.1` |
| `services/graphql/` | 5 | 1 | 4 | 0 | `@apollo/server@4.13.0` |

The frontend report includes a critical transitive `tar` finding and a high `nodemailer` finding. The GraphQL report includes a high `@apollo/server` finding; npm also warns that Apollo Server v4 reached end of life on 2026-01-26. The full findings can be regenerated with `npm audit` in each package directory.

This evidence supports checklist entries **#543 Vulnerable Dependencies**, **#544 Outdated Dependencies**, and **#618 JavaScript Dependency Vulnerability**. The audit data is time-sensitive and should be refreshed before any future release.
