# To run: python examples/14_standard_fonts.py
import pathlib
import sys
import os

# Make it works to import parent pacakage
cwd = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(cwd))

from caprice.document import Document
from caprice import font
from caprice.font.encoding.win_ansi_encoding import WinAnsiEncoding


CHARS = None
CHARS_PER_LINE = 40
x, y = 60, 30

def generate_text():
    win = WinAnsiEncoding()
    text = ""
    for code in win.code_to_name:
        unicode = win.unicode(code)
        text += unicode
    return "".join(sorted(text))


def save_pdf():
    global CHARS 
    CHARS = generate_text()
    doc = Document()
    page = doc.add_page()
    page.set_size(600, 1080)
    draw_text(page, font.Times_Roman)
    draw_text(page, font.Helvetica)
    draw_text(page, font.Courier)
    home = os.path.expanduser("~")
    filename = os.path.join(home, "standard_fonts.pdf")
    doc.save(filename)

def draw_text(page, font_name):
    global x
    global y
    font = page.add_font(font_name)
    page.use_font(font)
    page.set_font_size(14)
    # Draw font name
    page.draw_text(x, y, font_name)
    y += 16
    
    # Draw characters
    page.set_font_size(12)
    consumed = 0
    start = 0
    l = CHARS_PER_LINE
    while consumed < len(CHARS):
        text = CHARS[start:start+CHARS_PER_LINE]
        l = len(text)
        ix = x
        for c in text:
            page.draw_text(ix, y, c)
            ix += 12
        y += 14
        start += l
        consumed += l
    y += 20

save_pdf()
