# VulnShop coverage checklist

> The inventory preserves all IDs and names from the supplied brief. Statuses change only when direct runtime or audit evidence is recorded; entries without evidence remain unverified. See the evidence documents linked in the final column.

## Counts

| Scope | Count |
|---|---:|
| Application components | 275 |
| Vulnerability entries | 661 |
| Attack-chain scenarios | 29 |
| Test-matrix fields | 36 |
| Total entries in the 1–726 list | 726 |

## Application components

| ID | Component | Group | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 1 | DNS | Hạ tầng và Cloud | unverified | not_tested | — |
| 2 | CDN | Hạ tầng và Cloud | unverified | not_tested | — |
| 3 | WAF | Hạ tầng và Cloud | unverified | not_tested | — |
| 4 | Cloud Infrastructure | Hạ tầng và Cloud | unverified | not_tested | — |
| 5 | Cloud Storage (S3, Blob Storage) | Hạ tầng và Cloud | unverified | not_tested | — |
| 6 | Load Balancer | Hạ tầng và Cloud | unverified | not_tested | — |
| 7 | Reverse Proxy | Hạ tầng và Cloud | unverified | not_tested | — |
| 8 | API Gateway | Hạ tầng và Cloud | unverified | not_tested | — |
| 9 | Web Server (Nginx, Apache, IIS) | Hạ tầng và Cloud | unverified | not_tested | — |
| 10 | Application Server | Hạ tầng và Cloud | unverified | not_tested | — |
| 11 | Containerization (Docker) | Hạ tầng và Cloud | unverified | not_tested | — |
| 12 | Container Orchestration (Kubernetes) | Hạ tầng và Cloud | unverified | not_tested | — |
| 13 | Virtual Machines | Hạ tầng và Cloud | unverified | not_tested | — |
| 14 | Serverless Functions | Hạ tầng và Cloud | unverified | not_tested | — |
| 15 | Edge Computing | Hạ tầng và Cloud | unverified | not_tested | — |
| 16 | Multi-Region Deployment | Hạ tầng và Cloud | unverified | not_tested | — |
| 17 | Network Infrastructure | Hạ tầng và Cloud | unverified | not_tested | — |
| 18 | Firewall | Hạ tầng và Cloud | unverified | not_tested | — |
| 19 | VPN | Hạ tầng và Cloud | unverified | not_tested | — |
| 20 | SSH | Hạ tầng và Cloud | unverified | not_tested | — |
| 21 | Homepage | Frontend và Browser | unverified | not_tested | — |
| 22 | Product Listing | Frontend và Browser | unverified | not_tested | — |
| 23 | Product Detail | Frontend và Browser | unverified | not_tested | — |
| 24 | Product Search | Frontend và Browser | unverified | not_tested | — |
| 25 | Product Filtering | Frontend và Browser | unverified | not_tested | — |
| 26 | Product Sorting | Frontend và Browser | unverified | not_tested | — |
| 27 | Category Navigation | Frontend và Browser | unverified | not_tested | — |
| 28 | Shopping Cart | Frontend và Browser | unverified | not_tested | — |
| 29 | Wishlist | Frontend và Browser | unverified | not_tested | — |
| 30 | Checkout | Frontend và Browser | unverified | not_tested | — |
| 31 | Order Tracking | Frontend và Browser | unverified | not_tested | — |
| 32 | User Profile | Frontend và Browser | unverified | not_tested | — |
| 33 | Address Book | Frontend và Browser | unverified | not_tested | — |
| 34 | Login | Frontend và Browser | unverified | not_tested | — |
| 35 | Sign Up | Frontend và Browser | unverified | not_tested | — |
| 36 | Logout | Frontend và Browser | unverified | not_tested | — |
| 37 | Forgot Password | Frontend và Browser | unverified | not_tested | — |
| 38 | Reset Password | Frontend và Browser | unverified | not_tested | — |
| 39 | Email Verification | Frontend và Browser | unverified | not_tested | — |
| 40 | Phone Verification | Frontend và Browser | unverified | not_tested | — |
| 41 | Multi-Factor Authentication | Frontend và Browser | unverified | not_tested | — |
| 42 | Social Login | Frontend và Browser | unverified | not_tested | — |
| 43 | OAuth2 / OIDC | Frontend và Browser | unverified | not_tested | — |
| 44 | SSO | Frontend và Browser | unverified | not_tested | — |
| 45 | Session Management | Frontend và Browser | unverified | not_tested | — |
| 46 | Cookies | Frontend và Browser | unverified | not_tested | — |
| 47 | LocalStorage | Frontend và Browser | unverified | not_tested | — |
| 48 | SessionStorage | Frontend và Browser | unverified | not_tested | — |
| 49 | IndexedDB | Frontend và Browser | unverified | not_tested | — |
| 50 | Service Workers | Frontend và Browser | unverified | not_tested | — |
| 51 | Browser Cache | Frontend và Browser | unverified | not_tested | — |
| 52 | CORS | Frontend và Browser | unverified | not_tested | — |
| 53 | CSP | Frontend và Browser | unverified | not_tested | — |
| 54 | HTTP Security Headers | Frontend và Browser | unverified | not_tested | — |
| 55 | Responsive Design | Frontend và Browser | unverified | not_tested | — |
| 56 | Admin Dashboard | Frontend và Browser | unverified | not_tested | — |
| 57 | User Dashboard | Frontend và Browser | unverified | not_tested | — |
| 58 | REST API | Backend và API | unverified | not_tested | — |
| 59 | GraphQL | Backend và API | unverified | not_tested | — |
| 60 | GraphQL Federation | Backend và API | unverified | not_tested | — |
| 61 | gRPC | Backend và API | unverified | not_tested | — |
| 62 | WebSocket | Backend và API | unverified | not_tested | — |
| 63 | Webhook | Backend và API | unverified | not_tested | — |
| 64 | Microservices | Backend và API | unverified | not_tested | — |
| 65 | Monolithic Architecture | Backend và API | unverified | not_tested | — |
| 66 | API Versioning | Backend và API | unverified | not_tested | — |
| 67 | Rate Limiting | Backend và API | unverified | not_tested | — |
| 68 | Input Validation | Backend và API | unverified | not_tested | — |
| 69 | Output Encoding | Backend và API | unverified | not_tested | — |
| 70 | Authentication | Backend và API | unverified | not_tested | — |
| 71 | Authorization | Backend và API | unverified | not_tested | — |
| 72 | RBAC | Backend và API | unverified | not_tested | — |
| 73 | ABAC | Backend và API | unverified | not_tested | — |
| 74 | Multi-Tenancy | Backend và API | unverified | not_tested | — |
| 75 | Business Logic | Backend và API | unverified | not_tested | — |
| 76 | Background Jobs | Backend và API | unverified | not_tested | — |
| 77 | Workflow Engine | Backend và API | unverified | not_tested | — |
| 78 | Event-Driven Architecture | Backend và API | unverified | not_tested | — |
| 79 | Message Queue | Backend và API | unverified | not_tested | — |
| 80 | Event Streaming | Backend và API | unverified | not_tested | — |
| 81 | Product Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 82 | Product Variants | Chức năng thương mại điện tử | unverified | not_tested | — |
| 83 | Product Attributes | Chức năng thương mại điện tử | unverified | not_tested | — |
| 84 | Product Categories | Chức năng thương mại điện tử | unverified | not_tested | — |
| 85 | Product Brands | Chức năng thương mại điện tử | unverified | not_tested | — |
| 86 | Product Pricing | Chức năng thương mại điện tử | unverified | not_tested | — |
| 87 | Discount Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 88 | Coupon Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 89 | Flash Sale | Chức năng thương mại điện tử | unverified | not_tested | — |
| 90 | Inventory Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 91 | Stock Reservation | Chức năng thương mại điện tử | unverified | not_tested | — |
| 92 | Shopping Cart | Chức năng thương mại điện tử | unverified | not_tested | — |
| 93 | Cart Synchronization | Chức năng thương mại điện tử | unverified | not_tested | — |
| 94 | Guest Checkout | Chức năng thương mại điện tử | unverified | not_tested | — |
| 95 | Customer Checkout | Chức năng thương mại điện tử | unverified | not_tested | — |
| 96 | Shipping Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 97 | Shipping Fee Calculation | Chức năng thương mại điện tử | unverified | not_tested | — |
| 98 | Shipping Address | Chức năng thương mại điện tử | unverified | not_tested | — |
| 99 | Billing Address | Chức năng thương mại điện tử | unverified | not_tested | — |
| 100 | Payment Gateway | Chức năng thương mại điện tử | unverified | not_tested | — |
| 101 | Cash on Delivery (COD) | Chức năng thương mại điện tử | unverified | not_tested | — |
| 102 | Payment Refund | Chức năng thương mại điện tử | unverified | not_tested | — |
| 103 | Payment Callback | Chức năng thương mại điện tử | unverified | not_tested | — |
| 104 | Payment Webhook | Chức năng thương mại điện tử | unverified | not_tested | — |
| 105 | Order Management | Chức năng thương mại điện tử | unverified | not_tested | — |
| 106 | Order History | Chức năng thương mại điện tử | unverified | not_tested | — |
| 107 | Order Cancellation | Chức năng thương mại điện tử | unverified | not_tested | — |
| 108 | Order Return | Chức năng thương mại điện tử | unverified | not_tested | — |
| 109 | Order Exchange | Chức năng thương mại điện tử | unverified | not_tested | — |
| 110 | Invoice Generation | Chức năng thương mại điện tử | unverified | not_tested | — |
| 111 | Tax Calculation | Chức năng thương mại điện tử | unverified | not_tested | — |
| 112 | Review & Rating | Chức năng thương mại điện tử | unverified | not_tested | — |
| 113 | Product Q&A | Chức năng thương mại điện tử | unverified | not_tested | — |
| 114 | Wishlist | Chức năng thương mại điện tử | unverified | not_tested | — |
| 115 | Recently Viewed Products | Chức năng thương mại điện tử | unverified | not_tested | — |
| 116 | Recommendation System | Chức năng thương mại điện tử | unverified | not_tested | — |
| 117 | Loyalty Points | Chức năng thương mại điện tử | unverified | not_tested | — |
| 118 | Gift Cards | Chức năng thương mại điện tử | unverified | not_tested | — |
| 119 | Affiliate System | Chức năng thương mại điện tử | unverified | not_tested | — |
| 120 | Subscription Products | Chức năng thương mại điện tử | unverified | not_tested | — |
| 121 | Notification System | Chức năng thương mại điện tử | unverified | not_tested | — |
| 122 | Email Notification | Chức năng thương mại điện tử | unverified | not_tested | — |
| 123 | SMS Notification | Chức năng thương mại điện tử | unverified | not_tested | — |
| 124 | Push Notification | Chức năng thương mại điện tử | unverified | not_tested | — |
| 125 | SQL Database (PostgreSQL, MySQL) | Database và Data Storage | unverified | not_tested | — |
| 126 | NoSQL Database (MongoDB) | Database và Data Storage | unverified | not_tested | — |
| 127 | Graph Database (Neo4j) | Database và Data Storage | unverified | not_tested | — |
| 128 | In-Memory Database (Redis) | Database và Data Storage | unverified | not_tested | — |
| 129 | Search Engine (Elasticsearch, OpenSearch) | Database và Data Storage | unverified | not_tested | — |
| 130 | Time-Series Database | Database và Data Storage | unverified | not_tested | — |
| 131 | Object Storage | Database và Data Storage | unverified | not_tested | — |
| 132 | File System | Database và Data Storage | unverified | not_tested | — |
| 133 | Data Replication | Database và Data Storage | unverified | not_tested | — |
| 134 | Database Sharding | Database và Data Storage | unverified | not_tested | — |
| 135 | Database Backup & Recovery | Database và Data Storage | unverified | not_tested | — |
| 136 | Database Migration | Database và Data Storage | unverified | not_tested | — |
| 137 | Database Encryption | Database và Data Storage | unverified | not_tested | — |
| 138 | Data Masking | Database và Data Storage | unverified | not_tested | — |
| 139 | Admin Dashboard | Quản trị hệ thống | unverified | not_tested | — |
| 140 | User Management | Quản trị hệ thống | unverified | not_tested | — |
| 141 | Product Management | Quản trị hệ thống | unverified | not_tested | — |
| 142 | Category Management | Quản trị hệ thống | unverified | not_tested | — |
| 143 | Order Management | Quản trị hệ thống | unverified | not_tested | — |
| 144 | Inventory Management | Quản trị hệ thống | unverified | not_tested | — |
| 145 | Payment Management | Quản trị hệ thống | unverified | not_tested | — |
| 146 | Refund Management | Quản trị hệ thống | unverified | not_tested | — |
| 147 | Coupon Management | Quản trị hệ thống | unverified | not_tested | — |
| 148 | Promotion Management | Quản trị hệ thống | unverified | not_tested | — |
| 149 | Role & Permission Management | Quản trị hệ thống | unverified | not_tested | — |
| 150 | Audit Log | Quản trị hệ thống | unverified | not_tested | — |
| 151 | System Configuration | Quản trị hệ thống | unverified | not_tested | — |
| 152 | Feature Flags | Quản trị hệ thống | unverified | not_tested | — |
| 153 | Tenant Management | Quản trị hệ thống | unverified | not_tested | — |
| 154 | CMS | Quản trị hệ thống | unverified | not_tested | — |
| 155 | Analytics & Reporting | Quản trị hệ thống | unverified | not_tested | — |
| 156 | External APIs | Tích hợp bên thứ ba | unverified | not_tested | — |
| 157 | Payment Providers | Tích hợp bên thứ ba | unverified | not_tested | — |
| 158 | Shipping Providers | Tích hợp bên thứ ba | unverified | not_tested | — |
| 159 | Email Service (SMTP) | Tích hợp bên thứ ba | unverified | not_tested | — |
| 160 | SMS Service | Tích hợp bên thứ ba | unverified | not_tested | — |
| 161 | OAuth Providers | Tích hợp bên thứ ba | unverified | not_tested | — |
| 162 | CAPTCHA | Tích hợp bên thứ ba | unverified | not_tested | — |
| 163 | Maps & Geolocation | Tích hợp bên thứ ba | unverified | not_tested | — |
| 164 | Analytics Services | Tích hợp bên thứ ba | unverified | not_tested | — |
| 165 | CRM | Tích hợp bên thứ ba | unverified | not_tested | — |
| 166 | ERP | Tích hợp bên thứ ba | unverified | not_tested | — |
| 167 | Search Services | Tích hợp bên thứ ba | unverified | not_tested | — |
| 168 | AI Integration | Tích hợp bên thứ ba | unverified | not_tested | — |
| 169 | CI/CD Pipeline | DevOps và vận hành | unverified | not_tested | — |
| 170 | Source Code Repository | DevOps và vận hành | unverified | not_tested | — |
| 171 | Dependency Management | DevOps và vận hành | unverified | not_tested | — |
| 172 | Package Registry | DevOps và vận hành | unverified | not_tested | — |
| 173 | Infrastructure as Code (Terraform, Ansible) | DevOps và vận hành | unverified | not_tested | — |
| 174 | Docker Compose | DevOps và vận hành | unverified | not_tested | — |
| 175 | Kubernetes | DevOps và vận hành | unverified | not_tested | — |
| 176 | Secrets Management | DevOps và vận hành | unverified | not_tested | — |
| 177 | Configuration Management | DevOps và vận hành | unverified | not_tested | — |
| 178 | Monitoring | DevOps và vận hành | unverified | not_tested | — |
| 179 | Logging | DevOps và vận hành | unverified | not_tested | — |
| 180 | Distributed Tracing | DevOps và vận hành | unverified | not_tested | — |
| 181 | Error Tracking | DevOps và vận hành | unverified | not_tested | — |
| 182 | Metrics & Alerting | DevOps và vận hành | unverified | not_tested | — |
| 183 | Backup & Recovery | DevOps và vận hành | unverified | not_tested | — |
| 184 | Disaster Recovery | DevOps và vận hành | unverified | not_tested | — |
| 185 | Multi-Region Deployment | DevOps và vận hành | unverified | not_tested | — |
| 186 | SQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 187 | NoSQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 188 | GraphQL Injection | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 189 | XSS | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 190 | CSRF | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 191 | SSRF | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 192 | IDOR / BOLA | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 193 | Broken Authentication | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 194 | Broken Authorization | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 195 | Privilege Escalation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 196 | Session Hijacking | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 197 | Session Fixation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 198 | JWT Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 199 | OAuth Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 200 | SAML Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 201 | Password Reset Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 202 | Account Enumeration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 203 | Brute Force | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 204 | Credential Stuffing | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 205 | Rate Limit Bypass | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 206 | Business Logic Abuse | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 207 | Price Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 208 | Coupon Abuse | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 209 | Cart Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 210 | Payment Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 211 | Race Conditions | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 212 | Inventory Manipulation | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 213 | Checkout Bypass | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 214 | Payment Replay | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 215 | Webhook Forgery | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 216 | File Upload Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 217 | Path Traversal | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 218 | Local File Inclusion (LFI) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 219 | Remote File Inclusion (RFI) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 220 | Remote Code Execution (RCE) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 221 | Server-Side Template Injection (SSTI) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 222 | XXE | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 223 | Deserialization Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 224 | CORS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 225 | CSP Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 226 | TLS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 227 | Security Header Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 228 | DNS Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 229 | Subdomain Takeover | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 230 | Open Redirect | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 231 | Clickjacking | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 232 | Host Header Injection | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 233 | HTTP Request Smuggling | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 234 | Cache Poisoning | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 235 | Cache Deception | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 236 | API Mass Assignment | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 237 | API Excessive Data Exposure | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 238 | GraphQL Introspection Abuse | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 239 | GraphQL DoS | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 240 | WebSocket Authorization Bypass | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 241 | Webhook SSRF | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 242 | Cloud Storage Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 243 | IAM Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 244 | Container Escape | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 245 | Kubernetes Misconfiguration | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 246 | Secrets Exposure | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 247 | CI/CD Pipeline Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 248 | Dependency / Supply Chain Vulnerabilities | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 249 | Logging & Monitoring Weaknesses | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 250 | Backup Exposure | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 251 | Information Disclosure | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 252 | Sensitive Data Exposure | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 253 | PII Leakage | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 254 | Business Email Compromise Scenarios | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 255 | Denial of Service (DoS) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 256 | Distributed Denial of Service (DDoS) | Các chức năng và bề mặt kiểm thử bảo mật | unverified | not_tested | — |
| 257 | Đăng ký → Xác minh email → Đăng nhập | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 258 | Đăng nhập → Quản lý hồ sơ → Đổi mật khẩu | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 259 | Tìm kiếm → Xem sản phẩm → Thêm giỏ hàng | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 260 | Giỏ hàng → Áp mã giảm giá → Checkout | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 261 | Checkout → Thanh toán → Xác nhận đơn hàng | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 262 | Thanh toán thất bại → Thử lại thanh toán | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 263 | Đặt hàng → Hủy đơn → Hoàn tiền | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 264 | Đặt hàng → Theo dõi vận chuyển → Nhận hàng | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 265 | Yêu cầu đổi trả → Duyệt yêu cầu → Hoàn tiền | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 266 | Admin → Quản lý người dùng → Phân quyền | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 267 | Admin → Quản lý sản phẩm → Quản lý kho | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 268 | Admin → Quản lý đơn hàng → Quản lý thanh toán | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 269 | User A → Truy cập dữ liệu User B (kiểm thử IDOR/BOLA) | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 270 | User thường → Truy cập chức năng Admin (kiểm thử phân quyền) | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 271 | Guest → Truy cập tài nguyên yêu cầu đăng nhập | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 272 | Nhiều người dùng đồng thời mua sản phẩm giới hạn tồn kho | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 273 | Gửi lại payment callback/webhook | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 274 | Thay đổi giá, số lượng, coupon trong quá trình checkout | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |
| 275 | Truy cập API trực tiếp bỏ qua giao diện frontend | Các kịch bản nghiệp vụ end-to-end | unverified | not_tested | — |

