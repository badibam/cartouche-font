"""Read the upstream Mono10 TTFs and write their glyphs as pixel maps.

Run once. From then on the pixel maps are the source of truth and this script
only serves to prove that nothing was lost on the way in.
"""

from fontTools.ttLib import TTFont
from fontTools.pens.pointInsidePen import PointInsidePen

from pixelfont import BOTTOM_PX, CELL_W, GLYPHS, ROOT, TOP_PX, cells_to_rows, write_maps

DROPPED = {".notdef", ".null", "nonmarkingreturn"}

SOURCES = {
    "regular": ROOT / "upstream/mono10/mono10_regular.ttf",
    "thin": ROOT / "upstream/mono10/mono10_thin.ttf",
}

HEADER = """# Cartes de pixels — {weight}, extrait de Mono10 (SIL OFL 1.1).
# 11 colonnes sur 14 rangees, de y=11 a y=-2. Les capitales tiennent les rangees
# 0 a 9, les accents les rangees 10 et 11, les descendantes -1 et -2.
# La colonne 10 est l'interlettre et reste vide.
"""


def raster(glyphset, name):
    cells = set()
    for y in range(BOTTOM_PX, TOP_PX + 1):
        for x in range(CELL_W):
            pen = PointInsidePen(glyphset, (x * 64 + 32, y * 64 + 32))
            glyphset[name].draw(pen)
            if pen.getResult():
                cells.add((x, y))
    return cells


def main():
    for weight, src in SOURCES.items():
        font = TTFont(src)
        glyphset = font.getGlyphSet()
        by_name = {n: c for c, n in sorted(font.getBestCmap().items())}
        maps = {}
        for name in font.getGlyphOrder():
            if name in DROPPED:
                continue
            cells = raster(glyphset, name)
            outside = [n for n in cells if not 0 <= n[1] <= 9]
            assert not outside, (name, outside)
            maps[name] = (by_name.get(name), cells_to_rows(cells))
        path = GLYPHS / f"{weight}.txt"
        write_maps(path, maps, HEADER.format(weight=weight))
        print(f"{path.name}: {len(maps)} glyphes")


if __name__ == "__main__":
    main()
