from ..primitives import GDictionary, GName, GNumber, GArray, GStream
from .type1.font import Type1
from .truetype.font import TrueType
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
            self.type = "Type1"
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
            self.font = TrueType(font_file)
            self.type = "TrueType"
            # TODO: Remove standard_font_name attribute, since it's useless here
            self.standard_font_name = font_file
            self.dict = GDictionary()
            self.dict.set(GName("Type"), GName("Font"))
            self.dict.set(GName("Subtype"), GName("TrueType"))
            self.dict.set(GName("BaseFont"), GName(self.font.get_base_font()))
            self.unicode_set = set()

            # Font descriptor dictionary
            font_descriptor_indirect = doc.new_indirect()
            self.font_descriptor = GDictionary()
            self.font_descriptor.set(GName("Type"), GName("FontDescriptor"))
            self.font_descriptor.set(GName("FontName"), GName(self.font.get_base_font()))
            # Bit 3 Symbolic, see 9.8.2
            self.font_descriptor.set(GName("Flags"), GNumber(4))
            # FontBBox
            self.font_descriptor.set(GName("FontBBox"), self.get_bbox())
            metrics = self.font.get_metrics()
            # ItalicAngle
            self.font_descriptor.set(GName("ItalicAngle"), GNumber(metrics["italicAngle"]))
            # NOTE: PDF standard does not specifiy these metrics in 1000 units.
            #       Check it later.
            # Ascent
            self.font_descriptor.set(GName("Ascent"), GNumber(metrics["ascender"]))
            # Descent
            self.font_descriptor.set(GName("Descent"), GNumber(metrics["descender"]))
            # CapHeight
            self.font_descriptor.set(GName("CapHeight"), GNumber(metrics["capHeight"]))
            # StemV
            self.font_descriptor.set(GName("StemV"), GNumber(self.font.get_stemv()))
            font_descriptor_indirect.set_object(self.font_descriptor)
            self.dict.set(GName("FontDescriptor"), font_descriptor_indirect.get_ref())
            # FontFile2
            font_program_indirect = doc.new_indirect()
            self.font_program = GStream()
            font_program_indirect.set_object(self.font_program)
            self.dict.set(GName("FontFile2"), font_program_indirect.get_ref())
        self.doc = doc
        self.tag = new_tag

    def code(self, unicode):
        """Return character code for the given unicode for font"""
        return self.font.code(unicode)

    def width(self, unicode, font_size):
        return self.font.width(unicode, font_size)

    def font_metrics(self, font_size):
        return self.font.font_metrics(font_size)

    def get_bbox(self):
        bbox = self.font.get_bbox()
        bbox_rect = GArray()
        for v in bbox:
            bbox_rect.append(GNumber(v))
        return bbox_rect

    def text_unicode_to_code(self, text):
        """Convert a text in unicode strings into character code string"""
        code_string = self.font.text_unicode_to_code(text)
        self.build_difference()
        return code_string

    def build_difference(self):
        encoding_dict = self.dict.get(GName("Encoding"))
        difference = self.font.build_difference()
        encoding_dict.set(GName("Differences"), difference)

    def add_to_unicode_set(self, unicode):
        if self.type == "TrueType":
            self.unicode_set.add(unicode)

    def update_unicode_set(self, text):
        for c in text:
            self.add_to_unicode_set(ord(c))

    def update(self):
        """Update font dictionary for TrueType fonts"""
        if self.type == "TrueType" and len(self.unicode_set) > 0:
            sorted_unicode_set = sorted(self.unicode_set)
            self.dict.set(GName("FirstChar"), GNumber(sorted_unicode_set[0]))
            self.dict.set(GName("LastChar"), GNumber(sorted_unicode_set[-1]))
            widths = self.get_widths()
            self.dict.set(GName("Widths"), widths)
            # Font descriptor dictionary
            

    def get_widths(self):
        if self.type == "TrueType" and len(self.unicode_set) > 0:
            widths = GArray()
            cmap = self.font.font.getBestCmap()
            glyph_set = self.font.font.getGlyphSet()
            units_per_em = self.font.font['head'].unitsPerEm
            sorted_unicode_set = sorted(self.unicode_set)
            first_char = sorted_unicode_set[0]
            last_char = sorted_unicode_set[-1]
            for unicode in range(first_char, last_char + 1):
                if unicode in self.unicode_set:
                    if unicode in cmap and cmap[unicode] in glyph_set:
                        width = glyph_set[cmap[unicode]].width
                        width = width * (1000.0 / units_per_em)
                        width = int(width)
                    else:
                        width = 0
                    widths.append(GNumber(width))
                else:
                    widths.append(GNumber(0))
            return widths
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
