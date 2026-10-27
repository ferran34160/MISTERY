#!/usr/bin/env python3
"""Afegeix objectes «de decorat» als plànols perquè siguin tan plens com els de Murdoku (~40% de les caselles).

Els objectes nous són d'una classe que cap pista no cita, així que només treuen caselles possibles (els
bloquejants, mai la de la solució) o no canvien res (els ocupables): la solució continua sent única i la mateixa.
Es tria la quantitat més gran que deixa el nivell de dificultat igual que abans (si no, es proven menys objectes).
Escriu densitat.json {id: {"extra": [[r, c, bloqueja], ...], "niv": [nivell_motor, proves]}}.

Ús: python densifica.py ids.txt
"""
import glob
import json
import random
import sys
import zlib

import motor
from reskin import nivell_final

FRAC = 0.50            # fracció de caselles del plànol amb objecte (Murdoku: ~45-50%)
PART_BLOQ = 0.7        # part dels afegits que bloquegen
ESCALES = [1.0, 0.75, 0.5, 0.3]
LET = "ABCDEFGHIJ"


def plantilla(c, extra=()):
    n = c["n"]
    obj = [row[:] for row in c["obj"]]
    bloq = {k: v["bloqueja"] for k, v in c["objectes"].items()}
    bloq["_b"], bloq["_o"] = True, False
    for r, q, b in extra:
        obj[r][q] = "_b" if b else "_o"
    return motor.Plantilla(n, [[bool(x) for x in f] for f in c["pla"]], c["sala"], obj, bloq)


def pistes_motor(c):
    n = c["n"]
    idx = lambda l: n - 1 if l == "V" else LET.index(l)
    out = []
    for cl in c["pistes"]:
        d = dict(cl)
        for k in ("p", "q"):
            if k in d:
                d[k] = idx(d[k])
        out.append(d)
    return out


def tria_extres(c, rng, escala):
    n = c["n"]
    pla = [(r, q) for r in range(n) for q in range(n) if c["pla"][r][q]]
    lliures = [(r, q) for r, q in pla if not c["obj"][r][q]]
    sol = {tuple(v) for v in c["solucio"].values()}
    voler = int(FRAC * len(pla) * escala) - (len(pla) - len(lliures))
    if voler <= 0:
        return []
    rng.shuffle(lliures)
    out = []
    for r, q in lliures:
        if len(out) >= voler:
            break
        b = (r, q) not in sol and rng.random() < PART_BLOQ
        out.append([r, q, 1 if b else 0])
    return out


def main():
    ok = {l.strip() for l in open(sys.argv[1]) if l.strip()}
    dif = json.load(open("dificultats.json"))
    try:
        res = json.load(open("densitat.json"))
    except (OSError, ValueError):
        res = {}
    from escenaris import ESCENARIS
    from generador import objectes_json
    fet = 0
    for f in sorted(glob.glob("*.json")):
        if f in ("noms.json", "casos_final.json", "assignacions.json", "casos_kpop.json", "casos_meu.json",
                 "dificultats.json", "densitat.json"):
            continue
        for c in json.load(open(f, encoding="utf-8")):
            i = c["id"]
            if i not in ok or i in res or i not in dif:
                continue
            if "objectes" not in c:
                c["objectes"] = objectes_json(ESCENARIS[c["escenari"]], c["obj"])
            rng = random.Random(zlib.crc32(i.encode()))
            nivell0 = nivell_final(dif, i)
            pist = pistes_motor(c)
            trobat = {"extra": [], "niv": dif[i]}
            for esc in ESCALES:
                extra = tria_extres(c, rng, esc)
                if not extra:
                    break
                r = motor.valora(plantilla(c, extra), pist, c["n"], detall=True)
                if r and nivell_final({i: r}, i) == nivell0:
                    trobat = {"extra": extra, "niv": list(r)}
                    break
            res[i] = trobat
            fet += 1
    json.dump(res, open("densitat.json", "w"), separators=(",", ":"))
    from collections import Counter
    print(fet, "nous;", sum(1 for v in res.values() if v["extra"]), "amb objectes afegits de", len(res))


if __name__ == "__main__":
    main()
