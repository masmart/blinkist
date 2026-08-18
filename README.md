# Blinkist

A Flask application backed by PostgreSQL, with Tailwind CSS and optional MinIO object storage.

## Requirements

- Python 3.11
- PostgreSQL 15 or newer
- Node.js 18 or newer (only needed when rebuilding CSS)

## Local setup

1. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   npm install
   ```

3. Copy `.env.example` to `.env`, replace every placeholder, and load those variables into your shell. At minimum, configure `SECRET_KEY`, `DATABASE_URL`, and `ADMIN_EMAILS`.

4. Create an empty PostgreSQL database, import the sanitized seed dump, and apply migrations:

   ```powershell
   $env:PGCLIENTENCODING = "UTF8"
   psql -h 127.0.0.1 -U <user> -d blinkist -f public.sql
   python -m flask --app app db upgrade
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

   Open <http://127.0.0.1:5000>.

## Development

Rebuild Tailwind CSS while editing templates:

```powershell
npm run watch-css
```

Run the test suite:

```powershell
python -m pytest
```

## Security

- Never commit `.env`, database credentials, storage credentials, or production database exports.
- Admin access is restricted to authenticated email addresses listed in `ADMIN_EMAILS`.
- Rotate any credential that has previously appeared in Git history.
