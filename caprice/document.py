# -*- coding=utf-8 -*-
"""Document presents a PDF file
"""

from .page import Page

class Document:
    def __init__(self) -> None:
        self.pages = []
        
    def add_page(self):
        p = Page(self)
        self.pages.append(p)
        return p