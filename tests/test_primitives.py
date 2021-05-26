import unittest

from caprice.primitives import GObject, GNumber


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
    
if __name__ == '__main__':
    unittest.main()