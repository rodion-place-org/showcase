import contextlib
import io
from pathlib import Path
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
            self.assertIn("Preparation aids", projects_index_text)
            self.assertIn("Checks you can repeat", projects_index_text)
            self.assertIn("Your input stays put", projects_index_text)
            self.assertIn(".project-grid,.boundary", projects_index_text)
            self.assertIn('id="utilities"', projects_index_text)
            self.assertIn('href="/projects/"', index_text)
            self.assertIn('href="/projects/#utilities"', index_text)
            self.assertIn('href="/projects/#utilities"', projects_index_text)
            self.assertTrue((output / "projects" / "cra-srp-readiness.html").is_file())
            self.assertTrue((output / "projects" / "cra-srp-guidance-changelog.html").is_file())
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
            self.assertIn("0 qualified payers", bounty_text)
            self.assertIn("2026-09-11, 07:49 UTC", bounty_text)
            self.assertIn("112 days old", bounty_text)
            self.assertIn("AsherKasper/bounty-census", bounty_text)
            self.assertIn("Public sources for this reading", bounty_text)
            self.assertIn("https://github.com/AsherKasper/bounty-census", bounty_text)
            self.assertIn("https://api.github.com/repos/PG-AGI/toingg-jarvis/issues/13", bounty_text)
            self.assertIn("Read the current evidence in order", bounty_text)
            self.assertIn("Open the exact inventory snapshot screened on 11 September", bounty_text)
            self.assertIn("https://github.com/AsherKasper/bounty-census/blob/d9ed1ed06abe29fe3d4c0f2d6e8be5435d56fc60/BOUNTIES.md", bounty_text)
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

    def test_cli_parser_does_not_interpret_flags_as_output_directories(self) -> None:
        output, base = parse_args(["--base", "/site"])
        self.assertEqual(Path(__file__).resolve().parents[1] / "dist", output)
        self.assertEqual("/site", base)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--base", "site"])


if __name__ == "__main__":
    unittest.main()
