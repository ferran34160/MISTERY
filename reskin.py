#!/usr/bin/env python3
"""Reparteix els casos ja verificats entre els escenaris (3 per escenari) i en canvia l'aspecte.

La lògica d'un cas (plànol, sales, pistes, solució) no depèn de l'escenari: només hi canvien els
noms de les sales i dels objectes i els seus colors. Cada objecte antic es canvia per un d'únic del
nou escenari que bloqueja igual, així la solució continua sent la mateixa i no cal tornar a verificar.

Ús: python reskin.py verificats.txt sortida.json [preferits.txt]
(assignacions.json recorda quin escenari té cada cas; per fer lloc a casos nous, treu-ne entrades)
(verificats.txt: un identificador de cas per línia)
"""
import glob
import json
import random
import sys
import zlib

from escenaris import ESCENARIS, _OBJ
from textos import descriu

LLETRES = "ABCDEFGHIJ"
PER_ESCENARI = 3


def carrega_pool(ids_ok):
    pool = {}
    for f in sorted(glob.glob("*.json")):
        if f in ("noms.json", "casos_final.json", "assignacions.json", "dificultats.json", "densitat.json", "casos_kpop.json", "casos_meu.json"):
            continue
        for c in json.load(open(f, encoding="utf-8")):
            if c["id"] in ids_ok and c["id"] not in pool:
                pool[c["id"]] = c
    return pool


PER_MIDA = {6: 0.10, 7: 0.15, 8: 0.25, 9: 0.50}      # proporció per mida
PER_NIVELL = {1: 15, 2: 20, 3: 45, 4: 50, 5: 80}      # casos de cada nivell sobre 210
MIN_SALES = 5                                          # i amb 5 o 6 sales
PROVES_DIFICIL = 2     # un cas que el motor valora 5 (cal mirar endavant) és «Difícil» si calen <= 2 proves


def nivell_final(dif, i):
    """Nivell que veu el jugador: el del motor, però el 5 es parteix en 4 (poques proves) i 5 (moltes)."""
    niv, proves = dif[i]
    return 4 if niv == 5 and proves <= PROVES_DIFICIL else niv


def reparteix_enter(total, pesos):
    """Reparteix `total` en parts senceres proporcionals a `pesos` (dict), pel mètode del residu més gran."""
    s = float(sum(pesos.values()))
    base = {k: int(total * v / s) for k, v in pesos.items()}
    resta = sorted(pesos, key=lambda k: -(total * pesos[k] / s - base[k]))
    for k in resta[:total - sum(base.values())]:
        base[k] += 1
    return base


def tria_casos(pool, n_total, fixos=()):
    """Tria n_total casos amb 5 o 6 sales, repartits per mida (PER_MIDA) i per nivell (PER_NIVELL).
    Si d'una mida no hi ha prou casos d'un nivell, s'agafen del nivell que més falta. Els `fixos`
    (ja assignats abans) tenen preferència, perquè no canviï el que el jugador ja coneix."""
    dif = json.load(open("dificultats.json"))
    rng = random.Random(11)
    elig = {i: c for i, c in pool.items() if len(c["sales"]) >= MIN_SALES and i in dif}
    ordre_fix = {i: k for k, i in enumerate(fixos)}
    triats = []
    for n, k in reparteix_enter(n_total, PER_MIDA).items():
        meta = reparteix_enter(k, PER_NIVELL)
        per_niv = {l: [] for l in PER_NIVELL}
        for i, c in elig.items():
            if c["n"] == n:
                per_niv[nivell_final(dif, i)].append(c)
        for l in per_niv:
            rng.shuffle(per_niv[l])
            per_niv[l].sort(key=lambda c: ordre_fix.get(c["id"], 10 ** 9))   # primer els fixos
        agafats = {l: [] for l in PER_NIVELL}
        for l in PER_NIVELL:
            agafats[l] = per_niv[l][:meta[l]]
            per_niv[l] = per_niv[l][meta[l]:]
        while sum(len(v) for v in agafats.values()) < k and any(per_niv.values()):
            # el que falta es reparteix entre els altres nivells segons el seu pes (PER_NIVELL)
            l = min((x for x in PER_NIVELL if per_niv[x]), key=lambda x: (len(agafats[x]) / PER_NIVELL[x], -x))
            agafats[l].append(per_niv[l].pop(0))
        for v in agafats.values():
            triats += v
    triats.sort(key=lambda c: (c["n"], nivell_final(dif, c["id"]), c["id"]))
    return triats[:n_total]


