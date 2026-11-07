from shapely.geometry import Polygon, box
from shapely.ops import unary_union
import build
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

S = 190  # stem weight
def tri(*p): return Polygon(p)
SOLID = {
 'R': unary_union([box(0,0,S,700), box(0,300,600,700).difference(box(S,440,410,570)),
                   Polygon([(230,300),(440,300),(600,0),(390,0)])]),
 'E': box(0,0,600,700).difference(box(S,150,600,275)).difference(box(S,425,600,550)).difference(box(480,150,600,550)),
 'X': box(0,0,600,700).difference(unary_union([tri((170,700),(430,700),(300,470)), tri((170,0),(430,0),(300,230)),
                                               tri((0,130),(0,570),(200,350)), tri((600,130),(600,570),(400,350))])),
 'A': Polygon([(0,0),(150,700),(450,700),(600,0)]).difference(tri((300,560),(240,320),(360,320))).difference(
        Polygon([(230,0),(370,0),(350,190),(250,190)])),
 # lowercase forms at full cap height (700)
 'r': unary_union([box(0,0,S,700), Polygon([(0,460),(450,460),(450,610),(360,700),(0,700)])]),
 'e': box(0,0,560,700).difference(box(S,420,370,530)).difference(box(S,175,560,295)),
 'x': box(0,0,540,700).difference(unary_union([tri((160,700),(380,700),(270,465)), tri((160,0),(380,0),(270,235)),
                                               tri((0,130),(0,570),(185,350)), tri((540,130),(540,570),(355,350))])),
 'a': box(0,0,560,700).difference(box(S,175,370,295)).difference(box(0,420,370,530)),
}
def outline(g, t):
    return g.buffer(t/2, join_style=2).difference(g.buffer(-t/2, join_style=2))

def make(name, mode, t=34, gap=26):
    fb = FontBuilder(1000, isTTF=True)
    order = ['.notdef','space'] + list(SOLID)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c): c for c in SOLID} | {32: 'space'})
    glyphs = {'.notdef': TTGlyphPen(None).glyph(), 'space': TTGlyphPen(None).glyph()}
    mets = {'.notdef': (500,0), 'space': (260,0)}
    for c, g in SOLID.items():
        shp = outline(g, t) if mode == 'Outline' else g
        minx, _, maxx, _ = g.bounds
        sb = gap + (t/2 if mode == 'Outline' else 0)
        glyphs[c] = build.to_ttglyph(shp, sb - minx)
        mets[c] = (round(maxx - minx + 2*sb), round(sb - (t/2 if mode=='Outline' else 0)))
    fam = f"Rexxar Block {mode}"
    fb.setupGlyf(glyphs); fb.setupHorizontalMetrics(mets); fb.setupHorizontalHeader(ascent=900, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'psName': fam.replace(' ','')+'-Regular',
                       'copyright': '© 2026 Chia-Hung Lin'})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-250, usWinAscent=900, usWinDescent=260, sxHeight=700, sCapHeight=700)
    fb.setupPost(); fb.setupHead(unitsPerEm=1000)
    fb.save(f"out/RexxarBlock{mode}.ttf"); fb.font.flavor='woff2'; fb.font.save(f"out/RexxarBlock{mode}.woff2")
for m in ('Outline','Solid'): make('', m)
