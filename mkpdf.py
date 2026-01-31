"""Simple markdown->PDF renderer using reportlab.
Run: python mkpdf.py
Produces: HOWTO.pdf
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import textwrap

IN = 'HOWTO.md'
OUT = 'HOWTO.pdf'

def md_to_text(md):
    # Very small markdown -> plaintext converter
    lines = []
    for raw in md.splitlines():
        s = raw.strip()
        if s.startswith('#'):
            # headings
            s = s.lstrip('#').strip()
            lines.append(s.upper())
            lines.append('')
        else:
            lines.append(s)
    return '\n'.join(lines)


def render(text, outpath):
    c = canvas.Canvas(outpath, pagesize=letter)
    width, height = letter
    margin = 0.75 * inch
    max_width = width - 2 * margin
    y = height - margin
    wrapper = textwrap.TextWrapper(width=90)
    for paragraph in text.split('\n\n'):
        lines = wrapper.wrap(paragraph)
        for line in lines:
            if y < margin + 12:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line)
            y -= 14
        y -= 8
    c.save()


if __name__ == '__main__':
    import sys
    try:
        with open(IN, 'r', encoding='utf-8') as f:
            md = f.read()
    except Exception as e:
        print('Could not read HOWTO.md:', e)
        sys.exit(1)
    text = md_to_text(md)
    render(text, OUT)
    print('Wrote', OUT)
