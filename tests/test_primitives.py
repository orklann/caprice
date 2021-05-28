import unittest
from caprice.primitives import GLiteralString, GObject, GNumber, GBoolean
from caprice.primitives import GHexString, GName, GNull, GArray, GDictionary
from caprice.primitives import GStream, GIndirect
from caprice.primitives import UNDEFINED_NUMBER
import zlib

class TestGNumber(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, GNumber, "1")

    def test_str(self):
        n = GNumber(1)
        self.assertEqual(n.__str__(), "1")
        n = GNumber(1.2)
        self.assertEqual(n.__str__(), "1.2")

    def test_bytes(self):
        n = GNumber(1)
        self.assertEqual(n.bytes(), b"1")
        n = GNumber(1.2)
        self.assertEqual(n.bytes(), b"1.2")

    def test_compile_str(self):
        n = GNumber(1)
        self.assertEqual(n.compile_str(), "1")
        n = GNumber(1.2)
        self.assertEqual(n.compile_str(), "1.2")

    def test_compile_bytes(self):
        n = GNumber(1)
        self.assertEqual(n.compile_bytes(), b"1")
        n = GNumber(1.2)
        self.assertEqual(n.compile_bytes(), b"1.2")


class TestGBoolean(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, GBoolean, "True")

    def test_compile_str(self):
        b = GBoolean(True)
        self.assertEqual(b.compile_str(), "true")

        b = GBoolean(False)
        self.assertEqual(b.compile_str(), "false")

    def test_compile_bytes(self):
        b = GBoolean(True)
        self.assertEqual(b.compile_bytes(), b'true')

        b = GBoolean(False)
        self.assertEqual(b.compile_bytes(), b'false')


class TestGLiteralString(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, GLiteralString, 1)

    def test_str(self):
        ls = GLiteralString('This is a string')
        self.assertEqual(ls.__str__(), '(This is a string)')
        ls = GLiteralString('This is a string with a new line\n')
        self.assertEqual(ls.__str__(), '(This is a string with a new line\\n)')
        ls = GLiteralString("\n\r\t\b\f()\\")
        self.assertEqual(ls.__str__(), "(\\n\\r\\t\\b\\f\\(\\)\\\\)")
        ls = GLiteralString("This is not a printable ASCII:\x80")
        self.assertEqual(ls.__str__(), "(This is not a printable ASCII:\x80)")
        # Test character \x80 with value 0x80
        s = ls.__str__()
        self.assertEqual(ord(s[-2]), 0x80)

    def test_compile_str(self):
        ls = GLiteralString('This is a string')
        self.assertEqual(ls.compile_str(), '(This is a string)')
        ls = GLiteralString('This is a string with a new line\n')
        self.assertEqual(ls.compile_str(), '(This is a string with a new line\\n)')
        ls = GLiteralString("\n\r\t\b\f()\\")
        self.assertEqual(ls.compile_str(), "(\\n\\r\\t\\b\\f\\(\\)\\\\)")

    def test_compile_bytes(self):
        ls = GLiteralString('This is a string')
        self.assertEqual(ls.compile_bytes(), b'(This is a string)')
        ls = GLiteralString('This is a string with a new line\n')
        self.assertEqual(ls.compile_bytes(), b'(This is a string with a new line\\n)')
        ls = GLiteralString("\n\r\t\b\f()\\")
        self.assertEqual(ls.compile_bytes(), b"(\\n\\r\\t\\b\\f\\(\\)\\\\)")
        ls = GLiteralString("This is not a printable ASCII:\x80")
        self.assertEqual(ls.__str__(), "(This is not a printable ASCII:\x80)")
        # Test byte \x80 with value 0x80
        bytes = ls.bytes()
        self.assertEqual(bytes[-2], 0x80)

class TestGHexString(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, GHexString, 1)

    def test_str(self):
        h = GHexString("Hello, World!")
        self.assertEqual(h.__str__(), "<48656C6C6F2C20576F726C6421>")

    def test_bytes(self):
        h = GHexString("Hello, World!")
        self.assertEqual(h.bytes(), b"<48656C6C6F2C20576F726C6421>")

    def test_compile_str(self):
        h = GHexString("Hello, World!")
        self.assertEqual(h.compile_str(), "<48656C6C6F2C20576F726C6421>")

    def test_compile_bytes(self):
        h = GHexString("Hello, World!")
        self.assertEqual(h.compile_bytes(), b"<48656C6C6F2C20576F726C6421>")

class TestGName(unittest.TestCase):
    def test_type(self):
        self.assertRaises(TypeError, GName, 1)

    def test_str(self):
        n = GName("Name1")
        self.assertEqual(n.__str__(), "/Name1")

    def test_bytes(self):
        n = GName("Name1")
        self.assertEqual(n.bytes(), b"/Name1")

    def test_compile_str(self):
        n = GName("Name1")
        self.assertEqual(n.compile_str(), "/Name1")

    def test_compile_bytes(self):
        n = GName("Name1")
        self.assertEqual(n.compile_bytes(), b"/Name1")

    def test_as_dict_key(self):
        """Test GName as a dictionary key
        """
        key = GName("Font")
        key2 = GName("Size")
        dict = {}
        dict[key] = "Arial"
        dict[key2] = 12
        self.assertEqual(dict[key], "Arial")
        dict[key] = "Mono Serif"
        self.assertEqual(dict[key], "Mono Serif")
        self.assertEqual(dict[key2], 12)

