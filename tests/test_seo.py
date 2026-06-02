"""SEO tests for meta tags, sitemap, and robots."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_robots_txt():
    r = client.get("/robots.txt")
    assert r.status_code == 200
    assert "Sitemap:" in r.text
    assert "/blog/partials/" in r.text


def test_sitemap_xml():
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    assert "application/xml" in r.headers["content-type"]
    assert "<urlset" in r.text
    assert "/blog/koji-manifesto" in r.text
    assert "http://localhost:8000/" in r.text


def test_home_canonical_and_json_ld():
    r = client.get("/")
    assert r.status_code == 200
    assert 'rel="canonical"' in r.text
    assert "http://localhost:8000/" in r.text
    assert 'application/ld+json' in r.text
    assert '"@type": "WebSite"' in r.text or '"@type":"WebSite"' in r.text
    assert 'name="description"' in r.text
    assert 'property="og:title"' in r.text


def test_post_article_meta():
    r = client.get("/blog/koji-manifesto")
    assert r.status_code == 200
    assert 'property="og:type" content="article"' in r.text
    assert 'property="article:published_time"' in r.text
    assert '"@type": "BlogPosting"' in r.text or '"@type":"BlogPosting"' in r.text
    assert "<time datetime=" in r.text
    assert 'rel="canonical"' in r.text
    assert "/blog/koji-manifesto" in r.text


def test_blog_search_noindex():
    r = client.get("/blog", params={"q": "test"})
    assert r.status_code == 200
    assert 'content="noindex, follow"' in r.text


def test_htmx_partial_noindex_header():
    r = client.get("/blog/partials/posts", params={"q": "koji"})
    assert r.status_code == 200
    assert r.headers.get("x-robots-tag") == "noindex"


def test_page_meta_description():
    r = client.get("/projects")
    assert r.status_code == 200
    assert "Open source tools" in r.text


def test_sitemap_link_in_head():
    r = client.get("/")
    assert 'href="/sitemap.xml"' in r.text


def test_llms_and_feed_links_in_head():
    r = client.get("/")
    assert 'href="/llms.txt"' in r.text
    assert 'href="/atom.xml"' in r.text
    assert "text/markdown" in r.text


def test_projects_page_json_ld():
    r = client.get("/projects")
    assert '"@type": "WebPage"' in r.text or '"@type":"WebPage"' in r.text
    assert "Open source tools" in r.text
