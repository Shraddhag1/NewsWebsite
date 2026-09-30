# NewsWave

NewsWave is a simple online news portal built with **Python, Flask, SQLite, HTML, and CSS**. It provides a home page for news articles, an About page, a Contact form, and an admin area for managing news.

## Features

- Home page displaying the latest news
- News categories: Technology, Business, Sports, and Politics
- About page
- Contact form that stores messages in SQLite
- Admin login and dashboard
- Add, edit, and delete news articles
- SQLite database initialized with sample news

## Project structure

Flask expects templates and static assets in these locations:

```text
NewsWebsite/
├── app.py
├── newswave.db              # Created automatically when the app starts
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   ├── login.html
│   ├── admin.html
│   ├── add_news.html
│   └── edit_news.html
└── static/
    └── css/
        └── style.css
```

**Before running:** arrange the files into the structure above. In the supplied ZIP, the templates and stylesheet are at the project root, and `base.tml` should be renamed to `base.html` and placed in `templates/`. Move the other HTML template files into `templates/`, and place `style.css` at `static/css/style.css`.

## Requirements

- Python 3.9 or newer
- pip

## Run locally

1. Open a terminal in the `NewsWebsite` project directory.
2. (Optional but recommended) Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Flask:

   ```bash
   python -m pip install Flask
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

The SQLite database (`newswave.db`) is initialized when the application is run directly. It will be created in the project directory, and sample news is inserted if the news table is empty.

## Admin access

Open the **Admin** link in the website navigation.

The credentials currently hard-coded in `app.py` are:

- Username: `admin`
- Password: `admin123`

**Security note:** These are demonstration credentials. Change them and use a securely stored secret key before deploying publicly. Do not commit real passwords, secret keys, or private data to GitHub.

## Deployment

This project is a **Flask backend application**, not a static-only website. GitHub Pages supports static files and cannot run `app.py` or the SQLite-backed admin/contact features. You can use GitHub to store the source code, but deploy the running Flask application to a Python-compatible hosting service. Configure production environment variables, a production WSGI server, and persistent storage for the database as appropriate for your host.

## License

No license has been specified for this project.
