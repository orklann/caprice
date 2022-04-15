import unittest
from caprice.font.encoding import glyph_list

class TestGlyphList(unittest.TestCase):
    def test_glyph_list(self):
        self.assertEqual(id(glyph_list.glyph_list), id(glyph_list.glyph_list))

