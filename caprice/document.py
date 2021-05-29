# -*- coding=utf-8 -*-

from .primitives import GIndirect
from .page import Page

class Document:
    """Document presents a PDF file
    """
    # Increase this value after adding new GIndirect
    indirect_obj_num_count = 1

    def __init__(self) -> None:
        self.pages = []
        self.indirects_dict = {}
        
    def add_page(self):
        p = Page(self)
        self.pages.append(p)
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