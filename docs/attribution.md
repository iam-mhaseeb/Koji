# Powered by Koji

Koji is MIT-licensed and free to self-host. If it helps you, we’d love a small credit in the footer — but it’s your choice.

## The toggle

In `content/site.yaml`:

```yaml
powered_by: true   # default — shows “Built with Koji ( •ᴥ• )”
koji_url: https://github.com/heykoji/koji
```

Set `powered_by: false` to hide that line. Everything else keeps working.

## Why we ask you to leave it on

- **Discovery** — other developers find Koji through your site  
- **Sustainability** — credit makes it easier to justify maintaining the project  
- **Small footprint** — one line in an already-minimal footer  

If Koji saved you time or hosting cost, leaving it on is a kind (and free) way to say thanks.

## What you can customize

| Setting | Effect |
|---------|--------|
| `koji_url` | Where the footer link points (your fork, docs, or the main repo) |
| `panda_small` | The little panda next to “Koji”, e.g. `( •ᴥ• )` |

Please don’t use `custom.css` to hide the line while leaving `powered_by: true` — set the config flag instead so intent is clear.

## If you turn it off

That’s allowed. Consider:

- Starring the repo on GitHub  
- Mentioning Koji in a “built with” post or your repo README  
- Contributing docs or code if you hit a bug  

## Related

- [Configuration](configuration.md) — `powered_by`, `footer_subscribe`, `koji_url`
- [Theming](theming.md) — footer and `custom.css`