try:
    DENS = json.load(open("densitat.json"))
except (OSError, ValueError):
    DENS = {}


def aplica(c, clau, rng):
    esc = ESCENARIS[clau]
    sales_e = list(esc["sales"].items())
    ks = len(c["sales"])
    n = c["n"]
    if "objectes" not in c:
        from generador import objectes_json
        c["objectes"] = objectes_json(ESCENARIS[c["escenari"]], c["obj"])
    antic = c["objectes"]
    oe = dict(esc["objectes"])
    # on apareix cada objecte antic (sala del cas -> nombre de caselles)
    ubic = {}
    for r in range(n):
        for q in range(n):
            o = c["obj"][r][q]
            if o:
                ubic.setdefault(o, {}).setdefault(c["sala"][r][q], 0)
                ubic[o][c["sala"][r][q]] += 1
    GENERICS = ["taula", "cadira", "banc", "caixa", "bagul", "barril", "escala", "armari", "planta", "tamboret"]

    def prova(rg):
        """Una repartiment de sales i d'objectes; retorna (punts de coherència, triades, mapa, afegits)."""
        triades = rg.sample(sales_e, ks)
        usats, mapa, afegits, punts = set(), {}, {}, 0
        for old in sorted(ubic, key=lambda k: (-sum(ubic[k].values()), rg.random())):
            blk = antic[old]["bloqueja"]

            def sc(k):
                return sum(nc for i, nc in ubic[old].items() if k in triades[i][1]["objs"])
            cand = [k for k in oe if k not in usats and oe[k]["bloqueja"] == blk]
            cand_ok = [k for k in cand if sc(k) > 0]
            if cand_ok:
                k = max(cand_ok, key=lambda k: (sc(k), rg.random()))
            elif cand:
                k = rg.choice(cand)
            else:   # l'escenari no té prou objectes d'aquest tipus: es pren un de genèric
                gen = [x for x in GENERICS if x not in usats and _OBJ[x][4] == blk]
                pool = gen or [x for x in _OBJ if x not in usats and _OBJ[x][4] == blk]
                k = rg.choice(pool)
                afegits[k] = {"bloqueja": blk, "nom": {"ca": (_OBJ[k][1], _OBJ[k][0]), "fr": (_OBJ[k][3], _OBJ[k][2])}}
            usats.add(k)
            mapa[old] = k
            punts += sc(k)
        return punts, triades, mapa, afegits

    millor = None
    for _ in range(250):
        r_ = prova(rng)
        if millor is None or r_[0] > millor[0]:
            millor = r_
        if millor[0] == sum(sum(v.values()) for v in ubic.values()):
            break
    _, triades, mapa, afegits = millor
    oe.update(afegits)
    usats = set(mapa.values())
    c["obj"] = [[mapa[o] if o else None for o in fila] for fila in c["obj"]]
    # objectes de decorat (densitat.json): d'una classe que cap pista no cita, perquè no canviïn la solució
    refs = {mapa[cl["obj"]] for cl in c["pistes"] if "obj" in cl}
    for r, q, b in DENS.get(c["id"], {}).get("extra", []):
        sala_i = c["sala"][r][q]
        cand = [k for k in triades[sala_i][1]["objs"] if k in oe and oe[k]["bloqueja"] == bool(b) and k not in refs]
        if not cand:
            cand = [k for k in oe if oe[k]["bloqueja"] == bool(b) and k not in refs]
        if not cand:
            cand = [k for k in _OBJ if _OBJ[k][4] == bool(b) and k not in refs and k not in oe]
            k = rng.choice(cand)
            oe[k] = {"bloqueja": bool(b), "nom": {"ca": (_OBJ[k][1], _OBJ[k][0]), "fr": (_OBJ[k][3], _OBJ[k][2])}}
        else:
            k = rng.choice(cand)
        c["obj"][r][q] = k
        usats.add(k)
    c["objectes"] = {k: {"bloqueja": oe[k]["bloqueja"],
                         "ca": oe[k]["nom"]["ca"][1],
                         "fr": oe[k]["nom"]["fr"][1]} for k in sorted(usats)}
    c["sales"] = {str(i): {l: triades[i][1]["nom"][l][1] for l in ("ca", "fr")} for i in range(ks)}
    c["escenari"] = clau
    # textos nous
    idx = lambda l: n - 1 if l == "V" else LLETRES.index(l)
    e = dict(esc)
    e["objectes"] = oe
    e["_noms"] = {idx(p["id"]): (p["nom"], p["genere"]) for p in c["persones"]}
    e["_sales"] = {i: triades[i][0] for i in range(ks)}
    pistes = []
    for cl in c["pistes"]:
        d = dict(cl)
        if "p" in d:
            d["p"] = idx(d["p"])
        if "q" in d:
            d["q"] = idx(d["q"])
        if "obj" in d:
            d["obj"] = mapa[d["obj"]]
        pistes.append(d)
    # actualitza també les pistes del JSON (clau d'objecte)
    for cl in c["pistes"]:
        if "obj" in cl:
            cl["obj"] = mapa[cl["obj"]]
    c["textos"] = {l: descriu(l, e, pistes, rng) for l in ("ca", "fr")}
    return c


