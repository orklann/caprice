# -*- coding=utf-8 -*-

import unittest
from caprice.page import Page
from caprice.document import Document

class TestPage(unittest.TestCase):
    def test_indirect_obj(self):
        doc = Document()
        page = Page(doc)
        self.assertEqual(page.indirect_obj.get_ref_str(), "1 0 R")
