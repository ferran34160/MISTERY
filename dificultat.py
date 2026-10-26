#!/usr/bin/env python3
"""Calcula per a cada cas verificat quantes eliminacions «per hipòtesi» (mirar endavant) calen i en deriva
el nivell final: 1-3 i 4 (tècniques de patrons) tal com surten de motor.valora; el 5 (cal provar hipòtesis)
es parteix en 4 «Difícil» (poques proves) i 5 «Expert» (moltes). Escriu dificultats.json {id: [nivell_motor, proves]}.

Ús: python dificultat.py ids.txt
"""
import glob
import json
import sys

import motor

LET = "ABCDEFGHIJ"


def calcula(c):
    n = c["n"]
    idx = lambda l: n - 1 if l == "V" else LET.index(l)
    bloq = {k: v["bloqueja"] for k, v in c["objectes"].items()}
    L = motor.Plantilla(n, [[bool(x) for x in f] for f in c["pla"]], c["sala"], c["obj"], bloq)
    pistes = []
    for cl in c["pistes"]:
        d = dict(cl)
        for k in ("p", "q"):
            if k in d:
                d[k] = idx(d[k])
        pistes.append(d)
    return motor.valora(L, pistes, n, detall=True)


def main():
    ok = {l.strip() for l in open(sys.argv[1]) if l.strip()}
    try:
        res = json.load(open("dificultats.json"))
    except (OSError, ValueError):
        res = {}
    nous = 0
    for f in sorted(glob.glob("*.json")):
        if f in ("noms.json", "casos_final.json", "assignacions.json", "casos_kpop.json", "casos_meu.json", "dificultats.json"):
            continue
        for c in json.load(open(f, encoding="utf-8")):
            if c["id"] in ok and c["id"] not in res:
                if "objectes" not in c:
                    from escenaris import ESCENARIS
                    from generador import objectes_json
                    c["objectes"] = objectes_json(ESCENARIS[c["escenari"]], c["obj"])
                r = calcula(c)
                if r:
                    res[c["id"]] = list(r)
                    nous += 1
    json.dump(res, open("dificultats.json", "w"), indent=0, sort_keys=True)
    print(nous, "nous;", len(res), "en total")


if __name__ == "__main__":
    main()
