from math import ceil
import io
import random
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter

class TrueType:
    """TrueType class is for TrueType and OpenType fonts"""
    subset_tags = []

    @classmethod
    def generate_subset_tag(cls):
        LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        tag = ""
        for i in range(0, 6):
            l = LETTERS[random.randint(0, len(LETTERS) - 1)]
            tag += l
        while tag in cls.subset_tags:
            tag = cls.generate_subset_tag()
        cls.subset_tags.append(tag)
        return tag

    def __init__(self, font_file):
        with open(font_file, "rb") as ffh:
            self.font_file_bytes = ffh.read()
        self.font = TTFont(font_file)
        self.font_name = None

    def get_base_font(self):
        if self.font_name is not None:
            return self.font_name
        name = ""
        for record in self.font['name'].names:
            if b'\x00' in record.string:
                name_str = record.string.decode('utf-16-be')
            else:   
                name_str = record.string.decode('utf-8')
            if record.platformID == 3 and record.platEncID == 1 and record.nameID == 6:
                name = name_str
            if name: 
                break
        self.font_name = "".join([c for c in name if c.lower() in "abcdefghijklmnopqrstuvwxyz-"])
        # Subset font name
        tag = TrueType.generate_subset_tag()
        self.font_name = tag + "+" + self.font_name
        return self.font_name

    def get_metrics(self):
        """Font metrics in 1000 units per em for font descriptor"""
        UNITS_PER_EM = self.font['head'].unitsPerEm
        scale = 1000.0 / UNITS_PER_EM 
        metrics = {
            'upm': UNITS_PER_EM,
            'xMin': self.font['head'].xMin,
            'xMax': self.font['head'].xMax,
            'yMin': self.font['head'].yMin,
            'yMax': self.font['head'].yMax,
            'capHeight': self.font['OS/2'].sCapHeight * scale,
            'ascender': self.font['OS/2'].sTypoAscender * scale,
            'descender': self.font['OS/2'].sTypoDescender * scale,
            'italicAngle': self.font['post'].italicAngle,
            'usWeightClass': self.font['OS/2'].usWeightClass
        }
        return metrics

    def font_metrics(self, font_size):
        """Font metrics by applying font size"""
        metrics = self.get_metrics()
        UNITS_PER_EM = self.font['head'].unitsPerEm
        scale = font_size / UNITS_PER_EM 
        metrics = {}
        metrics["capHeight"] = ceil(self.font['OS/2'].sCapHeight * scale)
        metrics["ascender"] = ceil(self.font['OS/2'].sTypoAscender * scale)
        metrics["descender"] = ceil(self.font['OS/2'].sTypoDescender * scale)
        return metrics

    def get_bbox(self):
        metrics = self.get_metrics()
        return [metrics['xMin'], metrics['yMin'], metrics['xMax'], metrics['yMax']]

    def get_stemv(self):
        """See: https://stackoverflow.com/questions/35485179/stemv-value-of-the-truetype-font
                https://fossies.org/dox/PDFlib-Lite-7.0.5p3/ft__font_8c_source.html
        """
        weight = self.get_metrics()["usWeightClass"]
        FNT_STEMV_WEIGHT = 65.0
        FNT_STEMV_MIN = 50
        w = weight / FNT_STEMV_WEIGHT
        return int(FNT_STEMV_MIN + w * w + 0.5)

    def get_subset(self, unicodes=()):
        text = ""
        for code in unicodes:
            text += (chr(code))
        subsetter = Subsetter()
        subsetter.populate(text=text)
        subsetter.subset(self.font)
        with io.BytesIO() as buffer:
            self.font.save(buffer)
            return buffer.getvalue()

    def text_unicode_to_code(self, text):
        """Convert a text in unicode strings into character code string"""
        string = ""
        for char in text:
            c = ord(char)
            s = " (\\" + "{0:o}".format(c) + ")"
            string += s
        string += " "
        return string
