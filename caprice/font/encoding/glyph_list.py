import config

glyph_list = None

class GlyphList:
    """Mapping from glyph name to unicode, and unicode to glyph name for the
    Adobe Glyph List.

    More info at:
    * https://github.com/adobe-type-tools/agl-aglfn
    * https://github.com/adobe-type-tools/agl-specification
    """
    def __init__(self):
        pass

# Single instance of GlyphList
glyph_list = GlyphList()
