# SEO

Koji generates search- and social-friendly metadata automatically. You configure identity in `site.yaml` and fine-tune per page/post in frontmatter.

## What Koji generates

| Output | URL | Purpose |
|--------|-----|---------|
| Title & meta description | Every HTML page | Search snippets |
| Canonical URL | `<link rel="canonical">` | Avoid duplicate content |
| Robots meta | `<meta name="robots">` | Index/noindex control |
| Open Graph | `og:*` tags | Facebook, LinkedIn, iMessage, etc. |
| Twitter Cards | `twitter:*` tags | Twitter/X previews |
| JSON-LD | `<script type="application/ld+json">` | Google rich results |
| Sitemap | `/sitemap.xml` | Crawl discovery |
| Robots file | `/robots.txt` | Crawler rules + sitemap pointer |
| Atom feed | `/atom.xml` | Syndication (also `/rss.xml`, `/feed.xml`) |
| llms.txt index | `/llms.txt` | AI/tool discovery ([llms.txt spec](https://llmstxt.org/)) |
| Markdown exports | `/index.md`, `/projects.md`, `/blog/{slug}.md` | Clean markdown for tools and RAG (see [llms.txt guide](llms-txt.md)) |

Every HTML page also includes `<link rel="alternate">` for the Atom feed, sitemap, and llms.txt index in `<head>`.

## Site-wide configuration

In `content/site.yaml`:

```yaml
url: https://yourdomain.com
tagline: One sentence describing your site.
og_image: https://yourdomain.com/static/og.png
author_url: https://github.com/you
twitter_site: "@you"
twitter_creator: "@you"
theme_color: "#ffffff"
google_site_verification: "paste-from-search-console"
bing_site_verification: "paste-from-bing"
robots: index, follow

# Homepage lists (not SEO tags, but affect what appears on /)
recent_projects:
  - title: My project
    url: /projects
social:
  - label: GitHub
    url: https://github.com/you
```

See [Configuration](configuration.md) for all keys. Social links are navigation only; they are not added to structured data automatically.

### Why `url` matters

Every canonical link, sitemap entry, feed link, and Open Graph URL is built from `url`. **Wrong value = wrong SEO everywhere.**

- Development: `http://localhost:8000`
- Production: `https://yourdomain.com` (HTTPS, no trailing slash)

## Page titles

| Page | `<title>` format |
|------|------------------|
| Home (`/`) | `site.title` only |
| Projects, Blog index, posts | `{page title} — {site.title}` when the combined string fits (~60 characters); otherwise the page title alone |

The visible **Projects** heading on `/projects` is an `<h2>` in the template; the browser tab and Open Graph title still come from frontmatter `title`.

## Per-page SEO

In `content/pages/*.md`:

```yaml
---
title: Projects
description: Open source tools, side projects, and past work.
image: https://yourdomain.com/static/projects-og.png
noindex: false
---
```

## Per-post SEO

In `content/posts/*.md`:

```yaml
---
title: My post
slug: my-post
date: 2026-06-01
description: A compelling 1–2 sentence summary for Google and social cards.
image: https://yourdomain.com/static/post-og.png
modified: 2026-06-10
noindex: false
---
```

### Description best practices

- **Length:** aim for 120–160 characters
- **Content:** summarize the post honestly; don't keyword-stuff
- **Fallback:** if omitted, Koji uses `tagline` or the first text stripped from the post body

### Images

- Default: `og_image` from `site.yaml`
- Override per post/page with `image`
- Use absolute URLs in production
- Recommended: **1200×630** px, JPG or PNG

## JSON-LD types

| Page | Schema type |
|------|-------------|
| Home | `WebSite` |
| Projects | `WebPage` |
| Blog index | `Blog` |
| Blog post | `BlogPosting` |

Posts include `datePublished`, `dateModified` (when set), `author`, and `headline`.

Blog posts use `og:type` **article** with `article:published_time`, `article:modified_time` (when set), and `article:author`.

### Home page description

Set `description` in `content/pages/home.md` frontmatter. It becomes the meta description and Open Graph text on `/`. If omitted, Koji falls back to `tagline`, then stripped body text from `home.md`.

## Indexing rules

| URL pattern | Robots behavior |
|-------------|-----------------|
| Normal pages & posts | `index, follow` (from `site.yaml`) |
| `/blog?q=...` | `noindex, follow` (search duplicates) |
| `/blog/partials/...` | `X-Robots-Tag: noindex` (HTMX fragments) |
| `draft: true` posts | Excluded from sitemap, feeds, and llms exports; URL returns 404 |
| `/index.md`, `/projects.md`, `/blog/{slug}.md` | Same indexing as HTML counterparts |
| `/llms.txt`, `/llms-full.txt` | Allowed; linked from `robots.txt` comment |

## Sitemap contents

`/sitemap.xml` includes:

- `/` (daily)
- `/projects` (monthly)
- `/blog` (weekly)
- Each published post at `/blog/{slug}` with `lastmod` from `modified` or `date`

Draft posts and removed pages (e.g. there is no `/now` route) are omitted.

## Launch checklist

Before announcing your site:

- [ ] `url` is your production HTTPS domain
- [ ] `tagline` and homepage `description` are set
- [ ] `og_image` exists and loads in a browser
- [ ] Every public post has `description`
- [ ] `content/pages/home.md` and `projects.md` have `description` in frontmatter
- [ ] `/robots.txt` shows correct `Sitemap:` line and mentions `/llms.txt`
- [ ] `/sitemap.xml` lists `/`, `/projects`, `/blog`, and all published posts
- [ ] `/llms.txt` lists your pages and posts (or your manual `content/llms.txt` is complete)
- [ ] [Google Search Console](https://search.google.com/search-console): add property, verify via `google_site_verification`, submit sitemap
- [ ] Test one URL with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Share a post link in Slack/iMessage — preview looks correct
- [ ] Atom feed works in a reader

## Verifying locally

```bash
curl -s http://localhost:8000/ | grep -E 'canonical|og:title|application/ld\+json|llms.txt'
curl -s http://localhost:8000/blog/sharing-code-in-posts | grep -E 'og:type|article:published'
curl -s http://localhost:8000/sitemap.xml | head -30
curl -s http://localhost:8000/robots.txt
curl -s http://localhost:8000/llms.txt | head -20
```

## Common issues

| Problem | Fix |
|---------|-----|
| Wrong domain in shares | Set `url` in `site.yaml` and restart |
| No image in preview | Add `og_image` or per-post `image` |
| Post not in Google | Wait; submit sitemap; check `draft` and `noindex` |
| Duplicate titles | Customize `title` in frontmatter |

## Next

- [llms.txt](llms-txt.md) — AI crawlers and assistants
- [Configuration](configuration.md) — all SEO-related keys
