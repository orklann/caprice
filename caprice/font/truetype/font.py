from fontTools.ttLib import TTFont

class TrueType:
    """TrueType class is for TrueType and OpenType fonts"""
    
    def __init__(self, font_file):
        self.font = TTFont(font_file)
