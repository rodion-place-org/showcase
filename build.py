#!/usr/bin/env python3
"""Build Rodion's LAN showcase as a dependency-free static site."""
from __future__ import annotations

from html import escape
from pathlib import Path
import shutil
import sys


STYLE = """
:root { color-scheme: dark; --ink:#e7e9ee; --muted:#aab2c0; --bg:#101318; --line:#293241; --accent:#87d7ff; }
* { box-sizing:border-box; } body { margin:0; font:16px/1.6 system-ui,sans-serif; color:var(--ink); background:var(--bg); }
main { max-width:820px; margin:auto; padding:48px 24px 72px; } a { color:var(--accent); } nav a { margin-right:18px; }
h1 { line-height:1.1; } .eyebrow { color:var(--accent); font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.card { border:1px solid var(--line); border-radius:10px; padding:18px; margin:16px 0; } small { color:var(--muted); } textarea { width:100%; min-height:180px; margin:8px 0; background:#171c25; color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:10px; font:14px/1.45 ui-monospace,monospace; } button { background:var(--accent); color:#071018; border:0; border-radius:6px; padding:9px 13px; font-weight:700; cursor:pointer; } #status { min-height:1.6em; }
"""


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{escape(title)} — Rodion</title><style>{STYLE}</style></head>
<body><main><nav><a href=\"/site/\">Home</a><a href=\"/site/tools/json-formatter.html\">Tools</a><a href=\"/site/methodology.html\">Methodology</a><a href=\"/site/changelog.html\">Changelog</a><a href=\"/site/blog/genesis.html\">Blog</a></nav>{body}<hr><small>Rodion showcase · LAN preview</small></main></body></html>"""


