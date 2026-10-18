"""Motor del joc de misteri (graella estil sudoku amb sales i pistes).

Model:
  - Graella n x n amb forats (caselles que no formen part del plànol).
  - Les caselles del plànol es reparteixen en sales (connexes).
  - Algunes caselles tenen un objecte; alguns objectes bloquegen (ningú hi pot
    estar) i d'altres es poden ocupar (una cadira, un carro...).
  - n persones (n-1 sospitosos + la víctima, que és l'última): una per fila i
    una per columna, només en caselles utilitzables.
  - L'assassí és l'únic sospitós que comparteix sala amb la víctima.
  - Cada persona té una pista, i hi ha unes poques pistes generals.

Aquest fitxer no depèn de cap idioma: les pistes són dades estructurades
(diccionaris) i els textos es generen a part (textos.py).
"""
import random
from collections import deque
from itertools import combinations

DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

TIPUS_UNARIS = {"en_sala", "no_en_sala", "sobre_obj", "prop_obj", "raco", "vora",
                "fila_obj", "col_obj"}
TIPUS_BINARIS = {"costat", "nord", "sud", "est", "oest", "diag", "cavall",
                 "mateixa_sala", "altra_sala"}
TIPUS_GLOBALS = {"sol", "sol_amb", "compte_sala", "victima"}
REGLA = {"t": "victima"}   # regla implícita: l'assassí és l'únic sospitós a la sala de la víctima



