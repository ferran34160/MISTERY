#!/usr/bin/env python3
"""Reuneix fitxers de casos en JSON i crea casos.js per a la pàgina (index.html).

Afegeix el camp "objectes" als casos antics que no el tenen.
Ús: python construeix.py casos_prova.json casos_n3.json
"""
import json
import os
import random
import zlib
import sys

from escenaris import ESCENARIS
from generador import objectes_json
from textos import intro


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
        ("escala", "f", "échelle", "f")],
    "vaixell": [("àncora", "f", "ancre", "f"),
        ("timó", "m", "barre", "f"),
        ("bandera", "f", "drapeau", "m"),
        ("brúixola", "f", "boussole", "f"),
        ("mapa", "m", "carte", "f"),
        ("vela", "f", "voile", "f"),
        ("rem", "m", "rame", "f"),
        ("tempesta", "f", "tempête", "f"),
        ("cordam", "m", "cordage", "m"),
        ("cabina", "f", "cabine", "f"),
        ("farola", "f", "lanterne", "f"),
        ("bitàcola", "f", "journal", "m")],
    "hotel": [("clau", "f", "clé", "f"),
        ("maleta", "f", "valise", "f"),
        ("recepció", "f", "réception", "f"),
        ("ascensor", "m", "ascenseur", "m"),
        ("llit", "m", "lit", "m"),
        ("timbre", "m", "sonnette", "f"),
        ("passadís", "m", "couloir", "m"),
        ("catifa", "f", "tapis", "m"),
        ("registre", "m", "registre", "m"),
        ("convidat", "m", "invité", "m"),
        ("porter", "m", "portier", "m"),
        ("botons", "m", "groom", "m")],
    "museu": [("estàtua", "f", "statue", "f"),
        ("quadre", "m", "tableau", "m"),
        ("vitrina", "f", "vitrine", "f"),
        ("mòmia", "f", "momie", "f"),
        ("retrat", "m", "portrait", "m"),
        ("escultura", "f", "sculpture", "f"),
        ("pergamí", "m", "parchemin", "m"),
        ("joia", "f", "bijou", "m"),
        ("catàleg", "m", "catalogue", "m"),
        ("marc", "m", "cadre", "m"),
        ("mosaic", "m", "mosaïque", "f"),
        ("vas", "m", "vase", "m")],
    "castell": [("tron", "m", "trône", "m"),
        ("torre", "f", "tour", "f"),
        ("corona", "f", "couronne", "f"),
        ("espasa", "f", "épée", "f"),
        ("calabós", "m", "cachot", "m"),
        ("armadura", "f", "armure", "f"),
        ("torxa", "f", "torche", "f"),
        ("escut", "m", "écu", "m"),
        ("dama", "f", "dame", "f"),
        ("corn", "m", "cor", "m"),
        ("estendard", "m", "étendard", "m"),
        ("llegenda", "f", "légende", "f")],
    "escola": [("pissarra", "f", "tableau", "m"),
        ("pupitre", "m", "pupitre", "m"),
        ("timbre", "m", "sonnerie", "f"),
        ("llibre", "m", "livre", "m"),
        ("pilota", "f", "ballon", "m"),
        ("examen", "m", "examen", "m"),
        ("cartera", "f", "cartable", "m"),
        ("mestra", "f", "maîtresse", "f"),
        ("guix", "m", "craie", "f"),
        ("campana", "f", "cloche", "f"),
        ("deures", "m", "devoirs", "m"),
        ("recreació", "f", "récréation", "f")],
    "restaurant": [("menú", "m", "menu", "m"),
        ("cuiner", "m", "cuisinier", "m"),
        ("copa", "f", "verre", "m"),
        ("ganivet", "m", "couteau", "m"),
        ("forquilla", "f", "fourchette", "f"),
        ("sopa", "f", "soupe", "f"),
        ("compte", "m", "addition", "f"),
        ("cambrer", "m", "serveur", "m"),
        ("plat", "m", "plat", "m"),
        ("vi", "m", "vin", "m"),
        ("postre", "m", "dessert", "m"),
        ("reserva", "f", "réservation", "f")],
    "circ": [("carpa", "f", "tente", "f"),
        ("pallasso", "m", "clown", "m"),
        ("trapezi", "m", "trapèze", "m"),
        ("domador", "m", "dompteur", "m"),
        ("lleó", "m", "lion", "m"),
        ("equilibrista", "f", "équilibriste", "f"),
        ("bola", "f", "boule", "f"),
        ("aplaudiment", "m", "applaudissement", "m"),
        ("funàmbul", "m", "funambule", "m"),
        ("mag", "m", "magicien", "m"),
        ("tambor", "m", "tambour", "m"),
        ("cartell", "m", "affiche", "f")],
    "mansio": [("pianista", "f", "pianiste", "f"),
        ("majordom", "m", "majordome", "m"),
        ("testament", "m", "testament", "m"),
        ("retrat", "m", "portrait", "m"),
        ("cortina", "f", "rideau", "m"),
        ("copa", "f", "coupe", "f"),
        ("hereu", "m", "héritier", "m"),
        ("espelma", "f", "bougie", "f"),
        ("carta", "f", "lettre", "f"),
        ("rellotge", "m", "horloge", "f"),
        ("escala", "f", "escalier", "m"),
        ("candelabre", "m", "candélabre", "m")],
    "mercat": [("parada", "f", "étal", "m"),
        ("cistell", "m", "panier", "m"),
        ("balança", "f", "balance", "f"),
        ("fruita", "f", "fruit", "m"),
        ("peix", "m", "poisson", "m"),
        ("pregó", "m", "annonce", "f"),
        ("moneda", "f", "pièce", "f"),
        ("carretó", "m", "chariot", "m"),
        ("tomàquet", "m", "tomate", "f"),
        ("formatge", "m", "fromage", "m"),
        ("pa", "m", "pain", "m"),
        ("mercader", "m", "marchand", "m")]}
