#!/usr/bin/env python3
"""Comprovador independent: llegeix casos.json i compta les solucions per força
bruta (sense fer servir motor.py), amb una reimplementació pròpia de les
regles. Un cas és correcte si té exactament 1 solució i és la que el cas diu.

  python verifica.py casos.json
"""
import json
import sys
from itertools import permutations

from escenaris import ESCENARIS


def comprova(cas):
    n = cas["n"]
    esc = ESCENARIS[cas["escenari"]]
    pla, sala, obj = cas["pla"], cas["sala"], cas["obj"]
    objs = cas.get("objectes") or esc["objectes"]
    bloq = {k: v["bloqueja"] for k, v in objs.items()}
    ids = [p["id"] for p in cas["persones"]]
    vict = ids[-1]

    def lliure(r, c):
        return pla[r][c] == 1 and (obj[r][c] is None or not bloq[obj[r][c]])

    def dins(r, c):
        return 0 <= r < n and 0 <= c < n and pla[r][c] == 1

    def parets(r, c):
        # (dalt, baix, esquerra, dreta): cert si hi ha paret o buit
        return tuple(not dins(r + dr, c + dc) or sala[r + dr][c + dc] != sala[r][c]
                     for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))

    def comprova_pista(cl, pos):
        t = cl["t"]
        if t == "compte_sala":
            return sum(1 for c in pos.values() if sala[c[0]][c[1]] == cl["sala"]) == cl["k"]
        a = pos[cl["p"]]
        r, c = a
        if t == "en_sala":
            return sala[r][c] == cl["sala"]
        if t == "no_en_sala":
            return sala[r][c] != cl["sala"]
        if t == "sobre_obj":
            return obj[r][c] == cl["obj"]
        if t == "prop_obj":
            return any(dins(r + dr, c + dc) and sala[r + dr][c + dc] == sala[r][c]
                       and obj[r + dr][c + dc] == cl["obj"]
                       for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        if t == "raco":
            u, d, e, w = parets(r, c)
            return (u or d) and (e or w)
        if t == "vora":
            return any(not dins(r + dr, c + dc)
                       for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        if t == "fila_obj":
            return any(obj[r][j] == cl["obj"] and j != c for j in range(n))
        if t == "col_obj":
            return any(obj[i][c] == cl["obj"] and i != r for i in range(n))
        if t == "sol":
            return all(sala[x[0]][x[1]] != sala[r][c]
                       for k, x in pos.items() if k != cl["p"])
        b = pos[cl["q"]]
        dr, dc = abs(r - b[0]), abs(c - b[1])
        if t == "costat":
            return dr + dc == 1 and sala[r][c] == sala[b[0]][b[1]]
        if t == "nord":
            return r < b[0]
        if t == "sud":
            return r > b[0]
        if t == "est":
            return c > b[1]
        if t == "oest":
            return c < b[1]
        if t == "diag":
            return dr == dc and dr > 0
        if t == "cavall":
            return {dr, dc} == {1, 2}
        if t == "mateixa_sala":
            return sala[r][c] == sala[b[0]][b[1]]
        if t == "altra_sala":
            return sala[r][c] != sala[b[0]][b[1]]
        if t == "sol_amb":
            R = sala[r][c]
            if sala[b[0]][b[1]] != R:
                return False
            return all(sala[x[0]][x[1]] != R
                       for k, x in pos.items() if k not in (cl["p"], cl["q"]))
        raise ValueError(t)

    n_sol = 0
    trobades = []
    if FORCA:
        for cols in permutations(range(n)):
            if not all(lliure(r, cols[r]) for r in range(n)):
                continue
            cel = [(r, cols[r]) for r in range(n)]
            for perm in permutations(range(n)):
                pos = {ids[perm[r]]: cel[r] for r in range(n)}
                sv = sala[pos[vict][0]][pos[vict][1]]
                if sum(1 for k, x in pos.items() if k != vict and sala[x[0]][x[1]] == sv) != 1:
                    continue
                if all(comprova_pista(cl, pos) for cl in cas["pistes"]):
                    n_sol += 1
                    trobades.append(pos)
    else:
        # cerca amb retrocés: es col·loca una persona cada cop (una per fila i columna) i es
        # comproven les pistes tan bon punt les persones que hi surten ja són col·locades
        COMPLETES = {"compte_sala", "sol", "sol_amb"}
        cel_lliures = [(r, c) for r in range(n) for c in range(n) if lliure(r, c)]
        # domini de cada persona segons les seves pistes que només la mencionen a ella
        dom = {k: list(cel_lliures) for k in ids}
        for cl in cas["pistes"]:
            if cl["t"] not in COMPLETES and "q" not in cl:
                dom[cl["p"]] = [x for x in dom[cl["p"]] if comprova_pista(cl, {cl["p"]: x})]
        ordre = sorted(ids, key=lambda k: len(dom[k]))
        lloc = {k: i for i, k in enumerate(ordre)}
        parcials = [[] for _ in ids]
        finals = []
        for cl in cas["pistes"]:
            if cl["t"] in COMPLETES:
                finals.append(cl)
            else:
                ult = max(lloc[cl["p"]], lloc.get(cl.get("q"), 0))
                parcials[ult].append(cl)
        pos = {}
        files, cols_ = set(), set()

        def cerca(i):
            nonlocal n_sol
            if i == n:
                sv = sala[pos[vict][0]][pos[vict][1]]
                if sum(1 for k, x in pos.items() if k != vict and sala[x[0]][x[1]] == sv) != 1:
                    return
                if all(comprova_pista(cl, pos) for cl in finals):
                    n_sol += 1
                    trobades.append(dict(pos))
                return
            k = ordre[i]
            for x in dom[k]:
                if x[0] in files or x[1] in cols_:
                    continue
                pos[k] = x
                if all(comprova_pista(cl, pos) for cl in parcials[i]):
                    files.add(x[0])
                    cols_.add(x[1])
                    cerca(i + 1)
                    files.discard(x[0])
                    cols_.discard(x[1])
                del pos[k]

        cerca(0)
    esperada = {k: tuple(v) for k, v in cas["solucio"].items()}
    return n_sol, (len(trobades) == 1 and trobades[0] == esperada)


FORCA = "--forca" in sys.argv

if __name__ == "__main__":
    casos = json.load(open(sys.argv[1], encoding="utf-8"))
    mal = 0
    for cas in casos:
        n_sol, ok = comprova(cas)
        print(cas["id"], "nivell", cas["nivell"], "solucions:", n_sol,
              "OK" if ok else "ERROR")
        mal += not ok
    print("Tot correcte" if not mal else f"{mal} casos amb errors")
    sys.exit(1 if mal else 0)
