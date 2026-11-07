"""Build three monoline display fonts for rexxar.dev from centerline skeletons."""
import math, random
from shapely.geometry import LineString, Point, Polygon, MultiPolygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

T, B, M, XT = 655, 45, 355, 455

def P(pts, closed=False):
    return (pts, closed)

GLYPHS = {
    'R': [P([(0,0),(0,700)]), P([(0,T),(410,T,160),(410,M,160),(0,M)]), P([(230,M),(450,0)])],
    'E': [P([(420,T),(0,T),(0,B),(420,B)]), P([(0,M),(360,M)])],
    'X': [P([(0,0),(460,700)]), P([(0,700),(460,0)])],
    'A': [P([(0,0),(195,T,40),(285,T,40),(480,0)]), P([(60,220),(420,220)])],
    'C': [P([(440,T),(0,T,230),(0,B,230),(440,B)])],
    'G': [P([(440,T),(0,T,230),(0,B,230),(440,B,60),(440,310),(260,310)])],
    'H': [P([(0,0),(0,700)]), P([(440,0),(440,700)]), P([(0,M),(440,M)])],
    'I': [P([(0,0),(0,700)])],
    'U': [P([(0,700),(0,B,220),(440,B,220),(440,700)])],
    'N': [P([(0,0),(0,T),(440,B),(440,700)])],
    'L': [P([(0,700),(0,B),(400,B)])],
    'hyphen': [P([(0,290),(220,290)])],
    'e': [P([(0,250),(400,250),(400,XT,190),(0,XT,190),(0,B,190),(390,B)])],
    'x': [P([(0,0),(380,500)]), P([(0,500),(380,0)])],
    'a': [P([(20,XT),(360,XT,170),(360,0)]), P([(360,270),(0,270,110),(0,B,110),(360,B)])],
    'r': [P([(0,0),(0,500)]), P([(0,240),(0,XT,190),(250,XT)])],
    'h': [P([(0,0),(0,700)]), P([(0,250),(0,XT,180),(370,XT,180),(370,0)])],
    'n': [P([(0,0),(0,500)]), P([(0,250),(0,XT,180),(370,XT,180),(370,0)])],
    'u': [P([(370,500),(370,0)]), P([(370,250),(370,B,180),(0,B,180),(0,500)])],
    'i': [P([(0,0),(0,500)]), P([(0,600),(0,700)])],
    'g': [P([(370,500),(370,-155,180),(10,-155)]), P([(370,B),(0,B,170),(0,XT,170),(370,XT)])],
}
CHARS = {g: (ord(g) if len(g) == 1 else 0x2D) for g in GLYPHS}

def unit(v):
    l = math.hypot(*v); return (v[0]/l, v[1]/l), l

def expand(pts, closed, style):
    n = len(pts)
    xy = [(p[0], p[1]) for p in pts]
    rad = [style['rmap'](p[2]) if len(p) > 2 else 0 for p in pts]
    is_corner = [closed or 0 < i < n-1 for i in range(n)]
    out = []
    for i in range(n):
        if not is_corner[i] or rad[i] <= 0:
            out.append(xy[i]); continue
        A, Bv, C = xy[i-1], xy[i], xy[(i+1) % n]
        (u1, l1), (u2, l2) = unit((A[0]-Bv[0], A[1]-Bv[1])), unit((C[0]-Bv[0], C[1]-Bv[1]))
        th = math.acos(max(-1, min(1, u1[0]*u2[0]+u1[1]*u2[1])))
        t = rad[i] / math.tan(th/2)
        def lim(L, j):
            return L/2 if (is_corner[j % n] and rad[j % n] > 0) else L*0.999
        t = min(t, lim(l1, i-1), lim(l2, i+1))
        r = t * math.tan(th/2)
        P1 = (Bv[0]+u1[0]*t, Bv[1]+u1[1]*t); P2 = (Bv[0]+u2[0]*t, Bv[1]+u2[1]*t)
        if style['corner'] == 'chamfer':
            out += [P1, P2]; continue
        bis, _ = unit((u1[0]+u2[0], u1[1]+u2[1]))
        d = r / math.sin(th/2)
        c = (Bv[0]+bis[0]*d, Bv[1]+bis[1]*d)
        a1 = math.atan2(P1[1]-c[1], P1[0]-c[0]); a2 = math.atan2(P2[1]-c[1], P2[0]-c[0])
        sw = (a2 - a1 + math.pi) % (2*math.pi) - math.pi
        k = max(3, int(abs(sw) * r / 12))
        out += [(c[0]+r*math.cos(a1+sw*j/k), c[1]+r*math.sin(a1+sw*j/k)) for j in range(k+1)]
    return out

