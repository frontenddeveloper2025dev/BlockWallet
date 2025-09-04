#!/bin/bash
# Start script for Render deployment
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:$PORT app:app