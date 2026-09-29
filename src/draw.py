"""Rerun one drawing step on the pixel maps, showing what it changes first.

A step writes straight into `glyphs/`, the source of truth. So it runs first on
a scratch copy of the maps, the glyphs it would add, redraw or drop are listed,
and only then is it run for real.

    python3 src/draw.py <step> [--dry-run | --yes]
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pixelfont import GLYPHS, read_maps

SRC = Path(__file__).resolve().parent
STEPS = {
    "descenders": "the tails of g j p q y",
    "accents": "the accented letters, French signs and drawn glyphs",
    "frames": "the sixteen frame pieces",
    "furniture": "the interface symbols of the private area",
    "big": "the symbols again, for the second size",
    "phonemes": "the phonemes Saylune's analysis prints",
    "scramble": "the scrambled letters",
}


def run_step(step, glyphs):
    env = dict(os.environ, PIXEL_FONT_GLYPHS=str(glyphs))
    return subprocess.run([sys.executable, str(SRC / f"{step}.py")], env=env,
                          capture_output=True, text=True).returncode == 0


def changes(before, after):
    """{file: (added, redrawn, dropped)} for the files that differ."""
    out = {}
    for path in sorted(after.glob("*.txt")):
        old = read_maps(before / path.name) if (before / path.name).exists() else {}
        new = read_maps(path)
        added = sorted(set(new) - set(old))
        dropped = sorted(set(old) - set(new))
        redrawn = sorted(n for n in set(old) & set(new) if old[n] != new[n])
        if added or dropped or redrawn:
            out[path.name] = (added, redrawn, dropped)
    return out


def preview(step):
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / "glyphs"
        shutil.copytree(GLYPHS, copy)
        if not run_step(step, copy):
            print(f"{step}: failed on the scratch copy, nothing written")
            return None
        found = changes(GLYPHS, copy)
    if not found:
        print(f"{step}: the maps already hold this drawing, nothing to write")
    for name, (added, redrawn, dropped) in found.items():
        print(f"{name}: {len(added)} added, {len(redrawn)} redrawn, {len(dropped)} dropped")
        for label, names in (("added", added), ("redrawn", redrawn), ("dropped", dropped)):
            if names:
                print(f"  {label}: {' '.join(names[:12])}{' …' if len(names) > 12 else ''}")
    return found


def main(argv):
    if not argv or argv[0] not in STEPS:
        print(__doc__.strip().splitlines()[-1].strip())
        for step, what in STEPS.items():
            print(f"  {step:<11} {what}")
        return 1
    step, flags = argv[0], set(argv[1:])
    found = preview(step)
    if not found or "--dry-run" in flags:
        return 0 if found is not None else 1
    if "--yes" not in flags:
        try:
            if input("Write this into glyphs/? [y/N] ").strip().lower() != "y":
                print("Cancelled.")
                return 0
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 0
    if not run_step(step, GLYPHS):
        print(f"{step}: failed on glyphs/")
        return 1
    print(f"{step}: written. ./run build to compile it")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
