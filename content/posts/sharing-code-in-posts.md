---
title: Sharing code in your posts
slug: sharing-code-in-posts
date: 2026-06-02
description: How Koji renders fenced code blocks, inline snippets, and syntax highlighting for developer blogs.
popular: true
---

If you write for developers, most posts need **code**. Koji uses Python-Markdown with **Pygments** highlighting — fence your blocks with a language tag and it just works.

## Inline code

Use backticks for `pip install koji`, environment variables like `KOJI_CONTENT_DIR=/var/www/content`, and paths such as `content/posts/my-post.md`.

## Python

A tiny route handler pattern:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/blog/{slug}")
async def blog_post(slug: str):
  post = store.post_by_slug(slug)
  if not post:
    raise HTTPException(status_code=404, detail="Post not found")
  return templates.TemplateResponse("post.html", {"post": post})
```

## TypeScript

```typescript
type Post = {
  slug: string;
  title: string;
  date: string;
};

async function fetchPost(slug: string): Promise<Post> {
  const res = await fetch(`/blog/${slug}.md`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

## Shell

```bash
cd heykoji.com
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## JSON config

```json
{
  "title": "My blog",
  "recent_posts_count": 5,
  "nav": [
    { "label": "Home", "href": "/" },
    { "label": "Blog", "href": "/blog" }
  ]
}
```

## Tips

1. Always set the language on fenced blocks: ` ```python ` not bare ` ``` `.
2. Keep lines under ~100 characters when you can — blocks scroll horizontally on small screens.
3. Prefer **markdown exports** (`/blog/your-slug.md`) when sharing with tools or LLMs.

Happy shipping.
