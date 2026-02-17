## secure Authentication API

A production-grade Secure Authentication & Authorization API built with FastAPI, JWT, RBAC, Redis, and PostgreSQL.

This project focuses on API hardening, security boundaries, and DevSecOps automation.

-----
# Core Features 

## 1/ authentification 

- User Registration
- Login with JWT
- Access Token validation
- Refresh Token rotation
- Secure password hashing (bcrypt)

-----

## 2/Authorization

- Role-Based Access Control (RBAC)
- Permission-based access
- Protected routes
- Admin-only endpoints

-----

## 3/secure  api  

- Rate limiting (Redis sliding window)
- Login attempt monitoring
- Request tracking & IP monitoring
- Secure HTTP headers
- Strict CORS policy
- Input validation (Pydantic)
- Secure error handling (no sensitive leaks) 

-----

## Testing

- Unit tests for:
  - Authentication
  - Database connection
  - Redis connection
- API behavior validation
- Security behavior validation

----------

### the  tack  we use is  

- Backend: FastAPI (Python 3.12)
- Authentication: JWT
- Password Hashing: bcrypt
- Database: PostgreSQL 15+
- Cache / Rate Limiting: Redis
- Reverse Proxy: NGINX (optional)
- Containerization: Podman

-------
```

secure-auth-api/
├── app/
│   ├── main.py
│   ├── auth/
│   │   ├── oauth2.py       # JWT logic (create/decode)
│   │   └── hashing.py      # Bcrypt logic
│   ├── models/
│   │   └── config.py       # Pydantic Settings (ENV variables)
│   ├── routers/
│   │   ├── auth.py         # Login/Register routes
│   │   └── users.py        # RBAC protected routes
│   ├── middleware/
│   │   └── monitor.py      # IP tracking & Logging
│   ├── database/
│   │   ├── connection.py   # Engine & Session management
│   │   └── redis_cli.py    # Redis connection for rate limiting
|   └── security/
│       └── rbac.py         # Role-based access decorators
├── tests/
|   └── unit_conection_data.py        # Pytest logic
|   └── unit_conection_redis.py        # Pytest logic
|   └── test_auth.py        # Pytest logic
├── requirements.txt
└── README.md

```

-----

# 🏗 Architecture Overview

```

[ EXTERNAL NETWORK ]
                                         |
                                         | (HTTPS Request)
                                         v
                          +-----------------------------+
                          |      Reverse Proxy (NGINX)  |  <-- SSL Termination
                          |    (Secure Headers & CORS)  |      IP Filtering
                          +--------------+--------------+
                                         |
        _________________________|_________________________
       |                 [ FASTAPI APPLICATION ]           |
       |                                                   |
       |  1. [ MIDDLEWARE LAYER ]                          |
       |     +---------------------------------------+     |      +----------------+
       |     |  - IP Monitoring & Request Tracking   | <---|----> |  REDIS CACHE   |
       |     |  - Rate Limiter (Sliding Window)      |     |      | (Blocklists,   |
       |     |  - Secure Header Injection            |     |      |  Rate Limits)  |
       |     +-------------------+-------------------+     |      +----------------+
       |                         |                         |
       |  2. [ AUTHENTICATION LAYER ]                      |
       |     +---------------------------------------+     |      +----------------+
       |     |  - JWT Validation / Token Refresh     | <---|----> |  SECRET KEYS   |
       |     |  - Password Hashing (Bcrypt)          |     |      |  (.env Config) |
       |     +-------------------+-------------------+     |      +----------------+
       |                         |                         |
       |  3. [ AUTHORIZATION LAYER (RBAC) ]                |
       |     +---------------------------------------+     |
       |     |  - Role Verification (Admin/User)     |     |
       |     |  - Permission Scopes                  |     |
       |     +-------------------+-------------------+     |
       |                         |                         |
       |  4. [ BUSINESS LOGIC & DATA ]                     |      +----------------+
       |     +---------------------------------------+     |      |   POSTGRESQL   |
       |     |  - CRUD Operations                    | <---|----> | (Users, Roles, |
       |     |  - Input Validation (Pydantic)        |     |      |  Audit Logs)   |
       |     +---------------------------------------+     |      +----------------+
       |___________________________________________________|
                                 |
                                 | (Encrypted JSON Response)
                                 v
                          [ SECURE CLIENT ]


``` 

-------
## Containers

- Container A: FastAPI App
- Container B: PostgreSQL (Persistent storage)
- Container C: Redis (In-memory security engine)

