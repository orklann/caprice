from ..primitives import GDictionary, GName
from .type1.font import Type1
from .latin_chars import LATIN_CHARS

# All 14 Type1 standard fonts
Times_Roman = "Times-Roman"
Helvetica = "Helvetica"
Courier = "Courier"
Symbol = "Symbol"
Times_Bold = "Times-Bold"
Helvetica_Bold = "Helvetica-Bold"
Courier_Bold = "Courier-Bold"
ZapfDingbats = "ZapfDingbats"
Times_Italic = "Times-Italic"
Helvetica_Oblique = "Helvetica-Oblique"
Courier_Oblique = "Courier-Oblique"
Times_BoldItalic = "Times-BoldItalic"
Helvetica_BoldOblique = "Helvetica-BoldOblique"
Courier_BoldOblique = "Courier-BoldOblique"

# All 14 Type1 standard fonts in a list
Standard_Fonts = [
    Times_Roman,
    Helvetica,
    Courier,
    Symbol,
    Times_Bold,
    Helvetica_Bold,
    Courier_Bold,
    ZapfDingbats,
    Times_Italic,
    Helvetica_Oblique,
    Courier_Oblique,
    Times_BoldItalic,
    Helvetica_BoldOblique,
    Courier_BoldOblique
]

class Font:
    def __init__(self, font_file, doc, new_tag):
        if font_file in Standard_Fonts:
            # Type 1 font
            self.font = Type1(font_file)
            self.standard_font_name = font_file
            self.dict = GDictionary()
            self.dict.set(GName("Type"), GName("Font"))
            self.dict.set(GName("Subtype"), GName("Type1"))
            self.dict.set(GName("BaseFont"), GName(self.standard_font_name))
            encoding_dict = GDictionary()
            encoding_dict.set(GName("Type"), GName("Encoding"))
            encoding_dict.set(GName("BaseEncoding"), GName(self.font.encoding.encoding_name))
            self.dict.set(GName("Encoding"), encoding_dict)
            self.indirect_obj = doc.new_indirect()
            self.indirect_obj.set_object(self.dict)
        else:
            self.standard_font_name = None
        self.doc = doc
        self.tag = new_tag


    def code(self, unicode):
        """Return character code for the given unicode for font"""
        return self.font.code(unicode)

    def width(self, unicode, font_size):
        return self.font.width(unicode, font_size)

    def font_metrics(self, font_size):
        return self.font.font_metrics(font_size)

    def text_unicode_to_code(self, text):
        """Convert a text in unicode strings into character code string"""
        code_string = self.font.text_unicode_to_code(text)
        self.build_difference()
        return code_string

    def build_difference(self):
        encoding_dict = self.dict.get(GName("Encoding"))
        difference = self.font.build_difference()
        encoding_dict.set(GName("Differences"), difference)

    def compile_str(self):
        """Only for tests, we use primitives's compile_str()"""
        self.build_difference()
        if self.standard_font_name is not None:
            return self.indirect_obj.compile_str()
        else:
            # TODO: Handle external fonts for compile_str()
            pass

    def compile_bytes(self):
        """Only for tests, we use primitives's compile_bytes()"""
        return str.encode(self.compile_str())            
