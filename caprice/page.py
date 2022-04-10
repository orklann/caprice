from .primitives import GDictionary, GName, GArray, GIndirect, GStream
from .utils import rect_primitive

class Page:
    """Page presents a page in PDF.
    """

    def __init__(self, doc):
        # Document for this page
        self.doc = doc
        self.rect = [0, 0, 300, 144]
        self.content = ""
        self.dict = GDictionary()
        self.__init_dict()
        self.indirect_obj = doc.new_indirect()
        self.indirect_obj.set_object(self.dict)
    
    def set_size(self, w, h):
        self.rect[2] = w
        self.rect[3] = h

    def __init_dict(self):
        # /Type: /Page
        self.dict.set(GName("Type"), GName("Page"))
        # /Parent: Root Pages object ref
        root_page_ref = self.doc.catalog.object.get(GName("Pages"))
        self.dict.set(GName("Parent"), root_page_ref)
        # /Resources:
        resources = GDictionary()
        resources.set(GName("Font"), GDictionary())
        self.dict.set(GName("Resources"), resources)
        # /MediaBox: Hardcoded at the moment
        self.dict.set(GName("MediaBox"), rect_primitive(self.rect))
        # /CropBox: Hardcoded at the moment
        self.dict.set(GName("CropBox"), rect_primitive(self.rect))

    def set_content(self, content_obj):
        """Set value of /Contents in page dictionary.
        content_obj is an indirect object, it's an instance of GIndirect class.
        The content of content_obj is an stream object.
        """
        self.dict.set(GName("Contents"), content_obj.get_ref())

    def update_content(self):
        content_obj = self.doc.new_indirect()
        content_stream = GStream()
        content = self.content
        content_stream.set_content(content)
        content_obj.object = content_stream
        self.set_content(content_obj)

    def add_font(self, font_file):
        font = self.doc.add_font(font_file)
        resources = self.dict.get(GName("Resources"))
        font_dict = resources.get(GName("Font"))
        font_dict.set(GName(font.tag), font.indirect_obj.get_ref())
        return font

    def draw_text(self, x, y, text, bottom_left=False):
        if not bottom_left:
            height = self.rect[3]
            flipped_y = height - y
            y = flipped_y
        text_operators = "BT\n/F1 18 Tf\n%d %d Td\n(%s) Tj\nET\n" % (x, y, text)
        self.content += text_operators

    def compile_str(self):
        self.__init_dict()
        return self.indirect_obj.compile_str()

    def compile_bytes(self):
        return self.indirect_obj.compile_bytes()
