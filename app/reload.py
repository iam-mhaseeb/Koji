from __future__ import annotations

import os
from pathlib import Path

from app.config import SiteConfig, content_root, load_site_config
from app.content import ContentStore

_content_signature: float | None = None


def is_production() -> bool:
    return os.environ.get("KOJI_ENV", "").lower() == "production"


def content_tree_mtime(root: Path) -> float:
    """Latest modification time under the content directory."""
    latest = 0.0
    if not root.is_dir():
        return latest
    for path in root.rglob("*"):
        if path.is_file():
            latest = max(latest, path.stat().st_mtime)
    return latest


def refresh_content_if_changed(
    store_ref: list[ContentStore | None],
    site_ref: list[SiteConfig | None],
) -> None:
    """Reload site.yaml and markdown when content files change (dev only)."""
    global _content_signature
    if is_production():
        return

    root = content_root()
    signature = content_tree_mtime(root)
    if _content_signature is not None and signature <= _content_signature:
        return

    _content_signature = signature
    site_ref[0] = load_site_config(root)
    if store_ref[0] is None:
        store_ref[0] = ContentStore(site=site_ref[0])
    else:
        store_ref[0].site = site_ref[0]
        store_ref[0].reload()


def reset_content_signature() -> None:
    """Clear cached mtime (for tests)."""
    global _content_signature
    _content_signature = None
