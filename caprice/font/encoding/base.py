from .glyph_list import GlyphList

class Encoding:
    """Base class for all encoding classes"""
    
    def __init__(self):
        self.code_to_name = {}
        self.encoding_name = None

    def name(self, code):
        """Return the glyph name for the given character code, if not found,
        just return .notdef
        """
        # TODO: Add unit test for this method
        self.code_to_name.get(code, ".notdef")

    def unicode(self, code):
        """Return the Unicode value in UTF-8 for the given code, return None 
        if not found.
        """
        # TODO: Add unit test for this method
        return GlyphList.name_to_unicode(self.name(code))

    def code(self, name):
        """Return the character code for the given glyph name, return None if 
        not found.

        Note: If multiple character codes maps to the same given glyph name, the
        first found is returned.
        """
        # TODO: Add unit test for this method
        for c in self.code_to_name:
            if self.code_to_name[c] == name:
                return c
            return None