ADJ = [("mut", "muda", "muet", "muette"), ("trencat", "trencada", "brisé", "brisée"),
       ("perdut", "perduda", "perdu", "perdue"), ("llunyà", "llunyana", "lointain", "lointaine"),
       ("fosc", "fosca", "sombre", "sombre"), ("amagat", "amagada", "caché", "cachée"),
       ("tardà", "tardana", "tardif", "tardive"), ("buit", "buida", "vide", "vide")]


def noms_de(esc):
    """Substantius (ca, gènere ca, fr, gènere fr) que surten a l'escenari: objectes i sales."""
    e = ESCENARIS[esc]
    out = []
    for o in e["objectes"].values():
        out.append((o["nom"]["ca"][1], o["nom"]["ca"][0], o["nom"]["fr"][1], o["nom"]["fr"][0]))
    for s in e["sales"].values():
        out.append((s["nom"]["ca"][1], s["nom"]["ca"][0], s["nom"]["fr"][1], s["nom"]["fr"][0]))
    return list(dict.fromkeys(out))


def assigna_noms(casos):
    """Assigna un nom estable a cada cas (guardat a noms.json, per id), propi del seu escenari."""
    try:
        with open("noms.json", encoding="utf-8") as fh:
            noms = json.load(fh)
    except FileNotFoundError:
        noms = {}
    usats = {v["ca"] for v in noms.values()}
    lliures = {}
    for c in casos:
        esc = c["escenari"]
        if c["id"] in noms or esc in lliures:
            continue
        llista = noms_de(esc)
        combos = [(llista[a], b) for b in range(len(ADJ)) for a in range(len(llista))]
        random.Random(zlib.crc32(esc.encode())).shuffle(combos)
        lliures[esc] = iter(k for k in combos if titol(*k)["ca"] not in usats)
    for c in casos:
        if c["id"] not in noms:
            n = titol(*next(lliures[c["escenari"]]))
            usats.add(n["ca"])
            noms[c["id"]] = n
        c["nom"] = noms[c["id"]]
    with open("noms.json", "w", encoding="utf-8") as fh:
        json.dump(noms, fh, ensure_ascii=False, indent=0)


def titol(nom, j):
    ca, gca, fr, gfr = nom
    a = ADJ[j]
    art_ca = "El " if gca == "m" else "La "
    if ca[0] in "aeiouàèéíòóúh":
        art_ca = "L'"
    art_fr = "Le " if gfr == "m" else "La "
    if fr[0] in "aeiouéèh":
        art_fr = "L'"
    return {"ca": art_ca + ca + " " + (a[0] if gca == "m" else a[1]),
            "fr": art_fr + fr + " " + (a[2] if gfr == "m" else a[3])}


KPOP_NOMS = {"rumi": "Rumi", "mira": "Mira", "zoey": "Zoey", "jinu": "Jinu", "abby": "Abby", "baby": "Baby",
             "mystery": "Mystery", "romance": "Romance", "bobby": "Bobby", "gwima": "Gwi-Ma", "derpy": "Derpy",
             "sussie": "Sussie"}


def fotos_kpop():
    """JS que afegeix els retrats i objectes K-pop a PHOTOS/OBJIMG (només si hi ha la carpeta kpop/, que no es puja a git)."""
    arrel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpop")
    dr, do = os.path.join(arrel, "retrats"), os.path.join(arrel, "objectes")
    if not os.path.isdir(dr):
        return ""
    m = {KPOP_NOMS[f[:-4]]: "kpop/retrats/" + f for f in sorted(os.listdir(dr)) if f[:-4] in KPOP_NOMS}
    js = "Object.assign(PHOTOS," + json.dumps(m) + ");"
    if os.path.isdir(do):
        o = {f[:-4]: "kpop/objectes/" + f for f in sorted(os.listdir(do)) if f.endswith(".png")}
        js += "Object.assign(OBJIMG," + json.dumps(o) + ");"
    return js


