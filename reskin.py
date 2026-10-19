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
        if f in ("noms.json", "casos_final.json", "assignacions.json"):
            continue
        for c in json.load(open(f, encoding="utf-8")):
            if c["id"] in ids_ok and c["id"] not in pool:
                pool[c["id"]] = c
    return pool


def tria_casos(pool, n_total):
    """Tria n_total casos repartits per mida i nivell, i els ordena per mida perquè cada escenari en rebi de diferents."""
    per_mida = {6: 0.42, 7: 0.30, 8: 0.18, 9: 0.10}
    triats = []
    rng = random.Random(11)
    for n, frac in per_mida.items():
        cs = sorted((c for c in pool.values() if c["n"] == n), key=lambda c: (c["nivell"], c["id"]))
        k = min(len(cs), round(n_total * frac))
        # reparteix per nivells: agafa de cada nivell alternativament
        per_niv = {}
        for c in cs:
            per_niv.setdefault(c["nivell"], []).append(c)
        for l in per_niv.values():
            rng.shuffle(l)
        escollits = []
        while len(escollits) < k and any(per_niv.values()):
            for niv in sorted(per_niv):
                if per_niv[niv] and len(escollits) < k:
                    escollits.append(per_niv[niv].pop())
        triats += escollits
    # si falten casos, completa amb el que sobri
    resta = [c for c in pool.values() if c not in triats]
    rng.shuffle(resta)
    triats += resta[:max(0, n_total - len(triats))]
    triats.sort(key=lambda c: (c["n"], c["nivell"], c["id"]))
    return triats[:n_total]


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
    triats = tria_casos(pool, n_total)
    # els casos ja assignats es conserven; si en falten, es treuen els sobrants
    triats_ids = {c["id"] for c in triats}
    fixos = [pool[i] for i in prev if i in pool and prev[i] in escenaris]
    if len(fixos) >= n_total:
        triats = fixos[:n_total]
    else:
        pref = {l.strip() for l in open(sys.argv[3])} if len(sys.argv) > 3 else set()
        nous = [c for c in pool.values() if c["id"] in pref and c["id"] not in prev]
        nous += [c for c in triats if c["id"] not in prev and c["id"] not in pref]
        triats = fixos + nous[:n_total - len(fixos)]
        if len(triats) < n_total:
            triats += [c for c in pool.values() if c not in triats][:n_total - len(triats)]
    triats.sort(key=lambda c: (c["n"], c["nivell"], c["id"]))
    print(len(pool), "casos verificats;", len(triats), "triats per a", len(escenaris), "escenaris")
    asg = reparteix(triats, escenaris)
    out = []
    for c in triats:
        clau = asg[c["id"]]
        rng = random.Random(zlib.crc32((c["id"] + clau).encode()))
        r = aplica(json.loads(json.dumps(c)), clau, rng)
        r["font"] = c["id"]          # identificador de l'estructura (per migrar el progrés antic)
        r["id"] = id_estable(c, clau)
        out.append(r)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(c["escenari"] for c in out).most_common(3), Counter(c["n"] for c in out), Counter(c["nivell"] for c in out))


if __name__ == "__main__":
    main()
