"""Draw what the Western European set still lacked: the rest of Windows-1252, the
text arrows and the comparison signs.

A glyph that is another glyph moved or cut is taken from it, so that the two
never drift apart: the low quotes are the high ones on the baseline, the minus
is the bar of the plus, the text arrows are the interface arrows. The others are
drawn outright.

The superscripts, the ordinals and the trademark are one pixel wide in both
weights, like the fractions: a letter three pixels wide has no room for a
two-pixel stroke. The bullet is a symbol and is the same in both weights.
"""

from pixelfont import CELL_W, GLYPHS, ROWS, TOP_PX, cells_to_rows, read_maps, rows_to_cells, write_maps

BLANK = "." * CELL_W


def pad(top, rows):
    """A drawing whose first row sits at y = top, each row widened to the cell."""
    rows = [r.ljust(CELL_W, ".") for r in rows]
    assert all(len(r) == CELL_W and r[-1] == "." for r in rows), rows
    first = TOP_PX - top
    out = [BLANK] * first + rows
    assert len(out) <= ROWS, (top, len(rows))
    return out + [BLANK] * (ROWS - len(out))


def shift(cells, dx=0, dy=0):
    return {(x + dx, y + dy) for x, y in cells}


# drawn in both weights at one pixel: (top row, rows)
SMALL = {
    "onesuperior": (0x00B9, 9, ["....#", "...##", "....#", "....#", "...###"]),
    "twosuperior": (0x00B2, 9, ["...##", ".....#", "....#", "...#", "...###"]),
    "threesuperior": (0x00B3, 9, ["...##", ".....#", "....#", ".....#", "...##"]),
    "ordfeminine": (0x00AA, 9, ["...###", "......#", "....###", "...#..#", "....###", "", "...####"]),
    "ordmasculine": (0x00BA, 9, ["....##", "...#..#", "...#..#", "...#..#", "....##", "", "...####"]),
    "trademark": (0x2122, 9, ["###.#...#", ".#..##.##", ".#..#.#.#", ".#..#...#", ".#..#...#"]),
    "threequarters": (0x00BE, 9, [
        "##.....#",
        "..#....#",
        ".#....#",
        "..#...#",
        "##...#",
        ".....#.#.#",
        "....#..#.#",
        "....#..###",
        "...#.....#",
        "...#.....#",
    ]),
}

