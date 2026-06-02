---
title: No-database blogs load faster
slug: no-database-blogs
date: 2026-01-14
description: Files are the best CMS for a personal site.
popular: true
---

When content lives in git as markdown:

1. Edits are reviewable diffs
2. Backups are `git push`
3. Cold starts skip connection pools entirely

FastAPI reads files once per process and renders HTML. That's the whole data layer.
