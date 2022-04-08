from .primitives import GIndirect, GDictionary, GName, GRef, GArray, GNumber
from .page import Page
from .font import Font
from .utils import padding_10_xref

PDF_HEADER = "%PDF-1.5\n%Produced by Caprice"
LINE_FEED = "\n"
CARRIAGE_RETURN = "\r"
END_OF_LINE = "\r\n"

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
        return f
    
    def save(self, filename):
        buffer = self.build_pdf()
        with open(filename, "wb") as file:
            file.write(buffer)

    def build_pdf(self):
        data = bytearray()
        offset = 0
        # PDF HEADER
        header = (PDF_HEADER + LINE_FEED + LINE_FEED).encode()
        data.extend(header)
        # Indirect objects
        offset = len(data)
        objects_data = self.build_objects(offset)
        data.extend(objects_data)
        # xref table
        offset = len(data)
        start_xref_offset = offset
        xref_data = self.build_xref()
        data.extend(xref_data)
        # trailer dictionary
        trailer_data = self.build_trailer()
        data.extend(trailer_data)
        # startxref
        start_xref_data = self.build_start_xref(start_xref_offset)
        data.extend(start_xref_data)
        # %%EOF
        data.extend(b'%%EOF')
        return data

    def build_objects(self, offset):
        objects_data = bytearray()
        for key in sorted(self.indirects_dict):
            indirect = self.indirects_dict[key]
            indirect.offset = offset
            object_data = indirect.compile_bytes()
            objects_data.extend(object_data)
            offset += len(object_data)

            # Add two line feeds
            two_line_feeds = (LINE_FEED + LINE_FEED).encode()
            objects_data.extend(two_line_feeds)
            offset += len(two_line_feeds)
        return objects_data

    def build_xref(self):
        xref_data = bytearray()
        # xref keyword
        xref_data.extend(b'xref\n')
        # First section header
        objects_count = len(self.indirects_dict)
        header = "0 %d\n" % objects_count
        xref_data.extend(header.encode())
        # Object 0
        line = "0000000000 65535 f %s" % END_OF_LINE
        xref_data.extend(line.encode())
        # Other objects
        for key in sorted(self.indirects_dict):
            indirect = self.indirects_dict[key]
            offset = indirect.offset
            padding_offset = padding_10_xref(offset)
            line = "%s 00000 n %s" % (padding_offset, END_OF_LINE)
            xref_data.extend(line.encode())
        return xref_data

    def build_trailer(self):
        trailer_data = bytearray()
        # trailer keyword
        trailer_data.extend(b'trailer\n')
        # The start of dictionary
        trailer_data.extend(b'    <<')
        # /Root 
        trailer_data.extend(b'/Root 1 0 R\n')
        # /Size
        objects_count = len(self.indirects_dict)
        size_line = "/Size %d\n" % objects_count
        trailer_data.extend(size_line.encode())
        # The end of dictionary
        trailer_data.extend(b'    >>\n')
        return trailer_data

    def build_start_xref(self, start_xref_offset):
        start_xref_data = bytearray()
        # startxref keyword
        start_xref_data.extend(b'startxref\n')
        # startxref offset
        start_xref_data.extend(str(start_xref_offset).encode())
        # line feed
        start_xref_data.extend(LINE_FEED.encode())
        return start_xref_data
