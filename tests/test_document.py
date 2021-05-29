# -*- coding=utf-8 -*-

import unittest
from caprice.document import Document

class TestDocument(unittest.TestCase):
    def test_add_page(self):
        doc = Document()
        p1 = doc.add_page()
        doc.add_page()
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual(p1.doc, doc)
