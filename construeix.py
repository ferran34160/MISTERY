#!/usr/bin/env python3
"""Reuneix fitxers de casos en JSON i crea casos.js per a la pàgina (index.html).

Afegeix el camp "objectes" als casos antics que no el tenen.
Ús: python construeix.py casos_prova.json casos_n3.json
"""
import json
import random
import sys

from escenaris import ESCENARIS
from generador import objectes_json


# Noms propis dels casos: (nom ca, gènere ca, nom fr, gènere fr) i adjectius (m ca, f ca, m fr, f fr)
NOMS = {
    "mas": [("pou", "m", "puits", "m"),
        ("figuera", "f", "figuier", "m"),
        ("rellotge", "m", "horloge", "f"),
        ("clau", "f", "clé", "f"),
        ("candeler", "m", "chandelier", "m"),
        ("tonell", "m", "tonneau", "m"),
        ("carro", "m", "charrette", "f"),
        ("llindar", "m", "seuil", "m"),
        ("pastera", "f", "pétrin", "m"),
        ("graner", "m", "grenier", "m"),
        ("xemeneia", "f", "cheminée", "f"),
        ("escala", "f", "échelle", "f"),
        ("hort", "m", "potager", "m"),
        ("celler", "m", "cellier", "m"),
        ("llavor", "f", "graine", "f"),
        ("vinya", "f", "vigne", "f"),
        ("era", "f", "aire", "f"),
        ("sínia", "f", "noria", "f"),
        ("porxo", "m", "porche", "m"),
        ("fanal", "m", "lanterne", "f"),
        ("testament", "m", "testament", "m"),
        ("cistell", "m", "panier", "m"),
        ("galliner", "m", "poulailler", "m"),
        ("bassa", "f", "mare", "f"),
        ("trull", "m", "pressoir", "m"),
        ("forn", "m", "four", "m"),
        ("molí", "m", "moulin", "m"),
        ("rebost", "m", "garde-manger", "m"),
        ("sorra", "f", "sable", "m"),
        ("campana", "f", "cloche", "f")],
    "estacio": [("andana", "f", "quai", "m"),
        ("tren", "m", "train", "m"),
        ("locomotora", "f", "locomotive", "f"),
        ("bitllet", "m", "billet", "m"),
        ("maleta", "f", "valise", "f"),
        ("fanal", "m", "lampadaire", "m"),
        ("rellotge", "m", "horloge", "f"),
        ("via", "f", "voie", "f"),
        ("senyal", "m", "signal", "m"),
        ("vagó", "m", "wagon", "m"),
        ("taquilla", "f", "guichet", "m"),
        ("cafè", "m", "café", "m"),
        ("equipatge", "m", "bagage", "m"),
        ("passatger", "m", "voyageur", "m"),
        ("estufa", "f", "poêle", "m"),
        ("telègraf", "m", "télégraphe", "m"),
        ("campana", "f", "cloche", "f"),
        ("bàscula", "f", "bascule", "f"),
        ("llanterna", "f", "lanterne", "f"),
        ("horari", "m", "horaire", "m")],
    "teatre": [("teló", "m", "rideau", "m"),
        ("escenari", "m", "scène", "f"),
        ("piano", "m", "piano", "m"),
        ("mirall", "m", "miroir", "m"),
        ("maniquí", "m", "mannequin", "m"),
        ("reflector", "m", "projecteur", "m"),
        ("butaca", "f", "fauteuil", "m"),
        ("bagul", "m", "malle", "f"),
        ("camerino", "m", "loge", "f"),
        ("guió", "m", "scénario", "m"),
        ("rèplica", "f", "réplique", "f"),
        ("maquillatge", "m", "maquillage", "m"),
        ("aplaudiment", "m", "applaudissement", "m"),
        ("màscara", "f", "masque", "m"),
        ("corona", "f", "couronne", "f"),
        ("vestit", "m", "costume", "m"),
        ("ombra", "f", "ombre", "f"),
        ("ària", "f", "air", "m"),
        ("apuntador", "m", "souffleur", "m"),
        ("escala", "f", "échelle", "f")]}
ADJ = [("mut", "muda", "muet", "muette"), ("trencat", "trencada", "brisé", "brisée"),
       ("perdut", "perduda", "perdu", "perdue"), ("llunyà", "llunyana", "lointain", "lointaine"),
       ("fosc", "fosca", "sombre", "sombre"), ("amagat", "amagada", "caché", "cachée"),
       ("tardà", "tardana", "tardif", "tardive"), ("buit", "buida", "vide", "vide")]


def assigna_noms(casos):
    """Assigna un nom estable a cada cas (guardat a noms.json, per id), propi del seu escenari."""
    try:
        with open("noms.json", encoding="utf-8") as fh:
            noms = json.load(fh)
    except FileNotFoundError:
        noms = {}
    usats = {v["ca"] for v in noms.values()}
    lliures = {}
    for esc, llista in NOMS.items():
        combos = [(esc, a, b) for b in range(len(ADJ)) for a in range(len(llista))]
        random.Random(3).shuffle(combos)
        lliures[esc] = iter(k for k in combos if titol(*k)["ca"] not in usats)
    for c in casos:
        if c["id"] not in noms:
            noms[c["id"]] = titol(*next(lliures[c["escenari"]]))
        c["nom"] = noms[c["id"]]
    with open("noms.json", "w", encoding="utf-8") as fh:
        json.dump(noms, fh, ensure_ascii=False, indent=0)


def titol(esc, i, j):
    ca, gca, fr, gfr = NOMS[esc][i]
    a = ADJ[j]
    art_ca = "El " if gca == "m" else "La "
    if ca[0] in "aeiouàèéíòóúh":
        art_ca = "L'"
    art_fr = "Le " if gfr == "m" else "La "
    if fr[0] in "aeiouéèh":
        art_fr = "L'"
    return {"ca": art_ca + ca + " " + (a[0] if gca == "m" else a[1]),
            "fr": art_fr + fr + " " + (a[2] if gfr == "m" else a[3])}


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
    assigna_noms(casos)
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
