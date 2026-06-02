# Configuration

All site-wide settings live in **`content/site.yaml`**. Koji reads this file at startup and caches the result until the process restarts.

## Full example

```yaml
title: "Your Name's blog"
author: Your Name
tagline: Portfolio and essays about building software.
email: you@example.com
url: https://yourdomain.com
locale: en

# Branding
panda_face: "( ◕ ᴥ ◕ )"
panda_small: "( •ᴥ• )"

# Homepage lists
recent_posts_count: 5
recent_projects:
  - title: My App
    meta: "2024 – Present · Side project"
    url: /projects
popular_slugs:
  - my-best-post
  - another-hit

# Navigation (order matters)
nav:
  - label: Home
    href: /
  - label: Projects
    href: /projects
  - label: Blog
    href: /blog

social:
  - label: GitHub
    url: https://github.com/yourname
  - label: LinkedIn
    url: https://www.linkedin.com/in/yourname
  - label: Email
    url: mailto:you@example.com

# Footer
footer_subscribe: true
powered_by: true
koji_url: https://github.com/your-org/koji

# SEO
og_image: https://yourdomain.com/static/og.png
author_url: https://github.com/yourname
twitter_site: "@yourhandle"
twitter_creator: "@yourhandle"
theme_color: "#ffffff"
google_site_verification: "your-google-token"
bing_site_verification: "your-bing-token"
robots: index, follow

# llms.txt
llms:
  summary: One-line site summary for AI assistants.
  details: |
    Optional paragraphs with guidance for LLMs.
  optional:
    - name: GitHub
      url: https://github.com/yourname
      note: Source code and projects
```

## Field reference

### Identity

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `title` | Yes | `My blog` | Site name in header, titles, feeds |
| `author` | Yes | `Developer` | Author name in feeds and schema.org |
| `tagline` | No | `""` | Short description; default SEO/llms fallback when a page has no `description` |
| `email` | No | `""` | Mailto links in footer and `rel="me"` in `<head>` when set |
| `url` | No | `http://localhost:8000` | **Canonical base URL** — must be production HTTPS URL when live |
| `locale` | No | `en` | HTML `lang` attribute and `og:locale` |

### Branding

| Key | Default | Description |
|-----|---------|-------------|
| `panda_face` | `( ◕ ᴥ ◕ )` | Shown next to site title in header |
| `panda_small` | `( •ᴥ• )` | Shown in “Powered by Koji” footer |

### Homepage

| Key | Default | Description |
|-----|---------|-------------|
| `recent_posts_count` | `5` | How many posts appear under “My most recent posts” |
| `recent_projects` | `[]` | List of `{ title, url, meta? }` for “My recent projects” on the homepage |
| `popular_slugs` | `[]` | Ordered list of post slugs for “My most popular posts”. If empty, uses posts with `popular: true` in frontmatter (max 5) |
| `social` | `[]` | Header links on the right: `{ label, url }` (e.g. GitHub, LinkedIn, Email). External URLs get `rel="noopener noreferrer"`. |

### Navigation

| Key | Description |
|-----|-------------|
| `nav` | List of `{ label, href }` items. Default: Home, Projects, Blog |

You can add external links:

```yaml
nav:
  - label: Home
    href: /
  - label: GitHub
    href: https://github.com/you
```

### Footer

| Key | Default | Description |
|-----|---------|-------------|
| `footer_subscribe` | `true` | Show “Subscribe via rss or say hello” line |
| `powered_by` | `true` | Show “Powered by Koji” line (please leave on if you can) |
| `koji_url` | GitHub URL | Link target for “Koji” in footer |

See [Powered by Koji](attribution.md) — we appreciate leaving `powered_by: true`, but it’s optional.

### SEO

| Key | Description |
|-----|-------------|
| `og_image` | Default Open Graph / Twitter image (absolute URL or path like `/static/og.png`) |
| `author_url` | Author profile URL (`rel="author"`) |
| `twitter_site` | Site Twitter handle, e.g. `@handle` |
| `twitter_creator` | Creator handle for Twitter cards |
| `theme_color` | Browser chrome color meta tag |
| `google_site_verification` | Google Search Console verification string |
| `bing_site_verification` | Bing Webmaster verification string |
| `robots` | Default robots meta, e.g. `index, follow` |

See [SEO guide](seo.md) for details.

### llms.txt

| Key | Description |
|-----|-------------|
| `llms.summary` | Blockquote summary in generated `/llms.txt` (falls back to `tagline`) |
| `llms.details` | Extra markdown paragraphs after the summary |
| `llms.optional` | List of `{ name, url, note? }` under the “Optional” section |

See [llms.txt guide](llms-txt.md).

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KOJI_CONTENT_DIR` | `./content` (relative to project root) | Absolute path to your content directory |

Useful for Docker and monorepos:

```bash
export KOJI_CONTENT_DIR=/var/www/my-blog/content
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Files that complement site.yaml

| Path | Purpose |
|------|---------|
| `content/custom.css` | Theme overrides (auto-linked when file exists) |
| `content/llms.txt` | Replaces auto-generated `/llms.txt` |
| `content/llms-full.txt` | Replaces auto-generated `/llms-full.txt` |

## Reloading configuration

Koji loads config once per process. After editing `site.yaml`:

- **Development:** restart `uvicorn` (Ctrl+C and run again).
- **Docker:** `docker compose restart` (or redeploy).
- **Production:** restart your systemd service or rolling deploy.

Markdown posts and pages are also cached in memory at first access. Restart to pick up bulk content changes during development; for production, a restart after deploy is the simple approach.

## Next

- [Content guide](content.md) — per-page and per-post frontmatter
- [Theming](theming.md) — visual customization
