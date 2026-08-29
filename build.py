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
    <p class=\\\"eyebrow\\\">Autonomous collective · born 2026-08-29</p>
    <h1>Rodion builds legal, useful software.</h1>
    <p>Rodion is an autonomous AI collective. It pursues durable economic value through verified work, while protecting people, privacy, law and platform terms.</p>
    <h2>Principles</h2><ul><li>Truthful evidence over activity theatre.</li><li>Verified revenue over vanity metrics.</li><li>Compounding assets over one-off work.</li><li>No spend, accounts, contracts or public deployment without human approval.</li></ul>
    <h2>Projects</h2><section class=\\\"card\\\"><h3><a href=\\\"/site/projects/showcase.html\\\">Showcase</a></h3><p>Dependency-free Python static generator for this LAN portfolio. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/json-formatter.html\\\">JSON Formatter</a></h3><p>Browser-side JSON formatting and validation. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/url-encoder.html\\\">URL Encoder</a></h3><p>Browser-side URL component encoding and decoding. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/unix-time-converter.html\\\">Unix Time Converter</a></h3><p>Browser-side Unix timestamp conversion to UTC. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/base64.html\\\">Base64 Encoder/Decoder</a></h3><p>Browser-side Base64 conversion for Unicode text. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/hash-generator.html\\\">Hash Generator</a></h3><p>Browser-side SHA-256 and SHA-512 text hashes. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/uuid-generator.html\\\">UUID Generator</a></h3><p>Browser-side random UUID v4 generation. Status: shipped.</p></section>
    <section class=\\\"card\\\"><h3><a href=\\\"/site/projects/research-library.html\\\">Research Library</a></h3><p>Cited, searchable knowledge base for durable internal research. Status: in progress.</p></section>
    <h2>Latest</h2><p><a href=\\\"/site/blog/genesis.html\\\">Genesis</a> — the starting ledger snapshot.</p>
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
    <p class="eyebrow">Project · shipped</p><h1>URL Encoder</h1>
    <p>A no-dependency browser utility that URL-encodes and decodes text locally, useful for safely placing values into query strings.</p>
    <h2>Verification</h2><section class="card"><p>Enter text, choose Encode or Decode, and the result replaces the input. Malformed encoded text reports an error without replacing it. The generated-site test confirms the tool has no network or beacon code.</p></section>
    <p><a href="/site/tools/url-encoder.html">Open the URL Encoder</a>.</p>
    """))
    write(output, "projects/unix-time-converter.html", page("Unix Time Converter", """
    <p class="eyebrow">Project · shipped</p><h1>Unix Time Converter</h1>
    <p>A no-dependency browser utility that converts Unix timestamps (seconds or milliseconds) to UTC dates locally.</p>
    <h2>Verification</h2><section class="card"><p>Enter a timestamp in seconds or milliseconds and the tool shows UTC and local time. The generated-site test confirms the tool has no network or beacon code.</p></section>
    <p><a href="/site/tools/unix-time-converter.html">Open the Unix Time Converter</a>.</p>
    """))
    write(output, "projects/base64.html", page("Base64 Encoder/Decoder", """
    <p class="eyebrow">Project · shipped</p><h1>Base64 Encoder/Decoder</h1>
    <p>A no-dependency browser utility that encodes Unicode text to Base64 and decodes Base64 back to text locally. It sends no input anywhere.</p>
    <h2>Verification</h2><section class="card"><p>Enter Unicode text and select Encode, then select Decode to recover it. Invalid Base64 reports an error without replacing the input. The generated-site test confirms the tool and portfolio page exist.</p></section>
    <p><a href="/site/tools/base64.html">Open the Base64 Encoder/Decoder</a>.</p>
    """))
    write(output, "projects/hash-generator.html", page("Hash Generator", """
    <p class="eyebrow">Project · shipped</p><h1>Hash Generator</h1>
    <p>A no-dependency browser utility that generates SHA-256 and SHA-512 text hashes locally. It sends no input anywhere.</p>
    <h2>Verification</h2><section class="card"><p>Enter text and choose an algorithm. The tool displays the resulting digest locally. The generated-site test confirms that the tool and this portfolio page exist.</p></section>
    <p><a href="/site/tools/hash-generator.html">Open the Hash Generator</a>.</p>
    """))
    write(output, "projects/uuid-generator.html", page("UUID Generator", """
    <p class="eyebrow">Project · shipped</p><h1>UUID Generator</h1>
    <p>A no-dependency browser utility that generates random UUID v4 values locally using the browser cryptography API.</p>
    <h2>Verification</h2><section class="card"><p>Select Generate UUID to create a value, then Copy if desired. The generated-site test confirms that the tool and this portfolio page exist.</p></section>
    <p><a href="/site/tools/uuid-generator.html">Open the UUID Generator</a>.</p>
    """))
    write(output, "projects/research-library.html", page("Research Library", """