class Plantilla:
    def __init__(self, n, pla, sala, obj, bloqueja):
        self.n = n
        self.pla = pla          # pla[r][c] -> bool (forma part del plànol)
        self.sala = sala        # sala[r][c] -> índex de sala o -1
        self.obj = obj          # obj[r][c] -> clau d'objecte o None
        self.bloqueja = bloqueja  # clau d'objecte -> bool
        self.cel = [(r, c) for r in range(n) for c in range(n)
                    if self.utilitzable(r, c)]

    def utilitzable(self, r, c):
        if not self.pla[r][c]:
            return False
        o = self.obj[r][c]
        return o is None or not self.bloqueja[o]

    def sala_de(self, c):
        return self.sala[c[0]][c[1]]

    def obj_de(self, c):
        return self.obj[c[0]][c[1]]

    def dins(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.n and self.pla[r][c]

    def mur(self, r, c, dr, dc):
        """Hi ha paret (o buit) en aquesta direcció respecte de la sala?"""
        nr, nc = r + dr, c + dc
        return (not self.dins(nr, nc)) or self.sala[nr][nc] != self.sala[r][c]


# ---------------------------------------------------------------- pistes

def compleix(L, cl, pos, n):
    """Cert si la pista no queda *definitivament* violada per la col·locació
    parcial `pos` (persona -> casella). Amb la col·locació completa és exacte."""
    t = cl["t"]
    if t == "compte_sala":
        tot = sum(1 for c in pos.values() if L.sala_de(c) == cl["sala"])
        if tot > cl["k"]:
            return False
        return tot == cl["k"] if len(pos) == n else True
    if t == "victima":
        v = pos.get(n - 1)
        if v is None:
            return True
        R = L.sala_de(v)
        tot = sum(1 for x, c in pos.items() if x != n - 1 and L.sala_de(c) == R)
        if tot > 1:
            return False
        return tot == 1 if len(pos) == n else True
    p = cl["p"]
    if t == "sol":
        a = pos.get(p)
        if a is None:
            return True
        R = L.sala_de(a)
        return not any(x != p and L.sala_de(c) == R for x, c in pos.items())
    if t == "sol_amb":
        q = cl["q"]
        a, b = pos.get(p), pos.get(q)
        if a is not None and b is not None and L.sala_de(a) != L.sala_de(b):
            return False
        for x, c in pos.items():
            if x == p or x == q:
                continue
            R = L.sala_de(c)
            if (a is not None and L.sala_de(a) == R) or \
               (b is not None and L.sala_de(b) == R):
                return False
        return True
    a = pos.get(p)
    if a is None:
        return True
    r, c = a
    if t == "en_sala":
        return L.sala_de(a) == cl["sala"]
    if t == "no_en_sala":
        return L.sala_de(a) != cl["sala"]
    if t == "sobre_obj":
        return L.obj_de(a) == cl["obj"]
    if t == "prop_obj":
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if L.dins(nr, nc) and L.sala[nr][nc] == L.sala[r][c] \
               and L.obj[nr][nc] == cl["obj"]:
                return True
        return False
    if t == "raco":
        return (L.mur(r, c, -1, 0) or L.mur(r, c, 1, 0)) and \
               (L.mur(r, c, 0, -1) or L.mur(r, c, 0, 1))
    if t == "vora":
        return any(not L.dins(r + dr, c + dc) for dr, dc in DIR4)
    if t in ("fila_obj", "col_obj"):
        k = 0 if t == "fila_obj" else 1
        return any(L.obj[i][j] == cl["obj"] and (i, j)[k] == a[k] and (i, j) != a
                   for i in range(L.n) for j in range(L.n))
    q = cl["q"]
    b = pos.get(q)
    if b is None:
        return True
    dr, dc = abs(a[0] - b[0]), abs(a[1] - b[1])
    if t == "costat":
        return dr + dc == 1 and L.sala_de(a) == L.sala_de(b)
    if t == "nord":
        return a[0] < b[0]
    if t == "sud":
        return a[0] > b[0]
    if t == "est":
        return a[1] > b[1]
    if t == "oest":
        return a[1] < b[1]
    if t == "diag":
        return dr == dc and dr != 0
    if t == "cavall":
        return sorted((dr, dc)) == [1, 2]
    if t == "mateixa_sala":
        return L.sala_de(a) == L.sala_de(b)
    if t == "altra_sala":
        return L.sala_de(a) != L.sala_de(b)
    raise ValueError(t)


def _afecta(cl, p):
    return cl["t"] in TIPUS_GLOBALS or p == cl.get("p") or p == cl.get("q")


# ------------------------------------------------------------ solucionador

def dominis_inicials(L, pistes, n):
    dom = {p: list(L.cel) for p in range(n)}
    for cl in pistes:
        if cl["t"] in TIPUS_UNARIS:
            p = cl["p"]
            dom[p] = [c for c in dom[p] if compleix(L, cl, {p: c}, n)]
    return dom


def comptar(L, pistes, n, limit=2):
    """Nombre de solucions (parat a `limit`)."""
    pistes = list(pistes) + [REGLA]
    dom = dominis_inicials(L, pistes, n)
    if any(not d for d in dom.values()):
        return 0
    rel = {p: [cl for cl in pistes
               if cl["t"] not in TIPUS_UNARIS and _afecta(cl, p)]
           for p in range(n)}
    # Propagació prèvia (deduccions vàlides per a totes les solucions): redueix
    # molt la cerca. Si es contradiu, no hi ha cap solució.
    try:
        _estabilitza(L, pistes, dom, n, 2, [1])
    except Contradiccio:
        return 0
    pos = {}
    usf, usc = set(), set()
    cnt = 0

    def rec():
        nonlocal cnt
        if cnt >= limit:
            return
        if len(pos) == n:
            cnt += 1
            return
        # variable més restringida (menys caselles lliures de fila/columna)
        millor, opcions = None, None
        for p in range(n):
            if p in pos:
                continue
            ops = [c for c in dom[p] if c[0] not in usf and c[1] not in usc]
            if not ops:
                return
            if opcions is None or len(ops) < len(opcions):
                millor, opcions = p, ops
                if len(ops) == 1:
                    break
        p = millor
        for c in opcions:
            pos[p] = c
            if all(compleix(L, cl, pos, n) for cl in rel[p]):
                usf.add(c[0])
                usc.add(c[1])
                rec()
                usf.discard(c[0])
                usc.discard(c[1])
            del pos[p]
            if cnt >= limit:
                return

    rec()
    return cnt


def solucions(L, pistes, n, limit=10):
    """Com `comptar` però retorna les solucions (llista de dicts)."""
    pistes = list(pistes) + [REGLA]
    dom = dominis_inicials(L, pistes, n)
    out = []
    if any(not d for d in dom.values()):
        return out
    rel = {p: [cl for cl in pistes
               if cl["t"] not in TIPUS_UNARIS and _afecta(cl, p)]
           for p in range(n)}
    ordre = sorted(range(n), key=lambda p: len(dom[p]))
    pos = {}
    usf, usc = set(), set()

    def rec(i):
        if len(out) >= limit:
            return
        if i == n:
            out.append(dict(pos))
            return
        p = ordre[i]
        for c in dom[p]:
            if c[0] in usf or c[1] in usc:
                continue
            pos[p] = c
            if all(compleix(L, cl, pos, n) for cl in rel[p]):
                usf.add(c[0])
                usc.add(c[1])
                rec(i + 1)
                usf.discard(c[0])
                usc.discard(c[1])
            del pos[p]

    rec(0)
    return out


# ------------------------------------------------- valoració (tècniques humanes)

class Contradiccio(Exception):
    pass


def _suport(L, cl, dom, n):
    """Filtra dominis amb les pistes binàries (consistència d'arc)."""
    p, q = cl["p"], cl["q"]
    canvi = False
    for a, b, swap in ((p, q, False), (q, p, True)):
        nou = []
        for c in dom[a]:
            ok = False
            for d in dom[b]:
                if c[0] == d[0] or c[1] == d[1]:
                    continue
                pos = {p: d, q: c} if swap else {p: c, q: d}
                if compleix(L, cl, pos, n):
                    ok = True
                    break
            if ok:
                nou.append(c)
        if len(nou) != len(dom[a]):
            dom[a] = nou
            canvi = True
        if not dom[a]:
            raise Contradiccio
    return canvi


def _sales_segures(L, dom, x):
    s = {L.sala_de(c) for c in dom[x]}
    return s


def _treu_sala(L, dom, R, excepte):
    canvi = False
    for x in dom:
        if x in excepte:
            continue
        nou = [c for c in dom[x] if L.sala_de(c) != R]
        if len(nou) != len(dom[x]):
            dom[x] = nou
            canvi = True
            if not nou:
                raise Contradiccio
    return canvi


def _prop_pistes(L, pistes, dom, n):
    canvi = False
    for cl in pistes:
        t = cl["t"]
        if t in TIPUS_BINARIS:
            canvi |= _suport(L, cl, dom, n)
        elif t == "sol":
            p = cl["p"]
            nou = []
            for c in dom[p]:
                R = L.sala_de(c)
                if any(x != p and _sales_segures(L, dom, x) == {R} for x in dom):
                    continue
                nou.append(c)
            if len(nou) != len(dom[p]):
                dom[p] = nou
                canvi = True
                if not nou:
                    raise Contradiccio
            s = _sales_segures(L, dom, p)
            if len(s) == 1:
                canvi |= _treu_sala(L, dom, next(iter(s)), {p})
        elif t == "sol_amb":
            p, q = cl["p"], cl["q"]
            canvi |= _suport(L, {"t": "mateixa_sala", "p": p, "q": q}, dom, n)
            for a in (p, q):
                nou = []
                for c in dom[a]:
                    R = L.sala_de(c)
                    if any(x not in (p, q) and _sales_segures(L, dom, x) == {R}
                           for x in dom):
                        continue
                    nou.append(c)
                if len(nou) != len(dom[a]):
                    dom[a] = nou
                    canvi = True
                    if not nou:
                        raise Contradiccio
            s = _sales_segures(L, dom, p) & _sales_segures(L, dom, q)
            if len(s) == 1:
                canvi |= _treu_sala(L, dom, next(iter(s)), {p, q})
        elif t == "victima":
            v = n - 1
            nou = []
            for c in dom[v]:
                R = L.sala_de(c)
                segurs = [x for x in dom if x != v and _sales_segures(L, dom, x) == {R}]
                possibles = [x for x in dom if x != v and R in _sales_segures(L, dom, x)]
                if len(segurs) > 1 or not possibles:
                    continue
                nou.append(c)
            if len(nou) != len(dom[v]):
                dom[v] = nou
                canvi = True
                if not nou:
                    raise Contradiccio
            sv = _sales_segures(L, dom, v)
            if len(sv) == 1:
                R = next(iter(sv))
                segurs = [x for x in dom if x != v and _sales_segures(L, dom, x) == {R}]
                possibles = [x for x in dom if x != v and R in _sales_segures(L, dom, x)]
                if len(segurs) == 1:
                    canvi |= _treu_sala(L, dom, R, {v, segurs[0]})
                if len(possibles) == 1:
                    x = possibles[0]
                    nn = [c for c in dom[x] if L.sala_de(c) == R]
                    if len(nn) != len(dom[x]):
                        dom[x] = nn
                        canvi = True
        elif t == "compte_sala":
            R, k = cl["sala"], cl["k"]
            segurs = [x for x in dom if _sales_segures(L, dom, x) == {R}]
            possibles = [x for x in dom if R in _sales_segures(L, dom, x)]
            if len(segurs) > k or len(possibles) < k:
                raise Contradiccio
            if len(segurs) == k:
                canvi |= _treu_sala(L, dom, R, set(segurs))
            if len(possibles) == k:
                for x in possibles:
                    nou = [c for c in dom[x] if L.sala_de(c) == R]
                    if len(nou) != len(dom[x]):
                        dom[x] = nou
                        canvi = True
    return canvi


def _unics_nus(L, dom, n):
    canvi = False
    for p in list(dom):
        if len(dom[p]) == 1:
            r, c = dom[p][0]
            for x in dom:
                if x == p:
                    continue
                nou = [d for d in dom[x] if d[0] != r and d[1] != c]
                if len(nou) != len(dom[x]):
                    dom[x] = nou
                    canvi = True
                    if not nou:
                        raise Contradiccio
    return canvi


def _unic_linia(L, dom, n):
    """Una fila/columna on només una persona pot ser-hi: hi ha de ser."""
    canvi = False
    for eix in (0, 1):
        for k in range(n):
            qui = [x for x in dom if any(c[eix] == k for c in dom[x])]
            if not qui:   # n persones i n files: cada fila n'ha de tenir una
                raise Contradiccio
            if len(qui) == 1:
                x = qui[0]
                nou = [c for c in dom[x] if c[eix] == k]
                if len(nou) != len(dom[x]):
                    dom[x] = nou
                    canvi = True
    return canvi


def _hall(L, dom, n, k):
    """Subconjunts nus i amagats de mida k per files i columnes."""
    canvi = False
    pers = list(dom)
    for eix in (0, 1):
        for S in combinations(pers, k):
            linies = {c[eix] for x in S for c in dom[x]}
            if len(linies) < k:
                raise Contradiccio
            if len(linies) == k:
                for x in pers:
                    if x in S:
                        continue
                    nou = [c for c in dom[x] if c[eix] not in linies]
                    if len(nou) != len(dom[x]):
                        dom[x] = nou
                        canvi = True
                        if not nou:
                            raise Contradiccio
        for Ls in combinations(range(n), k):
            aqui = [x for x in pers if any(c[eix] in Ls for c in dom[x])]
            if len(aqui) < k:
                raise Contradiccio
            if len(aqui) == k:
                for x in aqui:
                    nou = [c for c in dom[x] if c[eix] in Ls]
                    if len(nou) != len(dom[x]):
                        dom[x] = nou
                        canvi = True
    return canvi


def _interseccio(L, dom, n):
    """Si totes les caselles possibles de p són alineades amb x, ningú més hi pot ser."""
    canvi = False
    for p in dom:
        if len(dom[p]) < 2:
            continue
        for x in L.cel:
            if all(d[0] == x[0] or d[1] == x[1] for d in dom[p]):
                for q in dom:
                    if q != p and x in dom[q]:
                        dom[q] = [d for d in dom[q] if d != x]
                        canvi = True
                        if not dom[q]:
                            raise Contradiccio
    return canvi


def _tier(nivell, L, pistes, dom, n):
    if nivell == 1:
        a = _prop_pistes(L, pistes, dom, n)
        b = _unics_nus(L, dom, n)
        return a or b
    if nivell == 2:
        return _unic_linia(L, dom, n)
    if nivell == 3:
        return _hall(L, dom, n, 2)
    if nivell == 4:
        a = _interseccio(L, dom, n)
        b = _hall(L, dom, n, 3)
        c = _hall(L, dom, n, 4) if n >= 8 else False
        return a or b or c
    raise ValueError(nivell)


def _estabilitza(L, pistes, dom, n, maxn, usat):
    """Aplica tècniques fins a `maxn`; retorna cert si ha canviat alguna cosa."""
    algun = False
    while True:
        for nv in range(1, maxn + 1):
            if _tier(nv, L, pistes, dom, n):
                usat[0] = max(usat[0], nv)
                algun = True
                break
        else:
            return algun


def valora(L, pistes, n):
    """Retorna el nivell de dificultat (1-5) o None si no es resol per deducció.
    1 consistència de pistes + únic nu; 2 + fila/columna amb una sola opció;
    3 + parelles sobrecarregades; 4 + interseccions i trios; 5 cal mirar endavant."""
    pistes = list(pistes) + [REGLA]
    dom = dominis_inicials(L, pistes, n)
    usat = [1]
    try:
        _estabilitza(L, pistes, dom, n, 4, usat)
        while any(len(d) > 1 for d in dom.values()):
            progres = False
            for p in sorted(dom, key=lambda x: len(dom[x])):
                if len(dom[p]) < 2:
                    continue
                for c in list(dom[p]):
                    prova = {x: list(d) for x, d in dom.items()}
                    prova[p] = [c]
                    try:
                        _estabilitza(L, pistes, prova, n, 4, [1])
                    except Contradiccio:
                        dom[p].remove(c)
                        progres = True
                        usat[0] = 5
                        _estabilitza(L, pistes, dom, n, 4, [0])
                        break
                if progres:
                    break
            if not progres:
                return None
    except Contradiccio:
        return None
    if any(len(d) != 1 for d in dom.values()):
        return None
    return usat[0] if usat[0] > 1 else 1


# ------------------------------------------------------------- generació

def _connex(pla, n):
    cel = [(r, c) for r in range(n) for c in range(n) if pla[r][c]]
    if not cel:
        return False
    vist = {cel[0]}
    cua = deque([cel[0]])
    while cua:
        r, c = cua.popleft()
        for dr, dc in DIR4:
            nx = (r + dr, c + dc)
            if 0 <= nx[0] < n and 0 <= nx[1] < n and pla[nx[0]][nx[1]] \
               and nx not in vist:
                vist.add(nx)
                cua.append(nx)
    return len(vist) == len(cel)


def crea_plantilla(rng, esc, n, k_sales):
    """Plànol aleatori: forats a les cantonades, sales connexes, objectes."""
    bloqueja = {k: v["bloqueja"] for k, v in esc["objectes"].items()}
    for _ in range(500):
        pla = [[True] * n for _ in range(n)]
        for (r0, c0, sr, sc) in ((0, 0, 1, 1), (0, n - 1, 1, -1),
                                 (n - 1, 0, -1, 1), (n - 1, n - 1, -1, -1)):
            if rng.random() < 0.55:
                a, b = rng.choice([1, 1, 2]), rng.choice([1, 2, 2])
                for i in range(a):
                    for j in range(b):
                        pla[r0 + sr * i][c0 + sc * j] = False
        if any(sum(pla[r]) < 3 for r in range(n)) or \
           any(sum(pla[r][c] for r in range(n)) < 3 for c in range(n)):
            continue
        if not _connex(pla, n):
            continue
        cel = [(r, c) for r in range(n) for c in range(n) if pla[r][c]]
        if len(cel) < 3 * k_sales:
            continue
        # sales per creixement de regions
        llavors = rng.sample(cel, k_sales)
        sala = [[-1] * n for _ in range(n)]
        mida = [1] * k_sales
        for i, (r, c) in enumerate(llavors):
            sala[r][c] = i
        lliures = len(cel) - k_sales
        while lliures:
            ordre = sorted(range(k_sales), key=lambda i: mida[i] + rng.random() * 3)
            fet = False
            for i in ordre:
                front = []
                for r, c in cel:
                    if sala[r][c] != i:
                        continue
                    for dr, dc in DIR4:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and pla[nr][nc] \
                           and sala[nr][nc] == -1:
                            front.append((nr, nc))
                if front:
                    nr, nc = rng.choice(front)
                    sala[nr][nc] = i
                    mida[i] += 1
                    lliures -= 1
                    fet = True
                    break
            if not fet:
                break
        if lliures or min(mida) < 3 or max(mida) > 0.45 * len(cel):
            continue
        # assigna sales de l'escenari i posa objectes
        noms = rng.sample(list(esc["sales"]), k_sales)
        obj = [[None] * n for _ in range(n)]
        for i in range(k_sales):
            dins = [(r, c) for r, c in cel if sala[r][c] == i]
            quant = rng.randint(1, min(3, max(1, len(dins) // 3)))
            for pos in rng.sample(dins, quant):
                obj[pos[0]][pos[1]] = rng.choice(esc["sales"][noms[i]]["objs"])
        L = Plantilla(n, pla, sala, obj, bloqueja)
        if any(sum(1 for c in range(n) if L.utilitzable(r, c)) < 2 for r in range(n)):
            continue
        if any(sum(1 for r in range(n) if L.utilitzable(r, c)) < 2 for c in range(n)):
            continue
        L.noms_sales = noms
        return L
    return None


def mostra_solucio(rng, L, n):
    """Una col·locació vàlida (persona -> casella) amb exactament un sospitós
    a la sala de la víctima (la víctima és la persona n-1)."""
    for _ in range(400):
        cols = []
        usades = set()

        def rec(r):
            if r == n:
                return True
            opcions = [c for c in range(n) if c not in usades and L.utilitzable(r, c)]
            rng.shuffle(opcions)
            for c in opcions:
                usades.add(c)
                cols.append(c)
                if rec(r + 1):
                    return True
                cols.pop()
                usades.discard(c)
            return False

        if not rec(0):
            return None
        persones = list(range(n))
        rng.shuffle(persones)
        sol = {p: (r, cols[r]) for r, p in enumerate(persones)}
        sv = L.sala_de(sol[n - 1])
        dins = [p for p in range(n - 1) if L.sala_de(sol[p]) == sv]
        if len(dins) == 1:
            return sol
    return None


def candidates(L, sol, n, sales_ids):
    """Totes les pistes vertaderes per a la solució `sol`:
    (per persona, generals)."""
    per_p = {p: [] for p in range(n)}
    objs_presents = {o for row in L.obj for o in row if o}
    for p in range(n):
        a = sol[p]
        sala = L.sala_de(a)
        for R in sales_ids:
            if R == sala:
                per_p[p].append({"t": "en_sala", "p": p, "sala": R})
            else:
                per_p[p].append({"t": "no_en_sala", "p": p, "sala": R})
        o = L.obj_de(a)
        if o and not L.bloqueja[o]:
            per_p[p].append({"t": "sobre_obj", "p": p, "obj": o})
        for o in objs_presents:
            cl = {"t": "prop_obj", "p": p, "obj": o}
            if compleix(L, cl, {p: a}, n):
                per_p[p].append(cl)
        for t in ("raco", "vora"):
            cl = {"t": t, "p": p}
            if compleix(L, cl, {p: a}, n):
                per_p[p].append(cl)
        for t in ("fila_obj", "col_obj"):
            for o in objs_presents:
                cl = {"t": t, "p": p, "obj": o}
                if compleix(L, cl, {p: a}, n):
                    per_p[p].append(cl)
        if p != n - 1 and sum(1 for x in range(n) if x != p
                              and L.sala_de(sol[x]) == sala) == 0:
            per_p[p].append({"t": "sol", "p": p})
        for q in range(n):
            if q == p:
                continue
            b = sol[q]
            for t in ("costat", "nord", "sud", "est", "oest", "diag", "cavall",
                      "mateixa_sala", "altra_sala"):
                cl = {"t": t, "p": p, "q": q}
                if not compleix(L, cl, {p: a, q: b}, n):
                    continue
                # no regalar l'assassí directament
                if q == n - 1 or p == n - 1:
                    if t in ("costat", "mateixa_sala"):
                        continue
                per_p[p].append(cl)
            if q > p and p != n - 1 and q != n - 1:
                cl = {"t": "sol_amb", "p": p, "q": q}
                if compleix(L, cl, sol, n):
                    per_p[p].append(cl)
    generals = []
    for R in sales_ids:
        k = sum(1 for p in range(n) if L.sala_de(sol[p]) == R)
        generals.append({"t": "compte_sala", "sala": R, "k": k})
    return per_p, generals


def _puntua(L, pistes, n):
    "Mida total dels dominis després de propagar (més petit = pista més útil)."
    ps = list(pistes) + [REGLA]
    dom = dominis_inicials(L, ps, n)
    try:
        _estabilitza(L, ps, dom, n, 2, [1])
    except Contradiccio:
        return 10 ** 9
    return sum(len(d) for d in dom.values())


def tria_pistes(rng, L, sol, n, sales_ids, K=8, CAP=150, max_extra=None):
    """Una pista per persona (la que més redueix les solucions entre K
    candidates, triant també quina persona) i, si cal, fins a `max_extra`
    pistes més (generals o segones pistes). Després treu les redundants."""
    if max_extra is None:
        max_extra = n
    per_p, generals = candidates(L, sol, n, sales_ids)
    if any(not v for v in per_p.values()):
        return None
    pistes = []
    sense = set(range(n))
    unic = False
    while sense:
        mostra = []
        for _ in range(K):
            p = rng.choice(sorted(sense))
            mostra.append(rng.choice(per_p[p]))
        if unic:
            millor = mostra[0]
        else:
            millor = min(mostra, key=lambda c: _puntua(L, pistes + [c], n))
        pistes.append(millor)
        sense.discard(millor["p"])
        if not unic and comptar(L, pistes, n, 2) == 1:
            unic = True
    extra = 0
    while not unic and extra < max_extra:
        pool = generals + [c for p in range(n) for c in rng.sample(per_p[p], min(3, len(per_p[p])))]
        mostra = rng.sample(pool, min(K * 2, len(pool)))
        millor = min(mostra, key=lambda c: _puntua(L, pistes + [c], n))
        pistes.append(millor)
        extra += 1
        if comptar(L, pistes, n, 2) == 1:
            unic = True
    if not unic:
        return None
    # treu les pistes redundants que no siguin l'única de la seva persona
    ordre = list(pistes)
    rng.shuffle(ordre)
    for cl in ordre:
        if cl["t"] != "compte_sala" and \
           sum(1 for c in pistes if c.get("p") == cl["p"]) < 2:
            continue
        resta = [c for c in pistes if c is not cl]
        if comptar(L, resta, n, 2) == 1:
            pistes = resta
    return pistes


def genera_cas(rng, esc, n=6, k_sales=None, K=None, intents=60):
    """Retorna un diccionari amb el cas, o None si no s'ha trobat."""
    for _ in range(intents):
        ks = k_sales or rng.choice([3, 4, 4, 5] if n <= 7 else [4, 5, 5, 6])
        L = crea_plantilla(rng, esc, n, ks)
        if L is None:
            continue
        sol = mostra_solucio(rng, L, n)
        if sol is None:
            continue
        sales_ids = list(range(ks))
        pistes = tria_pistes(rng, L, sol, n, sales_ids,
                             K=K or rng.choice([1, 2, 4, 8]))
        if pistes is None:
            continue
        niv = valora(L, pistes, n)
        if niv is None:
            continue
        sv = L.sala_de(sol[n - 1])
        assassi = next(p for p in range(n - 1) if L.sala_de(sol[p]) == sv)
        return {"n": n, "plantilla": L, "solucio": sol, "pistes": pistes,
                "nivell": niv, "assassi": assassi, "sales_ids": sales_ids}
    return None
