from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import datetime
from xml.sax.saxutils import escape

from app.config import SiteConfig
from app.content import ContentStore, Page, Post

MAX_DESCRIPTION_LEN = 160
MAX_TITLE_LEN = 60


@dataclass
class SeoMeta:
    title: str
    description: str
    canonical_url: str
    og_type: str = "website"
    og_image: str | None = None
    robots: str = "index, follow"
    json_ld: list[dict] = field(default_factory=list)
    published: datetime | None = None
    modified: datetime | None = None
    article_author: str | None = None


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def truncate_description(text: str, limit: int = MAX_DESCRIPTION_LEN) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return f"{cut}…" if cut else text[:limit]


def absolute_url(site: SiteConfig, path: str) -> str:
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{site.url}{path}"


def resolve_image(site: SiteConfig, image: str | None) -> str | None:
    if not image:
        return site.og_image or None
    if image.startswith("http"):
        return image
    return absolute_url(site, image)


def _description(primary: str, fallback_html: str, site: SiteConfig) -> str:
    if primary.strip():
        return truncate_description(primary)
    if site.tagline.strip():
        return truncate_description(site.tagline)
    if fallback_html.strip():
        return truncate_description(strip_html(fallback_html))
    return site.title


def _title(page_title: str, site: SiteConfig, *, standalone: bool = False) -> str:
    if standalone or page_title == site.title:
        return page_title
    combined = f"{page_title} — {site.title}"
    if len(combined) <= MAX_TITLE_LEN:
        return combined
    return page_title


def _person_schema(site: SiteConfig) -> dict:
    person: dict = {"@type": "Person", "name": site.author}
    if site.author_url:
        person["url"] = site.author_url
    if site.email:
        person["email"] = site.email
    return person


def _website_part(site: SiteConfig) -> dict:
    return {"@type": "WebSite", "name": site.title, "url": site.url}


def _webpage_schema(name: str, description: str, url: str, site: SiteConfig) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": description,
        "url": url,
        "isPartOf": _website_part(site),
    }


def _breadcrumb_schema(site: SiteConfig, crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": crumb_url,
            }
            for index, (name, crumb_url) in enumerate(crumbs, start=1)
        ],
    }


def _parse_json_ld_meta(value) -> list[dict]:
    if not value:
        return []
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _merge_json_ld(*groups: list[dict]) -> list[dict]:
    merged: list[dict] = []
    for group in groups:
        merged.extend(group)
    return merged


def _website_schema(site: SiteConfig) -> dict:
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site.title,
        "url": site.url,
        "description": site.tagline or site.title,
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": absolute_url(site, "/blog?q={search_term_string}"),
            },
            "query-input": "required name=search_term_string",
        },
    }
    if site.author:
        schema["author"] = _person_schema(site)
    return schema


def complete_seo_meta(seo: SeoMeta, site: SiteConfig) -> SeoMeta:
    """Fill in JSON-LD when a route passes SeoMeta without structured data."""
    if seo.json_ld:
        return seo

    if seo.og_type == "article" and seo.published:
        schema: dict = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": seo.title,
            "description": seo.description,
            "url": seo.canonical_url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": seo.canonical_url},
            "author": _person_schema(site),
            "publisher": {"@type": "Organization", "name": site.title, "url": site.url},
            "datePublished": _schema_date(seo.published),
        }
        if seo.modified and seo.modified.year > 1970:
            schema["dateModified"] = _schema_date(seo.modified)
        if seo.og_image:
            schema["image"] = [seo.og_image]
        return replace(seo, json_ld=[schema])

    page_name = seo.title.split(" — ", 1)[0]
    return replace(
        seo,
        json_ld=[
            _webpage_schema(page_name, seo.description, seo.canonical_url, site),
            _breadcrumb_schema(
                site,
                [(site.title, site.url + "/"), (page_name, seo.canonical_url)],
            ),
        ],
    )


def seo_for_home(site: SiteConfig, page: Page | None) -> SeoMeta:
    desc = _description(
        page.description if page else "",
        page.html if page else "",
        site,
    )
    return SeoMeta(
        title=site.title,
        description=desc,
        canonical_url=site.url + "/",
        og_type="website",
        og_image=resolve_image(site, page.image if page else None),
        json_ld=[_website_schema(site)],
    )


