from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from build import build


class BuildTests(unittest.TestCase):
    def test_build_writes_required_pages(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            index = output / "index.html"
            genesis = output / "blog" / "genesis.html"
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
            index_text = index.read_text(encoding="utf-8")
            self.assertIn("CRA SRP Readiness", index_text)
            self.assertIn("AI-built workflow/readiness aid", index_text)
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
            self.assertTrue((output / "projects" / "cra-srp-readiness.html").is_file())
            self.assertTrue((output / "projects" / "cra-srp-guidance-changelog.html").is_file())
            cra_text = (output / "projects" / "cra-srp-readiness.html").read_text(encoding="utf-8")
            self.assertIn("Deadline clock aid", cra_text)
            self.assertIn("Browser timezone", cra_text)
            self.assertIn("Stage-field preparation checklist", cra_text)
            self.assertIn("Assigned Representative limit conflict", cra_text)
            self.assertIn("Draft visibility warning", cra_text)
            self.assertIn("Guidance as of 31 August 2026", cra_text)
            self.assertIn("cra-deadline-calc", cra_text)
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
            self.assertNotIn('\\\\"', index.read_text(encoding="utf-8"))
            self.assertIn("No pitch deck. Just artifacts.", index.read_text(encoding="utf-8"))
            self.assertIn('href="#main"', index_text)
            self.assertIn('id="main"', index_text)
            self.assertIn(":focus-visible", index_text)
            self.assertIn("prefers-reduced-motion: reduce", index_text)
            self.assertIn("scroll-behavior:auto", index_text)
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


if __name__ == "__main__":
    unittest.main()
