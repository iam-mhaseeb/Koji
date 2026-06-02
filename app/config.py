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
    popular_slugs: list[str] = field(default_factory=list)
    footer_subscribe: bool = True
    powered_by: bool = True
    koji_url: str = "https://github.com/heykoji/koji"
    has_custom_css: bool = False

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
        popular_slugs=list(data.get("popular_slugs") or []),
        footer_subscribe=bool(data.get("footer_subscribe", True)),
        powered_by=bool(data.get("powered_by", True)),
        koji_url=data.get("koji_url", "https://github.com/heykoji/koji"),
        has_custom_css=has_custom,
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
