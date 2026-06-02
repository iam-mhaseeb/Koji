from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import __version__
from app.config import SiteConfig, content_root, load_site_config
from app.content import ContentStore, Post

APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_store()
    yield


app = FastAPI(
    title="Koji",
    description="Self-hostable portfolio + blog for developers",
    version=__version__,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

_store: ContentStore | None = None
_site: SiteConfig | None = None


def get_store() -> ContentStore:
    global _store, _site
    if _store is None:
        _site = load_site_config()
        _store = ContentStore(site=_site)
    return _store


def get_site() -> SiteConfig:
    global _site
    if _site is None:
        _site = load_site_config()
    return _site


def _ctx(**extra):
    return {"site": get_site(), **extra}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    store = get_store()
    page = store.page("home")
    return templates.TemplateResponse(
        request,
        "home.html",
        _ctx(page=page, recent=store.recent_posts(), popular=store.popular_posts()),
    )


@app.get("/now", response_class=HTMLResponse)
@app.get("/projects", response_class=HTMLResponse)
async def static_page(request: Request):
    slug = request.url.path.strip("/")
    store = get_store()
    page = store.page(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request,
        "page.html",
        _ctx(page=page, heading=page.title),
    )


@app.get("/blog", response_class=HTMLResponse)
async def blog_index(request: Request, q: str | None = None):
    store = get_store()
    posts = store.search_posts(q) if q else store.published_posts()
    return templates.TemplateResponse(
        request,
        "blog.html",
        _ctx(posts=posts, query=q or ""),
    )


@app.get("/blog/partials/posts", response_class=HTMLResponse)
async def blog_posts_partial(request: Request, q: str = Query(default="")):
    """HTMX partial: filtered post list."""
    store = get_store()
    posts = store.search_posts(q)
    return templates.TemplateResponse(
        request,
        "partials/post_list.html",
        _ctx(posts=posts),
    )


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    store = get_store()
    post = store.post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(
        request,
        "post.html",
        _ctx(post=post),
    )


@app.get("/rss.xml")
@app.get("/feed.xml")
@app.get("/atom.xml")
async def feed():
    store = get_store()
    site = get_site()
    posts = store.recent_posts(limit=20)
    updated = posts[0].date if posts else datetime.now(timezone.utc)
    items_xml = "\n".join(_atom_entry(p, site) for p in posts)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{escape(site.title)}</title>
  <link href="{escape(site.url)}/" rel="alternate"/>
  <link href="{escape(site.url)}/atom.xml" rel="self"/>
  <updated>{_atom_datetime(updated)}</updated>
  <id>{escape(site.url)}/</id>
  <author><name>{escape(site.author)}</name></author>
{items_xml}
</feed>"""
    return Response(content=xml, media_type="application/atom+xml; charset=utf-8")


def _atom_datetime(dt: datetime) -> str:
    if dt.tzinfo is None:
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atom_entry(post: Post, site: SiteConfig) -> str:
    url = f"{site.url}/blog/{post.slug}"
    return f"""  <entry>
    <title>{escape(post.title)}</title>
    <link href="{escape(url)}" rel="alternate"/>
    <id>{escape(url)}</id>
    <updated>{_atom_datetime(post.date)}</updated>
    <summary>{escape(post.description)}</summary>
  </entry>"""


@app.get("/custom.css", response_class=Response)
async def custom_css():
    path = content_root() / "custom.css"
    if not path.is_file():
        return Response(status_code=404)
    return Response(content=path.read_text(encoding="utf-8"), media_type="text/css")


@app.get("/health")
async def health():
    return {"status": "ok", "version": __version__}