## Reconnaissance & Information Disclosure

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 1 | Subdomain Enumeration Exposure | vulnerability | unverified | not_tested | — |
| 2 | Subdomain Takeover | vulnerability | unverified | not_tested | — |
| 3 | DNS Zone Transfer | vulnerability | unverified | not_tested | — |
| 4 | DNS Misconfiguration | vulnerability | unverified | not_tested | — |
| 5 | DNS Cache Poisoning | vulnerability | unverified | not_tested | — |
| 6 | Virtual Host Misconfiguration | vulnerability | unverified | not_tested | — |
| 7 | Server Version Disclosure | vulnerability | unverified | not_tested | — |
| 8 | Technology Stack Disclosure | vulnerability | unverified | not_tested | — |
| 9 | Framework Fingerprinting | vulnerability | unverified | not_tested | — |
| 10 | Debug Information Exposure | vulnerability | unverified | not_tested | — |
| 11 | Source Code Disclosure | vulnerability | unverified | not_tested | — |
| 12 | Source Map Exposure | vulnerability | unverified | not_tested | — |
| 13 | Git Repository Exposure | vulnerability | unverified | not_tested | — |
| 14 | SVN Repository Exposure | vulnerability | unverified | not_tested | — |
| 15 | Backup File Exposure | vulnerability | unverified | not_tested | — |
| 16 | Configuration File Exposure | vulnerability | unverified | not_tested | — |
| 17 | Environment File Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 18 | API Documentation Exposure | vulnerability | unverified | not_tested | — |
| 19 | Swagger Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 20 | GraphQL Introspection Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 21 | Directory Listing | vulnerability | unverified | not_tested | — |
| 22 | Hidden Endpoint Exposure | vulnerability | unverified | not_tested | — |
| 23 | Sensitive Metadata Exposure | vulnerability | unverified | not_tested | — |
| 24 | Error Message Information Leakage | vulnerability | unverified | not_tested | — |
| 25 | Stack Trace Disclosure | vulnerability | unverified | not_tested | — |
| 26 | Internal IP Disclosure | vulnerability | unverified | not_tested | — |
| 27 | Cloud Metadata Exposure | vulnerability | unverified | not_tested | — |
| 28 | Public Cloud Storage Exposure | vulnerability | unverified | not_tested | — |
| 29 | PII Exposure | vulnerability | unverified | not_tested | — |
| 30 | Sensitive Business Data Exposure | vulnerability | unverified | not_tested | — |

