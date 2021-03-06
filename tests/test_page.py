import unittest
import pathlib
from caprice.page import Page
from caprice.document import Document
from caprice.primitives import GName, GRef
from caprice import font
from caprice import utils

class TestPage(unittest.TestCase):
    def get_font_file_path(self):
        cwd = pathlib.Path(__file__).resolve().parent
        font_file = utils.join_paths(cwd, "data/fonts/Roboto Mono.otf")
        return font_file

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
        # Test 1
        doc = Document()
        page = doc.add_page()
        font1 = page.add_font(font.Times_Roman)
        page.use_font(font1)
        text = "Hello, World!"
        page.draw_text(0, 0, text)
        height = page.rect[3]
        flipped_y = height - 0
        y = flipped_y
        metrics = page.current_font.font_metrics(page.current_font_size)
        ascender = metrics["ascender"]
        y -= ascender
        code_string = page.current_font.text_unicode_to_code(text)
        expected = "BT\n/F1 12 Tf\n%d %d Td\n[%s] TJ\nET\n\n" % (0, y, code_string)
        self.assertEqual(page.content, expected)
        
        # Test 2, without explictly setting a font
        doc = Document()
        page = doc.add_page()
        text = "Hello, World!"
        page.set_font_size(18)
        page.draw_text(0, 0, text)
        height = page.rect[3]
        flipped_y = height - 0
        y = flipped_y
        metrics = page.current_font.font_metrics(page.current_font_size)
        ascender = metrics["ascender"]
        y -= ascender
        code_string = page.current_font.text_unicode_to_code(text)
        expected = "BT\n/F1 18 Tf\n%d %d Td\n[%s] TJ\nET\n\n" % (0, y, code_string)
        self.assertEqual(page.content, expected)
        
        # TODO: Test 3, particularly test update_unicode_text for TrueType font
