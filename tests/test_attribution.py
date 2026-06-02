"""Attribution footer enforcement tests."""

from app.attribution import validate_custom_css
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_footer_always_present():
    r = client.get("/")
    assert r.status_code == 200
    assert 'class="koji-attribution"' in r.text
    assert "Powered by" in r.text
    assert "Koji" in r.text


def test_attribution_css_loaded_after_custom():
    r = client.get("/")
    assert "/static/koji-attribution.css" in r.text
    # custom.css (if any) should appear before attribution css
    if "/custom.css" in r.text:
        assert r.text.index("/custom.css") < r.text.index("/static/koji-attribution.css")


def test_validate_custom_css_detects_hide():
    css = "footer { display: none; }"
    assert validate_custom_css(css)


def test_validate_custom_css_allows_safe_rules():
    css = "body { background: #111; } a { color: blue; }"
    assert not validate_custom_css(css)
