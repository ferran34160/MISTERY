#!/usr/bin/env python3
"""Retalla un full d'objectes grans (fons crema) en imatges transparents objectes/g_<nom>.png i en registra
les mides possibles a grans.json: {classe: [{"img", "w", "h"}]} (w, h = caselles; l'objecte es dibuixa «contain», a baix).

Ús: python crop_grans.py full.webp regions.json   (regions.json: [[nom, classe, [x0,y0,x1,y1]], ...])
"""
import json
import math
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

FOOT = [(2, 1), (3, 1), (2, 2), (1, 2)]   # (amplada, alçada) en caselles, fins a 4 caselles; mai 1x1
FOOT_CATIFA = FOOT + [(1, 3), (2, 3), (3, 2)]          # les catifes (planes) poden ser més grans
MIN_FILL = 0.68


def treu_fons(sub, bg, th=55):
    a = np.asarray(sub, float)
    h, w, _ = a.shape
    low = np.sqrt(((a - bg) ** 2).sum(2)) < th
    bgm = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if low[y, x] and not bgm[y, x]:
                bgm[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if low[y, x] and not bgm[y, x]:
                bgm[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not bgm[ny, nx] and low[ny, nx]:
                bgm[ny, nx] = True
                q.append((ny, nx))
    fg = ~bgm
    lab = np.zeros((h, w), int)
    n, sizes = 0, []
    for y in range(h):
        for x in range(w):
            if fg[y, x] and not lab[y, x]:
                n += 1
                lab[y, x] = n
                qq = deque([(y, x)])
                s = 0
                while qq:
                    p, r = qq.popleft()
                    s += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = p + dy, r + dx
                            if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = n
                                qq.append((ny, nx))
                sizes.append(s)
    big = max(sizes)
    keep = np.zeros_like(fg)
    for i, s in enumerate(sizes, 1):
        if s >= 0.01 * big:
            keep |= lab == i
    am = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    o = sub.convert("RGBA")
    o.putalpha(am)
    return o


def main():
    im = Image.open(sys.argv[1]).convert("RGB")
    regs = json.load(open(sys.argv[2]))
    bg = np.array(im.getpixel((5, 5)), float)
    try:
        grans = json.load(open("grans.json"))
    except (OSError, ValueError):
        grans = {}
    for nom, classe, box in regs:
        o = treu_fons(im.crop(tuple(box)), bg)
        bb = o.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
        o = o.crop(bb)
        asp = o.size[0] / o.size[1]
        sc = 300 / max(o.size)
        o = o.resize((max(1, round(o.size[0] * sc)), max(1, round(o.size[1] * sc))), Image.LANCZOS)
        o.save(f"objectes/g_{nom}.png")
        ajusts = []
        for w, h in (FOOT_CATIFA if classe == "catifa" else FOOT):
            r = asp / (w / h)
            fill = min(r, 1 / r)
            ajusts.append((fill, w, h))
        ajusts.sort(reverse=True)
        bons = [(f, w, h) for f, w, h in ajusts if f >= MIN_FILL] or ajusts[:1]
        llista = [e for e in grans.get(classe, []) if e["img"] != f"objectes/g_{nom}.png"]
        for f, w, h in bons:
            llista.append({"img": f"objectes/g_{nom}.png", "w": w, "h": h})
        grans[classe] = llista
        print(nom, classe, round(asp, 2), [(w, h) for _, w, h in bons])
    json.dump(grans, open("grans.json", "w"), indent=0)


if __name__ == "__main__":
    main()
