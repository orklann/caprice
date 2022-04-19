from ... import config
from ... import utils
from fontTools.afmLib import AFM

class Type1:
    """Type1 font class for 14 standard fonts"""

    def __init__(self, font_name):
        self.font_name = font_name
        self.afm = None
        self.load_afm()

    def load_afm(self):
        afm_file = utils.join_paths(config.data_dir, "caprice", "afm", \
                self.font_name + ".afm")
        self.afm = AFM(afm_file)
        
        

