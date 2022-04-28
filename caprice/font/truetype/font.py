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
