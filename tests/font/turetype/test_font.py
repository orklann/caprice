import unittest
import pathlib
from caprice import utils
from caprice.font.truetype.font import TrueType

class TestTrueType(unittest.TestCase):
    def get_font_file_path(self):
        cwd = pathlib.Path(__file__).resolve().parent.parent.parent
        font_file = utils.join_paths(cwd, "data/fonts/Roboto Mono.otf")
        return font_file

    def test_init(self):
        font_file = self.get_font_file_path()
        font = TrueType(font_file)
        self.assertEqual(font.font is not None, True)

    def test_get_base_font(self):
        font_file = self.get_font_file_path()
        font = TrueType(font_file)
        font_name = font.get_base_font().split("+")[1]
        self.assertEqual(font_name, "RobotoMonoNerdMediumPatchRegular")

    def test_generate_subset_tag(self):
        tag1 = TrueType.generate_subset_tag()
        tag2 = TrueType.generate_subset_tag()
        self.assertTrue(tag1 != tag2)
