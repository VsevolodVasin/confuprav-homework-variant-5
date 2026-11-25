"""Проверки вычислений, представления XML и диагностики CLI."""

import subprocess
import sys
import unittest
from xml.etree import ElementTree as et

from src.translator import translate


class TranslatorTests(unittest.TestCase):
    def test_nested_operations(self):
        text = "var x 2.; var y (list (list $pow $+ x 1$ 2$) $- 1 3$);"
        root = et.fromstring(translate(text))
        values = [n.text for n in root.iter("number")]
        self.assertEqual(values, ["2", "9", "-2"])
        self.assertEqual(root[1].attrib, {"name": "y"})
        self.assertEqual(root[1][0][0].tag, "list")

    def test_decimal(self):
        self.assertIn("<number>0.3</number>", translate("$+ 0.1 0.2$"))

    def test_empty_list_and_comments(self):
        self.assertEqual(translate("C x\n(list {-x-})"), translate("(list)"))
        self.assertIsNotNone(et.fromstring(translate("(list)")).find("list"))

    def test_errors(self):
        for source in ("$+ x 1$", "var x 1.; var x 2.;", "$+ (list) 1$",
                       "$pow 0 0$", "var z .;"):
            result = subprocess.run(
                [sys.executable, "-m", "src.cli"], input=source,
                capture_output=True, text=True, check=False,
            )
            with self.subTest(source=source):
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("Ошибка", result.stderr)
