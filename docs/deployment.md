# Deployment

Koji is designed as **one container (or process) per blog**. You deploy the app, mount or bake your `content/` directory, and point a domain at it.

## Docker (recommended)

### Build and run

```bash
docker compose up --build -d
```

Default `docker-compose.yml`:

- Builds from `Dockerfile`
- Publishes port **8000**
- Mounts `./content` read-only into the container

### Production compose example

```yaml
services:
  koji:
    build: .
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      KOJI_CONTENT_DIR: /app/content
    volumes:
      - ./content:/app/content:ro
```

Bind to localhost and put **nginx**, **Caddy**, or **Traefik** in front for HTTPS.

### Content-only updates

With a volume mount, update posts by editing files on the host and restarting:

```bash
docker compose restart koji
```

No rebuild needed for markdown changes.

## Manual deployment (venv)

On a VPS:

```bash
git clone https://github.com/you/koji.git
cd koji
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export KOJI_CONTENT_DIR=/opt/koji/content
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### systemd unit

`/etc/systemd/system/koji.service`:

```ini
[Unit]
Description=Koji blog
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/koji
Environment=KOJI_CONTENT_DIR=/opt/koji/content
ExecStart=/opt/koji/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now koji
```

## Reverse proxy (Caddy)

```
yourdomain.com {
    reverse_proxy 127.0.0.1:8000
}
```

Caddy obtains TLS certificates automatically.

## Reverse proxy (nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate     /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Pre-launch checklist

1. **`content/site.yaml` → `url`:** `https://yourdomain.com` (no trailing slash)
2. **Email and social handles** updated
3. **Remove or rewrite** sample posts you don't want public
4. **SEO:** follow [SEO launch checklist](seo.md#launch-checklist)
5. **Health check:** `curl https://yourdomain.com/health` → `{"status":"ok",...}`
6. **Feeds:** verify `/atom.xml` in a feed reader
7. **Robots/sitemap:** `curl https://yourdomain.com/robots.txt` and `/sitemap.xml`

## Environment variables

| Variable | When to use |
|----------|-------------|
| `KOJI_CONTENT_DIR` | Content lives outside the app tree |
| `PORT` | Not built-in; pass to uvicorn: `--port $PORT` (platforms like Railway set this) |

Example for Railway/Render:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Update your Dockerfile `CMD` if needed.

## Platform notes

| Platform | Notes |
|----------|-------|
| **Fly.io / Railway / Render** | Docker or Python buildpack; set `KOJI_CONTENT_DIR`; use persistent volume for content if not baking into image |
| **GitHub Pages** | Not supported — Koji needs Python/FastAPI |
| **Vercel / Netlify serverless** | Not a fit without major rewrite (long-running server preferred) |
| **Raspberry Pi** | Works well; low memory footprint |

## Security

- Koji has **no admin panel** and no user login — attack surface is small.
- Serve behind HTTPS only in production.
- Mount `content` **read-only** in Docker when possible.
- Do not expose `/health` publicly if you prefer — block in nginx (optional).

## Monitoring

- **Health:** `GET /health` returns JSON with version
- **Logs:** uvicorn logs to stdout; collect via Docker or journald
- **Uptime:** ping `/health` or `/` from an external monitor

## Backups

Your content **is** your site. Back up:

- `content/` directory (git remote is ideal)
- `site.yaml` and custom CSS

The application code can be re-cloned from upstream.

## Scaling

A single Koji instance handles typical personal blog traffic easily (static files in memory, simple rendering). For high traffic:

- Run multiple uvicorn workers: `uvicorn app.main:app --workers 4`
- Put a CDN in front (cache `/static/*`; dynamic HTML may need short TTL or no cache)

## Next

- [SEO](seo.md) — search engines after deploy
- [Configuration](configuration.md) — production `site.yaml`
