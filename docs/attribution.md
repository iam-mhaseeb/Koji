# Footer attribution

Koji always renders **“Powered by Koji”** in the site footer. This page explains what is enforced in software and what requires legal or hosted-product choices.

## What Koji enforces in code

| Measure | What it does |
|---------|----------------|
| **Always-on template** | Footer HTML is not gated by `site.yaml`; there is no `powered_by: false` option. |
| **`koji-attribution.css`** | Loaded **after** `custom.css` so simple hide rules are overridden. |
| **`custom.css` scan** | On startup, logs an **error** if CSS appears to hide `footer` or `.koji-attribution`. |

These stop casual removal via config or basic CSS. They do **not** stop a determined fork (see below).

## What you cannot enforce (self-hosted + MIT)

Anyone who self-hosts can still:

- Delete or edit `app/templates/base.html`
- Remove `koji-attribution.css` from the template
- Patch Python or run a fork without your updates
- Use `footer { display: none !important; }` in CSS loaded after yours (e.g. browser extension — not your problem)

**MIT license** requires keeping the copyright notice in **source** distributions, not in the live site UI. So legal attribution in code ≠ visible footer in production.

True “cannot remove” enforcement only works if:

1. **You host the product** (SaaS) and control the deployed HTML, or  
2. **You change the license** to require visible attribution (not MIT), or  
3. **Dual license** — MIT for contributors, commercial/terms for deployers who want no footer.

## Stronger options if you need real enforcement

### Option A: Hosted Koji only

You run the instances; users never deploy the server themselves. You control templates and assets.

### Option B: Custom license / CLA

Example clause (talk to a lawyer):

> Redistributions that provide the Software as a public website must display a “Powered by Koji” link in the footer of every page, linking to [URL], unless you have a separate written agreement.

MIT alone does not include this.

### Option C: Apache 2.0 + NOTICE

Requires preserving **NOTICE** file in distributions, not footer on the website. Helpful for source attribution, not UI.

### Option D: Trademark

Register “Koji” and restrict misleading use of the name/logo. Does not force a footer link by itself.

## For fork maintainers

If you are **allowed** to remove attribution (your own fork, commercial license, etc.):

1. Edit `app/templates/base.html` — remove the `.koji-attribution` block.
2. Remove the `<link>` to `koji-attribution.css`.
3. Delete or disable `check_custom_css_file` in `app/main.py` lifespan if desired.

## For site owners (default Koji)

- Do not hide the footer in `content/custom.css` — startup will log an error.
- Customize the link target with `koji_url` in `site.yaml` (e.g. your fork or docs).
- Panda emoji in the link text come from `panda_small` in `site.yaml`.

## Related

- [Configuration](configuration.md) — `koji_url`, footer subscribe line
- [Theming](theming.md) — `custom.css` rules
