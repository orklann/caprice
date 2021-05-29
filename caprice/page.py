# -*- coding=utf-8 -*-
"""Page presents a page in PDF.
"""

from .primitives import GDictionary, GName, GArray
from .utils import rect_primitive

class Page:
    def __init__(self, doc) -> None:
        # Document for this page
        self.doc = doc
        self.rect = [0, 0, 600, 800]
        self.dict = GDictionary()
        self.__init_dict()
    
    def set_size(w, h):
        self.rect[2] = w
        self.rect[3] = h

    def __init_dict(self):
        # /Type: /Page
        self.dict.set(GName("Type"), GName("Page"))
        # TODO: /Parent: Pages object
        # TODO: /Resources:
        # /MediaBox: Hardcoded at the moment
        self.dict.set(GName("MediaBox"), rect_primitive(self.rect))
        # /CropBox: Hardcoded at the moment
        self.dict.set(GName("CropBox"), rect_primitive(self.rect))
        # TODO: /Content:

    def compile_str(self):
        return self.dict.compile_str()

    def compile_bytes(self):
        return self.dict.compile_bytes()
