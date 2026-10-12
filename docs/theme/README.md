# Documentation theme

This directory holds the reusable Asciidoctor CSS, JavaScript, docinfo, and starter content used by the [Part 1 report site](../../README.md). It is a plain HTML/CSS/JavaScript theme; the SRAM measurements and requirements live in the report source, not in the theme.

## Build and preview

Install Asciidoctor, then run from the repository root:

```sh
make docs-check
make docs-open
```

`make docs-check` builds `build/docs`, validates local links and figures, and builds the exported starter in a temporary directory. `make docs-open` serves the site at `http://localhost:8000`. The output is ignored by Git.

## Reuse the theme

The site source is [`docs/index.adoc`](../index.adoc), branding is in [`docs/site.json`](../site.json), and the reusable starting point is [`starter.adoc`](starter.adoc). To use it elsewhere, run `python3 scripts/export-docs-template.py` from the repository root and extract `build/docs/downloads/docs-template.zip`. Edit the starter content and site configuration, then run `make docs-check`.

The theme provides chapter navigation, search, light and dark modes, keyboard access, mobile navigation, a mobile table layout, full-size figure links, and print styling. With JavaScript disabled, the complete Asciidoctor document remains readable. Equations use Asciidoctor's MathJax integration and need its CDN to render.

## Publishing this repository

The [Docs workflow](../../.github/workflows/docs.yml) validates the site on matching pushes to any branch. Its deploy job runs on `contribution-tmarhguy` and `main` after the build passes. The GitHub Pages environment must allow both branches; the repository currently has those branch policies. A local build does not publish the site.

The template archive is generic. Update its workflow branch condition and Pages environment policy for the destination repository before deployment. The theme's [MIT license](LICENSE) covers the reusable theme only; it does not change the status of the course report or media.
