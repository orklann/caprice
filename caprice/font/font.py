from primitives import GDictionary, GName

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
        if (font_file in Standard_Fonts):
            self.standard_font_name = font_file
            self.dict = GDictionary()
            self.dict.set(GName("Type"), GName("Font"))
            self.dict.set(GName("Subtype"), GName("Type1"))
            self.dict.set(GName("BaseFont"), GName(self.standard_font_name))
            self.indirect_obj = doc.new_indirect()
            self.indirect_obj.set_object(self.dict)
        else:
            self.standard_font_name = None
        self.doc = doc
        self.tag = new_tag

    def compile_str(self):
        if self.standard_font_name is not None:
            return self.indirect_obj.compile_str()
        else:
            # TODO: Handle external fonts for compile_str()
            pass

    def compile_bytes(self):
        return str.encode(self.compile_str())            
