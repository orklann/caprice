# -*- coding=utf-8 -*-
"""Document presents a PDF file
"""

from .primitives import GIndirect
from .page import Page

class Document:
    indirect_obj_num_count = 1 # Increase this value after add new GIndirect

    def __init__(self) -> None:
        self.pages = []
        self.indirects_dict = {}
        
    def add_page(self):
        p = Page(self)
        self.pages.append(p)
        return p

    def add_indirect(self, indirect: GIndirect):
        """Add GIndirect to Document, by using increasing object number
        """
        # Set the tracking object number
        indirect.set_obj_num(self.indirect_obj_num_count)
        indirect.set_generation_num(0)
        # Increse tracking object number
        self.indirect_obj_num_count += 1
        key = indirect.get_ref().compile_str()
        self.indirects_dict[key] = indirect