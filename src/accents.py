"""Draw the accented letters and the four French signs into the pixel maps.

An accent is drawn once and posed on a base letter: rows 9 and 8 over a
lowercase, 11 and 10 over a capital, which is why a capital keeps its full
height. The cedilla hangs in the two rows the descenders opened. The ring has
two rows only, so it is an arch that the top of its letter closes.

Alone, an accent sits where it sits over a lowercase.

Ligatures and signs have no base to sit on, so they are drawn outright.
"""

from pixelfont import CELL_W, GLYPHS, ROWS, TOP_PX, cells_to_rows, read_maps, rows_to_cells, write_maps

# Each mark gives the lit columns of its upper row, then of its lower row.
MARKS = {
    "regular": {
        "acute": ([4, 5, 6, 7], [2, 3, 4, 5]),
        "grave": ([2, 3, 4, 5], [4, 5, 6, 7]),
        "circumflex": ([3, 4, 5, 6], [1, 2, 7, 8]),
        "dieresis": ([2, 3, 6, 7], [2, 3, 6, 7]),
        "tilde": ([2, 3, 4, 7, 8], [1, 2, 5, 6, 7]),
        "ring": ([3, 4, 5, 6], [2, 3, 6, 7]),
        "caron": ([1, 2, 7, 8], [3, 4, 5, 6]),
        "macron": ([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]),
    },
    "thin": {
        "acute": ([5, 6], [3, 4]),
        "grave": ([3, 4], [5, 6]),
        "circumflex": ([4, 5], [3, 6]),
        "dieresis": ([3, 6], [3, 6]),
        "tilde": ([3, 4, 7], [2, 5, 6]),
        "ring": ([4, 5], [3, 6]),
        "caron": ([3, 6], [4, 5]),
        "macron": ([1, 2, 3, 4, 5, 6, 7, 8], []),
    },
}

CEDILLA = {
    "regular": ([4, 5], [2, 3, 4, 5]),
    "thin": ([4], [2, 3, 4]),
}

# base letter -> the accents it takes, and the codepoint of each result
ACCENTED = {
    "a": {"acute": 0x00E1, "grave": 0x00E0, "circumflex": 0x00E2, "dieresis": 0x00E4,
          "tilde": 0x00E3, "ring": 0x00E5},
    "e": {"acute": 0x00E9, "grave": 0x00E8, "circumflex": 0x00EA, "dieresis": 0x00EB},
    "i": {"acute": 0x00ED, "grave": 0x00EC, "circumflex": 0x00EE, "dieresis": 0x00EF},
    "n": {"tilde": 0x00F1},
    "o": {"acute": 0x00F3, "grave": 0x00F2, "circumflex": 0x00F4, "dieresis": 0x00F6,
          "tilde": 0x00F5},
    "s": {"caron": 0x0161},
    "u": {"acute": 0x00FA, "grave": 0x00F9, "circumflex": 0x00FB, "dieresis": 0x00FC},
    "y": {"acute": 0x00FD, "dieresis": 0x00FF},
    "z": {"caron": 0x017E},
    "A": {"acute": 0x00C1, "grave": 0x00C0, "circumflex": 0x00C2, "dieresis": 0x00C4,
          "tilde": 0x00C3, "ring": 0x00C5},
    "E": {"acute": 0x00C9, "grave": 0x00C8, "circumflex": 0x00CA, "dieresis": 0x00CB},
    "I": {"acute": 0x00CD, "grave": 0x00CC, "circumflex": 0x00CE, "dieresis": 0x00CF},
    "N": {"tilde": 0x00D1},
    "O": {"acute": 0x00D3, "grave": 0x00D2, "circumflex": 0x00D4, "dieresis": 0x00D6,
          "tilde": 0x00D5},
    "S": {"caron": 0x0160},
    "U": {"acute": 0x00DA, "grave": 0x00D9, "circumflex": 0x00DB, "dieresis": 0x00DC},
    "Y": {"acute": 0x00DD, "dieresis": 0x0178},
    "Z": {"caron": 0x017D},
}

# the accents alone: the spacing forms of Windows-1252
SPACING = {"dieresis": 0x00A8, "macron": 0x00AF, "acute": 0x00B4, "circumflex": 0x02C6,
           "tilde": 0x02DC}

CEDILLAS = {"c": 0x00E7, "C": 0x00C7}


def blank():
    return ["." * CELL_W for _ in range(ROWS)]


def place(rows, cols_hi, cols_lo, top):
    """Put a two-row mark on a copy of `rows`, its upper row at y = top."""
    cells = rows_to_cells(rows)
    cells |= {(x, top) for x in cols_hi}
    cells |= {(x, top - 1) for x in cols_lo}
    return cells_to_rows(cells)


def strip_dot(rows):
    """The dotless i: whatever sits above the x-height goes."""
    cells = {(x, y) for x, y in rows_to_cells(rows) if y < 8}
    return cells_to_rows(cells)


def main():
    from drawn import DRAWN

    for weight in ("regular", "thin"):
        path = GLYPHS / f"{weight}.txt"
        maps = read_maps(path)
        marks = MARKS[weight]
        added = 0

        for base, accents in ACCENTED.items():
            rows = maps[base][1]
            if base in ("i", "I"):
                rows = strip_dot(rows) if base == "i" else rows
            top = TOP_PX if base.isupper() else 9
            for accent, cp in accents.items():
                hi, lo = marks[accent]
                name = f"{base}{accent}"
                maps[name] = (cp, place(rows, hi, lo, top))
                added += 1

        hi, lo = CEDILLA[weight]
        for base, cp in CEDILLAS.items():
            maps[f"{base.lower()}cedilla" if base.islower() else "Ccedilla"] = (
                cp, place(maps[base][1], hi, lo, -1))
            added += 1
        maps["cedilla"] = (0x00B8, place(blank(), hi, lo, -1))
        added += 1

        for accent, cp in SPACING.items():
            hi, lo = marks[accent]
            maps[accent] = (cp, place(blank(), hi, lo, 9))
            added += 1

        for name, (cp, rows) in DRAWN[weight].items():
            maps[name] = (cp, rows)
            added += 1

        # The two dashes are the hyphen made longer. Mono10's hyphen already
        # fills ten of the eleven columns, so an en dash has no room to differ
        # from it and takes its drawing outright; the em dash takes the gutter
        # too, which is what makes two of them meet without a seam.
        hyphen = maps["hyphen"][1]
        ys = {y for _, y in rows_to_cells(hyphen)}
        maps["endash"] = (0x2013, hyphen)
        maps["emdash"] = (0x2014, cells_to_rows({(x, y) for y in ys for x in range(CELL_W)}))
        added += 2

        header = path.read_text(encoding="utf-8").split("\n@")[0]
        write_maps(path, maps, header)
        print(f"{path.name}: {added} glyphes ajoutes, {len(maps)} en tout")


if __name__ == "__main__":
    main()