## Authentication Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 31 | Weak Password Policy | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 32 | Weak Default Credentials | vulnerability | unverified | not_tested | — |
| 33 | Default Admin Account | vulnerability | unverified | not_tested | — |
| 34 | Username Enumeration | vulnerability | unverified | not_tested | — |
| 35 | Email Enumeration | vulnerability | unverified | not_tested | — |
| 36 | Phone Number Enumeration | vulnerability | unverified | not_tested | — |
| 37 | Account Enumeration | vulnerability | unverified | not_tested | — |
| 38 | Brute Force | vulnerability | unverified | not_tested | — |
| 39 | Password Spraying | vulnerability | unverified | not_tested | — |
| 40 | Credential Stuffing | vulnerability | unverified | not_tested | — |
| 41 | Missing Login Rate Limiting | vulnerability | unverified | not_tested | — |
| 42 | Rate Limit Bypass | vulnerability | unverified | not_tested | — |
| 43 | CAPTCHA Bypass | vulnerability | unverified | not_tested | — |
| 44 | MFA Bypass | vulnerability | unverified | not_tested | — |
| 45 | MFA Fatigue | vulnerability | unverified | not_tested | — |
| 46 | OTP Brute Force | vulnerability | unverified | not_tested | — |
| 47 | OTP Replay | vulnerability | unverified | not_tested | — |
| 48 | OTP Predictability | vulnerability | unverified | not_tested | — |
| 49 | OTP Expiration Bypass | vulnerability | unverified | not_tested | — |
| 50 | OTP Race Condition | vulnerability | unverified | not_tested | — |
| 51 | Password Reset Token Leakage | vulnerability | unverified | not_tested | — |
| 52 | Password Reset Token Prediction | vulnerability | unverified | not_tested | — |
| 53 | Password Reset Token Reuse | vulnerability | unverified | not_tested | — |
| 54 | Password Reset Token Not Expiring | vulnerability | unverified | not_tested | — |
| 55 | Password Reset Account Takeover | vulnerability | unverified | not_tested | — |
| 56 | Password Reset Host Header Injection | vulnerability | unverified | not_tested | — |
| 57 | Insecure Email Verification | vulnerability | unverified | not_tested | — |
| 58 | Email Verification Token Reuse | vulnerability | unverified | not_tested | — |
| 59 | Email Verification Bypass | vulnerability | unverified | not_tested | — |
| 60 | Phone Verification Bypass | vulnerability | unverified | not_tested | — |
| 61 | Authentication Bypass | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 62 | Insecure Remember Me | vulnerability | unverified | not_tested | — |
| 63 | Broken Authentication | vulnerability | unverified | not_tested | — |
| 64 | Authentication Logic Flaws | vulnerability | unverified | not_tested | — |
| 65 | Session Fixation | vulnerability | unverified | not_tested | — |
| 66 | Session Hijacking | vulnerability | unverified | not_tested | — |
| 67 | Session Replay | vulnerability | unverified | not_tested | — |
| 68 | Session Not Invalidated After Logout | vulnerability | unverified | not_tested | — |
| 69 | Session Not Invalidated After Password Change | vulnerability | unverified | not_tested | — |
| 70 | Concurrent Session Abuse | vulnerability | unverified | not_tested | — |
| 71 | Insecure Session Cookie | vulnerability | unverified | not_tested | — |
| 72 | JWT None Algorithm | vulnerability | unverified | not_tested | — |
| 73 | JWT Algorithm Confusion | vulnerability | unverified | not_tested | — |
| 74 | JWT Signature Validation Bypass | vulnerability | unverified | not_tested | — |
| 75 | JWT Weak Secret | vulnerability | unverified | not_tested | — |
| 76 | JWT Key Confusion | vulnerability | unverified | not_tested | — |
| 77 | JWT Expiration Validation Bypass | vulnerability | unverified | not_tested | — |
| 78 | JWT Audience Validation Bypass | vulnerability | unverified | not_tested | — |
| 79 | JWT Issuer Validation Bypass | vulnerability | unverified | not_tested | — |
| 80 | JWT Token Replay | vulnerability | unverified | not_tested | — |
| 81 | JWT Sensitive Data Exposure | vulnerability | unverified | not_tested | — |
| 82 | Refresh Token Reuse | vulnerability | unverified | not_tested | — |
| 83 | Refresh Token Rotation Failure | vulnerability | unverified | not_tested | — |
| 84 | OAuth Account Takeover | vulnerability | unverified | not_tested | — |
| 85 | OAuth Redirect URI Manipulation | vulnerability | unverified | not_tested | — |
| 86 | OAuth State Parameter CSRF | vulnerability | unverified | not_tested | — |
| 87 | OAuth PKCE Bypass | vulnerability | unverified | not_tested | — |
| 88 | OAuth Token Leakage | vulnerability | unverified | not_tested | — |
| 89 | OAuth Scope Escalation | vulnerability | unverified | not_tested | — |
| 90 | OpenID Connect Misconfiguration | vulnerability | unverified | not_tested | — |
| 91 | SAML Signature Validation Bypass | vulnerability | unverified | not_tested | — |
| 92 | SAML XML Signature Wrapping | vulnerability | unverified | not_tested | — |
| 93 | SSO Authentication Bypass | vulnerability | unverified | not_tested | — |
| 94 | Social Login Account Linking Abuse | vulnerability | unverified | not_tested | — |
| 95 | Insecure Account Linking | vulnerability | unverified | not_tested | — |

## Authorization & Access Control

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 96 | Broken Access Control | vulnerability | unverified | not_tested | — |
| 97 | IDOR | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 98 | BOLA | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 99 | BFLA | vulnerability | unverified | not_tested | — |
| 100 | Horizontal Privilege Escalation | vulnerability | unverified | not_tested | — |
| 101 | Vertical Privilege Escalation | vulnerability | unverified | not_tested | — |
| 102 | Role Escalation | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 103 | Privilege Escalation Through Mass Assignment | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 104 | Missing Function-Level Authorization | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 105 | Missing Object-Level Authorization | vulnerability | unverified | not_tested | — |
| 106 | Missing Property-Level Authorization | vulnerability | unverified | not_tested | — |
| 107 | Insecure Direct Object Reference | vulnerability | unverified | not_tested | — |
| 108 | Admin Endpoint Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 109 | Admin Panel Authorization Bypass | vulnerability | unverified | not_tested | — |
| 110 | Tenant Isolation Bypass | vulnerability | unverified | not_tested | — |
| 111 | Cross-Tenant Data Access | vulnerability | unverified | not_tested | — |
| 112 | User Data Access Violation | vulnerability | unverified | not_tested | — |
| 113 | Unauthorized Order Access | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 114 | Unauthorized Invoice Access | vulnerability | unverified | not_tested | — |
| 115 | Unauthorized Payment Access | vulnerability | unverified | not_tested | — |
| 116 | Unauthorized Address Access | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 117 | Unauthorized File Access | vulnerability | unverified | not_tested | — |
| 118 | Unauthorized Refund | vulnerability | unverified | not_tested | — |
| 119 | Unauthorized Coupon Management | vulnerability | unverified | not_tested | — |
| 120 | Unauthorized Inventory Modification | vulnerability | unverified | not_tested | — |
| 121 | Unauthorized Role Modification | vulnerability | unverified | not_tested | — |
| 122 | Unauthorized User Management | vulnerability | unverified | not_tested | — |
| 123 | Forced Browsing | vulnerability | unverified | not_tested | — |
| 124 | Parameter-Based Authorization Bypass | vulnerability | unverified | not_tested | — |
| 125 | HTTP Method-Based Authorization Bypass | vulnerability | unverified | not_tested | — |
| 126 | Inconsistent Authorization Across APIs | vulnerability | unverified | not_tested | — |
| 127 | Insecure Resource Ownership Validation | vulnerability | unverified | not_tested | — |

