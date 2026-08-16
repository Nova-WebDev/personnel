# Personnel

Internal personnel identity system — generates QR-coded employee ID cards and exposes a verification API for identity checks across internal apps.

## What it does

- Generates a personnel card (photo, first/last name, optional unit ID) with an embedded QR code
- The QR encodes an opaque, non-guessable token (not raw personnel data)
- Any internal service can scan the card and call the verification API to confirm identity and retrieve the associated data
- Tokens can be revoked/blocked centrally without reissuing cards for the whole organization

## Why

Instead of every internal app building its own identity-check flow, this project acts as a single source of truth: scan the card, hit one API, get a validated response.

## Architecture

```
personnel/
├── backend/     # FastAPI service — token generation, verification, card data
├── frontend/    # React app — card display page (scanned by end users)
├── nginx/       # Reverse proxy — routes /api/* to backend, else frontend
├── postgres/    # Database
├── base/        # Base Python image
└── docker-compose.yml
```

## API convention

- `domain/{uuid}` → served by frontend (human-readable card view)
- `domain/api/{uuid}` → served by backend (JSON, for service-to-service verification)

## Tech stack

- **Backend:** Python, FastAPI
- **Frontend:** React, Tailwind
- **Infra:** Docker, Nginx, PostgreSQL, Redis

## Status

🚧 Early development
