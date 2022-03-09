from .primitives import GIndirect, GDictionary, GName, GRef, GArray, GNumber
from .page import Page
from .font import Font

class Document:
    """Document presents a PDF file
    """
    # Increase this value after adding new GIndirect
    indirect_obj_num_count = 1
    font_reference_count = 1

    def __init__(self):
        self.pages = []
        self.indirects_dict = {}
        self.fonts_dict = {}
        self.create_catalog()
        self.create_root_pages()

    def create_catalog(self):
        self.catalog = self.new_indirect()
        dict = GDictionary()
        dict.set(GName("Type"), GName("Catalog"))
        rootPagesRef = GRef()
        rootPagesRef.obj_num = 2
        rootPagesRef.generation_num = 0
        dict.set(GName("Pages"), rootPagesRef)
        self.catalog.set_object(dict)

    def create_root_pages(self):
        self.root_pages = self.new_indirect()
        dict = GDictionary()
        dict.set(GName("Type"), GName("Pages"))
        dict.set(GName("Kids"), GArray())
        self.root_pages.set_object(dict)
        
    def add_page(self):
        p = Page(self)
        self.pages.append(p)
        page_ref = p.indirect_obj.get_ref()
        kids = self.root_pages.object.get(GName("Kids"))
        kids.append(page_ref)
        count = len(kids.array)
        self.root_pages.object.set(GName("Count"), GNumber(count))
        return p

    def new_indirect(self):
        """Creaat GIndirect and add it to Document, 
        by using increasing object number
        """
        indirect = GIndirect()
        # Set the tracking object number
        indirect.set_obj_num(self.indirect_obj_num_count)
        indirect.set_generation_num(0)
        # Increse tracking object number
        self.indirect_obj_num_count += 1
        key = indirect.get_ref_str()
        self.indirects_dict[key] = indirect
        return indirect

    def new_font_tag(self):
        tag = "F%d" % self.font_reference_count
        self.font_reference_count += 1
        return tag

    def add_font(self, font_file):
        new_tag = self.new_font_tag()
        f = Font(font_file, self, new_tag)
        self.fonts_dict[new_tag] = f
