# -*- coding=utf-8 -*-

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
    def __init__(self, font_file, doc, new_tag) -> None:
        if (font_file in Standard_Fonts):
            self.standard_font_name = font_file
        else:
            self.standard_font_name = None
        self.doc = doc
        self.tag = new_tag
