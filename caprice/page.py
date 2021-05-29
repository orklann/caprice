# -*- coding=utf-8 -*-
"""Page presents a page in PDF.
"""

from .primitives import GDictionary, GName, GArray
from .utils import rect_primitive

class Page:
    def __init__(self, doc) -> None:
        # Document for this page
        self.doc = doc
        self.dict = GDictionary()
        self.__init_dict()
    
    def __init_dict(self):
        # /Type: /Page
        self.dict.set(GName("Type"), GName("Page"))
        # TODO: /Parent: Pages object
        # TODO: /Resources:
        # /MediaBox: Hardcoded at the moment
        self.dict.set(GName("MediaBox"), rect_primitive([0, 0, 600, 800]))
        # /CropBox: Hardcoded at the moment
        self.dict.set(GName("CropBox"), rect_primitive([0, 0, 600, 800]))
        # TODO: /Content:

    def compile_str(self):
        return self.dict.compile_str()

    def compile_bytes(self):
        return self.dict.compile_bytes()
