"""Generate a simple single-page PDF from HOWTO.md without external dependencies.
This writes text using the built-in Helvetica font.
Usage: python generate_pdf_simple.py
Output: HOWTO.pdf
"""
import sys
from pathlib import Path

IN = Path('HOWTO.md')
OUT = Path('HOWTO.pdf')

if not IN.exists():
    print('Missing HOWTO.md')
    sys.exit(1)

text = IN.read_text(encoding='utf-8')
# very small markdown -> plain text
lines = []
for raw in text.splitlines():
    s = raw.strip()
    if s.startswith('#'):
        s = s.lstrip('#').strip()
        lines.append(s.upper())
        lines.append('')
    else:
        lines.append(s)

# wrap lines to ~80 chars
wrapped = []
for l in lines:
    if not l:
        wrapped.append('')
        continue
    while len(l) > 90:
        wrapped.append(l[:90])
        l = l[90:]
    wrapped.append(l)

# Build PDF objects
objs = []
# obj 1: Catalog
objs.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
# obj 2: Pages
objs.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
# Prepare content stream
content_lines = []
content_lines.append(b'BT')
content_lines.append(b'/F1 10 Tf')
# start at (72, 720) and move down
y = 740
for line in wrapped:
    # escape parentheses
    esc = line.replace('\\','\\\\').replace('(', '\\(').replace(')', '\\)')
    content_lines.append(f'72 {y} Td ({esc}) Tj'.encode('utf-8'))
    y -= 12
content_lines.append(b'ET')
content = b"\n".join(content_lines)
stream = b"<< /Length %d >>\nstream\n%s\nendstream\n" % (len(content), content)
# obj 5: Content
objs.append(b'5 0 obj\n' + stream + b'endobj\n')
# obj 4: Font
objs.append(b'4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')
# obj 3: Page referencing font and content
objs.append(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n')

# Now assemble PDF
pdf = b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'
offsets = []
for o in objs:
    offsets.append(len(pdf))
    pdf += o

# xref
xref_pos = len(pdf)
pdf += b'xref\n0 %d\n' % (len(objs) + 1)
pdf += b'0000000000 65535 f \n'
for off in offsets:
    pdf += b'%010d 00000 n \n' % off

pdf += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, xref_pos)

OUT.write_bytes(pdf)
print('Wrote', OUT)
