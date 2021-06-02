# -*- coding=utf-8 -*-

import unittest
from caprice.document import Document
from caprice.primitives import GIndirect
from caprice import font

class TestDocument(unittest.TestCase):
    def test_add_page(self):
        doc = Document()
        p1 = doc.add_page()
        doc.add_page()
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual(p1.doc, doc)

    def test_add_indirect(self):
        doc = Document()
        i1 = doc.new_indirect()
        i2 = doc.new_indirect()
        for i, v in enumerate(doc.indirects_dict):
            if i == 0:
                self.assertEqual(v, "1 0 R")
            elif i == 1:
                self.assertEqual(v, "2 0 R")

    def test_add_font(self):
        doc = Document()
        f1 = doc.add_font(font.Times_Roman)
        self.assertEqual(doc.fonts_dict["F1"].standard_font_name, font.Times_Roman)
        f2 = doc.add_font(font.Times_Italic)
        self.assertEqual(doc.fonts_dict["F2"].standard_font_name, font.Times_Italic)