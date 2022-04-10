# Make it works to import parent pacakage
# To run: python save_pdf_sample.py
import sys
sys.path.insert(0,'..')
from caprice.document import Document
from caprice import font
import os

def save_pdf():
    doc = Document()
    page = doc.add_page()
    page.add_font(font.Times_Roman)
    page.draw_text(0, 0, "Hello World!")
    home = os.path.expanduser("~")
    filename = os.path.join(home, "sample.pdf")
    doc.save(filename)

save_pdf()
