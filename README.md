# Rodion Showcase

Dependency-free static site generator for rodion.place.

## Public repository boundary

This repository is intentionally public. Never commit credentials, private correspondence, personal data, internal research, ledger snapshots, private infrastructure details, or anything that is not meant to be permanently public.

## Build

```sh
make build
```

This writes static HTML to `dist/` by default. To use another directory:

```sh
python3 build.py /tmp/site
```

Use `python3 build.py --help` to inspect the build options safely; flags are not interpreted as output paths.

## Test

```sh
make test
```

## URL Encoder

`/tools/url-encoder.html` encodes and decodes URL components entirely in the browser. It does not send or persist entered text. No analytics or telemetry script is included.

## Case Converter

`/tools/case-converter.html` converts text to uppercase, lowercase, title case, or sentence case entirely in the browser. It does not send or persist entered text. No analytics or telemetry script is included.

## Word Counter

`/tools/word-counter.html` counts words, characters, and lines entirely in the browser as text changes. It does not send or persist entered text. No analytics or telemetry script is included.

## JSON Formatter

`/tools/json-formatter.html` is a dependency-free, browser-side JSON validator, pretty-printer, and minifier. It does not send or persist pasted data. No analytics or telemetry script is included.

## Base64

`/tools/base64.html` encodes and decodes UTF-8 text as Base64 entirely in the browser. It does not send or persist entered text.

## UUID Generator

`/tools/uuid-generator.html` generates RFC 4122 version 4 UUIDs locally with the browser's cryptographic random source.

## Hash Generator

`/tools/hash-generator.html` computes browser-side cryptographic hashes without sending input anywhere.

## Bounty Eligibility Checker

`/tools/bounty-eligibility-checker.html` applies three conservative screen gates locally: at least five completed public awards in the prior 90 days, independently confirmed open work, and no more than three visible comments. A passing result only cues a source re-check; it does not establish payment, availability, authority to act, or create a marketplace account. No network requests or telemetry are included.

## Unix Time Converter

`/tools/unix-time-converter.html` converts Unix timestamps and human-readable dates locally in the browser.

The Genesis post is deliberately terse and public-facing; operational state belongs in the private vault, not here.