def end_dirs(line):
    (d0, _), (d1, _) = unit((line[0][0]-line[1][0], line[0][1]-line[1][1])), unit((line[-1][0]-line[-2][0], line[-1][1]-line[-2][1]))
    return d0, d1

def stroke_flat(line, w):
    """Square-ended stroke: ends cut horizontally (or vertically if the end runs horizontal)."""
    d0, d1 = end_dirs(line)
    ext = [(line[0][0]+d0[0]*w, line[0][1]+d0[1]*w)] + line[1:-1] + [(line[-1][0]+d1[0]*w, line[-1][1]+d1[1]*w)] if len(line) > 2 else \
          [(line[0][0]+d0[0]*w, line[0][1]+d0[1]*w), (line[-1][0]+d1[0]*w, line[-1][1]+d1[1]*w)]
    if len(line) > 2:
        ext = [ext[0]] + line[1:-1] + [ext[-1]]
    g = LineString(ext).buffer(w/2, cap_style=2, join_style=2, mitre_limit=2.0)
    for (ex, ey), d in ((line[0], d0), (line[-1], d1)):
        R, h = 2*w, w/2 + 1
        if abs(d[1]) > 0.05:
            cut = box(ex-R, ey, ex+R, ey+R) if d[1] > 0 else box(ex-R, ey-R, ex+R, ey)
        else:
            cut = box(ex, ey-h, ex+w+1, ey+h) if d[0] > 0 else box(ex-w-1, ey-h, ex, ey+h)
        g = g.difference(cut)
    return g

def inset_ends(line, by):
    d0, d1 = end_dirs(line)
    line = list(line)
    line[0] = (line[0][0]-d0[0]*by, line[0][1]-d0[1]*by)
    line[-1] = (line[-1][0]-d1[0]*by, line[-1][1]-d1[1]*by)
    return line

def densify(line, closed, step=7):
    pts = line + ([line[0]] if closed else [])
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0]-a[0], b[1]-a[1]); k = max(1, int(L/step))
        out += [(a[0]+(b[0]-a[0])*j/k, a[1]+(b[1]-a[1])*j/k) for j in range(1, k+1)]
    return out

def stroke_brush(line, closed, w, rng):
    p = [rng.uniform(0, 6.28) for _ in range(6)]
    pts = densify(line if closed else inset_ends(line, w*0.4), closed)
    warped = []
    for x, y in pts:
        dx = 9*math.sin(x*0.011+p[0]) + 6*math.sin(y*0.019+p[1])
        dy = 7*math.sin(x*0.016+p[2]) + 5*math.sin(y*0.013+p[3])
        warped.append((x+dx+0.21*y, y+dy))
    s = [0.0]
    for a, b in zip(warped, warped[1:]): s.append(s[-1]+math.hypot(b[0]-a[0], b[1]-a[1]))
    tot = s[-1]
    radii = []
    for si in s:
        r = w/2 * (0.82 + 0.22*math.sin(si*0.011+p[4]))
        if not closed:
            r *= min(1.0, 0.5 + 0.5*min(si, tot-si)/110)
        radii.append(r)
    parts = [Point(warped[0]).buffer(radii[0], 16)]
    for (a, ra), (b, rb) in zip(zip(warped, radii), zip(warped[1:], radii[1:])):
        parts.append(unary_union([Point(a).buffer(ra, 16), Point(b).buffer(rb, 16)]).convex_hull)
    return unary_union(parts)

