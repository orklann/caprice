# Make it works to import parent pacakage
import sys
sys.path.insert(0,'..')
from caprice.document import Document
from caprice import font
import os

def save_pdf():
    doc = Document()
    page = doc.add_page()
    page.add_font(font.Times_Roman)
    page.add_sample_content()
    home = os.path.expanduser("~")
    filename = os.path.join(home, "sample.pdf")
    doc.save(filename)

save_pdf()
