# Extending Koji

Koji is intentionally small. Most customization happens through **content** and **CSS**. When you need new behavior, you extend the FastAPI app and templates.

## Extension strategies (pick the lightest that works)

| Goal | Approach |
|------|----------|
| Change colors, fonts, spacing | `content/custom.css` |
| Change site name, nav, SEO | `content/site.yaml` |
| New blog post | `content/posts/*.md` |
| New static page at fixed URL | Add route + template + `content/pages/*.md` |
| New dynamic section | New route in `app/main.py` + template |
| Different homepage layout | Edit `app/templates/home.html` |
| Fork and maintain | Clone repo, modify `app/` |

## Adding a new static page

Example: an `/about` page.

### 1. Create content

`content/pages/about.md`:

```markdown
---
title: About
description: About me and this site.
---

Your about page content.
```

### 2. Register the route

In `app/main.py`, add the path to the existing static page handler:

```python
@app.get("/about", response_class=HTMLResponse)
@app.get("/about", response_class=HTMLResponse)
@app.get("/projects", response_class=HTMLResponse)
async def static_page(request: Request):
    slug = request.url.path.strip("/")
    ...
```

### 3. Add nav link

`content/site.yaml`:

```yaml
nav:
  - label: Home
    href: /
  - label: About
    href: /about
  ...
```

### 4. SEO and llms.txt

For full SEO, extend `seo_for_page` usage (already automatic once route exists).

For llms.txt, update `app/llms.py` `render_llms_txt()` to include `about` in the pages loop:

```python
for slug, label in (("home", "Home"), ("projects", "Projects"), ("about", "About")):
```

Also add `.md` export:

```python
@app.get("/about.md", response_class=Response)
async def about_markdown():
    ...
```

And include `about` in `render_llms_full_txt()` page loop.

### 5. Sitemap

Add the URL in `app/seo.py` → `render_sitemap_xml()` if you want it in the sitemap (copy the pattern for `/projects`).

## Adding a custom route

Example: `/tags/{tag}` listing posts (requires code — not built-in).

```python
@app.get("/tags/{tag}", response_class=HTMLResponse)
async def posts_by_tag(request: Request, tag: str):
    store = get_store()
    posts = [p for p in store.published_posts() if tag in p.tags]  # you'd add tags to Post
    site = get_site()
    return templates.TemplateResponse(
        request,
        "tag.html",
        _ctx(posts=posts, tag=tag, seo=seo_for_blog_index(site)),  # or custom SeoMeta
    )
```

You would extend:

- `Post` dataclass in `app/content.py`
- `_read_post()` to load `tags` from frontmatter
- New template `app/templates/tag.html`

## Custom SEO metadata

Build a `SeoMeta` object from `app/seo.py`:

```python
from app.seo import SeoMeta, absolute_url

seo = SeoMeta(
    title="My custom page",
    description="...",
    canonical_url=absolute_url(site, "/custom"),
    og_type="website",
)
```

Pass `seo=seo` in template context.

## Custom templates

1. Create `app/templates/my-page.html`:

```html
{% extends "base.html" %}
{% block main %}
<h1>{{ heading }}</h1>
<p>Custom layout here.</p>
{% endblock %}
```

2. Return it from a route with `templates.TemplateResponse(request, "my-page.html", _ctx(...))`.

### Template context

Every page receives at least:

| Key | Type | Description |
|-----|------|-------------|
| `request` | Request | Starlette request (required by TemplateResponse) |
| `site` | SiteConfig | From `site.yaml` |
| `seo` | SeoMeta | Optional; enables full meta tags |

## Reloading content in development

`ContentStore` caches posts and pages in memory. After bulk edits:

```python
get_store().reload()  # call from a debug route or restart uvicorn
```

For production, restarting the process is simplest.

## Adding markdown extensions

In `app/content.py`, extend the `_md` Markdown instance:

```python
_md = markdown.Markdown(
    extensions=[
        "meta",
        FencedCodeExtension(),
        CodeHiliteExtension(css_class="highlight", guess_lang=False),
        TableExtension(),
        "footnotes",  # add this
    ],
    output_format="html5",
)
```

Add the dependency if needed (`pip install markdown-extensions` or bundled).

## Static assets

Put files in `app/static/`:

```
app/static/
├── style.css
├── og.png
└── images/
```

Reference as `/static/og.png` in YAML and markdown.

## Middleware example (security headers)

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

Add in `app/main.py` after `app` creation.

## Redirects

```python
from fastapi.responses import RedirectResponse

@app.get("/old-url")
async def redirect_old():
    return RedirectResponse(url="/new-url", status_code=301)
```

## Post tags / categories (recipe)

1. Add `tags: list[str]` to `Post` and frontmatter parsing
2. Build a tag index dict in `ContentStore`
3. Add routes and templates
4. Include tag URLs in sitemap if desired

## Testing extensions

```bash
pip install -r requirements-dev.txt
pytest
```

Add tests under `tests/` mirroring `test_integration.py` and `test_seo.py`.

## Keeping upstream updates

If you fork Koji:

- Keep content in `content/` or a separate repo via `KOJI_CONTENT_DIR`
- Minimize changes in `app/main.py` — use a separate `app/custom_routes.py` imported from `main` if you want cleaner merges

## When to fork vs configure

| Need | Fork? |
|------|-------|
| Custom CSS | No |
| New posts/pages (existing types) | No |
| New page type with new URL | Small fork or PR |
| User accounts / comments | Different product — integrate external (Giscus, etc.) via HTML in markdown |
| Multi-tenant SaaS | Out of scope for Koji |

## Next

- [Architecture](architecture.md) — module map and request flow
- [Configuration](configuration.md) — all config keys