class TestGNull(unittest.TestCase):
    def test_compile_str(self):
        n = GNull()
        self.assertEqual(n.compile_str(), "null")

    def test_compile_bytes(self):
        n = GNull()
        self.assertEqual(n.compile_bytes(), b"null")

class TestGArray(unittest.TestCase):
    def test_type(self):
        a = GArray()
        self.assertRaises(TypeError, a.append, 1)

    def test_compile_str(self):
        a = GArray()
        a.append(GName("Font"))
        a.append(GNull())
        a.append(GNumber(3.14))
        a.append(GBoolean(False))
        a.append(GLiteralString("Hello"))
        self.assertEqual(a.compile_str(), "[/Font null 3.14 false (Hello)]")

    def test_compile_bytes(self):
        a = GArray()
        a.append(GName("Font"))
        a.append(GNull())
        a.append(GNumber(3.14))
        a.append(GBoolean(False))
        a.append(GLiteralString("Hello"))
        self.assertEqual(a.compile_bytes(), b"[/Font null 3.14 false (Hello)]")


class TestGDictionary(unittest.TestCase):
    def test_type(self):
        d = GDictionary()
        self.assertRaises(TypeError, d.set, GHexString("key"), GName("value"))
        self.assertRaises(TypeError, d.set, GName("key"), 1)

    def test_key_value(self):
        d = GDictionary()
        d.set(GName("Font"), GName("Arial"))
        self.assertEqual(d.get(GName("Font")), GName("Arial"))
        self.assertRaises(TypeError, d.set, GLiteralString("Font2"), GName("Mono"))

    def test_str(self):
        d = GDictionary()
        d.set(GName("Font"), GName("Arial"))
        d.set(GName("GS"), GNumber(3.14))
        d.set(GName("Encoding"), GLiteralString("UTF-8"))
        expect = "<</Font /Arial /GS 3.14 /Encoding (UTF-8)>>"
        self.assertEqual(d.__str__(), expect)

    def test_bytes(self):
        d = GDictionary()
        d.set(GName("Font"), GName("Arial"))
        d.set(GName("GS"), GNumber(3.14))
        d.set(GName("Encoding"), GLiteralString("UTF-8"))
        expect = b"<</Font /Arial /GS 3.14 /Encoding (UTF-8)>>"
        self.assertEqual(d.bytes(), expect)

    def test_compile_str(self):
        d = GDictionary()
        d.set(GName("Font"), GName("Arial"))
        d.set(GName("GS"), GNumber(3.14))
        d.set(GName("Encoding"), GLiteralString("UTF-8"))
        expect = "<</Font /Arial /GS 3.14 /Encoding (UTF-8)>>"
        self.assertEqual(d.compile_str(), expect)

    def test_compile_bytes(self):
        d = GDictionary()
        d.set(GName("Font"), GName("Arial"))
        d.set(GName("GS"), GNumber(3.14))
        d.set(GName("Encoding"), GLiteralString("UTF-8"))
        expect = b"<</Font /Arial /GS 3.14 /Encoding (UTF-8)>>"
        self.assertEqual(d.compile_bytes(), expect)

class TestGStream(unittest.TestCase):
    def test_type(self):
        s = GStream()
        self.assertRaises(TypeError, s.set_content, (b"Hello, World"))

    def test_dict(self):
        s = GStream()
        s.set_content("Hello, World")
        s.bytes()
        self.assertEqual(s.dict.compile_str(), "<</Length 20 /Filter /FlateDecode>>")

    def test_encode(self):
        s = GStream()
        s.set_content("Hello, World!")
        encoded_bytes = s.encoded_bytes()
        decoded_bytes = zlib.decompress(encoded_bytes)
        self.assertEqual(decoded_bytes, s.content)
        # We have tested the encoded stream by using external app `PEP` with it's 
        # Tests framework.
        # The test file is: caprice_stream.bin in `PEPTests/pdf`
        # Result: Passing

class TestGIndirect(unittest.TestCase):
    def test_type(self):
        i = GIndirect()
        self.assertRaises(TypeError, i.set_obj_num, 1.0)
        self.assertRaises(TypeError, i.set_generation_num, 1.0)
        self.assertRaises(TypeError, i.set_offset, 1.0)
        self.assertRaises(TypeError, i.set_object, 1.0)

    def test_compile_bytes(self):
        i = GIndirect()
        i.set_obj_num(1)
        i.set_generation_num(0)
        d = GDictionary()
        d.set(GName("Key1"), GName("Val1"))
        d.set(GName("Key2"), GNumber(1))
        i.set_object(d)
        expect = b"1 0 obj\r\n<</Key1 /Val1 /Key2 1>>\r\nendobj\r\n"
        self.assertEqual(i.compile_bytes(), expect)
        # Test exception for object is None
        i = GIndirect()
        self.assertRaises(Exception, i.compile_bytes)

if __name__ == '__main__':
    unittest.main()