def config_classificacio():
    """ranking_config.js (al repositori) + ranking_secret.js (el token; no es puja mai al repositori)."""
    text = open("ranking_config.js", encoding="utf-8").read()
    if os.path.exists("ranking_secret.js"):
        text += "\n" + open("ranking_secret.js", encoding="utf-8").read()
    return text


def main():
    fitxers = sys.argv[1:] or ["casos_final.json"] + [f for f in ("casos_kpop.json", "casos_meu.json") if os.path.exists(f)]
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
                v = next(p for p in c["persones"] if p["id"] == "V")
                c["intro"] = {l: intro(l, c["titol"][l], v["nom"], v["genere"], c["id"], bool(c.get("kpop")))
                              for l in ("ca", "fr")}
                casos.append(c)
    casos.sort(key=lambda c: (c["n"], c["nivell"]))
    kp = [c for c in casos if c.get("kpop")]
    for i, c in enumerate(kp, 1):
        c["nom"] = {"ca": "Missió K-pop %d" % i, "fr": "Mission K-pop %d" % i}
    assigna_noms([c for c in casos if not c.get("kpop") and "nom" not in c])
    meta = {}
    for c in casos:
        k = c["escenari"]
        tag = ESCENARIS[k].get("tag")
        if tag and k not in meta:
            base = zlib.crc32(k.encode()) % 360
            meta[k] = {"tag": tag, "hue": [(base + 47 * i) % 360 for i in range(8)],
                       "sat": 38 + zlib.crc32((k + "s").encode()) % 25, "col": base}
    with open("casos.js", "w", encoding="utf-8") as fh:
        fh.write("window.CASOS = " + json.dumps(casos, ensure_ascii=False) + ";\n")
        fh.write("window.SCEN_META = " + json.dumps(meta, ensure_ascii=False) + ";\n")
        try:
            fh.write("window.GRANS = " + json.dumps(json.load(open("grans.json", encoding="utf-8"))) + ";\n")
        except OSError:
            fh.write("window.GRANS = {};\n")
    print(len(casos), "casos a casos.js")
    # joc.html: tot en un sol fitxer (casos inclosos), per obrir-lo sense servidor
    with open("index.html", encoding="utf-8") as fh:
        html = fh.read()
    js = open("casos.js", encoding="utf-8").read()
    html = html.replace('<script src="casos.js"></script>', "<script>" + js + "</script>")
    html = html.replace("/*KPOP_PHOTOS*/", fotos_kpop())
    html = html.replace('<script src="ranking_config.js"></script>', "<script>" + config_classificacio() + "</script>")
    # imatges (retrats i objectes) incloses com a data URI: joc.html és un sol fitxer.
    # Si hi ha Pillow, s'encongeixen una mica perquè el fitxer pesi menys (index.html usa els originals).
    import base64
    import io
    import re
    try:
        from PIL import Image
    except ImportError:
        Image = None

    def dades(ruta):
        with open(ruta, "rb") as fh:
            raw = fh.read()
        if Image is None:
            return ("image/png" if ruta.endswith(".png") else "image/jpeg"), raw
        im = Image.open(io.BytesIO(raw))
        buf = io.BytesIO()
        if ruta.endswith(".png"):
            im = im.convert("RGBA")
            # mides màximes (px) i colors segons la imatge
            grans = {"logo.png": (420, 128), "sobre.png": (260, 128), "paper.png": (240, 128)}
            mida_max, colors = grans.get(ruta, (230, 160) if "/g_" in ruta else (104, 96))
            im.thumbnail((mida_max, mida_max), Image.LANCZOS)
            im = im.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.NONE)
            im.save(buf, "PNG", optimize=True)
            return "image/png", buf.getvalue()
        im = im.convert("RGB")
        im.thumbnail((144 if "retrats" in ruta else 96, 144 if "retrats" in ruta else 96), Image.LANCZOS)
        im.save(buf, "JPEG", quality=78, optimize=True)
        return "image/jpeg", buf.getvalue()

    for ruta in set(re.findall(r'"((?:kpop/retrats|kpop/objectes|retrats|objectes|terres)/[a-z_]+\.(?:jpg|png)|logo\.png|sobre\.png|paper\.png)"', html)):
        mime, raw = dades(ruta)
        html = html.replace('"' + ruta + '"', '"data:' + mime + ';base64,' + base64.b64encode(raw).decode() + '"')
    with open("joc.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    print("joc.html creat")


if __name__ == "__main__":
    main()
