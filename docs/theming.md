# Theming

Koji ships with a **minimal, text-first** default theme in `app/static/style.css`. You customize appearance without touching Python by adding **`content/custom.css`**.

## Quick customization

1. Create `content/custom.css`
2. Restart the server (or redeploy)
3. Koji auto-injects `<link rel="stylesheet" href="/custom.css" />` in every page

Example `content/custom.css`:

```css
/* Slightly wider reading column */
.container {
  max-width: 42rem;
}

/* Softer link color */
a {
  color: #0066cc;
}

/* More space before section headings */
main h2 {
  margin-top: 2.5rem;
}
```

## Default layout

| Element | Behavior |
|---------|----------|
| `.container` | Centered column, `max-width: 48rem` |
| `body` | System sans-serif stack, black on white |
| Links | Blue `#1d4ed8` |
| `.site-header` | Three-column grid: brand left, nav centered, social links right |
| `main` | Section headings (`h2`) with horizontal rules; project lists with optional meta |
| `footer` | Centered, subscribe + powered-by lines |
| `.blog-posts` | Post links separated by horizontal rules |
| `.project-list` | Homepage “recent projects” with title link + muted meta line |
| `.highlight` | Fenced code blocks with Pygments syntax colors and horizontal scroll |

Inspect `app/static/style.css` for all selectors.

## Template structure

Templates use Jinja2 inheritance:

```
base.html          # <html>, <head>, header, nav, footer
├── home.html      # Homepage body + post lists
├── page.html      # Static pages (projects, etc.)
├── blog.html      # Blog index + HTMX search
└── post.html      # Single post <article>
```

Partials:

- `partials/seo_head.html` — meta, Open Graph, JSON-LD
- `partials/post_list.html` — HTMX blog list items

To change HTML structure, edit templates in `app/templates/`. See [Extending Koji](extending.md).

## Panda branding

Override in `site.yaml`:

```yaml
panda_face: "( ◕ ᴥ ◕ )"
panda_small: "( •ᴥ• )"
```

## Dark mode

Koji does not include dark mode by default. Add it in `custom.css`:

```css
@media (prefers-color-scheme: dark) {
  body {
    background: #111;
    color: #eee;
  }
  a {
    color: #6af;
  }
  .site-brand {
    color: #eee;
  }
  main pre,
  .highlight,
  main p code,
  main li code {
    background: #222;
  }
}
```

## Custom fonts

```css
@import url("https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,700&display=swap");

body {
  font-family: "Literata", Georgia, serif;
}
```

Prefer self-hosting fonts in `app/static/` for privacy and performance.

## Social preview images

Set a default in `site.yaml`:

```yaml
og_image: https://yourdomain.com/static/og.png
```

Per-post override:

```yaml
image: https://yourdomain.com/static/post-image.png
```

Recommended size: **1200×630** px for Open Graph.

## Footer

Hide the subscribe line:

```yaml
footer_subscribe: false
```

Hide “Powered by Koji” (allowed, but we appreciate it if you keep it on):

```yaml
powered_by: false
```

See [Powered by Koji](attribution.md).

## Advanced: replace default CSS entirely

Not recommended for upgrades, but possible:

1. Copy `app/static/style.css` to `content/custom.css`
2. Modify heavily
3. Optionally remove or empty `app/static/style.css` in your fork

Better approach: keep the default and layer overrides in `custom.css`.

## Next

- [Extending Koji](extending.md) — new templates and routes
- [SEO](seo.md) — `theme-color`, og images
