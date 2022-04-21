import unittest
from caprice.font.encoding.win_ansi_encoding import WinAnsiEncoding

class TestWinAnsiEncoding(unittest.TestCase):
    """Test all base class's methods, and also test if this encoding 
    is correct"""

    def test_name(self):
        """Test base class's name() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.name(0o101), "A")
        self.assertEqual(win.name(0o255), "hyphen")
        # Make sure to call code_from_unicode() to construct difference
        c1 = win.code_from_unicode("˚")
        self.assertEqual(c1, 1)
        self.assertEqual(win.name(c1), "ring")
 
    def test_code(self):
        """Test base class's code() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.code("ydieresis"), 0o377)
        self.assertEqual(win.code("hyphen"), 0o055)
        # Make sure to call code_from_unicode() to construct difference
        c1 = win.code_from_unicode("˚")
        self.assertEqual(win.code("ring"), c1)

    def test_unicode(self):
        """Test base class's unicode() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.unicode(0o256), "®")
        self.assertEqual(win.unicode(0o200), "€")
        # Make sure to call code_from_unicode() to construct difference
        c1 = win.code_from_unicode("˚")
        self.assertEqual(win.unicode(c1), "˚")


    def test_code_from_unicode(self):
        """Test base class's code_from_unicode() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.code_from_unicode("®"), 0o256)
        self.assertEqual(win.code_from_unicode("€"), 0o200)
        # Make sure to call code_from_unicode() to construct difference
        c1 = win.code_from_unicode("˚")
        self.assertEqual(c1, 1)
        c2 = win.code_from_unicode("ı")
        self.assertEqual(c2, 2)

    def test_build_difference(self):
        """Test base class's build_difference() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.code_from_unicode("®"), 0o256)
        self.assertEqual(win.code_from_unicode("€"), 0o200)
        # Make sure to call code_from_unicode() to construct difference
        c1 = win.code_from_unicode("˚")
        c2 = win.code_from_unicode("ı")
        array = win.build_difference()
        expected = "[1 /ring 2 /dotlessi]"
        self.assertEqual(array.compile_str(), expected)
