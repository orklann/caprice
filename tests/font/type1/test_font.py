import unittest
from caprice.font.type1.font import Type1
from caprice import font
from math import ceil

class TestType1(unittest.TestCase):
    def test_load_afm(self):
        type1 = Type1(font.Times_Roman)
        cap_height = ceil(type1.afm.CapHeight)
        ascender = ceil(type1.afm.Ascender)
        descender = ceil(type1.afm.Descender)
        self.assertEqual(cap_height, 662)
        self.assertEqual(ascender, 683)
        self.assertEqual(descender, -217)

    def test_code(self):
        type1 = Type1(font.Times_Roman)
        # By default Type1 font use WinAnsiEncoding
        self.assertEqual(type1.code("®"), 0o256)
        self.assertEqual(type1.code("€"), 0o200)
