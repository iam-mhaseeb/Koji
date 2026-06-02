from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PANDA_FACE = "( ◕ ᴥ ◕ )"
PANDA_SMALL = "( •ᴥ• )"


@dataclass
class NavItem:
    label: str
    href: str


@dataclass
class LlmsLink:
    name: str
    url: str
    note: str = ""


@dataclass
class LlmsConfig:
    summary: str = ""
    details: str = ""
    optional_links: list[LlmsLink] = field(default_factory=list)


@dataclass
class SiteConfig:
    title: str
    author: str
    tagline: str = ""
    email: str = ""
    location: str = ""
    url: str = "http://localhost:8000"
    panda_face: str = PANDA_FACE
    panda_small: str = PANDA_SMALL
    nav: list[NavItem] = field(default_factory=list)
    recent_posts_count: int = 5
    recent_posts_heading: str = "Latest writing"
    popular_posts_heading: str = "Reader favorites"
    popular_slugs: list[str] = field(default_factory=list)
    footer_subscribe: bool = True
    powered_by: bool = True
    koji_url: str = "https://github.com/heykoji/koji"
    has_custom_css: bool = False
    locale: str = "en"
    og_image: str = ""
    twitter_site: str = ""
    twitter_creator: str = ""
    author_url: str = ""
    robots: str = "index, follow"
    google_site_verification: str = ""
    bing_site_verification: str = ""
    theme_color: str = "#f6f5f2"
    llms: LlmsConfig = field(default_factory=LlmsConfig)

    @property
    def blog_title(self) -> str:
        return f"{self.title}"


def content_root() -> Path:
    env = os.environ.get("KOJI_CONTENT_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent / "content"


def load_site_config(root: Path | None = None) -> SiteConfig:
    root = root or content_root()
    path = root / "site.yaml"
    if not path.is_file():
        return _default_site_config()

    with path.open(encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}

    nav_raw = data.get("nav") or _default_nav()
    nav = [NavItem(label=n["label"], href=n["href"]) for n in nav_raw]

    has_custom = (root / "custom.css").is_file()
    return SiteConfig(
        title=data.get("title", "My blog"),
        author=data.get("author", "Developer"),
        tagline=data.get("tagline", ""),
        email=data.get("email", ""),
        location=data.get("location", ""),
        url=data.get("url", "http://localhost:8000").rstrip("/"),
        panda_face=data.get("panda_face", PANDA_FACE),
        panda_small=data.get("panda_small", PANDA_SMALL),
        nav=nav,
        recent_posts_count=int(data.get("recent_posts_count", 5)),
        recent_posts_heading=str(data.get("recent_posts_heading", "Latest writing")),
        popular_posts_heading=str(data.get("popular_posts_heading", "Reader favorites")),
        popular_slugs=list(data.get("popular_slugs") or []),
        footer_subscribe=bool(data.get("footer_subscribe", True)),
        powered_by=bool(data.get("powered_by", True)),
        koji_url=data.get("koji_url", "https://github.com/heykoji/koji"),
        has_custom_css=has_custom,
        locale=data.get("locale", "en"),
        og_image=data.get("og_image", ""),
        twitter_site=data.get("twitter_site", ""),
        twitter_creator=data.get("twitter_creator", ""),
        author_url=data.get("author_url", ""),
        robots=data.get("robots", "index, follow"),
        google_site_verification=data.get("google_site_verification", ""),
        bing_site_verification=data.get("bing_site_verification", ""),
        theme_color=data.get("theme_color", "#ffffff"),
        llms=_load_llms_config(data.get("llms") or {}),
    )


def _load_llms_config(data: dict[str, Any]) -> LlmsConfig:
    optional_raw = data.get("optional") or data.get("optional_links") or []
    optional_links = [
        LlmsLink(
            name=item["name"],
            url=item["url"],
            note=str(item.get("note") or ""),
        )
        for item in optional_raw
        if item.get("name") and item.get("url")
    ]
    return LlmsConfig(
        summary=str(data.get("summary") or ""),
        details=str(data.get("details") or ""),
        optional_links=optional_links,
    )


def _default_nav() -> list[dict[str, str]]:
    return [
        {"label": "Home", "href": "/"},
        {"label": "Now", "href": "/now"},
        {"label": "Projects", "href": "/projects"},
        {"label": "Blog", "href": "/blog"},
    ]


def _default_site_config() -> SiteConfig:
    return SiteConfig(
        title="My blog",
        author="Developer",
        nav=[NavItem(**n) for n in _default_nav()],
    )