-------

## Define Security Boundaries

we divide the system into four distinct zones of trust.
the 4 trusted zone 

### 1/ The Untrusted Zone
Anything outside your Nginx/Reverse Proxy is unsecure 

### 2/ The DMZ / Validation Boundary
The space between Nginx and your Route Logic

### 3/ The Identity Boundary
inside app logic of authentification 
### 4/ The Trusted Data Zone

PostgreSQL and Redis behind a private network
[!] we can implement the zero trust methodologie inside the  database  for more secure 
[!!] made a devsecops test automation for hardering database 
-------
## Define Threat Model

### Threats:

- Credential stuffing
- Token theft
- Replay attacks
- Role escalation
- API abuse
- Injection attacks
- Enumeration attacks

---------
## security header 

-------

    - X-Frame-Options
        this avoid  clickjacking by ensure that their content is not emaded  into other sites 

```
X-Frame-Options: DENY
```

=>Recommendation
    - Modern  owsap  use CSP frame-ancestors

```
    Content-Security-Policy: frame-ancestors 'none';
```

- It is only relevant when:

    -- The response is HTML

    -- The page contains interactive elements (buttons, forms, links)

    -- The page can be rendered in a browser

-------

[!] X-XSS-Protection  
it's attempted to detect reflected XSS  but  now  : 
    - It is non-standard
    - It is deprecated
    - It has caused security bypasses
so  we need to  disable it and use 
For APIs:
```
Content-Security-Policy: default-src 'none';
```
For HTML pages:
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'none';
```

-------

[ok] X-Content-Type-Options
```
X-Content-Type-Options: nosniff
```

[!] with out it the browser  can  performe  MIME sniffing  whitch  can  lead to  
    Treating JSON as script
this will  return  
```
for JSon  responses 
    Content-Type: application/json
for  JSON  Downloads 
    Content-Type: application/pdf
    Content-Disposition: attachment;

```
-------

[good] Referrer-Policy

https://api.example.com/admin/dashboard?session=abc123
And the user clicks a link to another website: https://external-site.com
With: Referrer-Policy: strict-origin-when-cross-origin
the  browser will  send  to  Referer: https://api.example.com/

used in  API || web  dashboard || publick website 

--------
[good] Content-Type: application/json 
- Web app serving HTML → text/html; charset=UTF-8
- REST API → application/json
- plus add for security  → X-Content-Type-Options: nosniff
--------
    - set-cookie ( for  session/refresh  token )
    ```
    Set-Cookie: refresh_token=<token>; HttpOnly; Secure; SameSite=Strict; Path=/auth/refresh; Max-Age=604800
    ```
    Used for short-lived cookies to refresh token expiration
    - Strict-Transport-Security (HSTS)

    ```
    Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
    ```
    Start with a smaller max-age (1 day) for testing, then increase
--------
[info] if we use Fronend and  api  on  different origins 
    Dashboard: https://app.example.com → API: https://api.example.com
we  need  to  set Access-Control-Allow-Origin: https://app.example.com
[info] if  Frontend and API are on the same origin
Example: https://api.example.com serves both API and dashboard
    -You don’t need this header at all. SOP already blocks unwanted cross-origin requests.
--------
[can_be_useful]Permissions-Policy
Permissions-Policy: geolocation=(), camera=(), microphone=(), interest-cohort=()
    - Disable unneeded browser features for security and privacy
*Cache-Control: no-store*
*Pragma: no-cache*




---------
## API Endpoints Design


- POST /auth/register

Request:
    {
        "email": "user@example.com",
        "password": "StrongPassword123"
    }
Response TRUE:
    {
        "message": "User created"
    }
Respond FALSE:
    {
        no existe for now 
    }

- POST /auth/login

Request:
    {
        "email": "user@example.com",
        "password": "password"
    }

Response:
    {
        "access_token": "xxx",
        "refresh_token": "yyy",
        "token_type": "bearer"
    }
Security Steps:
check rate limit || verify password hash || log IP || monitor login attempts || generate access token || generate refresh token

- POST /auth/refresh

- POST /auth/logout
    blocklist token 
    log audit event 

User Endpoints

GET /users/me
requires authentication

Response:
{
  "id": "uuid",
  "email": "user@example.com",
  "roles": ["user"]
}

- PATCH /users/me
update profile

- GET /admin/users

- POST /admin/roles
Create new role.

- PATCH /admin/users/{id}/role
Assign roles.

