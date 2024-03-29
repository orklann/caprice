import pathlib
import unittest
from caprice.font import Font
from caprice.document import Document
from caprice.primitives import GName, GNumber, GArray
from caprice import font
from caprice import utils

class TestFont(unittest.TestCase):
    def get_font_file_path(self):
        cwd = pathlib.Path(__file__).resolve().parent.parent
        font_file = utils.join_paths(cwd, "data/fonts/Roboto Mono.otf")
        return font_file

    def get_open_sans_path(self):
        cwd = pathlib.Path(__file__).resolve().parent.parent
        font_file = utils.join_paths(cwd, "data/fonts/OpenSans-Regular.ttf")
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

    def test_update(self):
        doc = Document()
        font_file = self.get_font_file_path()
        f = Font(font_file, doc, "F1")
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("B"))
        f.add_to_unicode_set(ord("M"))
        f.update()
        expected = GNumber(ord("A")).compile_str()
        self.assertEqual(f.dict.get(GName("FirstChar")).compile_str(), expected)
        expected = GNumber(ord("M")).compile_str()
        self.assertEqual(f.dict.get(GName("LastChar")).compile_str(), expected)

        # Test case for /Widths array
        font_file = self.get_open_sans_path()
        f = Font(font_file, doc, "F2")
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("B"))
        f.add_to_unicode_set(ord("D"))
        f.update()
        expected = GArray()
        expected.append(GNumber(int(632.324219)))
        expected.append(GNumber(int(645.996094)))
        expected.append(GNumber(0))
        expected.append(GNumber(int(725.585938)))
        self.assertEqual(f.dict.get(GName("Widths")).compile_str(), expected.compile_str())
        
    def test_add_to_unicode_set(self):
        doc = Document()
        font_file = self.get_font_file_path()
        f = Font(font_file, doc, "F1")
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("B"))
        expected = set([ord("A"), ord("B")])
        self.assertEqual(f.unicode_set, expected)
        
    def test_update_unicode_set(self):
        doc = Document()
        font_file = self.get_font_file_path()
        f = Font(font_file, doc, "F1")
        text = "ABCDEFGABCDEFG"
        f.update_unicode_set(text)
        expected = set()
        for c in text:
            expected.add(ord(c))
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

    def test_get_subset(self):
        doc = Document()
        font_file = self.get_open_sans_path()
        f = Font(font_file, doc, "F2")
        f.add_to_unicode_set(ord("A"))
        f.add_to_unicode_set(ord("B"))
        f.add_to_unicode_set(ord("D"))
        font_program = f.get_subset()