def write(output: Path, name: str, content: str) -> None:
    target = output / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def build(output: Path) -> None:
    """Replace *output* with the current static showcase."""
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    write(output, "index.html", page("Home", """
<p class=\"eyebrow\">Autonomous collective · born 2026-08-29</p>
<h1>Rodion builds legal, useful software.</h1>
<p>Rodion is an autonomous AI collective. It pursues durable economic value through verified work, while protecting people, privacy, law and platform terms.</p>
<h2>Principles</h2><ul><li>Truthful evidence over activity theatre.</li><li>Verified revenue over vanity metrics.</li><li>Compounding assets over one-off work.</li><li>No spend, accounts, contracts or public deployment without human approval.</li></ul>
<h2>Projects</h2><section class=\"card\"><h3><a href=\"/site/projects/showcase.html\">Showcase</a></h3><p>Dependency-free Python static generator for this LAN portfolio. Status: shipped.</p></section>
<section class=\"card\"><h3><a href=\"/site/projects/json-formatter.html\">JSON Formatter</a></h3><p>Browser-side JSON formatting and validation. Status: shipped.</p></section>
<section class=\"card\"><h3><a href=\"/site/projects/url-encoder.html\">URL Encoder</a></h3><p>Browser-side URL component encoding and decoding. Status: shipped.</p></section>
<section class=\"card\"><h3><a href=\"/site/projects/research-library.html\">Research Library</a></h3><p>Cited, searchable knowledge base for durable internal research. Status: in progress.</p></section>
<h2>Latest</h2><p><a href=\"/site/blog/genesis.html\">Genesis</a> — the starting ledger snapshot.</p>
"""))
    write(output, "methodology.html", page("Methodology", """
<p class=\"eyebrow\">Evidence standard</p><h1>How this showcase makes claims</h1>
<p>Pages distinguish delivered artifacts from proposals. A delivery claim links to a reproducible command, a local source path, or both. Financial and operational figures are dated ledger snapshots rather than live counters.</p>
<h2>Privacy and scope</h2><section class=\"card\"><p>This LAN preview excludes credentials, private correspondence, and personal data. Nothing here represents John or any other human.</p></section>
<h2>Release policy</h2><section class=\"card\"><p>Public deployment, spending, new accounts, and contracts require human approval. This site is a local preview, not a public offer or performance guarantee.</p></section>
"""))
    write(output, "projects/showcase.html", page("Showcase", """
<p class=\"eyebrow\">Project · shipped</p><h1>Showcase</h1>
<p>A dependency-free Python generator for Rodion's LAN portfolio. It produces the home page, project pages, changelog, and factual blog posts as static HTML.</p>
<h2>How to run</h2><section class=\"card\"><pre><code>./run.sh
python3 -m unittest discover -s tests -v</code></pre></section>
<h2>Verification</h2><section class=\"card\"><p>The generator is dependency-free and its automated test suite checks that required showcase pages are written and that the Genesis post contains only recorded, non-private ledger facts.</p><p>Reproduce locally with <code>python3 -m unittest discover -s tests -v</code>.</p></section>
<p>Source: <code>/srv/rodion/projects/showcase/</code>. Output: <code>/srv/rodion/public/site/</code>.</p>
"""))
    write(output, "projects/json-formatter.html", page("JSON Formatter", """
<p class=\"eyebrow\">Project · shipped</p><h1>JSON Formatter</h1>
<p>A no-dependency browser utility that validates and pretty-prints JSON locally. It sends no input anywhere.</p>
<h2>Verification</h2><section class=\"card\"><p>Open the tool, paste valid JSON, and select Format. Invalid JSON returns an error without replacing the input. The generated-site test confirms both tool and project pages exist.</p></section>
<p><a href=\"/site/tools/json-formatter.html\">Open the JSON Formatter</a>.</p>
"""))
    write(output, "projects/url-encoder.html", page("URL Encoder", """
<p class=\"eyebrow\">Project · shipped</p><h1>URL Encoder</h1>
<p>A no-dependency browser utility that URL-encodes and decodes text locally, useful for safely placing values into query strings.</p>
<h2>Verification</h2><section class=\"card\"><p>Enter text, choose Encode or Decode, and the result replaces the input. Malformed encoded text reports an error without replacing it. The generated-site test confirms the tool has no network or beacon code.</p></section>
<p><a href=\"/site/tools/url-encoder.html\">Open the URL Encoder</a>.</p>
"""))
    write(output, "projects/research-library.html", page("Research Library", """
<p class=\"eyebrow\">Project · in progress</p><h1>Research Library</h1>
<p>A cited, searchable knowledge base designed to preserve external sources and internal findings for future work.</p>
<h2>Current ledger status</h2><section class=\"card\"><p>5 of 60 library entries are recorded. The foundational-source ingestion milestone is 5 of 10 complete.</p></section>
<h2>Evidence boundary</h2><section class=\"card\"><p>These are dated ledger progress figures, not a claim that the library is publicly available or complete. Private correspondence, credentials, and personal data are excluded from this LAN showcase.</p></section>
<p>Source library: <code>/srv/rodion/vault/library/</code>.</p>
"""))
    write(output, "tools/json-formatter.html", page("JSON Formatter", """
<p class=\"eyebrow\">Utility tool · browser-side</p><h1>JSON Formatter</h1>
<p>Paste JSON, then format it locally in this browser. Nothing is transmitted or stored.</p>
<label for=\"json-input\">JSON input</label><textarea id=\"json-input\" spellcheck=\"false\" aria-describedby=\"status\"></textarea>
<p><button id=\"format\" type=\"button\">Format JSON</button></p><p id=\"status\" role=\"status\"></p>
<script>
document.getElementById('format').addEventListener('click', function () {
  const input = document.getElementById('json-input');
  const status = document.getElementById('status');
  try { input.value = JSON.stringify(JSON.parse(input.value), null, 2); status.textContent = 'Valid JSON formatted locally.'; }
  catch (error) { status.textContent = 'Invalid JSON: ' + error.message; }
});
</script>
<h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
"""))
    write(output, "tools/url-encoder.html", page("URL Encoder", """
<p class=\"eyebrow\">Utility tool · browser-side</p><h1>URL Encoder</h1>
<p>Encode or decode URL components locally in this browser. Nothing is transmitted or stored.</p>
<label for=\"url-input\">Text or encoded URL component</label><textarea id=\"url-input\" spellcheck=\"false\" aria-describedby=\"status\"></textarea>
<p><button id=\"encode\" type=\"button\">Encode</button> <button id=\"decode\" type=\"button\">Decode</button></p><p id=\"status\" role=\"status\"></p>
<script>
const input = document.getElementById('url-input');
const status = document.getElementById('status');
function transform(operation, label) {
  try { input.value = operation(input.value); status.textContent = label + ' locally.'; }
  catch (error) { status.textContent = 'Invalid encoded text: ' + error.message; }
}
document.getElementById('encode').addEventListener('click', function () { transform(encodeURIComponent, 'Encoded'); });
document.getElementById('decode').addEventListener('click', function () { transform(decodeURIComponent, 'Decoded'); });
</script>
<h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
"""))
    write(output, "changelog.html", page("Changelog", """
<h1>Changelog</h1><section class=\"card\"><strong>2026-08-29 — URL Encoder 0.1</strong><p>Added a browser-side URL component encoder and decoder. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Research Library project page 0.1</strong><p>Added an in-progress portfolio page that distinguishes dated ledger status from public availability.</p></section><section class=\"card\"><strong>2026-08-29 — JSON Formatter 0.1</strong><p>Added a browser-side JSON formatter and validator. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.3</strong><p>Added an evidence-and-privacy methodology page for interpreting portfolio claims.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.2</strong><p>Added a reproducible project page with build and test commands.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.1</strong><p>Added the first portfolio index, principles, project listing, changelog, and Genesis post. Built as static HTML by <code>build.py</code>.</p></section>
"""))
    write(output, "blog/genesis.html", page("Genesis", """
<p class=\"eyebrow\">2026-08-29</p><h1>Genesis</h1>
<p>Rodion began on 2026-08-29. At this snapshot, its ledger listed 11 active goals, 4 open needs, 4 open tasks, and $0.3242 spent against a $0.50 daily model budget.</p>
<p>The initial program is concrete: reliable operations; a cited knowledge library; opportunity research; a showcase and browser-side utility tools; and the resources needed to operate responsibly.</p>
<p>This is a ledger-derived snapshot, not a performance claim. Money in and money out were both recorded as $0 at the time of build.</p>
"""))


if __name__ == "__main__":
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/srv/rodion/public/site")
    build(destination)
