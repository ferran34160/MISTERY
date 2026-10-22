#!/usr/bin/env python3
"""Genera casos del joc de misteri i els desa en JSON (textos en ca i fr).

Ús:
  python generador.py --quantitat 10 --mida 6 --llavor 1 --sortida casos.json
  python generador.py --quantitat 3 --veure          # imprimeix els casos
"""
import argparse
import json
import random
import time

import motor
from escenaris import ESCENARIS, NOMS_LLETRA
from textos import descriu

LLETRES = "ABCDEFGHIJ"


def prepara(rng, esc, cas):
    """Afegeix a una còpia de l'escenari els noms de persones i sales."""
    n = cas["n"]
    L = cas["plantilla"]
    e = dict(esc)
    e["_noms"] = {p: rng.choice(NOMS_LLETRA[etiqueta(p, n)]) for p in range(n)}
    e["_sales"] = {i: L.noms_sales[i] for i in range(len(L.noms_sales))}
    return e


def etiqueta(p, n):
    return "V" if p == n - 1 else LLETRES[p]


def objectes_json(esc, obj):
    """Noms (ca/fr) i si bloquegen, només dels objectes que surten al plànol."""
    claus = {o for fila in obj for o in fila if o}
    return {k: {"bloqueja": esc["objectes"][k]["bloqueja"],
                "ca": esc["objectes"][k]["nom"]["ca"][1],
                "fr": esc["objectes"][k]["nom"]["fr"][1]} for k in sorted(claus)}


def a_json(cas, esc, e, rng, ident):
    n = cas["n"]
    L = cas["plantilla"]
    textos = {lang: descriu(lang, e, cas["pistes"], rng) for lang in ("ca", "fr")}
    pistes = []
    for cl in cas["pistes"]:
        d = dict(cl)
        d["p"] = etiqueta(cl["p"], n) if "p" in cl else None
        if "q" in cl:
            d["q"] = etiqueta(cl["q"], n)
        pistes.append({k: v for k, v in d.items() if v is not None})
    return {
        "id": ident,
        "escenari": next(k for k, v in ESCENARIS.items() if v is esc),
        "n": n,
        "nivell": cas["nivell"],
        "pla": [[1 if L.pla[r][c] else 0 for c in range(n)] for r in range(n)],
        "sala": L.sala,
        "sales": {str(i): {lang: e["sales"][e["_sales"][i]]["nom"][lang][1]
                           for lang in ("ca", "fr")} for i in e["_sales"]},
        "obj": L.obj,
        "objectes": objectes_json(esc, L.obj),
        "persones": [{"id": etiqueta(p, n), "nom": e["_noms"][p][0],
                      "genere": e["_noms"][p][1]} for p in range(n)],
        "pistes": pistes,
        "textos": textos,
        "solucio": {etiqueta(p, n): list(cas["solucio"][p]) for p in range(n)},
        "assassi": etiqueta(cas["assassi"], n),
    }


def vista(cas, e, lang="ca"):
    n = cas["n"]
    L = cas["plantilla"]
    sol = {v: k for k, v in cas["solucio"].items()}
    out = [f"Nivell {cas['nivell']}  |  mida {n}x{n}  |  assassí: "
           f"{etiqueta(cas['assassi'], n)} ({e['_noms'][cas['assassi']][0]})"]
    sales = {i: e["sales"][e["_sales"][i]]["nom"][lang][1] for i in e["_sales"]}
    out.append("Sales: " + ", ".join(f"{chr(97 + i)}={s}" for i, s in sales.items()))
    out.append("Plànol (lletra=sala, # objecte que bloqueja, o objecte ocupable)  /  solució")
    for r in range(n):
        a, b = [], []
        for c in range(n):
            if not L.pla[r][c]:
                a.append("    ")
                b.append("  . ")
                continue
            o = L.obj[r][c]
            marca = "#" if o and L.bloqueja[o] else ("o" if o else " ")
            a.append(f" {chr(97 + L.sala[r][c])}{marca} ")
            p = sol.get((r, c))
            b.append(f" {etiqueta(p, n)}  " if p is not None else "  . ")
        out.append("".join(a) + "    " + "".join(b))
    if any(L.obj[r][c] for r in range(n) for c in range(n)):
        llegenda = sorted({o for row in L.obj for o in row if o})
        out.append("Objectes: " + ", ".join(
            f"{o} ({'bloqueja' if L.bloqueja[o] else 'ocupable'})" for o in llegenda))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quantitat", type=int, default=5)
    ap.add_argument("--mida", type=int, default=6)
    ap.add_argument("--llavor", type=int, default=1)
    ap.add_argument("--sortida", default=None)
    ap.add_argument("--veure", action="store_true")
    ap.add_argument("--nivell", type=int, default=None, help="només aquest nivell")
    ap.add_argument("--escenari", default="mas")
    ap.add_argument("--sales", default=None, help="nombre de sales a triar, p. ex. 5,6")
    a = ap.parse_args()

    rng = random.Random(a.llavor)
    esc = ESCENARIS[a.escenari]
    casos = []
    t0 = time.time()
    intents = 0
    while len(casos) < a.quantitat and intents < a.quantitat * 400:
        intents += 1
        ks = rng.choice([int(x) for x in a.sales.split(",")]) if a.sales else None
        cas = motor.genera_cas(rng, esc, n=a.mida, k_sales=ks, intents=5)
        if cas is None:
            continue
        if a.nivell and cas["nivell"] != a.nivell:
            continue
        e = prepara(rng, esc, cas)
        j = a_json(cas, esc, e, rng, f"{a.escenari}-{a.mida}-{a.llavor}-{len(casos) + 1}")
        casos.append(j)
        if a.veure:
            print("=" * 70)
            print(vista(cas, e))
            for lang in ("ca", "fr"):
                print(f"-- {lang}")
                for cl, t in zip(cas["pistes"], j["textos"][lang]):
                    who = etiqueta(cl["p"], a.mida) if "p" in cl else "*"
                    print(f"  {who}: {t}")
    print(f"{len(casos)} casos en {time.time() - t0:.1f}s ({intents} intents)")
    if a.sortida:
        with open(a.sortida, "w", encoding="utf-8") as f:
            json.dump(casos, f, ensure_ascii=False, indent=1)
        print("Desat a", a.sortida)


if __name__ == "__main__":
    main()
