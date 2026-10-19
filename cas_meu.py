#!/usr/bin/env python3
"""Cas dissenyat per l'usuari en un full de càlcul (casa d'estiu, 7x7): plànol, sales, objectes i solució
són els del full; el programa només tria les pistes (amb solució única). Escriu casos_meu.json.

Fila 2..8 = r 0..6; columna B..H = c 0..6. Persones A-F + V (la G del full és la víctima).
"""
import json
import random

import motor
from escenaris import ESCENARIS
from generador import a_json, prepara

N = 7
SALES = ["cuina", "menjador", "passadis", "porxo", "piscina", "terrassa"]


def pla_i_sales():
    sala = [[-1] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if c == 2:
                k = 2                       # passadís
            elif c < 2:
                k = 0 if r <= 2 else 1      # cuina d'estiu / menjador
            elif r <= 3:
                k = 4 if (r <= 1 and c >= 5) else 3   # piscina / porxo
            else:
                k = 5                       # terrassa
            sala[r][c] = k
    return sala


def main():
    sala = pla_i_sales()
    obj = [[None] * N for _ in range(N)]
    for (r, c), o in {(1, 0): "taula", (5, 0): "taula", (5, 1): "taula", (4, 0): "cadira",
                      (2, 3): "estatua", (2, 6): "planta", (4, 3): "planta"}.items():
        obj[r][c] = o
    bloqueja = {"taula": True, "cadira": False, "estatua": True, "planta": True}
    L = motor.Plantilla(N, [[True] * N for _ in range(N)], sala, obj, bloqueja)
    L.noms_sales = SALES
    # A B C D E F V
    sol = dict(enumerate([(3, 2), (0, 3), (6, 1), (5, 6), (1, 5), (4, 0), (2, 4)]))
    assert len({r for r, _ in sol.values()}) == N and len({c for _, c in sol.values()}) == N
    assert all(L.utilitzable(r, c) for r, c in sol.values())
    sv = L.sala_de(sol[N - 1])
    assassi = [p for p in range(N - 1) if L.sala_de(sol[p]) == sv]
    assert len(assassi) == 1, assassi
    esc = ESCENARIS["estiu"]
    rng = random.Random(7)
    cands = []
    for _ in range(400):
        p = motor.tria_pistes(rng, L, sol, N, list(range(len(SALES))), K=rng.choice([1, 2, 4, 8]))
        if p is None:
            continue
        niv = motor.valora(L, p, N)
        if niv:
            cands.append((niv, len(p), p))
    print("candidats:", len(cands), "nivells:", sorted({c[0] for c in cands}))
    niv, _, pistes = sorted(cands, key=lambda c: (abs(c[0] - 3), c[1]))[0]
    cas = {"n": N, "plantilla": L, "solucio": sol, "pistes": pistes, "nivell": niv,
           "assassi": assassi[0], "sales_ids": list(range(len(SALES)))}
    e = prepara(rng, esc, cas)
    j = a_json(cas, esc, e, rng, "meu-7-1")
    j["nom"] = {"ca": "El crim de la piscina", "fr": "Le crime de la piscine"}
    json.dump([j], open("casos_meu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("nivell", niv, "assassí", j["assassi"], [p["nom"] for p in j["persones"]])
    for t in j["textos"]["ca"]:
        print(" -", t)


if __name__ == "__main__":
    main()
