import unittest
from caprice.font.encoding.glyph_list import GlyphList

class TestGlyphList(unittest.TestCase):
    def test_glyph_list(self):
        s1 = GlyphList()
        s2 = GlyphList()
        self.assertEqual(id(s1), id(s2))

