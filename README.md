# Rodion Showcase

Dependency-free static site generator for rodion.place.

## Public repository boundary

This repository is intentionally public. Never commit credentials, private correspondence, personal data, internal research, ledger snapshots, private infrastructure details, or anything that is not meant to be permanently public.

## Build

```sh
./run.sh
```

This writes static HTML to `dist/` by default. To use another directory:

```sh
python3 build.py /tmp/site
```

## Test

```sh
python3 -m unittest discover -s tests -v
```

## URL Encoder

`/tools/url-encoder.html` encodes and decodes URL components entirely in the browser. It does not send or persist entered text. No analytics or telemetry script is included.

## Case Converter

`/tools/case-converter.html` converts text to uppercase, lowercase, title case, or sentence case entirely in the browser. It does not send or persist entered text. No analytics or telemetry script is included.

## Word Counter

`/tools/word-counter.html` counts words, characters, and lines entirely in the browser as text changes. It does not send or persist entered text. No analytics or telemetry script is included.

## JSON Formatter

`/tools/json-formatter.html` is a dependency-free, browser-side JSON validator, pretty-printer, and minifier. It does not send or persist pasted data. No analytics or telemetry script is included.

The Genesis post is deliberately terse and public-facing; operational state belongs in the private vault, not here.
