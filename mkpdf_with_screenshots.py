"""Generate HOWTO.pdf including screenshots.
Usage: python mkpdf_with_screenshots.py --screenshots img1.png img2.png
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

IN = 'HOWTO.md'
OUT = 'HOWTO_with_screenshots.pdf'

try:
    md = open(IN, 'r', encoding='utf-8').read()
except Exception as e:
    print('Could not read HOWTO.md:', e)
    sys.exit(1)

# simple convert
lines = []
for raw in md.splitlines():
    s = raw.strip()
    if s.startswith('#'):
        s = s.lstrip('#').strip()
        lines.append(s.upper())
        lines.append('')
    else:
        lines.append(s)
text = '\n'.join(lines)

c = canvas.Canvas(OUT, pagesize=letter)
width, height = letter
margin = 0.7 * inch
y = height - margin
c.setFont('Helvetica-Bold', 14)
for para in text.split('\n\n'):
    c.setFont('Helvetica', 10)
    for line in para.split('\n'):
        if y < margin + 80:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line)
        y -= 14
    y -= 8

# insert screenshots passed as args
imgs = sys.argv[1:]
for img in imgs:
    try:
        im = Image.open(img)
        # scale to page width minus margins
        max_w = width - 2*margin
        max_h = height - 2*margin
        im_w, im_h = im.size
        ratio = min(max_w / im_w, max_h / im_h)
        w = im_w * ratio
        h = im_h * ratio
        if y - h < margin:
            c.showPage()
            y = height - margin
        # draw image centered
        x = (width - w) / 2
        c.drawImage(img, x, y - h, width=w, height=h)
        y -= h + 12
    except Exception as e:
        print('Could not insert image', img, e)

c.save()
print('Wrote', OUT)
