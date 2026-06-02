from __future__ import annotations

from app.config import SiteConfig, content_root
from app.content import ContentStore, Page, Post
from app.seo import absolute_url


def _read_static(name: str) -> str | None:
    path = content_root() / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def _link_line(name: str, url: str, note: str = "") -> str:
    if note:
        return f"- [{name}]({url}): {note}"
    return f"- [{name}]({url})"


def _page_md_url(site: SiteConfig, slug: str) -> str:
    if slug == "home":
        return absolute_url(site, "/index.md")
    return absolute_url(site, f"/{slug}.md")


def _post_md_url(site: SiteConfig, post: Post) -> str:
    return absolute_url(site, f"/blog/{post.slug}.md")


def render_llms_txt(store: ContentStore) -> str:
    static = _read_static("llms.txt")
    if static is not None:
        return static

    site = store.site
    llms = site.llms
    lines = [f"# {site.title}", ""]

    summary = llms.summary or site.tagline or site.title
    lines.append(f"> {summary}")
    lines.append("")

    details = llms.details.strip()
    if details:
        lines.extend(details.splitlines())
        lines.append("")

    lines.append("## Pages")
    for slug, label in (("home", "Home"), ("projects", "Projects")):
        page = store.page(slug)
        if not page:
            continue
        note = page.description or label
        lines.append(_link_line(page.title or label, _page_md_url(site, slug), note))
    lines.append("")

    lines.append("## Blog")
    for post in store.published_posts():
        note = post.description or post.title
        lines.append(_link_line(post.title, _post_md_url(site, post), note))
    lines.append("")

    lines.append("## Feeds")
    lines.append(_link_line("Atom feed", absolute_url(site, "/atom.xml"), "Latest posts"))
    lines.append(_link_line("Full markdown export", absolute_url(site, "/llms-full.txt"), "All pages and posts"))
    lines.append("")

    optional_items = list(llms.optional_links)
    if optional_items:
        lines.append("## Optional")
        for link in optional_items:
            lines.append(_link_line(link.name, link.url, link.note))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_llms_full_txt(store: ContentStore) -> str:
    static = _read_static("llms-full.txt")
    if static is not None:
        return static

    site = store.site
    parts = [
        f"# {site.title}",
        "",
        f"> {site.tagline or site.title}",
        "",
        "Complete markdown export for LLM context.",
        "",
    ]

    for slug in ("home", "projects"):
        page = store.page(slug)
        if page:
            parts.extend(_format_section(page.title, page.raw_markdown))

    for post in store.published_posts():
        body = post.raw_markdown
        header = f"Published: {post.iso_date}" if post.date.year > 1970 else ""
        if post.description:
            header = f"{post.description}\n\n{header}".strip()
        parts.extend(_format_section(post.title, body, header))

    return "\n".join(parts).rstrip() + "\n"


def _format_section(title: str, body: str, preamble: str = "") -> list[str]:
    lines = ["---", "", f"# {title}", ""]
    if preamble:
        lines.extend([preamble, ""])
    lines.extend([body.strip(), ""])
    return lines


def format_page_markdown(page: Page) -> str:
    lines = [f"# {page.title}", ""]
    if page.description:
        lines.extend([page.description, ""])
    lines.append(page.raw_markdown.strip())
    return "\n".join(lines) + "\n"


def format_post_markdown(post: Post) -> str:
    lines = [f"# {post.title}", ""]
    if post.description:
        lines.extend([post.description, ""])
    if post.date.year > 1970:
        lines.append(f"*Published {post.date.strftime('%Y-%m-%d')}*")
        lines.append("")
    lines.append(post.raw_markdown.strip())
    return "\n".join(lines) + "\n"
