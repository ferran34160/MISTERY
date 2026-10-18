#!/usr/bin/env python3
"""Prova ràpida de tot el flux: genera 3 casos (llavor fixa) i els verifica
de manera independent. Ha de tardar uns minuts.

  python prova.py
"""
import random
import sys

import motor
import verifica
from escenaris import ESCENARIS
from generador import a_json, prepara

rng = random.Random(2026)
esc = ESCENARIS["mas"]
fets = 0
intents = 0
while fets < 3 and intents < 200:
    intents += 1
    cas = motor.genera_cas(rng, esc, n=6, intents=5)
    if cas is None:
        continue
    e = prepara(rng, esc, cas)
    j = a_json(cas, esc, e, rng, f"prova-{fets + 1}")
    n_sol, ok = verifica.comprova(j)
    print(j["id"], "nivell", j["nivell"], "solucions", n_sol, "OK" if ok else "ERROR")
    if not ok:
        sys.exit(1)
    fets += 1
print("Prova superada" if fets == 3 else "No s'han pogut generar 3 casos")
sys.exit(0 if fets == 3 else 1)