DRAWN = {
    "regular": {
        "Eth": (0x00D0, 9, [
            ".########",
            ".#########",
            ".##.....##",
            ".##.....##",
            "#####...##",
            "#####...##",
            ".##.....##",
            ".##.....##",
            ".#########",
            ".########",
        ]),
        "Thorn": (0x00DE, 9, [
            "##",
            "##",
            "#########",
            "##########",
            "##......##",
            "##......##",
            "##########",
            "#########",
            "##",
            "##",
        ]),
        "germandbls": (0x00DF, 9, [
            ".#######",
            "#########",
            "##.....##",
            "##.....##",
            "##...###",
            "##...####",
            "##......##",
            "##......##",
            "##...#####",
            "##...####",
        ]),
        "florin": (0x0192, 9, [
            ".....####",
            "....######",
            "....##",
            "....##",
            "..######",
            "..######",
            "....##",
            "....##",
            "....##",
            "....##",
            "######",
            ".####",
        ]),
        "section": (0x00A7, 9, [
            "..######",
            ".########",
            ".##",
            "..######",
            ".########",
            ".##....##",
            ".##....##",
            ".########",
            "..######",
            ".......##",
            ".########",
            "..######",
        ]),
        "paragraph": (0x00B6, 9, [
            ".########",
            "######.##",
            "######.##",
            "######.##",
            ".#####.##",
            "....##.##",
            "....##.##",
            "....##.##",
            "....##.##",
            "....##.##",
        ]),
        "currency": (0x00A4, 8, [
            "##......##",
            "..######",
            ".##....##",
            ".##....##",
            ".##....##",
            ".##....##",
            "..######",
            "##......##",
        ]),
        "dagger": (0x2020, 9, [
            "....##",
            "....##",
            ".########",
            ".########",
            "....##",
            "....##",
            "....##",
            "....##",
            "....##",
            "....##",
        ]),
        "daggerdbl": (0x2021, 9, [
            "....##",
            "....##",
            ".########",
            ".########",
            "....##",
            "....##",
            ".########",
            ".########",
            "....##",
            "....##",
        ]),
        "logicalnot": (0x00AC, 5, [
            "##########",
            "##########",
            "........##",
            "........##",
        ]),
        "plusminus": (0x00B1, 9, [
            "....##",
            "....##",
            "##########",
            "##########",
            "....##",
            "....##",
            "",
            "",
            "##########",
            "##########",
        ]),
        "divide": (0x00F7, 8, [
            "....##",
            "....##",
            "",
            "##########",
            "##########",
            "",
            "....##",
            "....##",
        ]),
        "lessequal": (0x2264, 8, [
            ".....#####",
            "..########",
            "###",
            "..########",
            ".....#####",
            "",
            "",
            "##########",
            "##########",
        ]),
        "greaterequal": (0x2265, 8, [
            "#####",
            "########",
            ".......###",
            "########",
            "#####",
            "",
            "",
            "##########",
            "##########",
        ]),
        "notequal": (0x2260, 8, [
            "........##",
            "##########",
            "##########",
            ".....##",
            "....##",
            "##########",
            "##########",
            ".##",
        ]),
        "approxequal": (0x2248, 7, [
            ".####...##",
            "##...####",
            "",
            "",
            ".####...##",
            "##...####",
        ]),
        "arrowboth": (0x2194, 6, [
            "..##..##",
            ".##....##",
            "##########",
            "##########",
            ".##....##",
            "..##..##",
        ]),
        "guilsinglleft": (0x2039, 6, [
            ".....##",
            "...##",
            "...##",
            ".....##",
        ]),
        "guilsinglright": (0x203A, 6, [
            "...##",
            ".....##",
            ".....##",
            "...##",
        ]),
        "perthousand": (0x2030, 9, [
            "........##",
            ".##....###",
            ".##...###",
            ".....###",
            "....###",
            "...###",
            "..###",
            ".###.##.##",
            "###..##.##",
        ]),
    },
    "thin": {
        "Eth": (0x00D0, 9, [
            ".########",
            ".#.......#",
            ".#.......#",
            ".#.......#",
            "####.....#",
            ".#.......#",
            ".#.......#",
            ".#.......#",
            ".#.......#",
            ".########",
        ]),
        "Thorn": (0x00DE, 9, [
            "#",
            "#",
            "#########",
            "#........#",
            "#........#",
            "#........#",
            "#########",
            "#",
            "#",
            "#",
        ]),
        "germandbls": (0x00DF, 9, [
            ".#######",
            "#.......#",
            "#.......#",
            "#......#",
            "#...###",
            "#......#",
            "#........#",
            "#........#",
            "#........#",
            "#...#####",
        ]),
        "florin": (0x0192, 9, [
            ".....####",
            "....#",
            "....#",
            "....#",
            "....#",
            "..#####",
            "....#",
            "....#",
            "....#",
            "....#",
            "....#",
            ".###",
        ]),
        "section": (0x00A7, 9, [
            "..######",
            ".#",
            ".#",
            "..######",
            ".#......#",
            ".#......#",
            ".#......#",
            ".#......#",
            "..######",
            "........#",
            "........#",
            "..######",
        ]),
        "paragraph": (0x00B6, 9, [
            "..######",
            ".#####.#",
            ".#####.#",
            "..####.#",
            ".....#.#",
            ".....#.#",
            ".....#.#",
            ".....#.#",
            ".....#.#",
            ".....#.#",
        ]),
        "currency": (0x00A4, 8, [
            ".#.....#",
            "..#####",
            "..#...#",
            "..#...#",
            "..#...#",
            "..#####",
            ".#.....#",
        ]),
        "dagger": (0x2020, 9, [
            "....#",
            "....#",
            ".#######",
            "....#",
            "....#",
            "....#",
            "....#",
            "....#",
            "....#",
            "....#",
        ]),
        "daggerdbl": (0x2021, 9, [
            "....#",
            "....#",
            ".#######",
            "....#",
            "....#",
            "....#",
            "....#",
            ".#######",
            "....#",
            "....#",
        ]),
        "logicalnot": (0x00AC, 4, [
            "##########",
            ".........#",
            ".........#",
        ]),
        "plusminus": (0x00B1, 9, [
            "....#",
            "....#",
            "....#",
            "##########",
            "....#",
            "....#",
            "....#",
            "",
            "",
            "##########",
        ]),
        "divide": (0x00F7, 7, [
            "....#",
            "",
            "",
            "##########",
            "",
            "",
            "....#",
        ]),
        "lessequal": (0x2264, 8, [
            "......####",
            "...###",
            "###",
            "...###",
            "......####",
            "",
            "",
            "",
            "##########",
        ]),
        "greaterequal": (0x2265, 8, [
            "####",
            "....###",
            ".......###",
            "....###",
            "####",
            "",
            "",
            "",
            "##########",
        ]),
        "notequal": (0x2260, 8, [
            ".......#",
            "......#",
            "##########",
            ".....#",
            "....#",
            "...#",
            "##########",
            ".#",
        ]),
        "approxequal": (0x2248, 7, [
            "..###...##",
            "##...###",
            "",
            "",
            "..###...##",
            "##...###",
        ]),
        "arrowboth": (0x2194, 6, [
            "..#....#",
            ".#......#",
            "##########",
            ".#......#",
            "..#....#",
        ]),
        "guilsinglleft": (0x2039, 6, [
            "....#",
            "...#",
            "...#",
            "....#",
        ]),
        "guilsinglright": (0x203A, 6, [
            "...#",
            "....#",
            "....#",
            "...#",
        ]),
        "perthousand": (0x2030, 9, [
            ".........#",
            "........#",
            "..#....#",
            "......#",
            ".....#",
            "....#",
            "...#",
            "..#....#.#",
            ".#",
            "#",
        ]),
    },
}

