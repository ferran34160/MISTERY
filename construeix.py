#!/usr/bin/env python3
"""Reuneix fitxers de casos en JSON i crea casos.js per a la pàgina (index.html).

Afegeix el camp "objectes" als casos antics que no el tenen.
Ús: python construeix.py casos_prova.json casos_n3.json
"""
import json
import sys

from escenaris import ESCENARIS
from generador import objectes_json


def main():
    fitxers = sys.argv[1:] or ["casos_prova.json", "casos_n3.json"]
    casos, vistos = [], set()
    for f in fitxers:
        with open(f, encoding="utf-8") as fh:
            for c in json.load(fh):
                if c["id"] in vistos:
                    continue
                vistos.add(c["id"])
                if "objectes" not in c:
                    c["objectes"] = objectes_json(ESCENARIS[c["escenari"]], c["obj"])
                c["titol"] = ESCENARIS[c["escenari"]]["titol"]
                casos.append(c)
    casos.sort(key=lambda c: (c["n"], c["nivell"]))
    with open("casos.js", "w", encoding="utf-8") as fh:
        fh.write("window.CASOS = " + json.dumps(casos, ensure_ascii=False) + ";\n")
    print(len(casos), "casos a casos.js")
    # joc.html: tot en un sol fitxer (casos inclosos), per obrir-lo sense servidor
    with open("index.html", encoding="utf-8") as fh:
        html = fh.read()
    js = open("casos.js", encoding="utf-8").read()
    html = html.replace('<script src="casos.js"></script>', "<script>" + js + "</script>")
    with open("joc.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    print("joc.html creat")


if __name__ == "__main__":
    main()
