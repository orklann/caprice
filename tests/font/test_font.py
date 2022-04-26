import pathlib
import unittest
from caprice.font import Font
from caprice.document import Document
from caprice.primitives import GName
from caprice import font
from caprice import utils

class TestFont(unittest.TestCase):
    def get_font_file_path(self):
        cwd = pathlib.Path(__file__).resolve().parent.parent
        font_file = utils.join_paths(cwd, "data/fonts/Roboto Mono.otf")
        return font_file

    def test_standard_font(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        self.assertEqual(f.standard_font_name, font.Times_Roman)

    def test_truetype_font(self):
        doc = Document()
        font_file = self.get_font_file_path()
        f = Font(font_file, doc, "F1")
        font_dict = f.dict
        self.assertEqual(font_dict.get(GName("Type")), GName("Font"))
        self.assertEqual(font_dict.get(GName("Subtype")), GName("TrueType"))

    def test_add_to_unicode_set(self):
        doc = Document()
        font_file = self.get_font_file_path()
        f = Font(font_file, doc, "F1")
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("B"))
        expected = set([ord("A"), ord("B")])
        self.assertEqual(f.unicode_set, expected)
        
    def test_compile_str(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        expected = "3 0 obj\r\n<</Type /Font /Subtype /Type1 /BaseFont /%s /Encoding <</Type /Encoding /BaseEncoding /WinAnsiEncoding /Differences []>>>>\r\nendobj\r\n\r\n" % font.Times_Roman
        self.assertEqual(f.compile_str(), expected)

    def test_compile_bytes(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        expected = "3 0 obj\r\n<</Type /Font /Subtype /Type1 /BaseFont /%s /Encoding <</Type /Encoding /BaseEncoding /WinAnsiEncoding /Differences []>>>>\r\nendobj\r\n\r\n" % font.Times_Roman
        self.assertEqual(f.compile_bytes(), str.encode(expected))

    def test_code(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        self.assertEqual(f.code("®"), 0o256)
        self.assertEqual(f.code("€"), 0o200)

    def test_width(self):
        doc = Document()
        f = Font(font.Courier, doc, "F1")
        w = f.width("A", 12)
        self.assertEqual(w, 8)

    def test_latin_chars(self):
        self.assertEqual(len(font.LATIN_CHARS), 229)
