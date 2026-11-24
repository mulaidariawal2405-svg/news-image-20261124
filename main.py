"""News image for 24 November 2026.

Draws a one-page newspaper front page that sums up the world's news of
Tuesday 24 November 2026, using only the Python standard library.
Writes a deterministic 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(or ./out/entry.png when the variable is unset).

Stories (all reported on 24 Nov 2026):
  1. Fire at a candy factory in Indonesia kills 24.
  2. Ukraine says it sank a Russian warship off the coast of Libya.
  3. Nvidia reinstates CEO Jensen Huang after an affair with an alleged
     spy; the US moves to blacklist AI firm Megaspeed.
  4. COP31 climate talks in Turkiye stall over fossil fuels.
  5. The UN's top court (ICJ) rules Myanmar committed genocide
     against the Rohingya.
Footer: EU 22nd sanctions package, Iran warning the US over a naval
blockade, and the Trump-Xi-Putin joint statement at APEC.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (250, 246, 236)
INK = (22, 22, 28)
RED = (176, 32, 32)
BLUE = (28, 74, 130)
ORANGE = (214, 110, 20)
GOLD = (196, 148, 28)
GREEN = (34, 110, 58)
PANEL = (255, 253, 248)
GREY = (120, 116, 108)
LIGHT = (232, 226, 212)

# ---------------------------------------------------------------- font
# Hand-built 5x7 bitmap font, uppercase only. Each glyph is 7 rows of
# 5 bits, "#" = on, "." = off.

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}

FONT.update({
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
})

BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def glyph(ch):
    return FONT.get(ch.upper(), BLANK)


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.pix = bytearray(bg * (w * h))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.pix[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def frame(self, x, y, w, h, c, t=2):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.px(xx, yy, c)

    def ring(self, cx, cy, r, c, t=3):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if abs(d - r) <= t / 2.0:
                    self.px(xx, yy, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c):
        # Filled triangle by scanline interpolation.
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        if ay == cy:
            return
        def interp(y, x_top, y_top, x_bot, y_bot):
            if y_bot == y_top:
                return x_top
            return x_top + (x_bot - x_top) * (y - y_top) / (y_bot - y_top)
        for y in range(ay, cy + 1):
            if y < by:
                xa = interp(y, ax, ay, bx, by)
                xb = interp(y, ax, ay, cx, cy)
            else:
                xa = interp(y, bx, by, cx, cy)
                xb = interp(y, ax, ay, cx, cy)
            lo, hi = sorted([int(round(xa)), int(round(xb))])
            for x in range(lo, hi + 1):
                self.px(x, y, c)


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, scale, color):
    for ch in s:
        g = glyph(ch)
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    cv.rect(x + col * scale, y + row * scale, scale, scale, color)
        x += 6 * scale
    return x


def wrap_lines(s, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines = []
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_para(cv, x, y, s, scale, color, max_w, leading=None):
    lh = leading if leading is not None else 10 * scale
    for line in wrap_lines(s, scale, max_w):
        draw_text(cv, x, y, line, scale, color)
        y += lh
    return y


# ---------------------------------------------------------------- png
def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.pix[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- icons
def icon_flame(cv, cx, cy, s):
    # A stylised flame: outer flame, inner flame, ember base.
    sc = s / 100.0
    def X(v):
        return int(cx + v * sc)
    def Y(v):
        return int(cy + v * sc)
    cv.triangle(X(-34), Y(30), X(0), Y(-52), X(20), Y(-6), ORANGE)
    cv.triangle(X(-6), Y(28), X(30), Y(-18), X(38), Y(32), ORANGE)
    cv.triangle(X(-22), Y(30), X(2), Y(-30), X(26), Y(30), RED)
    cv.triangle(X(-12), Y(30), X(4), Y(-8), X(18), Y(30), GOLD)
    cv.rect(X(-40), Y(30), 80, 7, INK)
    cv.rect(X(-40), Y(30), 80, 7, INK)


def icon_ship(cv, cx, cy, s):
    sc = s / 100.0
    def X(v):
        return int(cx + v * sc)
    def Y(v):
        return int(cy + v * sc)
    # Sea
    cv.rect(X(-52), Y(30), 104, 6, BLUE)
    cv.rect(X(-40), Y(42), 80, 5, BLUE)
    # Hull: block plus pointed bow
    cv.rect(X(-48), Y(-4), 84, 30, INK)
    cv.triangle(X(36), Y(-4), X(50), Y(10), X(36), Y(26), INK)
    # Deck cabin + mast + flag
    cv.rect(X(-18), Y(-24), 34, 20, RED)
    cv.vline(X(4), Y(-54), 32, INK, 4)
    cv.triangle(X(4), Y(-54), X(34), Y(-46), X(4), Y(-38), RED)
    # Smoke puffs
    cv.disc(X(-30), Y(-36), 7, GREY)
    cv.disc(X(-40), Y(-46), 5, GREY)


def icon_chip(cv, cx, cy, s):
    sc = s / 100.0
    def X(v):
        return int(cx + v * sc)
    def Y(v):
        return int(cy + v * sc)
    # Pins
    for i in range(-1, 2):
        cv.rect(X(i * 28 - 4), Y(-52), 8, 14, INK)
        cv.rect(X(i * 28 - 4), Y(38), 8, 14, INK)
        cv.rect(X(-52), Y(i * 28 - 4), 14, 8, INK)
        cv.rect(X(38), Y(i * 28 - 4), 14, 8, INK)
    cv.rect(X(-38), Y(-38), 76, 76, INK)
    cv.rect(X(-30), Y(-30), 60, 60, BLUE)
    cv.rect(X(-16), Y(-16), 32, 32, GOLD)
    draw_text(cv, X(-11), Y(-11), "AI", 2, INK)


def icon_globe(cv, cx, cy, s):
    sc = s / 100.0
    def X(v):
        return int(cx + v * sc)
    def Y(v):
        return int(cy + v * sc)
    cv.ring(cx, cy, int(42 * sc), BLUE, 6)
    cv.disc(cx, cy, int(42 * sc), (214, 235, 244))
    # Meridians and parallels
    for k in (-20, 0, 20):
        cv.vline(X(k), Y(-40), 80, BLUE, 3)
    cv.hline(X(-42), Y(0), 84, BLUE, 3)
    cv.hline(X(-38), Y(-22), 76, BLUE, 3)
    cv.hline(X(-38), Y(22), 76, BLUE, 3)
    # Land blobs
    cv.disc(X(-16), Y(-14), 12, GREEN)
    cv.disc(X(14), Y(12), 13, GREEN)
    cv.disc(X(20), Y(-18), 7, GREEN)
    # Small leaf sprouting on top
    cv.triangle(X(0), Y(-42), X(16), Y(-66), X(2), Y(-44), GREEN)
    cv.triangle(X(0), Y(-42), X(-14), Y(-62), X(-2), Y(-42), GREEN)


def icon_scales(cv, cx, cy, s):
    sc = s / 100.0
    def X(v):
        return int(cx + v * sc)
    def Y(v):
        return int(cy + v * sc)
    # Post and beam
    cv.vline(cx, Y(-46), 92, INK, 5)
    cv.hline(X(-42), Y(-44), 84, INK, 5)
    cv.disc(cx, Y(-48), 6, GOLD)
    # Left pan
    cv.line(X(-40), Y(-44), X(-52), Y(-6), INK, 3)
    cv.line(X(-40), Y(-44), X(-28), Y(-6), INK, 3)
    cv.triangle(X(-58), Y(-6), X(-22), Y(-6), X(-40), Y(18), GOLD)
    # Right pan
    cv.line(X(40), Y(-44), X(52), Y(-6), INK, 3)
    cv.line(X(40), Y(-44), X(28), Y(-6), INK, 3)
    cv.triangle(X(22), Y(-6), X(58), Y(-6), X(40), Y(18), GOLD)
    # Base
    cv.rect(X(-26), Y(44), 52, 6, INK)


# ---------------------------------------------------------------- layout
def kicker(cv, x, y, label, color):
    draw_text(cv, x, y, label, 2, color)
    return y + 22


def story_panel(cv, x, y, w, h, tag, tag_color, icon, headline, body):
    cv.rect(x, y, w, h, PANEL)
    cv.frame(x, y, w, h, INK, 3)
    icon(cv, x + 64, y + 56, 84)
    draw_text(cv, x + 128, y + 30, tag, 2, tag_color)
    hy = draw_para(cv, x + 22, y + 104, headline, 3, INK, w - 44, leading=32) + 8
    draw_para(cv, x + 22, hy, body, 2, (52, 52, 58), w - 44, leading=22)


def build():
    cv = Canvas(W, H, PAPER)
    # Double outer border
    cv.frame(10, 10, W - 20, H - 20, INK, 3)
    cv.frame(20, 20, W - 40, H - 40, INK, 1)

    # Masthead
    title = "THE WORLD IN ONE FRAME"
    draw_text(cv, (W - text_w(title, 5)) // 2, 38, title, 5, INK)
    date = "TUESDAY 24 NOVEMBER 2026"
    draw_text(cv, (W - text_w(date, 3)) // 2, 90, date, 3, RED)
    cv.hline(36, 124, W - 72, INK, 3)
    cv.hline(36, 130, W - 72, INK, 1)

    # Lead story: Indonesia factory fire
    story_panel(cv, 36, 142, W - 72, 200, "LEAD STORY  -  INDONESIA",
                RED, icon_flame,
                "FIRE AT CANDY FACTORY KILLS 24",
                "A blaze ripped through a candy factory in Indonesia, "
                "killing at least 24 people. Rescue teams searched for "
                "the missing.")

    # Row two: Ukraine at sea / Nvidia
    story_panel(cv, 36, 356, 466, 280, "WAR AT SEA  -  UKRAINE",
                BLUE, icon_ship,
                "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
                "Kyiv said its forces sank a Russian warship and hit a "
                "cargo vessel off Libya, widening the war at sea.")
    story_panel(cv, 522, 356, 466, 280, "TECH  -  NVIDIA",
                BLUE, icon_chip,
                "HUANG BACK AT NVIDIA AFTER SPY AFFAIR",
                "Nvidia reinstated Jensen Huang after an affair with an "
                "alleged spy. The US moved to blacklist Megaspeed.")

    # Row three: climate / justice
    story_panel(cv, 36, 650, 466, 280, "CLIMATE  -  COP31",
                GREEN, icon_globe,
                "COP31 TALKS STALL OVER FOSSIL FUELS",
                "Climate talks in Turkiye struggled as nations split "
                "over fossil fuels, finance and help for poorer "
                "countries.")
    story_panel(cv, 522, 650, 466, 280, "JUSTICE  -  THE HAGUE",
                BLUE, icon_scales,
                "COURT: MYANMAR COMMITTED GENOCIDE",
                "The UN top court ruled Myanmar committed genocide "
                "against the Rohingya minority, a landmark verdict.")

    # Footer strip
    cv.rect(36, 944, W - 72, 40, INK)
    draw_text(cv, 52, 956, "ALSO:", 2, GOLD)
    foot = ("EU 22ND SANCTIONS ON RUSSIA - IRAN WARNS US - "
            "TRUMP, XI, PUTIN AT APEC")
    draw_text(cv, 52 + text_w("ALSO:  ", 2), 956, foot, 2, (240, 236, 226))

    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    path = os.path.join(out_dir, "entry.png")
    size = write_png(cv, path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()
