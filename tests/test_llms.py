"""Tests for llms.txt and markdown exports."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_llms_txt():
    r = client.get("/llms.txt")
    assert r.status_code == 200
    assert "text/markdown" in r.headers["content-type"]
    text = r.text
    assert text.startswith("# ")
    assert "> " in text
    assert "## Pages" in text
    assert "## Blog" in text
    assert "/index.md" in text
    assert "/blog/koji-manifesto.md" in text
    assert "/llms-full.txt" in text


def test_llms_full_txt():
    r = client.get("/llms-full.txt")
    assert r.status_code == 200
    assert "text/markdown" in r.headers["content-type"]
    assert "# The Koji Manifesto" in r.text or "Koji Manifesto" in r.text
    assert "Hi I'm Alex" in r.text or "Alex Developer" in r.text


def test_index_md():
    r = client.get("/index.md")
    assert r.status_code == 200
    assert "text/markdown" in r.headers["content-type"]
    assert "# " in r.text
    assert "Alex Developer" in r.text


def test_post_md():
    r = client.get("/blog/koji-manifesto.md")
    assert r.status_code == 200
    assert "The Koji Manifesto" in r.text
    assert "markdown on disk" in r.text


def test_post_md_404():
    r = client.get("/blog/not-real.md")
    assert r.status_code == 404


def test_robots_mentions_llms():
    r = client.get("/robots.txt")
    assert "llms.txt" in r.text
