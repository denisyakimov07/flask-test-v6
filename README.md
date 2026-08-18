# Flask Blog (flask-test-v6)

A learning Flask blog: posts, authentication, email confirmation, and an admin panel.

## Stack

- **Flask 2.3** + SQLAlchemy 2.0 (Flask-SQLAlchemy 3.1)
- **Flask-Login** — authentication
- **Flask-WTF** — forms with CSRF protection
- **Flask-Admin** — admin panel (`/admin`)
- **Flask-Migrate** (Alembic) — database migrations
- **Flask-Mail** — email delivery
- **SQLite** — local database (`flaskblog.db`)
- UI theme: Start Bootstrap "Clean Blog" (Bootstrap 5)

## Features

- Register / login / logout, password change in profile
- Email confirmation via token (link is valid for 1 hour)
- Create / edit / delete posts (author only)
- User page with the list of their posts
- Admin panel: `/admin` (posts and users)
- Pages: Home, About, Contact, 404/403

## Project structure

```
app.py                  # entry point
environment.py          # loads configuration from .env
flaskblog/
    __init__.py         # Flask, DB, Admin, Login, Mail, Migrate initialization
    models.py           # User, BlogPost models + WTForms
    routes.py           # all routes
    templates/          # Jinja2 templates (Clean Blog)
    static/             # CSS/JS/fonts
migrations/             # Alembic migrations
flaskblog.db            # SQLite database (created by migration, not committed)
Dockerfile              # production image
```

## Installation and running

Requires Python 3.10+.

```bash
# 1. Virtual environment
py -3.10 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 2. Dependencies
pip install -r requirements.txt

# 3. Configuration — create .env and fill in the values
#    (see "Configuration" below)

# 4. Database
set FLASK_APP=app.py         # Windows; PowerShell: $env:FLASK_APP="app.py"
flask db upgrade             # creates/updates flaskblog.db

# 5. Run
flask run
# -> http://127.0.0.1:5000
```

New migration after changing models:

```bash
flask db migrate -m "description"
flask db upgrade
```

## Docker

The image is built by GitHub Actions on every push to `master` and published
to GHCR as a **public** package — no authentication is required to pull it.

```bash
# Pull the image (no docker login needed, the package is public)
docker pull ghcr.io/denisyakimov07/flask-test-v6:latest

# Run the container
docker run -d --name flask-blog -p 5000:5000 \
    -v flask-blog-data:/app/flaskblog.db \
    -e FLASK_SECRET_KEY=<long-random-string> \
    -e MAIL_SERVER=mail.smtp2go.com \
    -e MAIL_PORT=587 \
    -e MAIL_USERNAME=emailarmserver \
    -e MAIL_PASSWORD=<smtp2go-password> \
    -e MAIL_DEFAULT_SENDER=admin@denisdns.com \
    ghcr.io/denisyakimov07/flask-test-v6:latest
# -> http://localhost:5000
```

To build locally instead:

```bash
docker build -t flask-blog .
```

Package visibility can be changed in the repository settings:
**Packages -> flask-test-v6 -> package settings -> Visibility**.

The container applies database migrations on startup (`flask db upgrade`)
before starting gunicorn. The SQLite file is stored in the `flask-blog-data`
volume so it survives container recreation.

## Configuration (.env)

The `.env` file is not committed. Example:

```ini
# --- Database: local SQLite ---
DB_DATABASE_TYPE=sqlite
DB_DATABASE=flaskblog.db

# --- Mail: denisdns.com via SMTP2GO relay ---
# Oracle Cloud blocks outbound port 25, so outbound mail is relayed
# through mail.smtp2go.com:587 (TLS + SASL).
MAIL_SERVER=mail.smtp2go.com
MAIL_PORT=587
MAIL_USERNAME=emailarmserver
MAIL_PASSWORD=<smtp2go-password>
MAIL_DEFAULT_SENDER=admin@denisdns.com

# --- Flask ---
FLASK_SECRET_KEY=<long-random-string>
```

### Mail

Outbound mail for the `denisdns.com` domain is relayed through **SMTP2GO**
(`mail.smtp2go.com:587`, TLS, SASL authentication). The domain is verified
in SMTP2GO (Sending -> Verified Senders) with SPF/DKIM/DMARC configured.
The sender is `admin@denisdns.com`.

### Database

The default is a local SQLite file `flaskblog.db` in the project root.
For other databases set `DB_DATABASE_TYPE` (`postgresql`, `mysql`),
`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DATABASE` in `.env`
and install the matching driver (e.g. `psycopg2` or `mysqlclient`).

## Routes

| Route | Description |
|---|---|
| `/` | post list |
| `/post/<id>` | post page |
| `/about`, `/contact` | static pages |
| `/login`, `/sing_up`, `/logout` | authentication |
| `/profile` | profile, password change |
| `/user` | current user's page |
| `/add_new_post`, `/edit_post/<id>`, `/delete_post/<id>` | post CRUD (author only) |
| `/confirm_email/<token>` | email confirmation |
| `/admin` | admin panel |
