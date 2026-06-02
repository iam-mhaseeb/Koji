from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension

from app.config import SiteConfig, content_root, load_site_config


@dataclass
class Post:
    slug: str
    title: str
    date: datetime
    html: str
    description: str = ""
    popular: bool = False
    draft: bool = False

    @property
    def iso_date(self) -> str:
        return self.date.strftime("%Y-%m-%d")


@dataclass
class Page:
    slug: str
    title: str
    html: str
    raw_markdown: str = ""


_md = markdown.Markdown(
    extensions=[
        "meta",
        FencedCodeExtension(),
        CodeHiliteExtension(css_class="highlight", guess_lang=False),
        TableExtension(),
    ],
    output_format="html5",
)


def _render_md(text: str) -> str:
    _md.reset()
    return _md.convert(text)


def _parse_date(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if value is None:
        return datetime.min
    return datetime.fromisoformat(str(value).replace("Z", "+00:00").split("T")[0])


class ContentStore:
    def __init__(self, root: Path | None = None, site: SiteConfig | None = None):
        self.root = root or content_root()
        self.site = site or load_site_config(self.root)
        self._posts: list[Post] | None = None
        self._pages: dict[str, Page] | None = None

    def reload(self) -> None:
        self._posts = None
        self._pages = None

    def posts(self) -> list[Post]:
        if self._posts is None:
            self._posts = self._load_posts()
        return self._posts

    def published_posts(self) -> list[Post]:
        return [p for p in self.posts() if not p.draft]

    def post_by_slug(self, slug: str) -> Post | None:
        for p in self.published_posts():
            if p.slug == slug:
                return p
        return None

    def page(self, slug: str) -> Page | None:
        if self._pages is None:
            self._pages = self._load_pages()
        return self._pages.get(slug)

    def recent_posts(self, limit: int | None = None) -> list[Post]:
        limit = limit or self.site.recent_posts_count
        published = sorted(self.published_posts(), key=lambda p: p.date, reverse=True)
        return published[:limit]

    def popular_posts(self) -> list[Post]:
        by_slug = {p.slug: p for p in self.published_posts()}
        result: list[Post] = []
        for slug in self.site.popular_slugs:
            if slug in by_slug:
                result.append(by_slug[slug])
        if result:
            return result
        return [p for p in self.published_posts() if p.popular][:5]

    def search_posts(self, query: str) -> list[Post]:
        q = query.strip().lower()
        if not q:
            return self.published_posts()
        return [
            p
            for p in self.published_posts()
            if q in p.title.lower() or q in p.description.lower()
        ]

    def _load_posts(self) -> list[Post]:
        posts_dir = self.root / "posts"
        if not posts_dir.is_dir():
            return []

        items: list[Post] = []
        for path in sorted(posts_dir.glob("*.md")):
            post = self._read_post(path)
            if post:
                items.append(post)
        return sorted(items, key=lambda p: p.date, reverse=True)

    def _read_post(self, path: Path) -> Post | None:
        raw = path.read_text(encoding="utf-8")
        doc = frontmatter.loads(raw)
        meta = doc.metadata or {}
        slug = meta.get("slug") or path.stem
        title = meta.get("title") or slug.replace("-", " ").title()
        return Post(
            slug=slug,
            title=title,
            date=_parse_date(meta.get("date")),
            html=_render_md(doc.content),
            description=str(meta.get("description") or ""),
            popular=bool(meta.get("popular", False)),
            draft=bool(meta.get("draft", False)),
        )

    def _load_pages(self) -> dict[str, Page]:
        pages_dir = self.root / "pages"
        pages: dict[str, Page] = {}
        if not pages_dir.is_dir():
            return pages

        for path in pages_dir.glob("*.md"):
            slug = path.stem
            raw = path.read_text(encoding="utf-8")
            doc = frontmatter.loads(raw)
            meta = doc.metadata or {}
            title = meta.get("title") or slug.replace("-", " ").title()
            pages[slug] = Page(
                slug=slug,
                title=title,
                html=_render_md(doc.content),
                raw_markdown=doc.content,
            )
        return pages
