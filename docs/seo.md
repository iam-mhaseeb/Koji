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
```

### Why `url` matters

Every canonical link, sitemap entry, feed link, and Open Graph URL is built from `url`. **Wrong value = wrong SEO everywhere.**

- Development: `http://localhost:8000`
- Production: `https://yourdomain.com` (HTTPS, no trailing slash)

## Per-page SEO

In `content/pages/*.md`:

```yaml
---
title: Now
description: What I'm focused on in 2026 — projects, learning, and goals.
image: https://yourdomain.com/static/now-og.png
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
| Now, Projects | `WebPage` |
| Blog index | `Blog` |
| Blog post | `BlogPosting` |

Posts include `datePublished`, `dateModified` (when set), `author`, and `headline`.

## Indexing rules

| URL pattern | Robots behavior |
|-------------|-----------------|
| Normal pages & posts | `index, follow` (from `site.yaml`) |
| `/blog?q=...` | `noindex, follow` (search duplicates) |
| `/blog/partials/...` | `X-Robots-Tag: noindex` (HTMX fragments) |
| `draft: true` posts | Excluded from sitemap; URL returns 404 |

## Launch checklist

Before announcing your site:

- [ ] `url` is your production HTTPS domain
- [ ] `tagline` and homepage `description` are set
- [ ] `og_image` exists and loads in a browser
- [ ] Every public post has `description`
- [ ] `/robots.txt` shows correct `Sitemap:` line
- [ ] `/sitemap.xml` lists all important URLs
- [ ] [Google Search Console](https://search.google.com/search-console): add property, verify via `google_site_verification`, submit sitemap
- [ ] Test one URL with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Share a post link in Slack/iMessage — preview looks correct
- [ ] Atom feed works in a reader

## Verifying locally

```bash
curl -s http://localhost:8000/ | grep -E 'canonical|og:title|application/ld\+json'
curl -s http://localhost:8000/sitemap.xml | head -30
curl -s http://localhost:8000/robots.txt
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
