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
    font1 = page.add_font(font.Times_Roman)
    page.use_font(font1)
    page.draw_text(0, 14, "Hello World!")
    page.draw_text(0, 0, "Hello, World again!", bottom_left=True)
    page.use_font(None)
    page.draw_text(0, 50, "Text without explict font")
    home = os.path.expanduser("~")
    filename = os.path.join(home, "sample.pdf")
    doc.save(filename)

save_pdf()
