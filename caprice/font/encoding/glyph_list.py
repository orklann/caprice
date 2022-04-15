import config

class GlyphList:
    """Mapping from glyph name to unicode, and unicode to glyph name for the
    Adobe Glyph List.

    More info at:
    * https://github.com/adobe-type-tools/agl-aglfn
    * https://github.com/adobe-type-tools/agl-specification
    """
    def __new__(cls):
        """Make this GlyphList singleton"""
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init()
        return it

    def init(self):
        pass

