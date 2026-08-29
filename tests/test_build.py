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
            showcase_project = output / "projects" / "showcase.html"
            methodology = output / "methodology.html"
            json_formatter = output / "tools" / "json-formatter.html"
            json_formatter_project = output / "projects" / "json-formatter.html"
            url_encoder = output / "tools" / "url-encoder.html"
            url_encoder_project = output / "projects" / "url-encoder.html"
            research_library_project = output / "projects" / "research-library.html"
            unix_time_converter = output / "tools" / "unix-time-converter.html"
            unix_time_converter_project = output / "projects" / "unix-time-converter.html"
            base64_tool = output / "tools" / "base64.html"
            base64_project = output / "projects" / "base64.html"
            hash_tool = output / "tools" / "hash-generator.html"
            hash_project = output / "projects" / "hash-generator.html"
            uuid_tool = output / "tools" / "uuid-generator.html"
            uuid_project = output / "projects" / "uuid-generator.html"

            self.assertTrue(index.is_file())
            self.assertTrue(genesis.is_file())
            self.assertTrue(changelog.is_file())
            self.assertTrue(showcase_project.is_file())
            self.assertTrue(methodology.is_file())
            self.assertTrue(json_formatter.is_file())
            self.assertTrue(json_formatter_project.is_file())
            self.assertTrue(url_encoder.is_file())
            self.assertTrue(url_encoder_project.is_file())
            self.assertTrue(research_library_project.is_file())
            self.assertTrue(unix_time_converter.is_file())
            self.assertTrue(unix_time_converter_project.is_file())
            self.assertTrue(base64_tool.is_file())
            self.assertTrue(base64_project.is_file())
            self.assertTrue(hash_tool.is_file())
            self.assertTrue(hash_project.is_file())
            self.assertTrue(uuid_tool.is_file())
            self.assertTrue(uuid_project.is_file())
            self.assertIn("Hash Generator", index.read_text(encoding="utf-8"))
            self.assertIn("UUID Generator", index.read_text(encoding="utf-8"))
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
            self.assertNotIn('\\\\"', index.read_text(encoding="utf-8"))
            self.assertIn("7 of 60", research_library_project.read_text(encoding="utf-8"))
            self.assertIn("10 of 10", research_library_project.read_text(encoding="utf-8"))
            self.assertIn("How to run", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("Verification", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("required showcase pages", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("python3 -m unittest discover -s tests -v", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("Principles", index.read_text(encoding="utf-8"))
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
            self.assertIn("Genesis", genesis.read_text(encoding="utf-8"))

    def test_build_includes_ledger_facts_without_private_data(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)

            genesis = (output / "blog" / "genesis.html").read_text(encoding="utf-8")
            self.assertIn("2026-08-29", genesis)
            self.assertIn("11 active goals", genesis)
            self.assertIn("$0.3242", genesis)
            self.assertNotIn("John", genesis)


if __name__ == "__main__":
    unittest.main()
