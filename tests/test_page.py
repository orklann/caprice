import unittest
from caprice.page import Page
from caprice.document import Document
from caprice.primitives import GName, GRef

class TestPage(unittest.TestCase):
    def test_indirect_obj(self):
        doc = Document()
        page = Page(doc)
        self.assertEqual(page.indirect_obj.get_ref_str(), "3 0 R")
        parent_ref = page.dict.get(GName("Parent"))
        self.assertEqual(parent_ref.compile_str(), "2 0 R")
