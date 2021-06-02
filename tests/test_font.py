import unittest
from caprice.font import Font
from caprice import font

class TestFont(unittest.TestCase):
    def test_standard_font(self):
        f = Font(font.Times_Roman, None, "F1")
        self.assertEqual(f.standard_font_name, font.Times_Roman)
        f = Font("times_roman.ttf", None, "F1")
        self.assertEqual(f.standard_font_name, None)