# Microsoft Entra ID (Azure AD) SSO — IT Setup Guide

This document is for the IT team configuring SSO for **https://faq.arvindgcc.com** (Arvind GCC Employee FAQ Portal).

## App registration

| Setting | Value |
|---------|-------|
| **Name** | Arvind GCC FAQ Portal (or your standard naming) |
| **Platform** | Web |
| **Redirect URI** | `https://faq.arvindgcc.com/auth/callback` |
| **Front-channel logout URI** (optional) | `https://faq.arvindgcc.com/logout` |
| **Supported account types** | Accounts in this organizational directory only (Single tenant) |

## API permissions (delegated)

Add Microsoft Graph delegated permissions:

- `openid`
- `profile`
- `email`
- `User.Read`

Grant admin consent for the organization.

## User access

- Enable **User assignment required?** = **Yes**
- Assign only approved employee groups (e.g. GCC employees, HR, IT) to this app registration

This ensures only assigned users can sign in, even if they have valid Arvind credentials.

## Credentials to share with the application team

Provide these values securely (do not email in plain text if policy forbids it):

| Variable | Description |
|----------|-------------|
| `AZURE_TENANT_ID` | Directory (tenant) ID |
| `AZURE_CLIENT_ID` | Application (client) ID |
| `AZURE_CLIENT_SECRET` | Client secret (or configure certificate auth) |

## Reverse proxy requirements

The site runs on-prem behind a reverse proxy. Ensure the proxy forwards:

```
X-Forwarded-Proto: https
X-Forwarded-Host: faq.arvindgcc.com
```

No URL path changes are required.

The app server must allow **outbound HTTPS** to:

- `login.microsoftonline.com`
- `graph.microsoft.com` (fallback user profile lookup)

If JWKS validation fails (common on locked-down servers), the app uses the userinfo / Graph API instead of validating the ID token signature locally.

## Application environment variables

Set on the production server:

```env
AUTH_ENABLED=1
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
AZURE_REDIRECT_URI=https://faq.arvindgcc.com/auth/callback
SECRET_KEY=<strong-random-secret>
SESSION_COOKIE_SECURE=1
SESSION_COOKIE_HTTPONLY=1
SESSION_COOKIE_SAMESITE=Lax
```

## Verification checklist

1. Open `https://faq.arvindgcc.com/` in a private/incognito window → redirects to Microsoft login
2. Sign in with an **assigned** user → FAQ portal loads
3. Sign in with a **non-assigned** user → access denied by Entra ID
4. Sign out → visiting the site again requires login
5. API without session: `POST /api/feedback` returns `401 Unauthorized`

## Local development (no SSO)

Developers can set `AUTH_ENABLED=0` in `.env` to run the portal locally without Microsoft login.

## Access logs

User sign-ins and page visits are stored in the `access_logs` MySQL table.

- **Sign in** — logged when a user completes Microsoft SSO
- **Page view** — logged once per browser session when the user opens the portal

To view logs in the app, set admin emails in `.env`:

```env
LOG_ADMIN_EMAILS=you@arvind.com,admin@arvind.com
```

Then visit `https://faq.arvindgcc.com/admin/logs` while signed in with one of those accounts.
