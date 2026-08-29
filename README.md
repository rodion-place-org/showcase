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

The Genesis post is a dated ledger snapshot from 2026-08-29; update it only from `rodion status` and `rodion events`.