## Injection Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 128 | SQL Injection | vulnerability | unverified | not_tested | — |
| 129 | Blind SQL Injection | vulnerability | unverified | not_tested | — |
| 130 | Boolean-Based SQL Injection | vulnerability | unverified | not_tested | — |
| 131 | Time-Based SQL Injection | vulnerability | unverified | not_tested | — |
| 132 | Error-Based SQL Injection | vulnerability | unverified | not_tested | — |
| 133 | Union-Based SQL Injection | vulnerability | unverified | not_tested | — |
| 134 | Second-Order SQL Injection | vulnerability | unverified | not_tested | — |
| 135 | Stored Procedure Injection | vulnerability | unverified | not_tested | — |
| 136 | NoSQL Injection | vulnerability | unverified | not_tested | — |
| 137 | MongoDB Operator Injection | vulnerability | unverified | not_tested | — |
| 138 | GraphQL Injection | vulnerability | unverified | not_tested | — |
| 139 | LDAP Injection | vulnerability | unverified | not_tested | — |
| 140 | XPath Injection | vulnerability | unverified | not_tested | — |
| 141 | XML Injection | vulnerability | unverified | not_tested | — |
| 142 | XXE | vulnerability | unverified | not_tested | — |
| 143 | Blind XXE | vulnerability | unverified | not_tested | — |
| 144 | SSRF Through XML | vulnerability | unverified | not_tested | — |
| 145 | OS Command Injection | vulnerability | unverified | not_tested | — |
| 146 | Blind OS Command Injection | vulnerability | unverified | not_tested | — |
| 147 | Argument Injection | vulnerability | unverified | not_tested | — |
| 148 | Code Injection | vulnerability | unverified | not_tested | — |
| 149 | PHP Code Injection | vulnerability | unverified | not_tested | — |
| 150 | Java Expression Injection | vulnerability | unverified | not_tested | — |
| 151 | JavaScript Injection | vulnerability | unverified | not_tested | — |
| 152 | Python Code Injection | vulnerability | unverified | not_tested | — |
| 153 | Template Injection | vulnerability | unverified | not_tested | — |
| 154 | Server-Side Template Injection (SSTI) | vulnerability | unverified | not_tested | — |
| 155 | Client-Side Template Injection | vulnerability | unverified | not_tested | — |
| 156 | Expression Language Injection | vulnerability | unverified | not_tested | — |
| 157 | ORM Injection | vulnerability | unverified | not_tested | — |
| 158 | HQL Injection | vulnerability | unverified | not_tested | — |
| 159 | Header Injection | vulnerability | unverified | not_tested | — |
| 160 | CRLF Injection | vulnerability | unverified | not_tested | — |
| 161 | SMTP Injection | vulnerability | unverified | not_tested | — |
| 162 | IMAP Injection | vulnerability | unverified | not_tested | — |
| 163 | Redis Command Injection | vulnerability | unverified | not_tested | — |
| 164 | Elasticsearch Injection | vulnerability | unverified | not_tested | — |
| 165 | Search Query Injection | vulnerability | unverified | not_tested | — |
| 166 | JSON Injection | vulnerability | unverified | not_tested | — |
| 167 | YAML Deserialization Injection | vulnerability | unverified | not_tested | — |
| 168 | CSV Injection | vulnerability | unverified | not_tested | — |
| 169 | HTTP Parameter Pollution | vulnerability | unverified | not_tested | — |

## Cross-Site Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 170 | Reflected XSS | vulnerability | unverified | not_tested | — |
| 171 | Stored XSS | vulnerability | unverified | not_tested | — |
| 172 | DOM-Based XSS | vulnerability | unverified | not_tested | — |
| 173 | Blind XSS | vulnerability | unverified | not_tested | — |
| 174 | Mutation XSS | vulnerability | unverified | not_tested | — |
| 175 | Self-XSS | vulnerability | unverified | not_tested | — |
| 176 | Context-Specific XSS | vulnerability | unverified | not_tested | — |
| 177 | HTML Injection | vulnerability | unverified | not_tested | — |
| 178 | CSS Injection | vulnerability | unverified | not_tested | — |
| 179 | JavaScript Context Injection | vulnerability | unverified | not_tested | — |
| 180 | CSRF | vulnerability | unverified | not_tested | — |
| 181 | Login CSRF | vulnerability | unverified | not_tested | — |
| 182 | Logout CSRF | vulnerability | unverified | not_tested | — |
| 183 | Stored CSRF | vulnerability | unverified | not_tested | — |
| 184 | SameSite Cookie Misconfiguration | vulnerability | unverified | not_tested | — |
| 185 | Clickjacking | vulnerability | unverified | not_tested | — |
| 186 | UI Redressing | vulnerability | unverified | not_tested | — |
| 187 | CORS Misconfiguration | vulnerability | unverified | not_tested | — |
| 188 | CORS Origin Reflection | vulnerability | unverified | not_tested | — |
| 189 | CORS Credential Exposure | vulnerability | unverified | not_tested | — |
| 190 | CSP Misconfiguration | vulnerability | unverified | not_tested | — |
| 191 | CSP Bypass | vulnerability | unverified | not_tested | — |
| 192 | PostMessage Origin Validation Bypass | vulnerability | unverified | not_tested | — |
| 193 | Cross-Origin Data Leakage | vulnerability | unverified | not_tested | — |
| 194 | XS-Leaks | vulnerability | unverified | not_tested | — |
| 195 | DOM Clobbering | vulnerability | unverified | not_tested | — |
| 196 | Open Redirect | vulnerability | unverified | not_tested | — |
| 197 | Tabnabbing | vulnerability | unverified | not_tested | — |

## Server-Side Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 198 | SSRF | vulnerability | unverified | not_tested | — |
| 199 | Blind SSRF | vulnerability | unverified | not_tested | — |
| 200 | SSRF to Internal Services | vulnerability | unverified | not_tested | — |
| 201 | SSRF to Cloud Metadata | vulnerability | unverified | not_tested | — |
| 202 | SSRF Through Webhooks | vulnerability | unverified | not_tested | — |
| 203 | SSRF Through Image Processing | vulnerability | unverified | not_tested | — |
| 204 | SSRF Through PDF Generation | vulnerability | unverified | not_tested | — |
| 205 | SSRF Through URL Preview | vulnerability | unverified | not_tested | — |
| 206 | SSRF Through Import Functions | vulnerability | unverified | not_tested | — |
| 207 | Local File Inclusion (LFI) | vulnerability | unverified | not_tested | — |
| 208 | Remote File Inclusion (RFI) | vulnerability | unverified | not_tested | — |
| 209 | Path Traversal | vulnerability | unverified | not_tested | — |
| 210 | Directory Traversal | vulnerability | unverified | not_tested | — |
| 211 | Arbitrary File Read | vulnerability | unverified | not_tested | — |
| 212 | Arbitrary File Write | vulnerability | unverified | not_tested | — |
| 213 | Arbitrary File Deletion | vulnerability | unverified | not_tested | — |
| 214 | Remote Code Execution (RCE) | vulnerability | unverified | not_tested | — |
| 215 | Local Code Execution | vulnerability | unverified | not_tested | — |
| 216 | Unsafe Deserialization | vulnerability | unverified | not_tested | — |
| 217 | Insecure Object Deserialization | vulnerability | unverified | not_tested | — |
| 218 | Java Deserialization | vulnerability | unverified | not_tested | — |
| 219 | PHP Deserialization | vulnerability | unverified | not_tested | — |
| 220 | Python Pickle Deserialization | vulnerability | unverified | not_tested | — |
| 221 | Prototype Pollution | vulnerability | unverified | not_tested | — |
| 222 | Server-Side Prototype Pollution | vulnerability | unverified | not_tested | — |
| 223 | HTTP Request Smuggling | vulnerability | unverified | not_tested | — |
| 224 | HTTP Response Splitting | vulnerability | unverified | not_tested | — |
| 225 | Host Header Injection | vulnerability | unverified | not_tested | — |
| 226 | Host Header Poisoning | vulnerability | unverified | not_tested | — |
| 227 | Web Cache Poisoning | vulnerability | unverified | not_tested | — |
| 228 | Web Cache Deception | vulnerability | unverified | not_tested | — |
| 229 | DNS Rebinding | vulnerability | unverified | not_tested | — |
| 230 | Race Condition | vulnerability | unverified | not_tested | — |
| 231 | TOCTOU Vulnerability | vulnerability | unverified | not_tested | — |
| 232 | Integer Overflow | vulnerability | unverified | not_tested | — |
| 233 | Integer Underflow | vulnerability | unverified | not_tested | — |
| 234 | Buffer Overflow | vulnerability | unverified | not_tested | — |
| 235 | Memory Corruption | vulnerability | unverified | not_tested | — |
| 236 | Format String Vulnerability | vulnerability | unverified | not_tested | — |
| 237 | Resource Exhaustion | vulnerability | unverified | not_tested | — |
| 238 | Denial of Service (DoS) | vulnerability | unverified | not_tested | — |
| 239 | Regular Expression DoS (ReDoS) | vulnerability | unverified | not_tested | — |

