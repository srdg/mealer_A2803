"""
# PRODUCTION_DEPLOYMENT.md - Production Deployment Guide

Author: Soumik Ranjan Dasgupta

---

## Overview

This guide covers deploying the Mealer application to production.

---

## Pre-Deployment Checklist

- [ ] All code committed to git
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Tests passing
- [ ] Security headers configured
- [ ] SSL/HTTPS certificate obtained
- [ ] Database backups configured
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Error tracking configured

---

## Environment Setup

### Set Production Environment

```bash
# On Linux/macOS
export FLASK_ENV=production

# On Windows (Command Prompt)
set FLASK_ENV=production

# On Windows (PowerShell)
$env:FLASK_ENV='production'
```

### Required Environment Variables

Create a `.env` file (don't commit to git):

```bash
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here-min-32-chars
```

Load it with python-dotenv:

```bash
pip install python-dotenv
```

---

## Deployment Options

### Option 1: Gunicorn (Recommended for Linux)

#### Installation

```bash
pip install gunicorn
```

#### Run

```bash
# Correct way - use wsgi.py
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

**Parameters:**
- `-w 4`: Number of worker processes (CPU cores × 2 + 1)
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000
- `wsgi:app`: Reference to app instance in wsgi.py (NOT wsgi:create_app)

#### Full Production Command

```bash
gunicorn \
    -w 4 \
    -b 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    wsgi:app
```

### Option 2: Waitress (Windows-Friendly)

#### Installation

```bash
pip install waitress
```

#### Run

```bash
waitress-serve --host=0.0.0.0 --port=8000 'app:create_app()'
```

### Option 3: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

Build and run:

```bash
docker build -t mealer .
docker run -p 8000:8000 mealer
```

Update the Dockerfile CMD:

```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

---

## Nginx Configuration

Nginx as reverse proxy (recommended):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Systemd Service (Linux)

Create `/etc/systemd/system/mealer.service`:

```ini
[Unit]
Description=Mealer Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/user/mealer
Environment="FLASK_ENV=production"
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mealer
sudo systemctl start mealer
sudo systemctl status mealer
```

---

## Monitoring & Logging

### Application Logs

Logs are written to `logs/mealer.log` by default.

Monitor in real-time:

```bash
tail -f logs/mealer.log
```

### Health Check

Endpoint: `GET /health`

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-24T12:00:00"
}
```

Monitor with cron:

```bash
*/5 * * * * curl -s http://localhost:8000/health || alert
```

### Error Tracking

Recommended services:
- Sentry (https://sentry.io)
- Rollbar (https://rollbar.com)
- Bugsnag (https://www.bugsnag.com)

---

## Performance Optimization

### 1. Enable Caching

```python
# In app/__init__.py
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/meal-data/<int:day>')
@cache.cached(timeout=3600)  # Cache for 1 hour
def api_get_meal_data(day):
    ...
```

### 2. Use CDN

Upload static files to CDN:
```html
<link rel="stylesheet" href="https://cdn.example.com/mealer/style.css">
```

### 3. Enable Compression

Nginx will handle this with gzip setting.

### 4. Database Connection Pooling

If using a database, configure connection pooling:

```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

---

## Scaling

### Horizontal Scaling

Run multiple app instances behind load balancer:

```bash
# Terminal 1
gunicorn -w 4 -b 127.0.0.1:8000 'app:create_app()'

# Terminal 2
gunicorn -w 4 -b 127.0.0.1:8001 'app:create_app()'

# Terminal 3
gunicorn -w 4 -b 127.0.0.1:8002 'app:create_app()'
```

Configure Nginx to load balance:

```nginx
upstream mealer_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

location / {
    proxy_pass http://mealer_backend;
}
```

---

## Security Checklist

- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Secret keys rotated
- [ ] Dependencies updated
- [ ] Error messages sanitized
- [ ] Logs protected
- [ ] Database credentials secured

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Permission Denied

```bash
# Run with sudo
sudo systemctl restart mealer

# Or change file permissions
chmod -R 755 /path/to/mealer
```

### Out of Memory

Increase worker count or memory:

```bash
# Reduce workers
gunicorn -w 2 -b 0.0.0.0:8000 'app:create_app()'

# Or increase system memory
```

---

## Maintenance

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
tar -czf /backups/mealer-$(date +%Y%m%d).tar.gz /home/user/mealer/data.csv
```

### Update Procedure

```bash
# 1. Pull latest code
git pull origin main

# 2. Install new dependencies
pip install -r requirements.txt

# 3. Restart application
sudo systemctl restart mealer

# 4. Check status
sudo systemctl status mealer
```

---

## Resources

- [Gunicorn Documentation](https://gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

Author: Soumik Ranjan Dasgupta
Last Updated: January 2026
"""
