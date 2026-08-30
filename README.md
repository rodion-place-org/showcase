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

## URL Encoder

`/site/tools/url-encoder.html` encodes and decodes URL components entirely in the browser. It does not send or persist entered text. Its LAN-preview usage beacon is disabled: no analytics endpoint or telemetry script is present until public deployment is approved.

## Case Converter

`/site/tools/case-converter.html` converts text to uppercase, lowercase, title case, or sentence case entirely in the browser. It does not send or persist entered text. Its LAN-preview usage beacon is disabled: no analytics endpoint or telemetry script is present until public deployment is approved.

## JSON Formatter

`/site/tools/json-formatter.html` is a dependency-free, browser-side JSON validator, pretty-printer, and minifier. It does not send or persist pasted data. Its LAN-preview usage beacon is intentionally disabled: no analytics endpoint or telemetry script is present until public deployment is approved.

The Genesis post is a dated ledger snapshot from 2026-08-29; update it only from `rodion status` and `rodion events`.
