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
 
    def test_code(self):
        """Test base class's code() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.code("ydieresis"), 0o377)
        self.assertEqual(win.code("hyphen"), 0o055)

    def test_unicode(self):
        """Test base class's unicode() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.unicode(0o256), "®")
        self.assertEqual(win.unicode(0o200), "€")

    def test_code_from_unicode(self):
        """Test base class's code_from_unicode() method"""
        win = WinAnsiEncoding()
        self.assertEqual(win.code_from_unicode("®"), 0o256)
        self.assertEqual(win.code_from_unicode("€"), 0o200)
