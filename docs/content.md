# Content guide

Koji stores all public content as **markdown files with YAML frontmatter**. No admin UI, no database — just files you can edit in any editor and version with git.

## Directory structure

```
content/
├── site.yaml
├── custom.css              # optional
├── llms.txt                # optional override
├── llms-full.txt           # optional override
├── pages/
│   ├── home.md
│   └── projects.md
└── posts/
    ├── 2026-06-01-my-post.md
    └── another-post.md
```

The **filename** of a post (e.g. `2026-06-01-my-post.md`) is only used as a fallback slug. Prefer setting `slug` explicitly in frontmatter.

## Pages

Pages live in `content/pages/`. Each file maps to a fixed route:

| File | Route |
|------|-------|
| `home.md` | `/` (body only; lists are automatic) |
| `projects.md` | `/projects` |

### Page frontmatter

```yaml
---
title: Projects          # Page heading and browser title
description: What this page is about.   # SEO meta description
image: /static/projects-og.png          # Optional og:image for this page
noindex: true                             # Optional: hide from search engines
canonical: https://other.com/projects     # Optional: override canonical URL
---
```

The markdown **body** is rendered below the template page heading (`<h2>` on static pages). **SEO titles** and Open Graph still use frontmatter `title`, not the first markdown heading.

`home.md` has no extra template heading — put your main `<h1>` in the markdown body.

### Home page special behavior

`home.md` powers the intro on `/`. Koji **automatically appends**:

- “My recent projects” — from `recent_projects` in `site.yaml`
- “My most recent posts” — from `recent_posts_count` in `site.yaml`
- “My most popular posts” — from `popular_slugs` or `popular: true` posts

You don't write those lists in markdown; they're generated.

## Blog posts

Posts live in `content/posts/*.md`.

### Post frontmatter

```yaml
---
title: The title shown on the page
slug: url-slug              # URL: /blog/url-slug
date: 2026-06-01            # ISO date; used for sorting and feeds
description: Summary for SEO, Atom, and social cards.
popular: true               # Fallback for homepage “popular” list
draft: false                # true = hidden from blog index and feeds
image: https://yourdomain.com/img.png   # og:image for this post
modified: 2026-06-15        # Optional: article:modified_time
noindex: true               # Optional: exclude from search indexing
canonical: https://...      # Optional: canonical URL override
---
```

### Drafts

Set `draft: true` to hide a post from:

- `/blog` index
- Atom feed
- Recent/popular lists
- Sitemap
- llms.txt exports

Direct URL `/blog/{slug}` also returns **404** for drafts.

### Dates

- Use `YYYY-MM-DD` format.
- Posts without a valid date sort to the bottom (internal sentinel date).
- `modified` / `updated` in frontmatter sets `dateModified` in structured data and Atom.

### Slugs

- **Recommended:** `slug: my-post` in frontmatter.
- **Fallback:** filename without `.md` (e.g. `my-post.md` → `my-post`).

Avoid changing slugs after publishing; old links will break unless you add redirects (see [Extending](extending.md)).

## Markdown features

Koji uses Python-Markdown with:

- Fenced code blocks with syntax highlighting (`.highlight` class)
- Tables
- Standard markdown (headings, lists, links, blockquotes, images)

### Images

```markdown
![Alt text](/static/photo.jpg)
```

Place assets in `app/static/` (bundled with the app) or host externally. For user images, add e.g. `app/static/images/` in your fork.

### Code blocks

Always tag the language on the opening fence so Pygments can highlight correctly:

````markdown
```python
def hello():
    return "world"
```
````

Supported languages include `python`, `javascript`, `typescript`, `bash`, `json`, `yaml`, `rust`, `go`, and [many more](https://pygments.org/languages/) Pygments supports. Inline code uses single backticks: `` `npm install` ``.

If you omit the language tag, Koji tries to guess it (`guess_lang`). Tagging the language is still recommended for accurate highlighting.

Rendered output uses the `.highlight` wrapper with Pygments token colors and horizontal scroll on narrow screens. Example: `/blog/sharing-code-in-posts`.

### Internal links

```markdown
Read [my other post](/blog/other-slug).
```

## Markdown exports (for LLMs and tools)

Every page and post has a **clean markdown URL**:

| HTML | Markdown |
|------|----------|
| `/` | `/index.md` |
| `/projects` | `/projects.md` |
| `/blog/{slug}` | `/blog/{slug}.md` |

Exports include a title heading and body; posts also show description and publish date when set.

## Popular posts logic

1. If `popular_slugs` is set in `site.yaml`, those slugs are used **in that order**.
2. Otherwise, up to **5** published posts with `popular: true` in frontmatter.

## Search

The blog index (`/blog`) supports client-side search via HTMX:

- Typing in the search box filters posts by **title** and **description** (case-insensitive).
- `/blog?q=term` works without JavaScript (full page with filtered list).
- Search result pages are `noindex` for SEO.

## Workflow tips

### Edit in your editor, preview locally

```bash
uvicorn app.main:app --reload
```

### Content in a separate repo

Point `KOJI_CONTENT_DIR` at a cloned content repository:

```bash
export KOJI_CONTENT_DIR=/home/you/my-blog-content
```

### Pre-publish checklist for a post

- [ ] `title`, `slug`, `date`, `description` set
- [ ] `draft: false` (or remove draft key)
- [ ] Proofread on `/blog/{slug}`
- [ ] Check `/blog/{slug}.md` if you use llms.txt consumers

## Next

- [Theming](theming.md) — style your content
- [SEO](seo.md) — descriptions and social previews
- [llms.txt](llms-txt.md) — AI-oriented exports
