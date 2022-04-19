from .glyph_list import GlyphList

class Encoding:
    """Base class for all encoding classes"""
    
    def __init__(self):
        self.code_to_name = {}
        
