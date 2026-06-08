# llms.txt

Koji implements the [llms.txt proposal](https://llmstxt.org/) so AI assistants and tools can discover your content in **clean markdown** without parsing HTML.

## Endpoints

| URL | Purpose |
|-----|---------|
| `/llms.txt` | Curated index (spec format) |
| `/llms-full.txt` | All pages and posts in one file |
| `/index.md` | Home markdown |
| `/{page}.md` | Page markdown (`/projects.md`, etc.) |
| `/blog/{slug}.md` | Post markdown |

## Auto-generated `/llms.txt`

Unless you provide `content/llms.txt`, Koji builds:

```markdown
# Your Site Title

> Summary from llms.summary or site tagline

(Optional details from site.yaml)

## Pages
- [Home](https://yourdomain.com/index.md): ...
- [Projects](https://yourdomain.com/projects.md): ...

## Blog
- [Post title](https://yourdomain.com/blog/slug.md): description

## Feeds
- [Atom feed](https://yourdomain.com/atom.xml): Latest posts
- [Full markdown export](https://yourdomain.com/llms-full.txt): All pages and posts

## Optional
- [External link](https://...): note
```

The **Optional** section comes from `site.yaml` (see below). Per the spec, agents may skip Optional links when context is limited.

## Configuration

In `content/site.yaml`:

```yaml
llms:
  summary: One-line description for the blockquote.
  details: |
    Free-form paragraphs with instructions for LLMs.
    Example: prefer /blog/{slug}.md URLs over HTML.
  optional:
    - name: GitHub
      url: https://github.com/you
      note: Source code
    - name: API docs
      url: https://docs.example.com/llms.txt
      note: External documentation
```

| Key | Description |
|-----|-------------|
| `summary` | Blockquote under H1; defaults to `tagline` |
| `details` | Extra markdown paragraphs (no headings) |
| `optional` | Links under `## Optional` |

## Manual override

Place a file at **`content/llms.txt`** to replace auto-generation entirely. You are responsible for following the spec format and using **absolute URLs**.

Similarly, **`content/llms-full.txt`** replaces the auto-generated full export.

## Auto-generated `/llms-full.txt`

Concatenates all pages and published posts with separators:

```markdown
# Site Title

> Tagline

---

# Page Title

(page body)

---

# Post Title

(post body)
```

Draft posts are excluded.

## Markdown export format

`/blog/my-post.md` returns:

```markdown
# Post Title

Description from frontmatter.

*Published 2026-06-01*

(post markdown body)
```

Pages use `# Title` plus body from `content/pages/`.

## Discoverability

- `robots.txt` includes a comment pointing to `/llms.txt`
- HTML `<head>` includes `<link rel="alternate" type="text/markdown" href="/llms.txt" />`

## Use cases

| Audience | What to use |
|----------|-------------|
| ChatGPT / Claude with browsing | Give them `https://yourdomain.com/llms.txt` |
| RAG pipelines | Fetch `/llms-full.txt` or individual `.md` URLs |
| Documentation tools | Link `optional` to external llms.txt files |

## Testing

```bash
curl -s http://localhost:8000/llms.txt
curl -s http://localhost:8000/llms-full.txt | head -50
curl -s http://localhost:8000/blog/your-slug.md
```

## Next

- [Content guide](content.md) — writing posts that export well
- [Configuration](configuration.md) — all `llms` keys
