import unittest
from caprice import utils

class TestUtils(unittest.TestCase):
    def test_join_paths(self):
        path = utils.join_paths("/Users/James", "books", "Python")
        expected = "/Users/James/books/Python"
        self.assertEqual(path, expected)