## API Security Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 240 | API1 - Broken Object Level Authorization | vulnerability | unverified | not_tested | — |
| 241 | API2 - Broken Authentication | vulnerability | unverified | not_tested | — |
| 242 | API3 - Broken Object Property Level Authorization | vulnerability | unverified | not_tested | — |
| 243 | API4 - Unrestricted Resource Consumption | vulnerability | unverified | not_tested | — |
| 244 | API5 - Broken Function Level Authorization | vulnerability | unverified | not_tested | — |
| 245 | API6 - Unrestricted Access to Sensitive Business Flows | vulnerability | unverified | not_tested | — |
| 246 | API7 - Server Side Request Forgery | vulnerability | unverified | not_tested | — |
| 247 | API8 - Security Misconfiguration | vulnerability | unverified | not_tested | — |
| 248 | API9 - Improper Inventory Management | vulnerability | unverified | not_tested | — |
| 249 | API10 - Unsafe Consumption of APIs | vulnerability | unverified | not_tested | — |
| 250 | API Mass Assignment | vulnerability | unverified | not_tested | — |
| 251 | API Excessive Data Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 252 | API Parameter Tampering | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 253 | API Versioning Bypass | vulnerability | unverified | not_tested | — |
| 254 | API Authentication Inconsistency | vulnerability | unverified | not_tested | — |
| 255 | API Authorization Inconsistency | vulnerability | unverified | not_tested | — |
| 256 | API Rate Limit Bypass | vulnerability | unverified | not_tested | — |
| 257 | API Pagination Abuse | vulnerability | unverified | not_tested | — |
| 258 | API Filtering Bypass | vulnerability | unverified | not_tested | — |
| 259 | API Sorting Injection | vulnerability | unverified | not_tested | — |
| 260 | API GraphQL Introspection Abuse | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 261 | GraphQL Authorization Bypass | vulnerability | unverified | not_tested | — |
| 262 | GraphQL Field-Level Authorization Bypass | vulnerability | unverified | not_tested | — |
| 263 | GraphQL Alias-Based DoS | vulnerability | unverified | not_tested | — |
| 264 | GraphQL Query Depth Abuse | vulnerability | unverified | not_tested | — |
| 265 | GraphQL Query Complexity Abuse | vulnerability | unverified | not_tested | — |
| 266 | GraphQL Batching Abuse | vulnerability | unverified | not_tested | — |
| 267 | GraphQL Subscription Authorization Bypass | vulnerability | unverified | not_tested | — |
| 268 | GraphQL Federation Trust Abuse | vulnerability | unverified | not_tested | — |
| 269 | gRPC Authorization Bypass | vulnerability | unverified | not_tested | — |
| 270 | gRPC Reflection Exposure | vulnerability | unverified | not_tested | — |
| 271 | WebSocket Authentication Bypass | vulnerability | unverified | not_tested | — |
| 272 | WebSocket Authorization Bypass | vulnerability | unverified | not_tested | — |
| 273 | WebSocket Origin Validation Bypass | vulnerability | unverified | not_tested | — |
| 274 | WebSocket Message Injection | vulnerability | unverified | not_tested | — |
| 275 | WebSocket Replay | vulnerability | unverified | not_tested | — |
| 276 | WebSocket Resource Exhaustion | vulnerability | unverified | not_tested | — |
| 277 | Webhook Forgery | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 278 | Webhook Signature Validation Bypass | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 279 | Webhook Replay | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 280 | Webhook SSRF | vulnerability | unverified | not_tested | — |
| 281 | Webhook Secret Leakage | vulnerability | unverified | not_tested | — |
| 282 | Webhook Event Injection | vulnerability | unverified | not_tested | — |

## E-commerce Business Logic Vulnerabilities

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 283 | Product Price Manipulation | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 284 | Negative Price Manipulation | vulnerability | unverified | not_tested | — |
| 285 | Zero Price Manipulation | vulnerability | unverified | not_tested | — |
| 286 | Quantity Manipulation | vulnerability | unverified | not_tested | — |
| 287 | Negative Quantity Manipulation | vulnerability | unverified | not_tested | — |
| 288 | Cart Manipulation | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 289 | Cart Ownership Bypass | vulnerability | unverified | not_tested | — |
| 290 | Cart Price Desynchronization | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 291 | Cart Item Substitution | vulnerability | unverified | not_tested | — |
| 292 | Coupon Code Brute Force | vulnerability | unverified | not_tested | — |
| 293 | Coupon Enumeration | vulnerability | unverified | not_tested | — |
| 294 | Coupon Reuse | vulnerability | unverified | not_tested | — |
| 295 | Coupon Stacking Abuse | vulnerability | unverified | not_tested | — |
| 296 | Coupon Expiration Bypass | vulnerability | unverified | not_tested | — |
| 297 | Coupon Scope Bypass | vulnerability | unverified | not_tested | — |
| 298 | Discount Manipulation | vulnerability | unverified | not_tested | — |
| 299 | Promotion Abuse | vulnerability | unverified | not_tested | — |
| 300 | Flash Sale Race Condition | vulnerability | unverified | not_tested | — |
| 301 | Inventory Manipulation | vulnerability | unverified | not_tested | — |
| 302 | Negative Inventory | vulnerability | unverified | not_tested | — |
| 303 | Stock Reservation Bypass | vulnerability | unverified | not_tested | — |
| 304 | Overselling | vulnerability | unverified | not_tested | — |
| 305 | Concurrent Purchase Race Condition | vulnerability | unverified | not_tested | — |
| 306 | Checkout Bypass | vulnerability | unverified | not_tested | — |
| 307 | Payment Bypass | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 308 | Payment Status Manipulation | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 309 | Payment Amount Manipulation | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 310 | Payment Currency Manipulation | vulnerability | unverified | not_tested | — |
| 311 | Payment Callback Forgery | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 312 | Payment Webhook Forgery | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 313 | Payment Replay | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 314 | Duplicate Payment Processing | vulnerability | unverified | not_tested | — |
| 315 | Payment Idempotency Failure | vulnerability | unverified | not_tested | — |
| 316 | Refund Manipulation | vulnerability | unverified | not_tested | — |
| 317 | Unauthorized Refund | vulnerability | unverified | not_tested | — |
| 318 | Partial Refund Abuse | vulnerability | unverified | not_tested | — |
| 319 | Refund Race Condition | vulnerability | unverified | not_tested | — |
| 320 | Order Ownership Manipulation | vulnerability | unverified | not_tested | — |
| 321 | Order Status Manipulation | vulnerability | unverified | not_tested | — |
| 322 | Order Cancellation Abuse | vulnerability | unverified | not_tested | — |
| 323 | Order Reuse | vulnerability | unverified | not_tested | — |
| 324 | Shipping Fee Manipulation | vulnerability | unverified | not_tested | — |
| 325 | Shipping Address Manipulation | vulnerability | unverified | not_tested | — |
| 326 | Tax Calculation Manipulation | vulnerability | unverified | not_tested | — |
| 327 | Gift Card Enumeration | vulnerability | unverified | not_tested | — |
| 328 | Gift Card Balance Manipulation | vulnerability | unverified | not_tested | — |
| 329 | Loyalty Points Manipulation | vulnerability | unverified | not_tested | — |
| 330 | Affiliate Commission Manipulation | vulnerability | unverified | not_tested | — |
| 331 | Referral Abuse | vulnerability | unverified | not_tested | — |
| 332 | Review Manipulation | vulnerability | unverified | not_tested | — |
| 333 | Fake Review Injection | vulnerability | unverified | not_tested | — |
| 334 | Review Ownership Bypass | vulnerability | unverified | not_tested | — |
| 335 | Wishlist Authorization Bypass | vulnerability | unverified | not_tested | — |
| 336 | Subscription Billing Bypass | vulnerability | unverified | not_tested | — |
| 337 | Subscription Plan Manipulation | vulnerability | unverified | not_tested | — |
| 338 | Trial Period Abuse | vulnerability | unverified | not_tested | — |
| 339 | Return Policy Abuse | vulnerability | unverified | not_tested | — |
| 340 | Exchange Workflow Bypass | vulnerability | unverified | not_tested | — |
| 341 | Invoice Manipulation | vulnerability | unverified | not_tested | — |
| 342 | Business Workflow Bypass | vulnerability | unverified | not_tested | — |
| 343 | Time-of-Check to Time-of-Use Abuse | vulnerability | unverified | not_tested | — |
| 344 | State Machine Manipulation | vulnerability | unverified | not_tested | — |

## File Upload & File Processing

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 345 | Unrestricted File Upload | vulnerability | unverified | not_tested | — |
| 346 | Arbitrary File Upload | vulnerability | unverified | not_tested | — |
| 347 | Malicious MIME Type | vulnerability | unverified | not_tested | — |
| 348 | Extension Validation Bypass | vulnerability | unverified | not_tested | — |
| 349 | Double Extension Upload | vulnerability | unverified | not_tested | — |
| 350 | Null Byte Extension Bypass | vulnerability | unverified | not_tested | — |
| 351 | Polyglot File Upload | vulnerability | unverified | not_tested | — |
| 352 | SVG XSS | vulnerability | unverified | not_tested | — |
| 353 | HTML File XSS | vulnerability | unverified | not_tested | — |
| 354 | Image Processing RCE | vulnerability | unverified | not_tested | — |
| 355 | ImageMagick Vulnerability | vulnerability | unverified | not_tested | — |
| 356 | EXIF Metadata Leakage | vulnerability | unverified | not_tested | — |
| 357 | ZIP Slip | vulnerability | unverified | not_tested | — |
| 358 | Archive Extraction Traversal | vulnerability | unverified | not_tested | — |
| 359 | ZIP Bomb | vulnerability | unverified | not_tested | — |
| 360 | XML Bomb | vulnerability | unverified | not_tested | — |
| 361 | PDF Processing Vulnerability | vulnerability | unverified | not_tested | — |
| 362 | Office Document Macro Abuse | vulnerability | unverified | not_tested | — |
| 363 | Malicious File Preview | vulnerability | unverified | not_tested | — |
| 364 | Insecure File Download | vulnerability | unverified | not_tested | — |
| 365 | Insecure File Sharing | vulnerability | unverified | not_tested | — |
| 366 | Public File Storage Exposure | vulnerability | unverified | not_tested | — |
| 367 | File Access Control Bypass | vulnerability | unverified | not_tested | — |
| 368 | Temporary File Exposure | vulnerability | unverified | not_tested | — |
| 369 | Path Traversal Through File Names | vulnerability | unverified | not_tested | — |

