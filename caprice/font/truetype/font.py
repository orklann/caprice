from fontTools.ttLib import TTFont

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


