import unittest
from caprice.font.encoding.glyph_list import GlyphList
from caprice import config
from caprice import utils

class TestGlyphList(unittest.TestCase):
    def test_glyph_list(self):
        s1 = GlyphList()
        s2 = GlyphList()
        self.assertEqual(id(s1), id(s2))

    def test_load_file(self):
        file = utils.join_paths(config.data_dir, "caprice", "encoding", "glyphlist.txt")
        gl = GlyphList()
        name_to_unicode, unicode_to_name = gl.load_file(file)
        self.assertEqual(name_to_unicode["A"], "A")
        self.assertEqual(unicode_to_name["ד"], "afii57667")
        self.assertEqual(name_to_unicode["dalethiriq"], "דִ")

    def test_load(self):
        gl = GlyphList()
        gl.load()
        self.assertEqual(gl.standard_name_to_unicode["A"], "A")
        self.assertEqual(gl.standard_unicode_to_name["ד"], "afii57667")
        self.assertEqual(gl.standard_name_to_unicode["dalethiriq"], "דִ")
        self.assertEqual(gl.zapf_name_to_unicode["a9"], "✠")
        self.assertEqual(gl.zapf_unicode_to_name["❆"], "a65")


