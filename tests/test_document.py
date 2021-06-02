# -*- coding=utf-8 -*-

import unittest
from caprice.document import Document
from caprice.primitives import GIndirect, GName
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
            elif i == 2:
                self.assertEqual(v, "3 0 R")

    def test_add_font(self):
        doc = Document()
        f1 = doc.add_font(font.Times_Roman)
        self.assertEqual(doc.fonts_dict["F1"].standard_font_name, font.Times_Roman)
        self.assertEqual(doc.fonts_dict["F1"].indirect_obj.get_ref_str(), "2 0 R")
        f2 = doc.add_font(font.Times_Italic)
        self.assertEqual(doc.fonts_dict["F2"].standard_font_name, font.Times_Italic)
        self.assertEqual(doc.fonts_dict["F2"].indirect_obj.get_ref_str(), "3 0 R")
        self.assertEqual(len(doc.indirects_dict), 3)

    def test_create_catalog(self):
        doc = Document()
        catalog = doc.catalog.object
        rootPages = catalog.get(GName("Pages"))
        self.assertEqual(rootPages.compile_str(), "2 0 R")