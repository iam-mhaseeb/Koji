"""Integration tests for Koji."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_home_page():
    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    assert "Alex's blog" in html or "Alex&#39;s blog" in html
    assert "( ◕ ᴥ ◕ )" in html
    assert "My most recent posts" in html
    assert "My most popular posts" in html
    assert "/blog/koji-manifesto" in html


def test_now_page():
    r = client.get("/now")
    assert r.status_code == 200
    assert "<h1>Now</h1>" in r.text
    assert "Shipping Koji" in r.text


def test_projects_page():
    r = client.get("/projects")
    assert r.status_code == 200
    assert "<h1>Projects</h1>" in r.text
    assert "Ongoing projects" in r.text
    assert "Koji" in r.text


def test_blog_index():
    r = client.get("/blog")
    assert r.status_code == 200
    assert "<h1>Blog</h1>" in r.text
    assert "htmx.org" in r.text
    assert "/blog/koji-manifesto" in r.text


def test_blog_search_query():
    r = client.get("/blog/partials/posts", params={"q": "database"})
    assert r.status_code == 200
    assert "No-database blogs" in r.text
    assert r.text.count("<li>") == 1


def test_blog_partial_htmx():
    r = client.get("/blog/partials/posts", params={"q": "koji"})
    assert r.status_code == 200
    assert "koji-manifesto" in r.text
    assert "<!DOCTYPE" not in r.text


def test_blog_post():
    r = client.get("/blog/koji-manifesto")
    assert r.status_code == 200
    assert "The Koji Manifesto" in r.text
    assert "markdown on disk" in r.text
    assert "Back to blog" in r.text


def test_blog_post_404():
    r = client.get("/blog/does-not-exist")
    assert r.status_code == 404


def test_atom_feed():
    r = client.get("/atom.xml")
    assert r.status_code == 200
    assert "application/atom+xml" in r.headers["content-type"]
    assert "<feed " in r.text
    assert "koji-manifesto" in r.text


def test_feed_aliases():
    for path in ("/rss.xml", "/feed.xml"):
        r = client.get(path)
        assert r.status_code == 200
        assert "atom+xml" in r.headers["content-type"]


def test_static_css():
    r = client.get("/static/style.css")
    assert r.status_code == 200
    assert "text/css" in r.headers["content-type"]
    assert ".container" in r.text


def test_custom_css_404_when_missing():
    r = client.get("/custom.css")
    assert r.status_code == 404


def test_nav_links_present():
    r = client.get("/")
    for path in ("/", "/now", "/projects", "/blog"):
        assert f'href="{path}"' in r.text


def test_footer_subscribe():
    r = client.get("/")
    assert "/atom.xml" in r.text
    assert "mailto:hello@example.com" in r.text
    assert "Powered by" in r.text
    assert "Koji" in r.text
