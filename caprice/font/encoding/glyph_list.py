from ... import config
from ... import utils

class GlyphList:
    """Mapping from glyph name to unicode, and unicode to glyph name for the
    Adobe Glyph List.

    More info at:
    * https://github.com/adobe-type-tools/agl-aglfn
    * https://github.com/adobe-type-tools/agl-specification
    """

    def __new__(cls):
        """Make this GlyphList singleton

        More info at: 
        https://www.python.org/download/releases/2.2/descrintro/#__new__
        """
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init()
        return it

    def init(self):
        self.standard_name_to_unicode = None
        self.standard_unicode_to_name = None
        self.zapf_name_to_unicode = None
        self.zapf_unicode_to_name = None
        self.load()
    
    @classmethod
    def name_to_unicode(cls, name, zapf=False):
        return GlyphList()._name_to_unicode(name, zapf=zapf)

    @classmethod
    def unicode_to_name(cls, unicode, zapf=False):
        return GlyphList()._unicode_to_name(unicode, zapf=zapf)

    def _name_to_unicode(self, name, zapf=False):
        """Maps the given glyph name to a string by using Adobe glyph list.
        Return None if we find no mapping.

        If we are looking mapping for ZapfDingbats font, the `zapf` should be
        set to True.
        """
        if zapf and name in self.zapf_name_to_unicode:
            return self.zapf_name_to_unicode[name]
        elif name in self.standard_name_to_unicode:
            return self.standard_name_to_unicode[name]
        else:
            return None

    def _unicode_to_name(self, unicode, zapf=False):
        """Maps the given unicode to a glyph name by using Adobe glyph list.
        Return .notdef if there is no such mapping.

        If we are looking mapping for ZapfDingbats font, the `zapf` should be
        set to True.
        """
        if zapf:
            return self.zapf_unicode_to_name.get(unicode, ".notdef")
        else:
            return self.standard_unicode_to_name.get(unicode, ".notdef")

    def load(self):
        """Load two kinds of Adobe glyph list files as mappings"""
        glyph_list_path = utils.join_paths(config.data_dir, "caprice", "encoding", "glyphlist.txt")
        zapf_glyph_list_path = utils.join_paths(config.data_dir, "caprice", "encoding", "zapfdingbats.txt")
        self.standard_name_to_unicode, self.standard_unicode_to_name = \
            self.load_file(glyph_list_path)
        self.zapf_name_to_unicode, self.zapf_unicode_to_name = \
            self.load_file(zapf_glyph_list_path)

    def load_file(self, file):
        """Load an Adobe glyph list form external file, and return two mappings.

        * Name to unicode mapping
          This maps a glyph name to one or more UTF-8 characters.

        * Unicode to name mapping
          This maps UTF-8 character to a glyph name, this mapping is not 
          one-to-one, it just returns the first glyph name which matches.
        """
        name_to_unicode = {}
        unicode_to_name = {}
        with open(file, "r") as f:
            line = f.readline()
            while line:
                if line[0] != '#':
                    split = line.split(";")
                    name, codes = split[0], split[1]
                    unicodes = ""
                    for code in codes.split(" "):
                        unicode = chr(int(code, 16))
                        unicodes += unicode
                    name_to_unicode[name] = unicodes
                    if unicodes not in unicode_to_name:
                        unicode_to_name[unicodes] = name
                line = f.readline()
        return (name_to_unicode, unicode_to_name)
