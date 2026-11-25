"""Позитивные и отрицательные примеры синтаксиса."""

import unittest

from src.parser import parse


class ParserTests(unittest.TestCase):
    def test_comments_and_nesting(self):
        text = "C comment\nvar a (list 0. {-\nblock\n-} (list 1.25));"
        self.assertEqual(parse(text).children[0].data, "declaration")

    def test_invalid_inputs(self):
        for text in ("var a 1;", "var A 1.;", "{-a", "(list", "$+ 1$",
                     "var a 2.", "varname 2.;", "var a -1.;"):
            with self.subTest(text=text), self.assertRaisesRegex(
                ValueError, "строка"
            ):
                parse(text)
