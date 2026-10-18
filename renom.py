#!/usr/bin/env python3
"""Posa a cada persona d'uns casos ja generats un nom que comença per la seva lletra
(A, B, C... i V) i en refà les frases de les pistes (ca i fr). La solució no canvia.

Ús: python renom.py fitxer.json [altre.json ...]
"""
import json
import random
import sys
import zlib

from escenaris import ESCENARIS, NOMS_LLETRA
from textos import descriu

LLETRES = "ABCDEFGHIJ"


def renomena(c):
    esc = ESCENARIS[c["escenari"]]
    n = c["n"]
    rng = random.Random(zlib.crc32(c["id"].encode()))
    idx = lambda l: n - 1 if l == "V" else LLETRES.index(l)
    noms = {idx(p["id"]): rng.choice(NOMS_LLETRA[p["id"]]) for p in c["persones"]}
    for p in c["persones"]:
        p["nom"], p["genere"] = noms[idx(p["id"])]
    e = dict(esc)
    e["_noms"] = noms
    claus = {}
    for i, nom in c["sales"].items():
        claus[int(i)] = next(k for k, v in esc["sales"].items()
                             if v["nom"]["ca"][1] == nom["ca"])
    e["_sales"] = claus
    pistes = []
    for cl in c["pistes"]:
        d = dict(cl)
        if "p" in d:
            d["p"] = idx(d["p"])
        if "q" in d:
            d["q"] = idx(d["q"])
        pistes.append(d)
    c["textos"] = {lang: descriu(lang, e, pistes, rng) for lang in ("ca", "fr")}


def main():
    for f in sys.argv[1:]:
        with open(f, encoding="utf-8") as fh:
            casos = json.load(fh)
        for c in casos:
            renomena(c)
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(casos, fh, ensure_ascii=False, indent=1)
        print(f, len(casos), "casos")


if __name__ == "__main__":
    main()