def _canonical(site: SiteConfig, path: str, override: str = "") -> str:
    if override:
        return override if override.startswith("http") else absolute_url(site, override)
    return absolute_url(site, path)


def seo_for_page(site: SiteConfig, page: Page, path: str) -> SeoMeta:
    heading = page.title
    desc = _description(page.description, page.html, site)
    url = _canonical(site, path, page.canonical)
    return SeoMeta(
        title=_title(heading, site),
        description=desc,
        canonical_url=url,
        og_type="website",
        og_image=resolve_image(site, page.image),
        robots="noindex, follow" if page.noindex else site.robots,
        json_ld=_merge_json_ld(
            [
                _webpage_schema(heading, desc, url, site),
                _breadcrumb_schema(
                    site,
                    [(site.title, site.url + "/"), (heading, url)],
                ),
            ],
            page.json_ld,
        ),
    )


def seo_for_blog_index(
    site: SiteConfig,
    query: str = "",
    posts: list[Post] | None = None,
) -> SeoMeta:
    desc = truncate_description(
        f"All posts from {site.author}. {site.tagline}".strip()
    )
    blog_url = absolute_url(site, "/blog")
    robots = "noindex, follow" if query.strip() else site.robots
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": f"{site.title} Blog",
        "url": blog_url,
        "description": desc,
        "author": _person_schema(site),
    }
    if posts and not query.strip():
        schema["blogPost"] = [
            {
                "@type": "BlogPosting",
                "headline": post.title,
                "url": absolute_url(site, f"/blog/{post.slug}"),
                "datePublished": _schema_date(post.date),
            }
            for post in posts
            if post.date.year > 1970
        ]
    return SeoMeta(
        title=_title("Blog", site),
        description=desc,
        canonical_url=blog_url,
        og_type="website",
        og_image=site.og_image,
        robots=robots,
        json_ld=[
            schema,
            _breadcrumb_schema(
                site,
                [(site.title, site.url + "/"), ("Blog", blog_url)],
            ),
        ],
    )


def seo_for_post(site: SiteConfig, post: Post) -> SeoMeta:
    desc = _description(post.description, post.html, site)
    url = _canonical(site, f"/blog/{post.slug}", post.canonical)
    modified = post.modified or post.date
    image = resolve_image(site, post.image)
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": desc,
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": _person_schema(site),
        "publisher": {"@type": "Organization", "name": site.title, "url": site.url},
        "datePublished": _schema_date(post.date),
    }
    if modified.year > 1970:
        schema["dateModified"] = _schema_date(modified)
    if image:
        schema["image"] = [image]

    return SeoMeta(
        title=_title(post.title, site),
        description=desc,
        canonical_url=url,
        og_type="article",
        og_image=image,
        robots="noindex, follow" if post.noindex else site.robots,
        json_ld=_merge_json_ld(
            [
                schema,
                _breadcrumb_schema(
                    site,
                    [
                        (site.title, site.url + "/"),
                        ("Blog", absolute_url(site, "/blog")),
                        (post.title, url),
                    ],
                ),
            ],
            post.json_ld,
        ),
        published=post.date if post.date.year > 1970 else None,
        modified=modified if modified.year > 1970 else None,
        article_author=site.author,
    )


def _schema_date(dt: datetime) -> str:
    if dt.tzinfo is None:
        return dt.strftime("%Y-%m-%d")
    return dt.date().isoformat()


def render_robots_txt(site: SiteConfig) -> str:
    return f"""User-agent: *
Allow: /

Disallow: /blog/partials/
Disallow: /health

Sitemap: {site.url}/sitemap.xml

# LLM-friendly site map: {site.url}/llms.txt
"""


def render_sitemap_xml(store: ContentStore) -> str:
    site = store.site
    urls: list[tuple[str, datetime | None, str]] = [
        (site.url + "/", None, "daily"),
    ]
    for page in store.indexable_static_pages():
        urls.append((absolute_url(site, f"/{page.slug}"), None, "monthly"))
    urls.append((absolute_url(site, "/blog"), None, "weekly"))
    for post in store.indexable_posts():
        lastmod = post.modified or post.date
        if lastmod.year <= 1970:
            lastmod = None
        urls.append((absolute_url(site, f"/blog/{post.slug}"), lastmod, "monthly"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod, changefreq in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        if lastmod and lastmod.year > 1970:
            lines.append(f"    <lastmod>{lastmod.date().isoformat()}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"