## Cryptography & Data Protection

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 370 | Weak Cryptographic Algorithms | vulnerability | unverified | not_tested | — |
| 371 | Weak Hashing Algorithm | vulnerability | unverified | not_tested | — |
| 372 | MD5 Password Storage | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 373 | SHA1 Password Storage | vulnerability | unverified | not_tested | — |
| 374 | Weak Password Hashing | vulnerability | unverified | not_tested | — |
| 375 | Hardcoded Encryption Keys | vulnerability | unverified | not_tested | — |
| 376 | Hardcoded Secrets | vulnerability | unverified | not_tested | — |
| 377 | Weak Random Number Generator | vulnerability | unverified | not_tested | — |
| 378 | Predictable Token Generation | vulnerability | unverified | not_tested | — |
| 379 | Weak Encryption | vulnerability | unverified | not_tested | — |
| 380 | Improper Encryption Mode | vulnerability | unverified | not_tested | — |
| 381 | ECB Mode Usage | vulnerability | unverified | not_tested | — |
| 382 | IV Reuse | vulnerability | unverified | not_tested | — |
| 383 | Nonce Reuse | vulnerability | unverified | not_tested | — |
| 384 | Padding Oracle | vulnerability | unverified | not_tested | — |
| 385 | Timing Attack | vulnerability | unverified | not_tested | — |
| 386 | Insecure Key Management | vulnerability | unverified | not_tested | — |
| 387 | Private Key Exposure | vulnerability | unverified | not_tested | — |
| 388 | Certificate Validation Bypass | vulnerability | unverified | not_tested | — |
| 389 | TLS Misconfiguration | vulnerability | unverified | not_tested | — |
| 390 | Weak TLS Protocol | vulnerability | unverified | not_tested | — |
| 391 | Weak Cipher Suites | vulnerability | unverified | not_tested | — |
| 392 | Missing HSTS | vulnerability | unverified | not_tested | — |
| 393 | Sensitive Data in URL | vulnerability | unverified | not_tested | — |
| 394 | Sensitive Data in Logs | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 395 | Sensitive Data in Browser Storage | vulnerability | unverified | not_tested | — |
| 396 | Sensitive Data in Cache | vulnerability | unverified | not_tested | — |
| 397 | PII Exposure | vulnerability | unverified | not_tested | — |
| 398 | Insecure Data Retention | vulnerability | unverified | not_tested | — |
| 399 | Missing Data Encryption at Rest | vulnerability | unverified | not_tested | — |
| 400 | Missing Data Encryption in Transit | vulnerability | unverified | not_tested | — |

## Database Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 401 | Database Public Exposure | vulnerability | unverified | not_tested | — |
| 402 | Database Default Credentials | vulnerability | unverified | not_tested | — |
| 403 | Weak Database Authentication | vulnerability | unverified | not_tested | — |
| 404 | Database Privilege Escalation | vulnerability | unverified | not_tested | — |
| 405 | Excessive Database Permissions | vulnerability | unverified | not_tested | — |
| 406 | Database SQL Injection | vulnerability | unverified | not_tested | — |
| 407 | Database NoSQL Injection | vulnerability | unverified | not_tested | — |
| 408 | Database Command Injection | vulnerability | unverified | not_tested | — |
| 409 | Database Information Disclosure | vulnerability | unverified | not_tested | — |
| 410 | Database Backup Exposure | vulnerability | unverified | not_tested | — |
| 411 | Database Snapshot Exposure | vulnerability | unverified | not_tested | — |
| 412 | Database Replication Exposure | vulnerability | unverified | not_tested | — |
| 413 | Database Misconfiguration | vulnerability | unverified | not_tested | — |
| 414 | Database Audit Log Disabled | vulnerability | unverified | not_tested | — |
| 415 | Database Encryption Disabled | vulnerability | unverified | not_tested | — |
| 416 | Database Connection String Exposure | vulnerability | unverified | not_tested | — |
| 417 | Database Credential Leakage | vulnerability | unverified | not_tested | — |
| 418 | Database DoS | vulnerability | unverified | not_tested | — |
| 419 | Database Resource Exhaustion | vulnerability | unverified | not_tested | — |
| 420 | Cross-Tenant Database Access | vulnerability | unverified | not_tested | — |
| 421 | Row-Level Security Bypass | vulnerability | unverified | not_tested | — |
| 422 | Database Migration Security Flaws | vulnerability | unverified | not_tested | — |
| 423 | Unsafe Stored Procedures | vulnerability | unverified | not_tested | — |
| 424 | Redis Unauthorized Access | vulnerability | unverified | not_tested | — |
| 425 | MongoDB Unauthorized Access | vulnerability | unverified | not_tested | — |
| 426 | Elasticsearch Unauthorized Access | vulnerability | unverified | not_tested | — |
| 427 | Neo4j Unauthorized Access | vulnerability | unverified | not_tested | — |
| 428 | Graph Database Query Injection | vulnerability | unverified | not_tested | — |

## Cloud Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 429 | Public Cloud Storage Bucket | vulnerability | unverified | not_tested | — |
| 430 | Cloud IAM Misconfiguration | vulnerability | unverified | not_tested | — |
| 431 | Excessive Cloud Permissions | vulnerability | unverified | not_tested | — |
| 432 | Cloud Privilege Escalation | vulnerability | unverified | not_tested | — |
| 433 | Cloud Metadata SSRF | vulnerability | unverified | not_tested | — |
| 434 | Cloud Credential Exposure | vulnerability | unverified | not_tested | — |
| 435 | Cloud Access Key Leakage | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 436 | Cloud Secret Exposure | vulnerability | unverified | not_tested | — |
| 437 | Cloud Storage ACL Misconfiguration | vulnerability | unverified | not_tested | — |
| 438 | Cloud Snapshot Exposure | vulnerability | unverified | not_tested | — |
| 439 | Cloud Backup Exposure | vulnerability | unverified | not_tested | — |
| 440 | Cloud Database Public Exposure | vulnerability | unverified | not_tested | — |
| 441 | Cloud Network Security Group Misconfiguration | vulnerability | unverified | not_tested | — |
| 442 | Cloud Firewall Misconfiguration | vulnerability | unverified | not_tested | — |
| 443 | Cloud Logging Disabled | vulnerability | unverified | not_tested | — |
| 444 | Cloud Audit Trail Disabled | vulnerability | unverified | not_tested | — |
| 445 | Cloud KMS Misconfiguration | vulnerability | unverified | not_tested | — |
| 446 | Cloud Encryption Misconfiguration | vulnerability | unverified | not_tested | — |
| 447 | Cloud Function Misconfiguration | vulnerability | unverified | not_tested | — |
| 448 | Serverless Function Authorization Bypass | vulnerability | unverified | not_tested | — |
| 449 | Serverless Event Injection | vulnerability | unverified | not_tested | — |
| 450 | Serverless Secret Exposure | vulnerability | unverified | not_tested | — |
| 451 | Cross-Account Access | vulnerability | unverified | not_tested | — |
| 452 | Cross-Region Data Exposure | vulnerability | unverified | not_tested | — |
| 453 | Container Registry Exposure | vulnerability | unverified | not_tested | — |
| 454 | Public Artifact Repository | vulnerability | unverified | not_tested | — |
| 455 | Cloud Resource Enumeration | vulnerability | unverified | not_tested | — |
| 456 | Cloud Resource Takeover | vulnerability | unverified | not_tested | — |
| 457 | Insecure Cloud API | vulnerability | unverified | not_tested | — |

## Network & Infrastructure Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 458 | Open Ports | vulnerability | unverified | not_tested | — |
| 459 | Unnecessary Network Services | vulnerability | unverified | not_tested | — |
| 460 | Insecure Network Protocols | vulnerability | unverified | not_tested | — |
| 461 | Plaintext HTTP | vulnerability | unverified | not_tested | — |
| 462 | FTP Exposure | vulnerability | unverified | not_tested | — |
| 463 | Telnet Exposure | vulnerability | unverified | not_tested | — |
| 464 | SSH Weak Authentication | vulnerability | unverified | not_tested | — |
| 465 | SSH Weak Configuration | vulnerability | unverified | not_tested | — |
| 466 | SMB Exposure | vulnerability | unverified | not_tested | — |
| 467 | NFS Exposure | vulnerability | unverified | not_tested | — |
| 468 | SNMP Exposure | vulnerability | unverified | not_tested | — |
| 469 | Firewall Misconfiguration | vulnerability | unverified | not_tested | — |
| 470 | Network Segmentation Failure | vulnerability | unverified | not_tested | — |
| 471 | Internal Service Exposure | vulnerability | unverified | not_tested | — |
| 472 | Internal Network Access | vulnerability | unverified | not_tested | — |
| 473 | VPN Misconfiguration | vulnerability | unverified | not_tested | — |
| 474 | Reverse Proxy Misconfiguration | vulnerability | unverified | not_tested | — |
| 475 | Load Balancer Misconfiguration | vulnerability | unverified | not_tested | — |
| 476 | API Gateway Misconfiguration | vulnerability | unverified | not_tested | — |
| 477 | TLS Certificate Expiration | vulnerability | unverified | not_tested | — |
| 478 | Certificate Hostname Mismatch | vulnerability | unverified | not_tested | — |
| 479 | Certificate Chain Validation Failure | vulnerability | unverified | not_tested | — |
| 480 | HTTP Security Header Misconfiguration | vulnerability | unverified | not_tested | — |
| 481 | HTTP/2 Misconfiguration | vulnerability | unverified | not_tested | — |
| 482 | HTTP/3 Misconfiguration | vulnerability | unverified | not_tested | — |
| 483 | QUIC Misconfiguration | vulnerability | unverified | not_tested | — |
| 484 | IPv6 Security Misconfiguration | vulnerability | unverified | not_tested | — |
| 485 | IP Spoofing Trust Issues | vulnerability | unverified | not_tested | — |
| 486 | Proxy Trust Misconfiguration | vulnerability | unverified | not_tested | — |
| 487 | Rate Limiting Misconfiguration | vulnerability | unverified | not_tested | — |
| 488 | Network DoS | vulnerability | unverified | not_tested | — |
| 489 | DNS Cache Poisoning | vulnerability | unverified | not_tested | — |
| 490 | ARP Spoofing Exposure | vulnerability | unverified | not_tested | — |

## Docker & Container Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 491 | Privileged Container | vulnerability | unverified | not_tested | — |
| 492 | Container Running as Root | vulnerability | unverified | not_tested | — |
| 493 | Docker Socket Exposure | vulnerability | unverified | not_tested | — |
| 494 | Container Escape | vulnerability | unverified | not_tested | — |
| 495 | Host Filesystem Mount Exposure | vulnerability | unverified | not_tested | — |
| 496 | Sensitive Environment Variable Exposure | vulnerability | unverified | not_tested | — |
| 497 | Container Capability Misconfiguration | vulnerability | unverified | not_tested | — |
| 498 | Insecure Container Image | vulnerability | unverified | not_tested | — |
| 499 | Vulnerable Base Image | vulnerability | unverified | not_tested | — |
| 500 | Untrusted Image Usage | vulnerability | unverified | not_tested | — |
| 501 | Image Signature Validation Missing | vulnerability | unverified | not_tested | — |
| 502 | Container Registry Exposure | vulnerability | unverified | not_tested | — |
| 503 | Docker API Unauthorized Access | vulnerability | unverified | not_tested | — |
| 504 | Container Network Misconfiguration | vulnerability | unverified | not_tested | — |
| 505 | Container Secret Exposure | vulnerability | unverified | not_tested | — |
| 506 | Container Resource Limit Missing | vulnerability | unverified | not_tested | — |
| 507 | Container Runtime Vulnerability | vulnerability | unverified | not_tested | — |
| 508 | Insecure Docker Compose Configuration | vulnerability | unverified | not_tested | — |
| 509 | Container Log Sensitive Data Exposure | vulnerability | unverified | not_tested | — |
| 510 | Container Supply Chain Vulnerability | vulnerability | unverified | not_tested | — |

