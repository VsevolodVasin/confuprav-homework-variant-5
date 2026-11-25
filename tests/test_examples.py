"""Проверка трёх конфигураций через стандартные потоки CLI."""

import subprocess
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree


class ExampleTests(unittest.TestCase):
    def test_domains(self):
        cases = [("audio", "stereo", "96000"),
                 ("orchard", "water", "12"),
                 ("graphics", "pixels", "65536")]
        for domain, name, expected in cases:
            source = Path(f"examples/{domain}.cfg").read_text(encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "src.cli"], input=source,
                capture_output=True, text=True, check=True,
            )
            root = ElementTree.fromstring(result.stdout)
            with self.subTest(domain=domain):
                self.assertEqual(result.stderr, "")
                self.assertEqual(
                    root.find(f"./var[@name='{name}']//number").text, expected
                )
