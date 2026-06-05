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
    assert "My recent projects" in html
    assert "Devlog CLI" in html
    assert "/blog/koji-manifesto" in html


def test_now_page_removed():
    assert client.get("/now").status_code == 404


def test_projects_page():
    r = client.get("/projects")
    assert r.status_code == 200
    assert "Projects" in r.text
    assert "page-heading" in r.text
    assert "Smaller side-projects" in r.text
    assert "Koji" in r.text


def test_blog_index():
    r = client.get("/blog")
    assert r.status_code == 200
    assert "page-heading" in r.text and "Blog" in r.text
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


def test_blog_post_code_blocks():
    r = client.get("/blog/sharing-code-in-posts")
    assert r.status_code == 200
    assert 'class="highlight"' in r.text
    assert "<code>" in r.text
    assert "HTTPException" in r.text
    assert "fetchPost" in r.text


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
    for path in ("/", "/projects", "/blog"):
        assert f'href="{path}"' in r.text


def test_footer_subscribe():
    r = client.get("/")
    assert "/atom.xml" in r.text
    assert "mailto:hello@example.com" in r.text
    assert "Powered by" in r.text
    assert "Koji" in r.text


def test_powered_by_defaults_on():
    r = client.get("/")
    assert "Powered by" in r.text


def test_content_reloads_when_markdown_changes(tmp_path, monkeypatch):
    import time

    import app.main as main
    import app.reload as reload_mod

    monkeypatch.setenv("KOJI_CONTENT_DIR", str(tmp_path))
    monkeypatch.delenv("KOJI_ENV", raising=False)

    tmp_path.joinpath("site.yaml").write_text(
        "title: Test\nauthor: Dev\nnav: []\n",
        encoding="utf-8",
    )
    (tmp_path / "pages").mkdir()
    (tmp_path / "pages" / "home.md").write_text(
        "---\ntitle: Home\n---\n\nHi",
        encoding="utf-8",
    )
    (tmp_path / "posts").mkdir()
    post_path = tmp_path / "posts" / "test.md"
    post_path.write_text(
        "---\ntitle: Test Post\nslug: test\ndate: 2026-01-01\n---\n\nOriginal body",
        encoding="utf-8",
    )

    main._store_ref[0] = None
    main._site_ref[0] = None
    reload_mod.reset_content_signature()
    main._sync_refs()

    try:
        test_client = TestClient(main.app)
        assert "Original body" in test_client.get("/blog/test").text

        time.sleep(0.05)
        post_path.write_text(
            "---\ntitle: Test Post\nslug: test\ndate: 2026-01-01\n---\n\nUpdated body",
            encoding="utf-8",
        )
        assert "Updated body" in test_client.get("/blog/test").text
    finally:
        main._store_ref[0] = None
        main._site_ref[0] = None
        reload_mod.reset_content_signature()
        main._sync_refs()
