---
title: HTMX without building an SPA
slug: htmx-without-spa
date: 2026-02-05
description: Progressive enhancement for a static-fast blog.
---

The blog search box swaps a list partial over the wire. No React, no build step, no client router.

The default experience works without JavaScript — search degrades to a full page reload if you add `?q=` to `/blog` (already supported).
