import unittest
from caprice.page import Page
from caprice.document import Document
from caprice.primitives import GName, GRef
from caprice import font

class TestPage(unittest.TestCase):
    def test_indirect_obj(self):
        doc = Document()
        page = Page(doc)
        self.assertEqual(page.indirect_obj.get_ref_str(), "3 0 R")
        parent_ref = page.dict.get(GName("Parent"))
        self.assertEqual(parent_ref.compile_str(), "2 0 R")

    def test_add_font(self):
        doc = Document()
        page = Page(doc)
        page.add_font(font.Times_Roman)
        page.add_font(font.Times_Roman)
        resource = page.dict.get(GName("Resources"))
        font_dict = resource.get(GName("Font"))
        expected = "<</F1 4 0 R /F2 5 0 R>>"
        self.assertEqual(font_dict.compile_str(), expected)

    def test_draw_text(self):
        doc = Document()
        page = doc.add_page()
        page.add_font(font.Times_Roman)
        text = "Hello, World!"
        page.draw_text(0, 0, text)

        # Test data
        height = page.rect[3]
        flipped_y = height - 0
        y = flipped_y
        expected = "BT\n/F1 18 Tf\n%d %d Td\n(%s) Tj\nET\n" % (0, y, text)
        self.assertEqual(page.content, expected)
