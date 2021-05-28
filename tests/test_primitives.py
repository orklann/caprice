import unittest

from caprice.primitives import GLiteralString, GObject, GNumber, GBoolean
from caprice.primitives import GHexString, GName, GNull, GArray
from caprice.primitives import UNDEFINED_NUMBER


class TestGObject(unittest.TestCase):
    def test_attrs(self):
        o = GObject()
        self.assertEqual(o.obj_num, UNDEFINED_NUMBER)
        self.assertEqual(o.generation_num, UNDEFINED_NUMBER)
        self.assertEqual(o.offset, UNDEFINED_NUMBER)
        o.obj_num = 1
        o.generation_num = 0
        o.offset = 1024
        self.assertEqual(o.obj_num, 1)
        self.assertEqual(o.generation_num, 0)
        self.assertEqual(o.offset, 1024)
    

class TestGNumber(unittest.TestCase):
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

    def test_super_class(self):
        n = GNull()
        self.assertEqual(n.obj_num, UNDEFINED_NUMBER)
        n.obj_num = 2
        self.assertEqual(n.obj_num, 2)

class TestGArray(unittest.TestCase):
    def test_compile_str(self):
        a = GArray()
        a.array.append(GName("Font"))
        a.array.append(GNull())
        a.array.append(GNumber(3.14))
        a.array.append(GBoolean(False))
        a.array.append(GLiteralString("Hello"))
        self.assertEqual(a.compile_str(), "[ /Font null 3.14 false (Hello) ]")

    def test_compile_bytes(self):
        a = GArray()
        a.array.append(GName("Font"))
        a.array.append(GNull())
        a.array.append(GNumber(3.14))
        a.array.append(GBoolean(False))
        a.array.append(GLiteralString("Hello"))
        self.assertEqual(a.compile_bytes(), b"[ /Font null 3.14 false (Hello) ]")

if __name__ == '__main__':
    unittest.main()