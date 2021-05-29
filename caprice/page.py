# -*- coding=utf-8 -*-
"""Page presents a page in PDF.
"""

class Page:
    def __init__(self, doc) -> None:
        # Document for this page
        self.doc = doc