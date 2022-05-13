from math import ceil
import io
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter

class TrueType:
    """TrueType class is for TrueType and OpenType fonts"""
    
    def __init__(self, font_file):
        self.font = TTFont(font_file)

    def get_base_font(self):
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
        font_name = "".join([c for c in name if c.lower() in "abcdefghijklmnopqrstuvwxyz-"])
        return font_name

    def get_metrics(self):
        metrics = {
            'upm': self.font['head'].unitsPerEm,
            'xMin': self.font['head'].xMin,
            'xMax': self.font['head'].xMax,
            'yMin': self.font['head'].yMin,
            'yMax': self.font['head'].yMax,
            'capHeight': self.font['OS/2'].sCapHeight,
            'ascender': self.font['OS/2'].sTypoAscender,
            'descender': self.font['OS/2'].sTypoDescender,
            'italicAngle': self.font['post'].italicAngle,
            'usWeightClass': self.font['OS/2'].usWeightClass
        }
        return metrics

    def font_metrics(self, font_size):
        """Font metrics by applying font size"""
        metrics = self.get_metrics()
        UNITS_PER_EM = metrics["upm"]
        scale = font_size / UNITS_PER_EM 
        metrics["capHeight"] = ceil(metrics["capHeight"] * scale)
        metrics["ascender"] = ceil(metrics["ascender"] * scale)
        metrics["descender"] = ceil(metrics["descender"] * scale)
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
