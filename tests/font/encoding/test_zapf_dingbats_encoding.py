import unittest
from caprice.font.encoding.zapf_dingbats_encoding import ZapfDingbatsEncoding

class TestZapfDingbatsEncoding(unittest.TestCase):
    """Test all base class's methods, and also test if this encoding 
    is correct"""

    def test_name(self):
        """Test base class's name() method"""
        zapf = ZapfDingbatsEncoding()
        self.assertEqual(zapf.name(0o040), "space")
        self.assertEqual(zapf.name(0o376 ), "a191")
 
    def test_code(self):
        """Test base class's code() method"""
        zapf = ZapfDingbatsEncoding()
        self.assertEqual(zapf.code("space"), 0o040)
        self.assertEqual(zapf.code("a179"), 0o351)

    def test_unicode(self):
        """Test base class's unicode() method"""
        zapf = ZapfDingbatsEncoding()
        self.assertEqual(zapf.unicode(0o042), "✂")
        self.assertEqual(zapf.unicode(0o244), "❤")

    def test_code_from_unicode(self):
        """Test base class's code_from_unicode() method"""
        zapf = ZapfDingbatsEncoding()
        self.assertEqual(zapf.code_from_unicode("✂"), 0o042)
        self.assertEqual(zapf.code_from_unicode("❤"), 0o244)
