# To run: python examples/truetype_font.py
import pathlib
import sys
import os

# Make it works to import parent pacakage
cwd = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(cwd))

from caprice.document import Document
from caprice import font

def save_pdf():
    doc = Document()
    page = doc.add_page()
    font1 = page.add_font("examples/data/fonts/ZCOOLXiaoWei-Regular.ttf")
    page.use_font(font1)
    page.set_font_size(48)
    page.draw_text(0, 0, "他们所有!")
    home = os.path.expanduser("~")
    filename = os.path.join(home, "chinese_font.pdf")
    doc.save(filename)

save_pdf()
