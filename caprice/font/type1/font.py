from math import ceil
from fontTools.afmLib import AFM
from ... import config
from ... import utils
from ..encoding import WinAnsiEncoding

class Type1:
    """Type1 font class for 14 standard fonts"""

    def __init__(self, font_name):
        self.font_name = font_name
        self.afm = None
        self.load_afm()
        # All measurements in AFM files use 1000 as units per em
        self.UNITS_PER_EM = 1000.0
        # We here use WinAnsiEncoding for all 14 standards fonts in PDF 
        self.encoding = WinAnsiEncoding()

    def load_afm(self):
        afm_file = utils.join_paths(config.data_dir, "caprice", "afm", \
                self.font_name + ".afm")
        self.afm = AFM(afm_file)

    def code(self, unicode):
        """Return character code for the given unicode for Type1 font"""
        return self.encoding.code_from_unicode(unicode)

    def width(self, unicode, font_size):
        glyph_name = self.encoding.unicode_to_name(unicode)
        if glyph_name is None:
            raise Exception("Glyph name not found in encoding for unicode " \
                    + unicode)
        metrics = self.afm[glyph_name]
        return ceil(font_size / self.UNITS_PER_EM * metrics[1])

    def text_unicode_to_code(self, text):
        """Convert a text in unicode strings into character code string"""
        string = ""
        for unicode in text:
            c = self.code(unicode)
            s = "\\" + "{0:o}".format(c)
            string += s
        return string
