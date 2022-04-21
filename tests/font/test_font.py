import unittest
from caprice.font import Font
from caprice.document import Document
from caprice import font

class TestFont(unittest.TestCase):
    def test_standard_font(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        self.assertEqual(f.standard_font_name, font.Times_Roman)
        f = Font("times_roman.ttf", doc, "F1")
        self.assertEqual(f.standard_font_name, None)

    def test_compile_str(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        expected = "3 0 obj\r\n<</Type /Font /Subtype /Type1 /BaseFont /%s /Encoding <</Type /Encoding /BaseEncoding /WinAnsiEncoding>>>>\r\nendobj\r\n\r\n" % font.Times_Roman
        self.assertEqual(f.compile_str(), expected)

    def test_compile_bytes(self):
        doc = Document()
        f = Font(font.Times_Roman, doc, "F1")
        expected = "3 0 obj\r\n<</Type /Font /Subtype /Type1 /BaseFont /%s /Encoding <</Type /Encoding /BaseEncoding /WinAnsiEncoding>>>>\r\nendobj\r\n\r\n" % font.Times_Roman
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
