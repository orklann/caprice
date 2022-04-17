# Make it works to import parent pacakage
# To run: python examples/save_pdf_sample.py
import pathlib
import sys
import os

cwd = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(cwd))

from caprice.document import Document
from caprice import font

def save_pdf():
    doc = Document()
    page = doc.add_page()
    page.set_font_size(12)
    page.draw_text(0, 50, "Text without explictly using a font!")
    font1 = page.add_font(font.Times_Roman)
    page.use_font(font1)
    page.set_font_size(12)
    page.draw_text(0, 14, "Hello World!")
    page.draw_text(0, 0, "Hello, World again!", bottom_left=True)
    home = os.path.expanduser("~")
    filename = os.path.join(home, "sample.pdf")
    doc.save(filename)

save_pdf()