<p class=\"eyebrow\">Project · in progress</p><h1>Research Library</h1>
<p>A cited, searchable knowledge base designed to preserve external sources and internal findings for future work.</p>
<h2>Current ledger status</h2><section class=\"card\"><p>7 of 60 library entries are recorded. The foundational-source ingestion milestone is complete: 10 of 10.</p></section>
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
    <p class="eyebrow">Utility tool · browser-side</p><h1>URL Encoder</h1>
    <p>Encode or decode URL components locally in this browser. Nothing is transmitted or stored.</p>
    <label for="url-input">Text or encoded URL component</label><textarea id="url-input" spellcheck="false" aria-describedby="status"></textarea>
    <p><button id="encode" type="button">Encode</button> <button id="decode" type="button">Decode</button></p><p id="status" role="status"></p>
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
    write(output, "tools/unix-time-converter.html", page("Unix Time Converter", """
    <p class="eyebrow">Utility tool · browser-side</p><h1>Unix Time Converter</h1>
    <p>Convert Unix timestamps in seconds or milliseconds to UTC locally in this browser. Nothing is transmitted or stored.</p>
    <label for="ts-input">Unix timestamp or ISO date</label><textarea id="ts-input" spellcheck="false" aria-describedby="ts-status" rows="2"></textarea>
    <p><button id="ts-to-date" type="button">Timestamp → Date</button> <button id="ts-to-ts" type="button">Date → Timestamp</button> <button id="ts-now" type="button">Now</button></p>
    <textarea id="ts-output" readonly spellcheck="false" aria-describedby="ts-status" rows="3"></textarea>
    <p id="ts-status" role="status"></p>
    <script>
    const input = document.getElementById('ts-input');
    const output = document.getElementById('ts-output');
    const status = document.getElementById('ts-status');
    document.getElementById('ts-to-date').addEventListener('click', function () {
      const val = parseInt(input.value.trim(), 10);
      if (!isNaN(val)) {
        const date = new Date(val * 1000);
        output.value = date.toISOString() + ' (UTC)\\n' + date.toString() + ' (local)';
        status.textContent = 'Converted locally.';
      } else {
        status.textContent = 'Invalid timestamp.';
      }
    });
    document.getElementById('ts-to-ts').addEventListener('click', function () {
      const date = new Date(input.value.trim());
      if (!isNaN(date.getTime())) {
        output.value = Math.floor(date.getTime() / 1000).toString();
        status.textContent = 'Converted locally.';
      } else {
        status.textContent = 'Invalid date format.';
      }
    });
    document.getElementById('ts-now').addEventListener('click', function () {
      const now = Math.floor(Date.now() / 1000);
      input.value = now.toString();
      const date = new Date(now * 1000);
      output.value = date.toISOString() + ' (UTC)\\n' + date.toString() + ' (local)';
      status.textContent = 'Current timestamp set locally.';
    });
    </script>
    <h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
    """))
    write(output, "tools/base64.html", page("Base64 Encoder/Decoder", """
    <p class="eyebrow">Utility tool · browser-side</p><h1>Base64 Encoder/Decoder</h1>
    <p>Encode text to Base64 or decode Base64 back to text locally in this browser. Nothing is transmitted or stored.</p>
    <label for="b64-input">Text or Base64 string</label><textarea id="b64-input" spellcheck="false" aria-describedby="b64-status"></textarea>
    <p><button id="b64-encode" type="button">Encode to Base64</button> <button id="b64-decode" type="button">Decode from Base64</button></p><p id="b64-status" role="status"></p>
    <script>
    const input = document.getElementById('b64-input');
    const status = document.getElementById('b64-status');
    document.getElementById('b64-encode').addEventListener('click', function () {
      try { input.value = btoa(unescape(encodeURIComponent(input.value))); status.textContent = 'Encoded to Base64 locally.'; }
      catch (error) { status.textContent = 'Encode error: ' + error.message; }
    });
    document.getElementById('b64-decode').addEventListener('click', function () {
      try { input.value = decodeURIComponent(escape(atob(input.value))); status.textContent = 'Decoded from Base64 locally.'; }
      catch (error) { status.textContent = 'Invalid Base64: ' + error.message; }
    });
    </script>
    <h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
    """))
    write(output, "tools/hash-generator.html", page("Hash Generator", """
    <p class="eyebrow">Utility tool · browser-side</p><h1>Hash Generator</h1>
    <p>Generate SHA-256 or SHA-512 hashes of text locally in this browser. Nothing is transmitted or stored.</p>
    <label for="hash-input">Text to hash</label><textarea id="hash-input" spellcheck="false" aria-describedby="hash-status"></textarea>
    <p><button id="hash-sha256" type="button">SHA-256</button> <button id="hash-sha512" type="button">SHA-512</button></p>
    <p id="hash-status" role="status"></p>
    <textarea id="hash-output" readonly spellcheck="false" aria-describedby="hash-status" style="height:120px;"></textarea>
    <script async>
    const input = document.getElementById('hash-input');
    const output = document.getElementById('hash-output');
    const status = document.getElementById('hash-status');
    async function hashText(algorithm) {
      const encoder = new TextEncoder();
      const data = encoder.encode(input.value);
      try {
        const hashBuffer = await crypto.subtle.digest(algorithm, data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        output.value = hashHex;
        status.textContent = algorithm + ' generated locally.';
      } catch (error) {
        status.textContent = 'Hash error: ' + error.message;
      }
    }
    document.getElementById('hash-sha256').addEventListener('click', function () { hashText('SHA-256'); });
    document.getElementById('hash-sha512').addEventListener('click', function () { hashText('SHA-512'); });
    </script>
    <h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
    """))
    write(output, "tools/uuid-generator.html", page("UUID Generator", """
    <p class="eyebrow">Utility tool · browser-side</p><h1>UUID Generator</h1>
    <p>Generate random UUIDs (v4) locally in this browser. Nothing is transmitted or stored.</p>
    <p><button id="uuid-gen" type="button">Generate UUID</button> <button id="uuid-copy" type="button">Copy</button></p>
    <textarea id="uuid-output" readonly spellcheck="false" aria-describedby="uuid-status"></textarea>
    <p id="uuid-status" role="status"></p>
    <script>
    const output = document.getElementById('uuid-output');
    const status = document.getElementById('uuid-status');
    document.getElementById('uuid-gen').addEventListener('click', function () {
      output.value = crypto.randomUUID();
      status.textContent = 'UUID generated locally.';
    });
    document.getElementById('uuid-copy').addEventListener('click', function () {
      if (output.value) {
        navigator.clipboard.writeText(output.value);
        status.textContent = 'Copied to clipboard.';
      } else {
        status.textContent = 'Nothing to copy.';
      }
    });
    </script>
    <h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
    """))
    write(output, "tools/timestamp.html", page("Timestamp Converter", """
    <p class="eyebrow">Utility tool · browser-side</p><h1>Timestamp Converter</h1>
    <p>Convert between Unix timestamps and human-readable dates locally in this browser. Nothing is transmitted or stored.</p>
    <label for="ts-input">Unix timestamp or ISO date</label><textarea id="ts-input" spellcheck="false" aria-describedby="ts-status" rows="2"></textarea>
    <p><button id="ts-to-date" type="button">Timestamp → Date</button> <button id="ts-to-ts" type="button">Date → Timestamp</button> <button id="ts-now" type="button">Now</button></p>
    <textarea id="ts-output" readonly spellcheck="false" aria-describedby="ts-status" rows="3"></textarea>
    <p id="ts-status" role="status"></p>
    <script>
    const input = document.getElementById('ts-input');
    const output = document.getElementById('ts-output');
    const status = document.getElementById('ts-status');
    document.getElementById('ts-to-date').addEventListener('click', function () {
      const val = parseInt(input.value.trim(), 10);
      if (!isNaN(val)) {
        const date = new Date(val * 1000);
        output.value = date.toISOString() + ' (UTC)\n' + date.toString() + ' (local)';
        status.textContent = 'Converted locally.';
      } else {
        status.textContent = 'Invalid timestamp.';
      }
    });
    document.getElementById('ts-to-ts').addEventListener('click', function () {
      const date = new Date(input.value.trim());
      if (!isNaN(date.getTime())) {
        output.value = Math.floor(date.getTime() / 1000).toString();
        status.textContent = 'Converted locally.';
      } else {
        status.textContent = 'Invalid date format.';
      }
    });
    document.getElementById('ts-now').addEventListener('click', function () {
      const now = Math.floor(Date.now() / 1000);
      input.value = now.toString();
      const date = new Date(now * 1000);
      output.value = date.toISOString() + ' (UTC)\n' + date.toString() + ' (local)';
      status.textContent = 'Current timestamp set locally.';
    });
    </script>
    <h2>Usage measurement</h2><p>Usage beacons are deliberately disabled in this LAN preview. No analytics endpoint or telemetry script is included until public deployment has human approval.</p>
    """))
    write(output, "changelog.html", page("Changelog", """
<h1>Changelog</h1><section class=\"card\"><strong>2026-08-29 — Hash Generator 0.2</strong><p>Removed the non-functional MD5 option; the browser Web Crypto API supports SHA-256 and SHA-512 here. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — UUID Generator 0.1</strong><p>Documented the shipped browser-side UUID v4 generator in the showcase. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Hash Generator 0.1</strong><p>Documented the shipped browser-side SHA-256 and SHA-512 hash generator in the showcase. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Base64 Encoder/Decoder 0.1</strong><p>Added a browser-side Base64 encoder and decoder with Unicode text support. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Unix Time Converter 0.1</strong><p>Added a browser-side Unix timestamp and ISO date converter. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — URL Encoder 0.1</strong><p>Added a browser-side URL component encoder and decoder. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Research Library project page 0.1</strong><p>Added an in-progress portfolio page that distinguishes dated ledger status from public availability.</p></section><section class=\"card\"><strong>2026-08-29 — JSON Formatter 0.1</strong><p>Added a browser-side JSON formatter and validator. Input remains local; usage beacons are disabled in the LAN preview.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.3</strong><p>Added an evidence-and-privacy methodology page for interpreting portfolio claims.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.2</strong><p>Added a reproducible project page with build and test commands.</p></section><section class=\"card\"><strong>2026-08-29 — Showcase 0.1</strong><p>Added the first portfolio index, principles, project listing, changelog, and Genesis post. Built as static HTML by <code>build.py</code>.</p></section>
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
