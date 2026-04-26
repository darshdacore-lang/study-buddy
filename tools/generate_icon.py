from pathlib import Path
import math
import struct
import zlib


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "study-helper-icon.png"

SIZE = 1024
BACKGROUND = (33, 81, 69, 255)
CARD = (251, 248, 241, 255)
PAGE_LEFT = (33, 81, 69, 255)
PAGE_RIGHT = (46, 109, 95, 255)
ACCENT = (217, 139, 95, 255)
LINE_LEFT = (144, 212, 193, 255)
LINE_RIGHT = (196, 239, 226, 255)


def point_in_polygon(x, y, points):
    inside = False
    j = len(points) - 1
    for i in range(len(points)):
        xi, yi = points[i]
        xj, yj = points[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def dist_to_segment(px, py, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    if dx == dy == 0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def rounded_rect(x, y, w, h, radius):
    def contains(px, py):
        cx = min(max(px, x + radius), x + w - radius)
        cy = min(max(py, y + radius), y + h - radius)
        return (px - cx) ** 2 + (py - cy) ** 2 <= radius ** 2

    return contains


def circle(cx, cy, radius):
    radius_sq = radius * radius

    def contains(px, py):
        return (px - cx) ** 2 + (py - cy) ** 2 <= radius_sq

    return contains


def polygon(points):
    return lambda px, py: point_in_polygon(px, py, points)


def stroke(points, width):
    half = width / 2

    def contains(px, py):
        for start, end in zip(points, points[1:]):
            if dist_to_segment(px, py, start[0], start[1], end[0], end[1]) <= half:
                return True
        return False

    return contains


def write_png(path, width, height, rows):
    def chunk(kind, data):
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw.extend(row)

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png.extend(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)))
    png.extend(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
    png.extend(chunk(b"IEND", b""))
    path.write_bytes(png)


def build_icon():
    bg_shape = rounded_rect(0, 0, SIZE, SIZE, 232)
    circle_shape = circle(512, 512, 332)
    left_page = polygon(
        [
            (322, 390),
            (322, 617),
            (366, 661),
            (482, 661),
            (560, 710),
            (560, 391),
            (470, 346),
            (366, 346),
        ]
    )
    right_page = polygon(
        [
            (464, 391),
            (464, 710),
            (542, 661),
            (658, 661),
            (702, 617),
            (702, 390),
            (658, 346),
            (554, 346),
        ]
    )
    arrow = stroke([(494, 430), (558, 366), (630, 438)], 54)
    shaft = stroke([(558, 366), (558, 548)], 54)
    left_lines = [
        stroke([(388, 495), (496, 495)], 30),
        stroke([(388, 564), (478, 564)], 30),
    ]
    right_lines = [
        stroke([(528, 495), (636, 495)], 30),
        stroke([(546, 564), (636, 564)], 30),
    ]

    rows = []
    for y in range(SIZE):
        row = bytearray()
        for x in range(SIZE):
            color = (0, 0, 0, 0)
            if bg_shape(x, y):
                color = BACKGROUND
            if circle_shape(x, y):
                color = CARD
            if left_page(x, y):
                color = PAGE_LEFT
            if right_page(x, y):
                color = PAGE_RIGHT
            if any(line(x, y) for line in left_lines):
                color = LINE_LEFT
            if any(line(x, y) for line in right_lines):
                color = LINE_RIGHT
            if arrow(x, y) or shaft(x, y):
                color = ACCENT
            row.extend(color)
        rows.append(bytes(row))
    write_png(OUT, SIZE, SIZE, rows)


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    build_icon()
    print(OUT)
