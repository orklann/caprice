from ... import config
from ... import utils
from ..encoding import WinAnsiEncoding

from fontTools.afmLib import AFM

class Type1:
    """Type1 font class for 14 standard fonts"""

    def __init__(self, font_name):
        self.font_name = font_name
        self.afm = None
        self.load_afm()
        # We here use WinAnsiEncoding for all 14 standards fonts in PDF 
        self.encoding = WinAnsiEncoding()

    def load_afm(self):
        afm_file = utils.join_paths(config.data_dir, "caprice", "afm", \
                self.font_name + ".afm")
        self.afm = AFM(afm_file)

    def code(self, unicode):
        """Return character code for the given unicode for Type1 font"""
        return self.encoding.code_from_unicode(unicode)