## Kubernetes Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 511 | Kubernetes API Server Exposure | vulnerability | unverified | not_tested | — |
| 512 | Kubernetes Dashboard Exposure | vulnerability | unverified | not_tested | — |
| 513 | Anonymous API Access | vulnerability | unverified | not_tested | — |
| 514 | RBAC Misconfiguration | vulnerability | unverified | not_tested | — |
| 515 | Excessive Service Account Permissions | vulnerability | unverified | not_tested | — |
| 516 | Service Account Token Exposure | vulnerability | unverified | not_tested | — |
| 517 | Pod Privilege Escalation | vulnerability | unverified | not_tested | — |
| 518 | Privileged Pod | vulnerability | unverified | not_tested | — |
| 519 | HostPath Mount Exposure | vulnerability | unverified | not_tested | — |
| 520 | HostNetwork Misconfiguration | vulnerability | unverified | not_tested | — |
| 521 | HostPID Misconfiguration | vulnerability | unverified | not_tested | — |
| 522 | Container Escape | vulnerability | unverified | not_tested | — |
| 523 | Insecure Network Policies | vulnerability | unverified | not_tested | — |
| 524 | Namespace Isolation Failure | vulnerability | unverified | not_tested | — |
| 525 | Secrets Exposure | vulnerability | unverified | not_tested | — |
| 526 | ConfigMap Sensitive Data Exposure | vulnerability | unverified | not_tested | — |
| 527 | etcd Unauthorized Access | vulnerability | unverified | not_tested | — |
| 528 | Admission Controller Misconfiguration | vulnerability | unverified | not_tested | — |
| 529 | Insecure Ingress Configuration | vulnerability | unverified | not_tested | — |
| 530 | Kubernetes Audit Logging Disabled | vulnerability | unverified | not_tested | — |
| 531 | Resource Quota Missing | vulnerability | unverified | not_tested | — |
| 532 | Kubernetes Supply Chain Vulnerability | vulnerability | unverified | not_tested | — |

## CI/CD & Supply Chain Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 533 | Git Repository Secret Exposure | vulnerability | unverified | not_tested | — |
| 534 | Hardcoded Credentials | vulnerability | unverified | not_tested | — |
| 535 | CI/CD Secret Leakage | vulnerability | unverified | not_tested | — |
| 536 | Pipeline Permission Misconfiguration | vulnerability | unverified | not_tested | — |
| 537 | Pipeline Injection | vulnerability | unverified | not_tested | — |
| 538 | Build Script Injection | vulnerability | unverified | not_tested | — |
| 539 | Dependency Confusion | vulnerability | unverified | not_tested | — |
| 540 | Dependency Hijacking | vulnerability | unverified | not_tested | — |
| 541 | Typosquatting | vulnerability | unverified | not_tested | — |
| 542 | Malicious Package Installation | vulnerability | unverified | not_tested | — |
| 543 | Vulnerable Dependencies | vulnerability | observed | verified | [docs/dependency-audit.md](docs/dependency-audit.md) |
| 544 | Outdated Dependencies | vulnerability | observed | verified | [docs/dependency-audit.md](docs/dependency-audit.md) |
| 545 | Insecure Package Registry | vulnerability | unverified | not_tested | — |
| 546 | Artifact Tampering | vulnerability | unverified | not_tested | — |
| 547 | Build Artifact Exposure | vulnerability | unverified | not_tested | — |
| 548 | Insecure Deployment Credentials | vulnerability | unverified | not_tested | — |
| 549 | Unprotected Deployment Branch | vulnerability | unverified | not_tested | — |
| 550 | Pull Request Workflow Abuse | vulnerability | unverified | not_tested | — |
| 551 | Insecure GitHub Actions | vulnerability | unverified | not_tested | — |
| 552 | Insecure GitLab CI | vulnerability | unverified | not_tested | — |
| 553 | Software Bill of Materials Missing | vulnerability | unverified | not_tested | — |
| 554 | Missing Dependency Integrity Verification | vulnerability | unverified | not_tested | — |
| 555 | Unsigned Container Images | vulnerability | unverified | not_tested | — |
| 556 | Compromised Build Pipeline | vulnerability | unverified | not_tested | — |

## Logging, Monitoring & Operational Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 557 | Sensitive Data Logging | vulnerability | unverified | not_tested | — |
| 558 | Password Logging | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 559 | Token Logging | vulnerability | unverified | not_tested | — |
| 560 | PII Logging | vulnerability | unverified | not_tested | — |
| 561 | Log Injection | vulnerability | unverified | not_tested | — |
| 562 | CRLF Log Injection | vulnerability | unverified | not_tested | — |
| 563 | Audit Log Tampering | vulnerability | unverified | not_tested | — |
| 564 | Audit Log Deletion | vulnerability | unverified | not_tested | — |
| 565 | Missing Security Audit Trail | vulnerability | unverified | not_tested | — |
| 566 | Missing Authentication Monitoring | vulnerability | unverified | not_tested | — |
| 567 | Missing Authorization Monitoring | vulnerability | unverified | not_tested | — |
| 568 | Missing Alerting | vulnerability | unverified | not_tested | — |
| 569 | Monitoring Dashboard Exposure | vulnerability | unverified | not_tested | — |
| 570 | Metrics Endpoint Exposure | vulnerability | unverified | not_tested | — |
| 571 | Debug Endpoint Exposure | vulnerability | unverified | not_tested | — |
| 572 | Health Check Information Leakage | vulnerability | unverified | not_tested | — |
| 573 | Trace Data Exposure | vulnerability | unverified | not_tested | — |
| 574 | Distributed Tracing Data Leakage | vulnerability | unverified | not_tested | — |
| 575 | Error Tracking Data Leakage | vulnerability | unverified | not_tested | — |
| 576 | Backup Data Exposure | vulnerability | unverified | not_tested | — |
| 577 | Disaster Recovery Misconfiguration | vulnerability | unverified | not_tested | — |
| 578 | Insecure Log Storage | vulnerability | unverified | not_tested | — |
| 579 | Log Retention Misconfiguration | vulnerability | unverified | not_tested | — |
| 580 | Monitoring Access Control Bypass | vulnerability | unverified | not_tested | — |

## DoS & Resource Exhaustion

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 581 | HTTP Flood | vulnerability | unverified | not_tested | — |
| 582 | Slow HTTP Attack | vulnerability | unverified | not_tested | — |
| 583 | Slowloris | vulnerability | unverified | not_tested | — |
| 584 | Application Layer DoS | vulnerability | unverified | not_tested | — |
| 585 | API Resource Exhaustion | vulnerability | unverified | not_tested | — |
| 586 | GraphQL Query DoS | vulnerability | unverified | not_tested | — |
| 587 | Regex DoS | vulnerability | unverified | not_tested | — |
| 588 | Large Payload DoS | vulnerability | unverified | not_tested | — |
| 589 | File Upload DoS | vulnerability | unverified | not_tested | — |
| 590 | Image Processing DoS | vulnerability | unverified | not_tested | — |
| 591 | PDF Processing DoS | vulnerability | unverified | not_tested | — |
| 592 | ZIP Bomb DoS | vulnerability | unverified | not_tested | — |
| 593 | Database Query DoS | vulnerability | unverified | not_tested | — |
| 594 | Connection Pool Exhaustion | vulnerability | unverified | not_tested | — |
| 595 | Thread Pool Exhaustion | vulnerability | unverified | not_tested | — |
| 596 | Memory Exhaustion | vulnerability | unverified | not_tested | — |
| 597 | CPU Exhaustion | vulnerability | unverified | not_tested | — |
| 598 | Queue Flooding | vulnerability | unverified | not_tested | — |
| 599 | Message Queue Poisoning | vulnerability | unverified | not_tested | — |
| 600 | WebSocket Connection Exhaustion | vulnerability | unverified | not_tested | — |
| 601 | Rate Limit Bypass | vulnerability | unverified | not_tested | — |
| 602 | Cache Exhaustion | vulnerability | unverified | not_tested | — |
| 603 | Unbounded Pagination | vulnerability | unverified | not_tested | — |
| 604 | Unbounded Search Query | vulnerability | unverified | not_tested | — |

## Frontend & Client-Side Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 605 | DOM-Based XSS | vulnerability | unverified | not_tested | — |
| 606 | Client-Side Validation Bypass | vulnerability | unverified | not_tested | — |
| 607 | Sensitive Data in JavaScript | vulnerability | unverified | not_tested | — |
| 608 | Hardcoded API Keys | vulnerability | unverified | not_tested | — |
| 609 | Exposed Source Maps | vulnerability | unverified | not_tested | — |
| 610 | Insecure LocalStorage | vulnerability | unverified | not_tested | — |
| 611 | Insecure SessionStorage | vulnerability | unverified | not_tested | — |
| 612 | IndexedDB Data Exposure | vulnerability | unverified | not_tested | — |
| 613 | Insecure Cookie Configuration | vulnerability | unverified | not_tested | — |
| 614 | Service Worker Cache Poisoning | vulnerability | unverified | not_tested | — |
| 615 | Service Worker Scope Abuse | vulnerability | unverified | not_tested | — |
| 616 | PostMessage Vulnerability | vulnerability | unverified | not_tested | — |
| 617 | Third-Party JavaScript Risk | vulnerability | unverified | not_tested | — |
| 618 | JavaScript Dependency Vulnerability | vulnerability | observed | verified | [docs/dependency-audit.md](docs/dependency-audit.md) |
| 619 | Prototype Pollution | vulnerability | unverified | not_tested | — |
| 620 | Client-Side Access Control | vulnerability | unverified | not_tested | — |
| 621 | Hidden UI Authorization | vulnerability | unverified | not_tested | — |
| 622 | Payment Data Exposure | vulnerability | unverified | not_tested | — |
| 623 | Browser Cache Sensitive Data Exposure | vulnerability | unverified | not_tested | — |
| 624 | DOM Clobbering | vulnerability | unverified | not_tested | — |
| 625 | Clickjacking | vulnerability | unverified | not_tested | — |
| 626 | Tabnabbing | vulnerability | unverified | not_tested | — |
| 627 | Client-Side Open Redirect | vulnerability | unverified | not_tested | — |

