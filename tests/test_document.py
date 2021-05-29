# -*- coding=utf-8 -*-

import unittest
from caprice.document import Document
from caprice.primitives import GIndirect

class TestDocument(unittest.TestCase):
    def test_add_page(self):
        doc = Document()
        p1 = doc.add_page()
        doc.add_page()
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual(p1.doc, doc)

    def test_add_indirect(self):
        doc = Document()
        i1 = GIndirect()
        doc.add_indirect(i1)
        i2 = GIndirect()
        doc.add_indirect(i2)
        for i, v in enumerate(doc.indirects_dict):
            if i == 0:
                self.assertEqual(v, "1 0 R")
            elif i == 1:
                self.assertEqual(v, "2 0 R")
