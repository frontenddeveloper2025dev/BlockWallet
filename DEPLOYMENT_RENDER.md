# Deployment Instructions for Render

## Files ready for Render deployment:

### Required files created:
- `requirements.txt` - Python dependencies including gunicorn
- `runtime.txt` - Specifies Python 3.11
- `Procfile` - Web service startup command
- `start.sh` - Alternative startup script
- `README.md` - Project documentation (renamed from replit.md)

### Main application:
- `app.py` - Flask application (production-ready)

## Deploy on Render:

1. **Create a new Web Service** on Render
2. **Connect your repository** (GitHub, GitLab, etc.)
3. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Python Version:** 3.11

4. **Environment Variables** (set in Render dashboard):
   - `SESSION_SECRET` - Generate a strong secret key
   - `FLASK_ENV` - Set to `production`

5. **Deploy** - Render will automatically build and deploy your app

## Notes:
- The app automatically detects production environment
- Health check endpoints are available at `/health` and `/?health=1`
- All static files are served from `/static/` directory
- Database functionality uses file-based storage (wallet files)

## Alternative startup methods:
- Using Procfile: `web: gunicorn --bind 0.0.0.0:$PORT app:app`
- Using start.sh: `./start.sh` (if executable permissions are set)