import unittest

from caprice.primitives import GLiteralString, GObject, GNumber, GBoolean


class TestGObject(unittest.TestCase):
    def test_attrs(self):
        o = GObject()
        self.assertEqual(o.obj_num, -1)
        self.assertEqual(o.generation_num, -1)
        self.assertEqual(o.offset, -1)
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
        self.assertEqual(n.__str__(), "1.200000")

    def test_bytes(self):
        n = GNumber(1)
        self.assertEqual(n.bytes(), b"1")
        n = GNumber(1.2)
        self.assertEqual(n.bytes(), b"1.200000")

    def test_compile_str(self):
        n = GNumber(1)
        self.assertEqual(n.compile_str(), "1")
        n = GNumber(1.2)
        self.assertEqual(n.compile_str(), "1.200000")

    def test_compile_bytes(self):
        n = GNumber(1)
        self.assertEqual(n.compile_bytes(), b"1")
        n = GNumber(1.2)
        self.assertEqual(n.compile_bytes(), b"1.200000")


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

if __name__ == '__main__':
    unittest.main()