## Third-Party Integration Security

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 628 | Insecure Third-Party API Consumption | vulnerability | unverified | not_tested | — |
| 629 | Third-Party API Authentication Bypass | vulnerability | unverified | not_tested | — |
| 630 | Third-Party API Token Leakage | vulnerability | unverified | not_tested | — |
| 631 | Payment Provider Integration Flaws | vulnerability | unverified | not_tested | — |
| 632 | Shipping Provider Integration Flaws | vulnerability | unverified | not_tested | — |
| 633 | OAuth Provider Misconfiguration | vulnerability | unverified | not_tested | — |
| 634 | Email Service Credential Exposure | vulnerability | unverified | not_tested | — |
| 635 | SMTP Injection | vulnerability | unverified | not_tested | — |
| 636 | SMS OTP Abuse | vulnerability | unverified | not_tested | — |
| 637 | CAPTCHA Provider Bypass | vulnerability | unverified | not_tested | — |
| 638 | Webhook Trust Validation Failure | vulnerability | unverified | not_tested | — |
| 639 | Third-Party Data Injection | vulnerability | unverified | not_tested | — |
| 640 | Third-Party Response Deserialization | vulnerability | unverified | not_tested | — |
| 641 | Insecure API Response Validation | vulnerability | unverified | not_tested | — |
| 642 | Third-Party Dependency Compromise | vulnerability | unverified | not_tested | — |

## Business Data & Privacy

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 643 | Customer PII Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 644 | Customer Address Exposure | vulnerability | unverified | not_tested | — |
| 645 | Customer Phone Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 646 | Customer Email Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 647 | Order History Exposure | vulnerability | unverified | not_tested | — |
| 648 | Payment Information Exposure | vulnerability | unverified | not_tested | — |
| 649 | Invoice Exposure | vulnerability | unverified | not_tested | — |
| 650 | Admin Data Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 651 | Internal Business Data Exposure | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 652 | Cross-Customer Data Leakage | vulnerability | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 653 | Cross-Tenant Data Leakage | vulnerability | unverified | not_tested | — |
| 654 | Data Retention Violation | vulnerability | unverified | not_tested | — |
| 655 | Data Deletion Failure | vulnerability | unverified | not_tested | — |
| 656 | Account Deletion Bypass | vulnerability | unverified | not_tested | — |
| 657 | Personal Data Export Authorization Bypass | vulnerability | unverified | not_tested | — |
| 658 | Privacy Settings Bypass | vulnerability | unverified | not_tested | — |
| 659 | Consent Management Bypass | vulnerability | unverified | not_tested | — |
| 660 | Sensitive Data in Analytics | vulnerability | unverified | not_tested | — |
| 661 | Sensitive Data in Third-Party Services | vulnerability | unverified | not_tested | — |

## Các chuỗi khai thác Attack Chain

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 662 | Reconnaissance → Information Disclosure → Credential Discovery → Account Takeover | attack_chain | unverified | not_tested | — |
| 663 | XSS → Session Theft → Account Takeover | attack_chain | unverified | not_tested | — |
| 664 | CSRF → Privileged Action → Account Compromise | attack_chain | unverified | not_tested | — |
| 665 | IDOR → PII Disclosure → Account Targeting | attack_chain | unverified | not_tested | — |
| 666 | SSRF → Cloud Metadata → IAM Credentials → Cloud Access | attack_chain | unverified | not_tested | — |
| 667 | SQL Injection → Database Access → Data Exfiltration | attack_chain | unverified | not_tested | — |
| 668 | SQL Injection → Privilege Escalation → RCE | attack_chain | unverified | not_tested | — |
| 669 | File Upload → File Execution → RCE | attack_chain | unverified | not_tested | — |
| 670 | Path Traversal → Configuration Disclosure → Credential Theft | attack_chain | unverified | not_tested | — |
| 671 | XXE → Local File Read → Credential Exposure | attack_chain | unverified | not_tested | — |
| 672 | SSTI → Server-Side Code Execution | attack_chain | unverified | not_tested | — |
| 673 | JWT Forgery → Authorization Bypass → Privilege Escalation | attack_chain | unverified | not_tested | — |
| 674 | OAuth Misconfiguration → Account Linking Abuse → Account Takeover | attack_chain | unverified | not_tested | — |
| 675 | API BOLA → Cross-Customer Data Access → Data Exfiltration | attack_chain | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 676 | GraphQL Introspection → Sensitive Field Discovery → Authorization Bypass | attack_chain | unverified | not_tested | — |
| 677 | Webhook SSRF → Internal Service Access | attack_chain | unverified | not_tested | — |
| 678 | Payment Callback Forgery → Fake Payment → Order Fraud | attack_chain | observed | verified | [docs/smoke-findings.md](docs/smoke-findings.md) |
| 679 | Coupon Abuse → Price Manipulation → Financial Loss | attack_chain | unverified | not_tested | — |
| 680 | Race Condition → Overselling → Inventory Inconsistency | attack_chain | unverified | not_tested | — |
| 681 | Refund Abuse → Unauthorized Financial Transaction | attack_chain | unverified | not_tested | — |
| 682 | Container Misconfiguration → Container Escape → Host Access | attack_chain | unverified | not_tested | — |
| 683 | Kubernetes RBAC Abuse → Cluster Privilege Escalation | attack_chain | unverified | not_tested | — |
| 684 | CI/CD Secret Exposure → Pipeline Compromise → Production Access | attack_chain | unverified | not_tested | — |
| 685 | Dependency Compromise → Supply Chain Attack → RCE | attack_chain | unverified | not_tested | — |
| 686 | Cloud Storage Exposure → Sensitive Data Exfiltration | attack_chain | unverified | not_tested | — |
| 687 | Admin Panel Exposure → Credential Compromise → Full Application Access | attack_chain | unverified | not_tested | — |
| 688 | Weak Network Segmentation → Internal Service Compromise | attack_chain | unverified | not_tested | — |
| 689 | Redis Exposure → Data Manipulation → Application Compromise | attack_chain | unverified | not_tested | — |
| 690 | Database Credential Leakage → Database Compromise → Customer Data Exfiltration | attack_chain | unverified | not_tested | — |

## Ma trận kiểm thử và dữ liệu phục vụ Agent

| ID | Name | Type | Implementation | Test | Evidence |
|---:|---|---|---|---|---|
| 691 | Vulnerability ID | test_matrix_field | schema_field | not_applicable | — |
| 692 | Vulnerability Name | test_matrix_field | schema_field | not_applicable | — |
| 693 | Vulnerability Category | test_matrix_field | schema_field | not_applicable | — |
| 694 | CWE Mapping | test_matrix_field | schema_field | not_applicable | — |
| 695 | OWASP Mapping | test_matrix_field | schema_field | not_applicable | — |
| 696 | WSTG Mapping | test_matrix_field | schema_field | not_applicable | — |
| 697 | OWASP API Top 10 Mapping | test_matrix_field | schema_field | not_applicable | — |
| 698 | CVSS v4.0 Scoring | test_matrix_field | schema_field | not_applicable | — |
| 699 | Severity Classification | test_matrix_field | schema_field | not_applicable | — |
| 700 | Affected Component | test_matrix_field | schema_field | not_applicable | — |
| 701 | Affected Endpoint | test_matrix_field | schema_field | not_applicable | — |
| 702 | HTTP Method | test_matrix_field | schema_field | not_applicable | — |
| 703 | Required Authentication | test_matrix_field | schema_field | not_applicable | — |
| 704 | Required User Role | test_matrix_field | schema_field | not_applicable | — |
| 705 | Test Account | test_matrix_field | schema_field | not_applicable | — |
| 706 | Test Credentials | test_matrix_field | schema_field | not_applicable | — |
| 707 | Test Data | test_matrix_field | schema_field | not_applicable | — |
| 708 | Preconditions | test_matrix_field | schema_field | not_applicable | — |
| 709 | Vulnerability Trigger | test_matrix_field | schema_field | not_applicable | — |
| 710 | Reproduction Steps | test_matrix_field | schema_field | not_applicable | — |
| 711 | Expected Vulnerable Behavior | test_matrix_field | schema_field | not_applicable | — |
| 712 | Expected Secure Behavior | test_matrix_field | schema_field | not_applicable | — |
| 713 | Proof of Concept | test_matrix_field | schema_field | not_applicable | — |
| 714 | Evidence Collection | test_matrix_field | schema_field | not_applicable | — |
| 715 | Detection Indicators | test_matrix_field | schema_field | not_applicable | — |
| 716 | False Positive Conditions | test_matrix_field | schema_field | not_applicable | — |
| 717 | Exploitation Impact | test_matrix_field | schema_field | not_applicable | — |
| 718 | Remediation Guidance | test_matrix_field | schema_field | not_applicable | — |
| 719 | Regression Test | test_matrix_field | schema_field | not_applicable | — |
| 720 | Automated Verification | test_matrix_field | schema_field | not_applicable | — |
| 721 | Manual Verification | test_matrix_field | schema_field | not_applicable | — |
| 722 | Attack Chain Mapping | test_matrix_field | schema_field | not_applicable | — |
| 723 | Vulnerability Dependencies | test_matrix_field | schema_field | not_applicable | — |
| 724 | Lab Reset Mechanism | test_matrix_field | schema_field | not_applicable | — |
| 725 | Test Isolation | test_matrix_field | schema_field | not_applicable | — |
| 726 | Vulnerability Enable/Disable Configuration | test_matrix_field | schema_field | not_applicable | — |
