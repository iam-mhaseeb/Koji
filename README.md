# Koji `( ◕ ᴥ ◕ )`

**Koji** is a self-hostable portfolio + blog for developers. One instance per site, no database, markdown on disk, and a minimalist layout inspired by [Bear Blog](https://bearblog.dev/).

Design follows Bear’s text-first aesthetic; **this repository is original code** (MIT licensed) and is not a fork of [bearblog](https://github.com/HermanMartinus/bearblog) (Bear Blog License 2.0).

## Features

- **FastAPI** backend with server-rendered HTML
- **Markdown** pages and posts with YAML frontmatter
- **HTMX** live search on the blog index (progressive enhancement)
- **Atom feed** at `/atom.xml`
- **No database** — content lives in `content/`
- **Docker**-ready single-container deploy

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

### Docker

```bash
docker compose up --build
```

## Customize your site

Edit `content/site.yaml` for title, nav, email, and popular posts:

```yaml
title: "Your Name's blog"
author: Your Name
email: you@example.com
url: https://yourdomain.com
```

| Path | Purpose |
|------|---------|
| `content/pages/home.md` | Homepage intro |
| `content/pages/now.md` | `/now` page |
| `content/pages/projects.md` | `/projects` page |
| `content/posts/*.md` | Blog posts |

### Post frontmatter

```yaml
---
title: My post title
slug: my-post
date: 2026-06-01
description: Optional summary for feeds
popular: true
draft: false
---
```

Set `popular_slugs` in `site.yaml` to control the homepage “most popular” list, or mark posts with `popular: true`.

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `KOJI_CONTENT_DIR` | `./content` | Path to markdown content |

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home + recent & popular posts |
| `/now` | Now page |
| `/projects` | Projects page |
| `/blog` | All posts (+ HTMX search) |
| `/blog/{slug}` | Single post |
| `/atom.xml` | Atom feed |

## License

MIT — see [LICENSE](LICENSE).

Visual design inspiration from Bear Blog; implementation is independent. Do not copy Bear Blog’s proprietary source if you need a hosted SaaS—use Bear for that, or self-host Koji.
