import build
from build import P
T, B, M, W = 615, 85, 350, 760
R1, R2 = 250, 140
WIDE = {
    'R': [P([(0,0),(0,700)]), P([(0,T),(W,T,R2),(W,M,R2),(0,M)]), P([(420,M),(W,0)])],
    'E': [P([(W,T),(0,T,R1),(0,B,R1),(W,B)]), P([(0,M),(W-120,M)])],
    'X': [P([(0,0),(W,700)]), P([(0,700),(W,0)])],
    'A': [P([(0,0),(0,T,R1),(W,T,R1),(W,0)]), P([(0,M-30),(W,M-30)])],
    'C': [P([(W,T),(0,T,R1),(0,B,R1),(W,B)])],
    'G': [P([(W,T),(0,T,R1),(0,B,R1),(W,B,R2),(W,M),(400,M)])],
    'H': [P([(0,0),(0,700)]), P([(W,0),(W,700)]), P([(0,M),(W,M)])],
    'I': [P([(0,0),(0,700)])],
    'U': [P([(0,700),(0,B,R1),(W,B,R1),(W,700)])],
    'N': [P([(0,0),(0,T,R1),(W,T,R1),(W,0)])],
    'L': [P([(0,700),(0,B,R1),(W-40,B)])],
    'hyphen': [P([(0,M),(300,M)])],
}
build.GLYPHS.clear(); build.GLYPHS.update(WIDE)
build.CHARS.clear(); build.CHARS.update({g: (ord(g) if len(g)==1 else 0x2D) for g in WIDE})
build.STYLES['Wide'] = dict(w=172, corner='arc', rmap=lambda r: r, sb=38, term='flat')
# unicase: lowercase maps to the same glyphs
_orig = build.FontBuilder.setupCharacterMap
def cmap(self, m):
    m = dict(m); m.update({ord(c.lower()): c for c in WIDE if len(c)==1}); _orig(self, m)
build.FontBuilder.setupCharacterMap = cmap
print(build.build_font('Wide'))
