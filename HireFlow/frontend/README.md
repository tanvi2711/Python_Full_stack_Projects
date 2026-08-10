# HireFlow Frontend

Premium white/navy/blue React frontend wired to the supplied Django backend.

## Run

```bash
npm install
npm run dev
```

Backend:

```bash
cd backend
python manage.py runserver
```

The frontend uses `http://localhost:8000/api` by default. You can override it with `VITE_API_URL`.

## Real Django endpoints used

- `GET /api/auth/csrf/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/profile/`
- `PUT /api/profile/`
- `GET /api/jobs/list/`
- `GET /api/skills/`
- `GET /api/jobs/<id>/`
- `POST /api/jobs/<id>/apply/`
- `GET /api/applications/mine/`

Saved jobs are stored in browser localStorage because the supplied backend has no saved-job endpoint. Interviews/notifications are not fabricated because the supplied backend has no corresponding endpoints.

Applications upload the resume as multipart form data exactly as required by the supplied Django view (PDF/DOC/DOCX, max 5 MB).