def id_estable(c, clau):
    """Identificador que no canvia mentre el cas es vegi en el mateix escenari."""
    return "%s-%d-%s" % (clau, c["n"], "%06x" % (zlib.crc32((c["id"] + "|" + clau).encode()) & 0xFFFFFF))


def reparteix(triats, escenaris):
    """Manté l'escenari que ja tenia cada cas (assignacions.json) i col·loca els nous als llocs lliures."""
    try:
        ant = json.load(open("assignacions.json", encoding="utf-8"))
    except (OSError, ValueError):
        ant = {}
    lliures = {e: PER_ESCENARI for e in escenaris}
    asg = {}
    for c in triats:
        e = ant.get(c["id"])
        if e in lliures and lliures[e] > 0:
            asg[c["id"]] = e
            lliures[e] -= 1
    rng0 = random.Random(5)
    ordre = escenaris[:]
    rng0.shuffle(ordre)
    for c in triats:
        if c["id"] in asg:
            continue
        # l'escenari amb més lloc lliure; en empat, l'ordre barrejat
        e = max(ordre, key=lambda x: (lliures[x], -ordre.index(x)))
        asg[c["id"]] = e
        lliures[e] -= 1
    json.dump(asg, open("assignacions.json", "w", encoding="utf-8"), indent=0, sort_keys=True)
    return asg


def main():
    ok = {l.strip() for l in open(sys.argv[1]) if l.strip()}
    pool = carrega_pool(ok)
    escenaris = sorted(e for e in ESCENARIS if not ESCENARIS[e].get("especial"))
    n_total = len(escenaris) * PER_ESCENARI
    try:
        prev = json.load(open("assignacions.json", encoding="utf-8"))
    except (OSError, ValueError):
        prev = {}
    triats = tria_casos(pool, n_total, [i for i in prev if prev[i] in escenaris])
    print(len(pool), "casos verificats;", len(triats), "triats per a", len(escenaris), "escenaris")
    asg = reparteix(triats, escenaris)
    out = []
    for c in triats:
        clau = asg[c["id"]]
        rng = random.Random(zlib.crc32((c["id"] + clau).encode()))
        r = aplica(json.loads(json.dumps(c)), clau, rng)
        r["nivell"] = nivell_final(json.load(open("dificultats.json")), c["id"])
        r["font"] = c["id"]          # identificador de l'estructura (per migrar el progrés antic)
        r["id"] = id_estable(c, clau)
        out.append(r)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(c["escenari"] for c in out).most_common(3), Counter(c["n"] for c in out), Counter(c["nivell"] for c in out))


if __name__ == "__main__":
    main()