BULLET = (0x2022, 6, ["...##", "..####", "..####", "...##"])


def derived(maps):
    """{name: (cp, rows)} for the glyphs taken from others."""
    out = {}

    def cells(name):
        return rows_to_cells(maps[name][1])

    def lowest(c):
        return min(y for _, y in c)

    # The low quotes: the high ones set down until they end where a comma does.
    drop = lowest(cells("comma")) - lowest(cells("quoteright"))
    out["quotesinglbase"] = (0x201A, cells_to_rows(shift(cells("quoteright"), dy=drop)))
    out["quotedblbase"] = (0x201E, cells_to_rows(shift(cells("quotedblright"), dy=drop)))

    # The middle dot: the period raised to the hyphen.
    rise = lowest(cells("hyphen")) - lowest(cells("period"))
    out["periodcentered"] = (0x00B7, cells_to_rows(shift(cells("period"), dy=rise)))

    # The minus: the plus without its stem, that is its widest rows.
    plus = cells("plus")
    width = {y: sum(1 for _, yy in plus if yy == y) for _, y in plus}
    out["minus"] = (0x2212, cells_to_rows({(x, y) for x, y in plus if width[y] == max(width.values())}))

    # The broken bar: the bar cut in its middle.
    bar = cells("bar")
    out["brokenbar"] = (0x00A6, cells_to_rows({(x, y) for x, y in bar if y not in (4, 5)}))

    # The micro sign: the u, its left stem run down to the descenders.
    u = cells("u")
    stem = {x for x, y in u if y == 3 and x < 5}
    out["mu"] = (0x00B5, cells_to_rows(u | {(x, y) for x in stem for y in range(-2, 1)}))

    # The thorn: the p, its stem run up to the ascenders.
    p = cells("p")
    stem = {x for x, y in p if y == 0}
    out["thorn"] = (0x00FE, cells_to_rows(p | {(x, y) for x in stem for y in range(5, 10)}))

    # The slashed o: the o crossed from its lower left to its upper right,
    # as thick as its walls.
    thick = 2 if (1, 4) in cells("O") else 1
    for name, cp, first in (("O", 0x00D8, 0), ("o", 0x00F8, 1)):
        c = cells(name)
        top = max(y for _, y in c)
        slash = {(y + first + dx, y) for y in range(thick, top + 1 - thick) for dx in range(thick)}
        out[f"{name}slash"] = (cp, cells_to_rows(c | slash))

    # The text arrows are the interface arrows.
    for arrow, cp in (("left", 0x2190), ("up", 0x2191), ("right", 0x2192), ("down", 0x2193)):
        out[f"arrow{arrow}"] = (cp, maps[f"arrow.{arrow}"][1])

    # The three spaces and the soft hyphen take the cell of what they stand for.
    out["uni00A0"] = (0x00A0, maps["space"][1])
    out["uni202F"] = (0x202F, maps["space"][1])
    out["uni00AD"] = (0x00AD, maps["hyphen"][1])
    return out


def main():
    for weight in ("regular", "thin"):
        path = GLYPHS / f"{weight}.txt"
        maps = read_maps(path)
        entries = {name: (cp, pad(top, rows)) for name, (cp, top, rows) in SMALL.items()}
        entries.update({name: (cp, pad(top, rows)) for name, (cp, top, rows) in DRAWN[weight].items()})
        entries["bullet"] = (BULLET[0], pad(BULLET[1], BULLET[2]))
        entries.update(derived(maps))
        taken = {cp: name for name, (cp, _) in maps.items() if cp is not None and name not in entries}
        clash = {name: taken[cp] for name, (cp, _) in entries.items() if cp in taken}
        assert not clash, clash
        maps.update(entries)
        header = path.read_text(encoding="utf-8").split("\n@")[0]
        write_maps(path, maps, header)
        print(f"{path.name}: {len(entries)} glyphes, {len(maps)} en tout")


if __name__ == "__main__":
    main()
