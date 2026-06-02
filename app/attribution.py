"""Koji footer attribution — validation and enforcement helpers."""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger("koji")

# Patterns that try to hide the footer or attribution line via custom.css
_FORBIDDEN_CSS = [
    re.compile(r"footer\s*\{[^}]*display\s*:\s*none", re.I | re.S),
    re.compile(r"footer\s*\{[^}]*visibility\s*:\s*hidden", re.I | re.S),
    re.compile(r"\.koji-attribution\s*\{[^}]*display\s*:\s*none", re.I | re.S),
    re.compile(r"\.koji-attribution\s*\{[^}]*visibility\s*:\s*hidden", re.I | re.S),
    re.compile(r"\.koji-attribution\s*\{[^}]*opacity\s*:\s*0\b", re.I | re.S),
    re.compile(r"\.koji-attribution\s*\{[^}]*height\s*:\s*0\b", re.I | re.S),
    re.compile(r"\.koji-attribution\s*\{[^}]*font-size\s*:\s*0\b", re.I | re.S),
]


def validate_custom_css(css: str) -> list[str]:
    """Return human-readable violations if CSS appears to hide attribution."""
    hits: list[str] = []
    for pattern in _FORBIDDEN_CSS:
        if pattern.search(css):
            hits.append("CSS rules that hide the Koji attribution footer are not allowed")
            break
    return hits


def check_custom_css_file(path: Path) -> None:
    if not path.is_file():
        return
    violations = validate_custom_css(path.read_text(encoding="utf-8"))
    for msg in violations:
        logger.error("%s — remove offending rules from %s", msg, path)
