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
            research_library_project = output / "projects" / "research-library.html"

            self.assertTrue(index.is_file())
            self.assertTrue(genesis.is_file())
            self.assertTrue(changelog.is_file())
            self.assertTrue(showcase_project.is_file())
            self.assertTrue(methodology.is_file())
            self.assertTrue(json_formatter.is_file())
            self.assertTrue(json_formatter_project.is_file())
            self.assertTrue(research_library_project.is_file())
            self.assertIn("Rodion", index.read_text(encoding="utf-8"))
            self.assertIn("5 of 60", research_library_project.read_text(encoding="utf-8"))
            self.assertIn("How to run", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("Verification", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("required showcase pages", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("python3 -m unittest discover -s tests -v", showcase_project.read_text(encoding="utf-8"))
            self.assertIn("Principles", index.read_text(encoding="utf-8"))
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
