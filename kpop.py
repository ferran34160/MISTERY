#!/usr/bin/env python3
"""Casos del mode K-pop (molt fàcils, per a una nena de 6 anys): graelles de 5x5 (i alguns 6x6)
amb només les pistes més simples. Els personatges són els del retrat (kpop/retrats/).

Ús: python kpop.py [--cinc 12] [--sis 6] [--llavor 1]   -> escriu casos_kpop.json (verificats)
"""
import argparse
import json
import random
import zlib

import motor
from escenaris import ESCENARIS, KPOP_PERSONATGES
from generador import a_json, prepara
from textos import descriu

TIPUS = {"en_sala", "sobre_obj", "prop_obj", "raco", "costat", "compte_sala"}
LLETRES = "ABCDEFGHIJ"


def fes_casos(n, quantitat, llavor, nivells):
    esc = ESCENARIS["kpop"]
    motor.TIPUS_PERMESOS = TIPUS
    rng = random.Random(llavor)
    out, intents = [], 0
    while len(out) < quantitat and intents < 5000:
        intents += 1
        cas = motor.genera_cas(rng, esc, n=n, intents=5)
        if cas is None or cas["nivell"] not in nivells:
            continue
        e = prepara(rng, esc, cas)
        j = a_json(cas, esc, e, rng, f"kpop-{n}-{llavor}-{len(out) + 1}")
        # personatges amb inicials diferents
        ini = rng.sample(sorted(KPOP_PERSONATGES), n)
        idx = lambda l: n - 1 if l == "V" else LLETRES.index(l)
        noms = {}
        for p in j["persones"]:
            i = idx(p["id"])
            nom, g = rng.choice(KPOP_PERSONATGES[ini[i]])
            p["nom"], p["genere"], p["ins"] = nom, g, ini[i]
            noms[i] = (nom, g)
        e2 = dict(esc)
        e2["_noms"] = noms
        claus = {int(i): next(k for k, v in esc["sales"].items() if v["nom"]["ca"][1] == nom["ca"])
                 for i, nom in j["sales"].items()}
        e2["_sales"] = claus
        vistes, unics = [], []
        for cl in j["pistes"]:        # sense pistes idèntiques repetides
            if cl not in vistes:
                vistes.append(cl)
                unics.append(cl)
        j["pistes"] = unics
        pistes = []
        for cl in j["pistes"]:
            d = dict(cl)
            for k in ("p", "q"):
                if k in d:
                    d[k] = idx(d[k])
            pistes.append(d)
        j["textos"] = {l: descriu(l, e2, pistes, rng) for l in ("ca", "fr")}
        j["kpop"] = True
        out.append(j)
    return out


def refa_textos():
    """Torna a redactar les pistes dels casos ja generats (sense canviar-les)."""
    casos = json.load(open("casos_kpop.json", encoding="utf-8"))
    esc = ESCENARIS["kpop"]
    for j in casos:
        n = j["n"]
        idx = lambda l: n - 1 if l == "V" else LLETRES.index(l)
        e = dict(esc)
        e["_noms"] = {idx(p["id"]): (p["nom"], p["genere"]) for p in j["persones"]}
        e["_sales"] = {int(i): next(k for k, v in esc["sales"].items() if v["nom"]["ca"][1] == nm["ca"])
                       for i, nm in j["sales"].items()}
        pistes = []
        for cl in j["pistes"]:
            d = dict(cl)
            for k in ("p", "q"):
                if k in d:
                    d[k] = idx(d[k])
            pistes.append(d)
        rng = random.Random(zlib.crc32(j["id"].encode()))
        j["textos"] = {l: descriu(l, e, pistes, rng) for l in ("ca", "fr")}
    json.dump(casos, open("casos_kpop.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(casos), "casos K-pop (textos refets)")


def main():
    import os
    import sys
    if os.path.exists("casos_kpop.json") and "--nous" not in sys.argv:
        return refa_textos()      # els casos ja existeixen: només es redacten de nou les pistes
    ap = argparse.ArgumentParser()
    ap.add_argument("--cinc", type=int, default=12)
    ap.add_argument("--sis", type=int, default=6)
    ap.add_argument("--llavor", type=int, default=1)
    a = ap.parse_args()
    casos = fes_casos(5, a.cinc, a.llavor, {1}) + fes_casos(6, a.sis, a.llavor + 100, {1, 2})
    with open("casos_kpop.json", "w", encoding="utf-8") as fh:
        json.dump(casos, fh, ensure_ascii=False, indent=1)
    print(len(casos), "casos K-pop")


if __name__ == "__main__":
    main()