STYLES = {
    'Tech':  dict(w=88, corner='chamfer', rmap=lambda r: min(r*0.55, 105), sb=62, term='flat'),
    'Round': dict(w=88, corner='arc', rmap=lambda r: r, sb=60, term='round'),
    'Scribe':  dict(w=46, corner='arc', rmap=lambda r: r, sb=58, term='round', sx=0.84, slant=0.0),
    'ScribeSlant': dict(w=46, corner='arc', rmap=lambda r: r, sb=50, term='round', sx=0.84, slant=0.27),
    'Hand':  dict(w=74, corner='arc', rmap=lambda r: r*0.9, sb=34, term='brush'),
}

def build_glyph(name, style, rng):
    w = style['w']; shapes = []
    for pts, closed in GLYPHS[name]:
        line = expand(pts, closed, style)
        if 'sx' in style:
            line = [(x*style['sx'] + y*style['slant'], y) for x, y in line]
        if style['term'] == 'flat':
            shapes.append(LineString(line + [line[0]]).buffer(w/2, join_style=2) if closed else stroke_flat(line, w))
        elif style['term'] == 'round':
            if not closed and math.hypot(line[0][0]-line[-1][0], line[0][1]-line[-1][1]) <= 2.2*w and len(line) == 2:
                shapes.append(Point(((line[0][0]+line[-1][0])/2, (line[0][1]+line[-1][1])/2)).buffer(w/2, 12)); continue
            shapes.append(LineString(line + [line[0]] if closed else inset_ends(line, w/2)).buffer(w/2, quad_segs=12))
        else:
            shapes.append(stroke_brush(line, closed, w, rng))
    g = unary_union(shapes)
    if style['term'] == 'flat':
        g = g.intersection(box(-1e4, -200 if name == 'g' else 0, 1e4, 700))
    return g.simplify(0.6)

def to_ttglyph(geom, dx):
    pen = TTGlyphPen(None)
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for poly in polys:
        if poly.is_empty or not isinstance(poly, Polygon): continue
        poly = orient(poly, sign=-1.0)
        for ring in [poly.exterior] + list(poly.interiors):
            c = [(round(x+dx), round(y)) for x, y in ring.coords[:-1]]
            dd = [c[0]] + [q for k, q in enumerate(c[1:], 1) if q != c[k-1]]
            if len(dd) < 3: continue
            pen.moveTo(dd[0]); [pen.lineTo(q) for q in dd[1:]]; pen.closePath()
    return pen.glyph()

def build_font(sname):
    style = STYLES[sname]; rng = random.Random(42)
    fam = f"Rexxar {sname}"
    order = ['.notdef', 'space'] + list(GLYPHS)
    glyphs, metrics = {}, {}
    glyphs['.notdef'] = TTGlyphPen(None).glyph(); metrics['.notdef'] = (500, 0)
    glyphs['space'] = TTGlyphPen(None).glyph(); metrics['space'] = (250 if sname != 'Hand' else 220, 0)
    for name in GLYPHS:
        g = build_glyph(name, style, rng)
        minx, _, maxx, _ = g.bounds
        dx = style['sb'] - minx
        if style.get('slant'):
            up = build_glyph(name, dict(style, slant=0.0), rng)
            minx, _, maxx, _ = up.bounds
            dx = style['sb'] - minx - style['slant']*250
        glyphs[name] = to_ttglyph(g, dx)
        metrics[name] = (round(maxx - minx + 2*style['sb']), style['sb'])
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {CHARS[n]: n for n in GLYPHS}; cmap[0x20] = 'space'
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-260)
    fb.setupNameTable({'familyName': fam, 'styleName': 'Regular', 'uniqueFontIdentifier': f'{fam}-1.0',
                       'fullName': fam, 'psName': fam.replace(' ', '') + '-Regular', 'version': 'Version 1.000',
                       'copyright': '© 2026 Chia-Hung Lin'})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-250, sTypoLineGap=0, usWinAscent=900, usWinDescent=260,
                sxHeight=500, sCapHeight=700, achVendID='RXXR')
    fb.setupPost(); fb.setupHead(unitsPerEm=1000)
    path = f"out/Rexxar{sname}.ttf"
    fb.save(path)
    fb.font.flavor = 'woff2'; fb.font.save(path.replace('.ttf', '.woff2'))
    return path

if __name__ == '__main__':
    import os; os.makedirs('out', exist_ok=True)
    import sys
    for s in (sys.argv[1:] or STYLES): print(build_font(s))
