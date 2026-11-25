#!/usr/bin/env python3
"""WCAG 2.x contrast checker. Standard library only.

Usage:
  python3 contrast.py FG BG [FG BG ...]
  python3 contrast.py "#9ca3af" "#080808" "#ffffff" "#fc964c"

Colours are hex: #rgb, #rrggbb or #rrggbbaa. A foreground with alpha is
blended over its background first (as a browser would).
Exit code 1 if any pair fails AA for normal text.
"""
import sys


def parse(hex_colour):
    h = hex_colour.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8):
        raise ValueError(f"not a hex colour: {hex_colour}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r, g, b, a


def blend(fg, bg):
    r, g, b, a = fg
    br, bgc, bb, _ = bg
    return (
        round(r * a + br * (1 - a)),
        round(g * a + bgc * (1 - a)),
        round(b * a + bb * (1 - a)),
    )


def luminance(rgb):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_hex, bg_hex):
    bg = parse(bg_hex)
    fg = blend(parse(fg_hex), bg)
    l1, l2 = sorted((luminance(fg), luminance(bg[:3])), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main(argv):
    if len(argv) < 2 or len(argv) % 2:
        print(__doc__)
        return 2
    failed = False
    print(f"{'foreground':<12} {'background':<12} {'ratio':>6}  normal  large/UI")
    for fg, bg in zip(argv[0::2], argv[1::2]):
        r = ratio(fg, bg)
        normal = r >= 4.5
        large = r >= 3.0
        failed |= not normal
        print(
            f"{fg:<12} {bg:<12} {r:>6.2f}  "
            f"{'PASS' if normal else 'FAIL':<6}  {'PASS' if large else 'FAIL'}"
        )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
