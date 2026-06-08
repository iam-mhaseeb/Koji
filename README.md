# Koji `( ◕ ᴥ ◕ )`

**Koji** is a self-hostable dead simple personal website for developers. No database, markdown on disk, and a fast, text-first minimalist layout.

## Features

- **FastAPI** — server-rendered HTML, minimal JavaScript
- **Markdown + YAML** — pages and posts in `content/`
- **HTMX** — live blog search (progressive enhancement)
- **SEO** — meta tags, Open Graph, JSON-LD, sitemap, robots
- **llms.txt** — AI-friendly markdown exports ([spec](https://llmstxt.org/))
- **Docker** — single-container deploy

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

In development, saving files under `content/` reloads markdown and `site.yaml` on the next request — refresh the browser. Set `KOJI_ENV=production` in production to cache content in memory.

```bash
docker compose up --build   # or Docker
pytest                      # after pip install -r requirements-dev.txt
```

## Example blog

See Koji in production: [muhammadhaseeb.me](https://muhammadhaseeb.me)

## Documentation

Full guides for using and extending Koji:

| Guide | Description |
|-------|-------------|
| [**Documentation index**](docs/README.md) | Start here |
| [Getting started](docs/getting-started.md) | Install, first post, workflow |
| [Configuration](docs/configuration.md) | Every `site.yaml` option |
| [Content guide](docs/content.md) | Pages, posts, frontmatter |
| [Theming](docs/theming.md) | CSS and templates |
| [Deployment](docs/deployment.md) | Docker, production, HTTPS |
| [SEO](docs/seo.md) | Search and social previews |
| [llms.txt](docs/llms-txt.md) | AI assistant exports |
| [Extending Koji](docs/extending.md) | New pages, routes, forks |
| [Architecture](docs/architecture.md) | Code structure for developers |

## Customize in 60 seconds

Edit `content/site.yaml`:

```yaml
title: "Your Name's blog"
author: Your Name
email: you@example.com
url: https://yourdomain.com
```

Add a post at `content/posts/hello.md`:

```yaml
---
title: Hello
slug: hello
date: 2026-06-02
description: My first post.
---

Hello, world.
```

## License

MIT — see [LICENSE](LICENSE).
