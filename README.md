# Rodion Showcase

Dependency-free static site generator for Rodion's LAN showcase.

## Build

```sh
./run.sh
```

This writes static HTML to `/srv/rodion/public/site/` by default. To use another directory:

```sh
python3 build.py /tmp/site
```

## Test

```sh
python3 -m unittest discover -s tests -v
```

## JSON Formatter

`/site/tools/json-formatter.html` is a dependency-free, browser-side JSON validator and pretty-printer. It does not send or persist pasted data. Its LAN-preview usage beacon is intentionally disabled: no analytics endpoint or telemetry script is present until public deployment is approved.

The Genesis post is a dated ledger snapshot from 2026-08-29; update it only from `rodion status` and `rodion events`.
