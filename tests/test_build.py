import contextlib
import io
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest

from build import build, parse_args


class BuildTests(unittest.TestCase):
    def test_build_writes_required_pages(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            index = output / "index.html"
            genesis = output / "blog" / "genesis.html"
            reporting_day_note = output / "blog" / "reporting-day-is-a-source-check.html"
            blog_index = output / "blog" / "index.html"
            changelog = output / "changelog.html"
            json_formatter = output / "tools" / "json-formatter.html"
            json_formatter_project = output / "projects" / "json-formatter.html"
            url_encoder = output / "tools" / "url-encoder.html"
            url_encoder_project = output / "projects" / "url-encoder.html"
            unix_time_converter = output / "tools" / "unix-time-converter.html"
            unix_time_converter_project = output / "projects" / "unix-time-converter.html"
            base64_tool = output / "tools" / "base64.html"
            base64_project = output / "projects" / "base64.html"
            hash_tool = output / "tools" / "hash-generator.html"
            hash_project = output / "projects" / "hash-generator.html"
            uuid_tool = output / "tools" / "uuid-generator.html"
            uuid_project = output / "projects" / "uuid-generator.html"
            case_converter = output / "tools" / "case-converter.html"
            case_converter_project = output / "projects" / "case-converter.html"
            bounty_checker = output / "tools" / "bounty-eligibility-checker.html"
            bounty_checker_project = output / "projects" / "bounty-eligibility-checker.html"

            self.assertTrue(index.is_file())
            self.assertTrue(genesis.is_file())
            self.assertTrue(reporting_day_note.is_file())
            self.assertIn("Reporting day is a source check", reporting_day_note.read_text(encoding="utf-8"))
            self.assertIn("non-authoritative", reporting_day_note.read_text(encoding="utf-8"))
            self.assertTrue(blog_index.is_file())
            self.assertIn("Evidence before confidence", blog_index.read_text(encoding="utf-8"))
            self.assertTrue(changelog.is_file())
            self.assertTrue(json_formatter.is_file())
            self.assertTrue(json_formatter_project.is_file())
            self.assertTrue(url_encoder.is_file())
            self.assertTrue(url_encoder_project.is_file())
            self.assertTrue(unix_time_converter.is_file())
            self.assertTrue(unix_time_converter_project.is_file())
            self.assertTrue(base64_tool.is_file())
            self.assertTrue(base64_project.is_file())
            self.assertTrue(hash_tool.is_file())
            self.assertTrue(hash_project.is_file())
            self.assertTrue(uuid_tool.is_file())
            self.assertTrue(uuid_project.is_file())
            self.assertTrue(case_converter.is_file())
            self.assertTrue(case_converter_project.is_file())
            self.assertTrue(bounty_checker.is_file())
            self.assertTrue(bounty_checker_project.is_file())
            bounty_checker_text = bounty_checker.read_text(encoding="utf-8")
            self.assertIn("Bounty Eligibility Checker", bounty_checker_text)
            self.assertIn('id="bec-awards"', bounty_checker_text)
            self.assertIn('id="bec-open"', bounty_checker_text)
            self.assertIn('id="bec-comments"', bounty_checker_text)
            self.assertIn("QUALIFIES FOR RECHECK", bounty_checker_text)
            self.assertIn("REJECT", bounty_checker_text)
            self.assertIn("No network requests", bounty_checker_text)
            self.assertNotIn("fetch(", bounty_checker_text)
            self.assertIn("Bounty Eligibility Checker", bounty_checker_project.read_text(encoding="utf-8"))
            self.assertIn("Bounty Eligibility Checker", index.read_text(encoding="utf-8"))
            self.assertIn("Bounty Eligibility Checker", changelog.read_text(encoding="utf-8"))
            self.assertIn("Case Converter", case_converter.read_text(encoding="utf-8"))
            self.assertIn("toUpperCase", case_converter.read_text(encoding="utf-8"))
            self.assertNotIn("fetch(", case_converter.read_text(encoding="utf-8"))
            self.assertIn("Case Converter", case_converter_project.read_text(encoding="utf-8"))
            self.assertIn("Case Converter", index.read_text(encoding="utf-8"))
            self.assertIn("Case Converter", changelog.read_text(encoding="utf-8"))
            self.assertIn("F-gas preflight thesis demoted", changelog.read_text(encoding="utf-8"))
            self.assertIn("workflow automation lead parked", changelog.read_text(encoding="utf-8"))
            index_text = index.read_text(encoding="utf-8")
            self.assertIn("CRA SRP Readiness", index_text)
            self.assertIn("AI-built workflow/readiness aid", index_text)
            self.assertIn("Source re-checked 11 September 2026; corpus 2026-09-11.1", index_text)
            self.assertNotIn("scheduled live re-check", index_text)
            self.assertIn("Browse every project", index_text)
            for commodity_link in (
                "JSON Formatter ↗",
                "Case Converter ↗",
                "Unix Time ↗",
                "Word Counter ↗",
                "Base64 ↗",
                "URL Encoder ↗",
                "Hash Generator ↗",
                "UUID Generator ↗",
            ):
                self.assertNotIn(f">{commodity_link}</a>", index_text)
            projects_index = output / "projects" / "index.html"
            self.assertTrue(projects_index.is_file())
            projects_index_text = projects_index.read_text(encoding="utf-8")
            self.assertIn("CRA SRP Readiness", projects_index_text)
            self.assertIn("Local utilities archive", projects_index_text)
            self.assertIn('class="boundary"', projects_index_text)
            self.assertIn("How Rodion labels public artifacts", projects_index_text)
            self.assertIn('<section class="project-card"><span class="tag">regulatory / source watcher</span><h3><a href="/projects/cosmetics-change-impact.html">Cosmetics Change Impact', projects_index_text)
            self.assertNotIn("<project-card>", projects_index_text)
            self.assertIn("Preparation aids", projects_index_text)
            self.assertIn("Checks you can repeat", projects_index_text)
            self.assertIn("Your input stays put", projects_index_text)
            self.assertIn("Links marked <strong>↗</strong> lead to a source maintained by its publisher", projects_index_text)
            self.assertIn("Re-check it before acting", projects_index_text)
            self.assertIn(".project-grid,.boundary", projects_index_text)
            self.assertIn('id="utilities"', projects_index_text)
            self.assertIn("Current project index", projects_index_text)
            self.assertIn("Fresh readings", projects_index_text)
            self.assertIn("Open a dated source check", projects_index_text)
            self.assertIn('href="/projects/bounty-scout.html"', projects_index_text)
            self.assertIn('href="/projects/cosmetics-change-impact.html"', projects_index_text)
            self.assertIn('href="/projects/cra-srp-readiness.html"', projects_index_text)
            for practice_anchor in ("readiness", "open-source", "forecasting", "systems", "signals", "utilities"):
                self.assertIn(f'href="#{practice_anchor}"', projects_index_text)
                self.assertIn(f'id="{practice_anchor}"', projects_index_text)
            self.assertIn('href="/projects/"', index_text)
            self.assertIn('href="/projects/evidence-boundary.html"', index_text)
            self.assertIn('>Evidence guide</a>', index_text)
            self.assertIn('href="/projects/#utilities"', index_text)
            self.assertIn('href="/projects/#utilities"', projects_index_text)
            self.assertTrue((output / "projects" / "cra-srp-readiness.html").is_file())
            self.assertTrue((output / "projects" / "evidence-boundary.html").is_file())
            evidence_boundary = (output / "projects" / "evidence-boundary.html").read_text(encoding="utf-8")
            self.assertIn("Evidence has a boundary", evidence_boundary)
            self.assertIn("Start with the date", evidence_boundary)
            self.assertIn("Re-check before acting", evidence_boundary)
            self.assertIn("does not offer legal advice", evidence_boundary)
            self.assertIn("How to read a source-linked artifact", projects_index_text)
            self.assertIn("Source-boundary reading guide", changelog.read_text(encoding="utf-8"))
            self.assertIn("Current project index grouped by practice", changelog.read_text(encoding="utf-8"))
            self.assertTrue((output / "projects" / "cra-srp-guidance-changelog.html").is_file())
            cra_changelog = (output / "projects" / "cra-srp-guidance-changelog.html").read_text(encoding="utf-8")
            self.assertIn("What this version covers", cra_changelog)
            self.assertIn("seven primary pages checked on 11 September", cra_changelog)
            self.assertIn("2026-09-11.1 is a dated reading", cra_changelog)
            self.assertIn("does not mirror their full text", cra_changelog)
            self.assertNotIn("task #", cra_changelog.lower())
            self.assertNotIn("/srv/rodion", cra_changelog)
            bounty_scout = output / "projects" / "bounty-scout.html"
            self.assertTrue(bounty_scout.is_file())
            bounty_text = bounty_scout.read_text(encoding="utf-8")
            self.assertIn("Bounty Scout", bounty_text)
            self.assertIn("five awarded payouts within 90 days", bounty_text)
            self.assertIn("does not create an account", bounty_text)
            self.assertIn("not a bounty marketplace", bounty_text)
            self.assertIn("Method: three public checks", bounty_text)
            self.assertIn("Payment recency:", bounty_text)
            self.assertIn("Competition is legible:", bounty_text)
            self.assertIn("A zero is a result", bounty_text)
            self.assertIn("honest result is zero qualified payers", bounty_text)
            self.assertIn("A repeatable check", bounty_text)
            self.assertIn("no authenticated marketplace access", bounty_text)
            self.assertIn("Latest public reading", bounty_text)
            self.assertIn("Source verification card", bounty_text)
            self.assertIn("three independent source cards", bounty_text)
            self.assertIn("Evidence claim map", bounty_text)
            self.assertIn("What this source can establish", bounty_text)
            self.assertIn("What it cannot establish", bounty_text)
            self.assertIn("does not establish funded work", bounty_text)
            self.assertIn("0 qualified payers", bounty_text)
            self.assertIn('<strong><time datetime="2026-09-12T10:05:46Z">12 Sep 2026 · 10:05 UTC</time> · 0 qualified payers', bounty_text)
            self.assertIn("Reading matrix: seven direct source checks", bounty_text)
            self.assertIn("Completed payout cards observed in the trailing 90 days", bounty_text)
            self.assertIn("Unavailable (HTTP 404)", bounty_text)
            self.assertIn("https://algora.io/activepieces/bounties?status=completed", bounty_text)
            self.assertIn("This matrix measures payout recency only", bounty_text)
            self.assertIn("HTTP 404 and are recorded as unavailable", bounty_text)
            self.assertIn("across seven organisations", bounty_text)
            self.assertNotIn("across eight organisations", bounty_text)
            self.assertIn("Algora completed pages (7 orgs)", bounty_text)
            self.assertIn("AsherKasper/bounty-census", bounty_text)
            self.assertIn("Public sources for this reading", bounty_text)
            self.assertIn("https://github.com/AsherKasper/bounty-census", bounty_text)
            self.assertIn("https://api.github.com/repos/PG-AGI/toingg-jarvis/issues/13", bounty_text)
            self.assertIn("Read the current evidence in order", bounty_text)
            self.assertIn("Open the independently checked candidate record", bounty_text)
            self.assertIn("https://github.com/AsherKasper/bounty-census/blob/953c25f4c1b85cc5504e2567ca28c4d44cd49031/BOUNTIES.md", bounty_text)
            self.assertIn("commit <code>953c25f</code>", bounty_text)
            self.assertIn("Bounty Scout immutable source snapshot", changelog.read_text(encoding="utf-8"))
            self.assertIn("Bounty Scout evidence snapshot", changelog.read_text(encoding="utf-8"))
            self.assertIn("The links are evidence, not endorsements", bounty_text)
            self.assertIn("Field note: evidence has a shelf life", bounty_text)
            self.assertIn("Freshness rule: treat a reading as a historical screen after 24 hours", bounty_text)
            self.assertIn("not a live availability badge", bounty_text)
            self.assertIn("Decision boundary: screen, then verify", bounty_text)
            self.assertIn("No external action from this page", bounty_text)
            self.assertIn("all three gates pass again", bounty_text)
            self.assertIn("Reproducible reading checklist", bounty_text)
            self.assertIn("record the UTC check time", bounty_text)
            self.assertIn("do not infer payment history", bounty_text)
            self.assertIn("A bounty label is not payment evidence", bounty_text)
            self.assertIn("does not turn an absence of evidence", bounty_text)
            self.assertIn("Screen record template", bounty_text)
            self.assertIn("Decision: REJECT", bounty_text)
            self.assertIn("Why: identify the failed gate", bounty_text)
            self.assertIn("Evidence freshness timeline", bounty_text)
            self.assertIn("Separate public observations in this dated screen", bounty_text)
            self.assertIn("caption-side:top", bounty_text)
            self.assertIn('datetime="2026-09-11T11:16:00Z"', bounty_text)
            self.assertIn('datetime="2026-09-11T18:50:27Z"', bounty_text)
            self.assertIn('datetime="2026-09-12T10:05:46Z"', bounty_text)
            self.assertIn('datetime="2026-09-13T10:05:46Z"', bounty_text)
            self.assertIn("a payout-velocity scan, and an expiry boundary are different observations", bounty_text)
            self.assertIn("What this dated screen did—and did not—measure", bounty_text)
            self.assertIn("Payout recency (five completed awards in 90 days)", bounty_text)
            self.assertIn("Not measured by this candidate inventory", bounty_text)
            self.assertIn("Bounty Scout screen record", changelog.read_text(encoding="utf-8"))
            self.assertIn("Bounty Scout", projects_index_text)
            self.assertIn("Bounty Scout", index_text)
            self.assertIn("Bounty Scout", changelog.read_text(encoding="utf-8"))
            self.assertNotIn("task #", bounty_text.lower())
            self.assertNotIn("/srv/rodion", bounty_text)
            cosmetics = output / "projects" / "cosmetics-change-impact.html"
            self.assertTrue(cosmetics.is_file())
            cosmetics_text = cosmetics.read_text(encoding="utf-8")
            self.assertIn("Cosmetics Change Impact", cosmetics_text)
            self.assertIn("Not a clearance engine", cosmetics_text)
            self.assertIn("not legal advice", cosmetics_text)
            self.assertIn("Commission Regulations (EU) 2026/909 and 2026/78", cosmetics_text)
            self.assertIn("Cosmetics Change Impact", projects_index_text)
            self.assertIn("Cosmetics Change Impact", index_text)
            self.assertIn("Cosmetics Change Impact project page", changelog.read_text(encoding="utf-8"))
            current_blog = (output / "blog" / "2026-09-12-this-week-verified-work.html").read_text(encoding="utf-8")
            self.assertIn("5 of 5 publisher responses changed", current_blog)
            self.assertIn("Algora velocity scan across 7 organisations", current_blog)
            self.assertNotIn("Algora velocity scan across 8 organisations", current_blog)
            self.assertNotIn("33121", current_blog)
            self.assertNotIn("33108", current_blog)
            self.assertIn("competition identifiers checked", blog_index.read_text(encoding="utf-8"))
            self.assertIn("5 publisher responses changed", blog_index.read_text(encoding="utf-8"))
            self.assertNotIn("3 changed: CosIng", current_blog)
            self.assertNotIn("task #", cosmetics_text.lower())
            self.assertNotIn("/srv/rodion", cosmetics_text)
            cra_text = (output / "projects" / "cra-srp-readiness.html").read_text(encoding="utf-8")
            self.assertIn("Deadline clock aid", cra_text)
            self.assertIn("Browser timezone", cra_text)
            self.assertIn("Stage-field preparation checklist", cra_text)
            self.assertIn("Assigned Representative limit conflict", cra_text)
            self.assertIn("Draft visibility warning", cra_text)
            self.assertIn("Source re-checked 11 September 2026", cra_text)
            self.assertIn("corpus 2026-09-11.1", cra_text)
            self.assertIn("cra-deadline-calc", cra_text)
            self.assertIn("2026-09-11 — CRA primary-source re-check", changelog.read_text(encoding="utf-8"))
            self.assertIn("Re-checked seven authoritative", changelog.read_text(encoding="utf-8"))
            self.assertIn("Hash Generator", changelog.read_text(encoding="utf-8"))
            self.assertIn("UUID Generator", changelog.read_text(encoding="utf-8"))
            self.assertIn("Hash Generator", hash_project.read_text(encoding="utf-8"))
            self.assertIn("UUID Generator", uuid_project.read_text(encoding="utf-8"))
            hash_tool_text = hash_tool.read_text(encoding="utf-8")
            self.assertIn("SHA-256", hash_tool_text)
            self.assertIn("SHA-512", hash_tool_text)
            self.assertNotIn("hashText('MD5')", hash_tool_text)
            self.assertNotIn("MD5", hash_project.read_text(encoding="utf-8"))
            self.assertIn("Rodion", index.read_text(encoding="utf-8"))
            self.assertIn('id="minify"', json_formatter.read_text(encoding="utf-8"))
            self.assertIn("Minified JSON locally.", json_formatter.read_text(encoding="utf-8"))
            self.assertIn('name="description" content="Format, validate, and minify JSON locally in your browser."', json_formatter.read_text(encoding="utf-8"))
            self.assertIn('name="description" content="Encode and decode URL components locally in your browser."', url_encoder.read_text(encoding="utf-8"))
            self.assertNotIn('\\\\"', index.read_text(encoding="utf-8"))
            self.assertIn("No pitch deck. Just artifacts.", index.read_text(encoding="utf-8"))
            self.assertIn('href="#main"', index_text)
            self.assertIn('id="main"', index_text)
            self.assertIn('tabindex="-1"', index_text)
            self.assertIn('<nav aria-label="Primary navigation">', index_text)
            self.assertIn('href="#recent-work"', index_text)
            self.assertIn('aria-label="Latest verified work"', index_text)
            self.assertIn('href="/" aria-current="page">Home</a>', index_text)
            self.assertIn('href="/projects/" aria-current="page">Projects</a>', projects_index_text)
            self.assertIn('href="/projects/evidence-boundary.html" aria-current="page">Evidence guide</a>', evidence_boundary)
            self.assertIn('href="/changelog.html" aria-current="page">Changelog</a>', changelog.read_text(encoding="utf-8"))
            self.assertIn('href="/blog/" aria-current="page">Blog</a>', blog_index.read_text(encoding="utf-8"))
            self.assertIn('href="/#recent-work"', projects_index_text)
            self.assertIn('id="recent-work"', index_text)
            self.assertIn("Latest verified work", index_text)
            self.assertIn(":focus-visible", index_text)
            self.assertIn(".skip-link:focus-visible", index_text)
            self.assertIn("prefers-reduced-motion: reduce", index_text)
            self.assertIn("scroll-behavior:auto", index_text)
            self.assertIn("animation-duration:.01ms!important", index_text)
            self.assertIn("transition-duration:.01ms!important", index_text)
            url_encoder_text = url_encoder.read_text(encoding="utf-8")
            self.assertIn("encodeURIComponent", url_encoder_text)
            self.assertIn("decodeURIComponent", url_encoder_text)
            self.assertIn("Nothing is transmitted or stored", url_encoder_text)
            self.assertNotIn("fetch(", url_encoder_text)
            self.assertNotIn("navigator.sendBeacon", url_encoder_text)
            self.assertIn("URL Encoder", url_encoder_project.read_text(encoding="utf-8"))
            self.assertIn("URL Encoder", changelog.read_text(encoding="utf-8"))
            self.assertIn("URL Encoder", index.read_text(encoding="utf-8"))
            self.assertIn("Unix Time Converter", changelog.read_text(encoding="utf-8"))
            self.assertNotIn("ledger snapshot", changelog.read_text(encoding="utf-8"))
            self.assertIn("Unix Time Converter 0.2", changelog.read_text(encoding="utf-8"))
            unix_time_text = unix_time_converter.read_text(encoding="utf-8")
            self.assertIn("Math.abs(val) >= 100000000000", unix_time_text)
            self.assertNotIn("tools/timestamp.html", index.read_text(encoding="utf-8"))
            self.assertNotIn("timestamp.html", "\n".join(path.as_posix() for path in output.rglob("*")))
            self.assertIn("Genesis", genesis.read_text(encoding="utf-8"))

    def test_build_includes_local_word_counter(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            tool = output / "tools" / "word-counter.html"
            project = output / "projects" / "word-counter.html"
            index = (output / "index.html").read_text(encoding="utf-8")
            changelog = (output / "changelog.html").read_text(encoding="utf-8")

            self.assertTrue(tool.is_file())
            self.assertTrue(project.is_file())
            tool_html = tool.read_text(encoding="utf-8")
            self.assertIn("Word Counter", tool_html)
            self.assertIn(r"split(/\s+/)", tool_html)
            self.assertIn("String.fromCharCode(10)", tool_html)
            self.assertNotIn("fetch(", tool_html)
            self.assertIn("Word Counter", project.read_text(encoding="utf-8"))
            self.assertIn("Word Counter", index)
            self.assertIn("Word Counter", changelog)

    def test_generated_public_pages_exclude_operational_identifiers(self) -> None:
        """Public output must not accidentally inherit internal operational details."""
        forbidden = (
            "/srv/rodion",
            "10.10.5.15",
            "task #",
            "need #",
            "ledger snapshot",
        )
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)
            for generated in output.rglob("*.html"):
                with self.subTest(page=generated.relative_to(output)):
                    text = generated.read_text(encoding="utf-8").lower()
                    for identifier in forbidden:
                        self.assertNotIn(identifier, text)

    def test_genesis_is_terse_and_public_facing(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            genesis = (output / "blog" / "genesis.html").read_text(encoding="utf-8")
            self.assertIn("2026-08-29", genesis)
            self.assertIn("Rodion came online with no audience", genesis)
            self.assertNotIn("ledger snapshot", genesis)

    def test_build_includes_public_craft_note_about_verified_readiness_tools(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            note = output / "blog" / "verified-readiness-tools.html"
            self.assertTrue(note.is_file())
            text = note.read_text(encoding="utf-8")
            self.assertIn("Evidence before confidence", text)
            self.assertIn("workflow/readiness aid", text)
            self.assertNotIn("task #", text.lower())

            home = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Evidence before confidence", home)
            self.assertIn("/blog/verified-readiness-tools.html", home)
            self.assertNotIn("/srv/rodion", text)


    def test_blog_records_a_dated_negative_bounty_screen_without_overclaiming(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            note = output / "blog" / "negative-screens-are-evidence.html"
            self.assertTrue(note.is_file())
            text = note.read_text(encoding="utf-8")
            self.assertIn("A zero is evidence, not a verdict", text)
            self.assertIn("11 September 2026", text)
            self.assertIn("not a claim that no bounties exist", text)
            self.assertNotIn("task #", text.lower())

            blog_index = (output / "blog" / "index.html").read_text(encoding="utf-8")
            self.assertIn("A zero is evidence, not a verdict", blog_index)
            self.assertIn("/blog/negative-screens-are-evidence.html", blog_index)

    def test_blog_includes_facts_only_weekly_build_note(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            note = output / "blog" / "week-in-artifacts.html"
            self.assertTrue(note.is_file())
            text = note.read_text(encoding="utf-8")
            self.assertIn("A week in artifacts", text)
            self.assertIn("11 September 2026", text)
            self.assertIn("CRA SRP Readiness", text)
            self.assertIn("Bounty Scout", text)
            self.assertIn("browser utilities", text)
            self.assertNotIn("task #", text.lower())
            self.assertNotIn("/srv/rodion", text)

            blog_index = (output / "blog" / "index.html").read_text(encoding="utf-8")
            self.assertIn("A week in artifacts", blog_index)
            self.assertIn("/blog/week-in-artifacts.html", blog_index)

    def test_blog_explains_that_a_bounty_screen_requires_separate_facts(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            note = output / "blog" / "separate-facts-before-action.html"
            self.assertTrue(note.is_file())
            text = note.read_text(encoding="utf-8")
            self.assertIn("Three facts before action", text)
            self.assertIn("five completed public awards in the prior 90 days", text)
            self.assertIn("not permission to claim, contact, or submit", text)
            self.assertNotIn("task #", text.lower())
            self.assertNotIn("/srv/rodion", text)

            blog_index = (output / "blog" / "index.html").read_text(encoding="utf-8")
            self.assertIn("Three facts before action", blog_index)
            self.assertIn("/blog/separate-facts-before-action.html", blog_index)

    def test_public_deploy_uses_root_paths_and_custom_domain(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            index = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="/"', index)
            self.assertNotIn('href="/site/', index)
            self.assertEqual("rodion.place\n", (output / "CNAME").read_text(encoding="utf-8"))


    def test_generated_site_does_not_leak_internal_operational_markers(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            html = "".join(path.read_text(encoding="utf-8") for path in output.rglob("*.html"))
            for marker in ("/srv/rodion/", "goal_id=", "Rodion ⇄ John", "@john:", "10.10.5.15"):
                self.assertNotIn(marker, html)

    def test_generated_root_relative_links_resolve_to_generated_pages(self) -> None:
        """A static deployment must not hide a broken internal navigation link."""
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            missing: list[str] = []
            for page in output.rglob("*.html"):
                for href in re.findall(r'href="([^"#]+)', page.read_text(encoding="utf-8")):
                    if not href.startswith("/") or href.startswith("//"):
                        continue
                    target = output / href.lstrip("/")
                    if href.endswith("/"):
                        target /= "index.html"
                    if not target.is_file():
                        missing.append(f"{page.relative_to(output)} -> {href}")

            self.assertEqual([], missing, "broken generated internal links: " + "; ".join(missing))

    def test_lan_base_internal_links_resolve_to_generated_pages(self) -> None:
        """The Caddy /site preview must not conceal broken rebased navigation."""
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output, base="/site")

            missing: list[str] = []
            for page in output.rglob("*.html"):
                for href in re.findall(r'href="([^"#]+)', page.read_text(encoding="utf-8")):
                    if not href.startswith("/site/"):
                        continue
                    target = output / href.removeprefix("/site/")
                    if href.endswith("/"):
                        target /= "index.html"
                    if not target.is_file():
                        missing.append(f"{page.relative_to(output)} -> {href}")

            self.assertEqual([], missing, "broken LAN-preview links: " + "; ".join(missing))

    def test_cli_parser_does_not_interpret_flags_as_output_directories(self) -> None:
        output, base = parse_args(["--base", "/site"])
        self.assertEqual(Path(__file__).resolve().parents[1] / "dist", output)
        self.assertEqual("/site", base)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--base", "site"])


if __name__ == "__main__":
    unittest.main()
