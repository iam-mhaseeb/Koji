# Koji documentation

Welcome to Koji — a self-hostable portfolio and blog for developers. One instance per site, markdown on disk, no database.

## Who this is for

- Developers who want a **fast, minimal** personal site
- People who prefer **git-backed** content over a CMS
- Anyone who wants **full control** over hosting and code

## Documentation map

| Guide | What you'll learn |
|-------|-------------------|
| [Getting started](getting-started.md) | Install, run locally, publish your first post |
| [Configuration](configuration.md) | Every `site.yaml` option explained |
| [Content guide](content.md) | Pages, posts, frontmatter, drafts, popular lists |
| [Theming](theming.md) | CSS, layout, customizing the look |
| [Deployment](deployment.md) | Docker, production, reverse proxy, env vars |
| [SEO](seo.md) | Meta tags, sitemap, structured data, launch checklist |
| [llms.txt](llms-txt.md) | AI-friendly exports and overrides |
| [Extending Koji](extending.md) | New routes, templates, content types, forks |
| [Architecture](architecture.md) | How the app is structured (for contributors) |

## Quick reference

### Content layout

```
content/
├── site.yaml          # Site identity and settings
├── custom.css         # Optional theme overrides
├── llms.txt           # Optional manual llms.txt
├── llms-full.txt      # Optional full markdown export
├── pages/
│   ├── home.md        # /
│   ├── now.md         # /now
│   └── projects.md    # /projects
└── posts/
    └── my-post.md     # /blog/my-post
```

### Common commands

```bash
# Local development
pip install -r requirements.txt
uvicorn app.main:app --reload

# Tests
pip install -r requirements-dev.txt
pytest

# Docker
docker compose up --build
```

### All routes

| URL | Type |
|-----|------|
| `/` | Home |
| `/now`, `/projects` | Static pages |
| `/blog`, `/blog/{slug}` | Blog |
| `/atom.xml`, `/rss.xml`, `/feed.xml` | Atom feed |
| `/sitemap.xml` | Sitemap |
| `/robots.txt` | Robots |
| `/llms.txt`, `/llms-full.txt` | LLM maps |
| `/index.md`, `/{page}.md`, `/blog/{slug}.md` | Markdown exports |
| `/static/*` | Bundled CSS |
| `/custom.css` | Your theme file |
| `/health` | Health check |

## Getting help

- Read the guide that matches your task (table above)
- Check [Extending Koji](extending.md) if you need behavior the defaults don't provide
- Open an issue on your fork's repository for bugs or feature requests

## License

MIT — see [LICENSE](../LICENSE).
