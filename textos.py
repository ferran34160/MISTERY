"""Textos de les pistes en català i francès.

Les pistes són dades (motor.py); aquí es converteixen en frases amb articles,
contraccions (al, del / au, du), elisions (l', d') i gènere de la persona.
"""

VOCALS = "aeiouàèéíòóúâêîôûhAEIOUÀÈÉÍÒÓÚH"


def _elideix(s):
    return s[:1] in VOCALS


def det(lang, nom, cas="def"):
    """Sintagma nominal. nom = (gènere, text). cas: def, indef, a, de, dins."""
    g, t = nom
    if cas == "indef":
        return ("un " if g == "m" else "una " if lang == "ca" else "une ") + t
    if _elideix(t):
        d = "l'" + t
        base = "l'"
    else:
        base = "el " if (lang == "ca" and g == "m") else "la " if lang == "ca" \
            else "le " if g == "m" else "la "
        d = base + t
    if cas == "def":
        return d
    if lang == "ca":
        if cas == "a":
            return "a " + d if base != "el " else "al " + t
        if cas == "de":
            return "de " + d if base != "el " else "del " + t
        if cas == "dins":
            return "a " + d if base != "el " else "al " + t
    else:
        if cas == "a":
            return "à " + d if base != "le " else "au " + t
        if cas == "de":
            return "de " + d if base != "le " else "du " + t
        if cas == "dins":
            return "dans " + d
    raise ValueError(cas)


def de_lloc(lloc, lang):
    """'el taller' -> 'del taller', 'le garage' -> 'du garage'; la/l' -> de la/de l'."""
    pre = "el " if lang == "ca" else "le "
    if lloc.startswith(pre):
        return ("del " if lang == "ca" else "du ") + lloc[len(pre):]
    return "de " + lloc


def de_nom(nom):
    return ("d'" if _elideix(nom) else "de ") + nom


def _p(esc, p, n):
    """(nom, gènere, lletra) de la persona p."""
    return esc["_noms"][p]


def _pron(lang, g):
    return {"m": "Il", "f": "Elle"}[g]


def frase(lang, esc, cl, tria):
    """Frase de la pista `cl` en `lang`. `tria(clau, variants)` escull una variant diferent de les ja usades."""
    ob = esc["objectes"]
    sa = esc["sales"]
    t = cl["t"]
    noms = esc["_noms"]
    ca = lang == "ca"

    def que(nom):
        if lang == "fr" and _elideix(nom):
            return "qu'" + nom
        return "que " + nom

    def sala(R, cas):
        return det(lang, sa[esc["_sales"][R]]["nom"][lang], cas)

    def objecte(o, cas):
        return det(lang, ob[o]["nom"][lang], cas)

    def indef(o):
        return _indef(lang, ob[o]["nom"][lang])

    def dindef(o):
        return _de_indef(lang, ob[o]["nom"][lang])

    def cap(x):
        return x[:1].upper() + x[1:]

    if t == "compte_sala":
        k = cl["k"]
        R = cl["sala"]
        if ca:
            if k == 0:
                return tria(t + "0", [f"Ningú no era {sala(R, 'a')}, ni tan sols la víctima.",
                                      f"{cap(sala(R, 'def'))} estava buida: ni un sol cos.",
                                      f"No hi havia ànima {sala(R, 'a')}, ni la víctima."])
            if k == 1:
                return tria(t + "1", [f"Només hi havia una persona {sala(R, 'a')}, víctima inclosa.",
                                      f"{cap(sala(R, 'def'))} només tenia una persona, comptant la víctima."])
            return tria(t + "n", [f"Hi havia exactament {k} persones {sala(R, 'a')}, víctima inclosa.",
                                  f"{cap(sala(R, 'def'))} acollia {k} persones, comptant la víctima.",
                                  f"Comptant la víctima, {k} persones eren {sala(R, 'a')}."])
        if k == 0:
            return tria(t + "0", [f"Personne n'était {sala(R, 'dins')}, pas même la victime.",
                                  f"{cap(sala(R, 'def'))} était vide : pas une âme.",
                                  f"Pas âme qui vive {sala(R, 'dins')}, la victime non plus."])
        if k == 1:
            return tria(t + "1", [f"Il n'y avait qu'une personne {sala(R, 'dins')}, victime comprise.",
                                  f"{cap(sala(R, 'def'))} ne comptait qu'une personne, victime comprise."])
        return tria(t + "n", [f"Il y avait exactement {k} personnes {sala(R, 'dins')}, victime comprise.",
                              f"{cap(sala(R, 'def'))} accueillait {k} personnes, victime comprise.",
                              f"Victime comprise, {k} personnes se trouvaient {sala(R, 'dins')}."])

    p = cl["p"]
    g = noms[p][1]
    pr = _pron(lang, g)
    m = g == "m"
    if ca:
        el = "El" if m else "La"            # «El van veure»
        ell = "ell" if m else "ella"
        sol_ = "sol" if m else "sola"
        if t == "en_sala":
            R = cl["sala"]
            return tria(t, [f"Era {sala(R, 'a')}.", f"Estava {sala(R, 'a')}.", f"Es trobava {sala(R, 'a')}.",
                            f"{el} van veure {sala(R, 'a')}.", f"Va passar l'estona {sala(R, 'a')}."])
        if t == "no_en_sala":
            R = cl["sala"]
            return tria(t, [f"No era {sala(R, 'a')}.", f"No es trobava {sala(R, 'a')}.",
                            f"Ningú no {el.lower()} va veure {sala(R, 'a')}.", f"No va posar els peus {sala(R, 'a')}."])
        if t == "sobre_obj":
            o = cl["obj"]
            return tria(t, [f"Era sobre {objecte(o, 'def')}.", f"Estava damunt {objecte(o, 'def')}.",
                            f"Es va deixar caure sobre {objecte(o, 'def')}.", f"Va quedar-se sobre {objecte(o, 'def')}."])
        if t == "prop_obj":
            o = cl["obj"]
            return tria(t, [f"Era al costat {dindef(o)}.", f"Tenia {indef(o)} a tocar.",
                            f"Prop seu hi havia {indef(o)}.", f"Estava vora {indef(o)}."])
        if t == "fila_obj":
            o = cl["obj"]
            return tria(t, [f"A la seva fila hi havia {indef(o)}.", f"Compartia fila amb {indef(o)}.",
                            f"Tenia {indef(o)} a la mateixa fila.", f"{cap(indef(o))} era a la seva fila."])
        if t == "col_obj":
            o = cl["obj"]
            return tria(t, [f"A la seva columna hi havia {indef(o)}.", f"Compartia columna amb {indef(o)}.",
                            f"Tenia {indef(o)} a la mateixa columna.", f"{cap(indef(o))} era a la seva columna."])
        if t == "raco":
            return tria(t, ["Era en un racó d'una habitació.", "Va quedar-se en un racó d'una habitació.",
                            "Ocupava un racó d'una habitació.", "Estava en una cantonada d'una habitació."])
        if t == "vora":
            L = de_lloc(esc["lloc"][lang], lang)
            return tria(t, [f"Era al costat d'una paret exterior {L}.", f"Tocava una paret exterior {L}.",
                            f"Tenia una paret exterior {L} just al costat."])
        if t == "sol":
            return tria(t, ["No compartia habitació amb ningú, ni tan sols amb la víctima.",
                            f"Era {sol_} a la seva habitació.",
                            "A la seva habitació no hi havia ningú més, ni la víctima."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return tria(t, [f"Era just al costat {de_nom(nq)}, a la mateixa habitació.",
                            f"Es trobava tot just al costat {de_nom(nq)}, dins la mateixa habitació.",
                            f"{nq} era el seu veí immediat, a la mateixa habitació."])
        if t == "nord":
            return tria(t, [f"Era al nord {de_nom(nq)}.", f"Estava més al nord que {nq}.", f"Tenia {nq} al seu sud."])
        if t == "sud":
            return tria(t, [f"Era al sud {de_nom(nq)}.", f"Estava més al sud que {nq}.", f"Tenia {nq} al seu nord."])
        if t == "est":
            return tria(t, [f"Era a l'est {de_nom(nq)}.", f"Estava més a l'est que {nq}.", f"Tenia {nq} al seu oest."])
        if t == "oest":
            return tria(t, [f"Era a l'oest {de_nom(nq)}.", f"Estava més a l'oest que {nq}.", f"Tenia {nq} al seu est."])
        if t == "diag":
            return tria(t, [f"Era a la mateixa diagonal {que(nq)}.", f"Compartia diagonal amb {nq}.",
                            f"{nq} i {ell} eren en una mateixa línia diagonal."])
        if t == "cavall":
            return tria(t, [f"Era a un salt de cavall {de_nom(nq)} (com als escacs).",
                            f"Estava a un salt de cavall {de_nom(nq)}.",
                            f"Respecte a {nq}, estava a un moviment de cavall."])
        if t == "mateixa_sala":
            return tria(t, [f"Era a la mateixa habitació {que(nq)}.", f"Compartia habitació amb {nq}.",
                            f"{nq} i {ell} eren a la mateixa habitació."])
        if t == "altra_sala":
            return tria(t, [f"No era a la mateixa habitació {que(nq)}.", f"No compartia habitació amb {nq}.",
                            f"Era en una altra habitació que {nq}."])
        if t == "sol_amb":
            return tria(t, [f"Només {ell} i {nq} eren a la seva habitació.",
                            f"A la seva habitació només hi havia {nq} amb {ell}.",
                            f"Compartia habitació només amb {nq}."])
    else:
        lui = "lui" if m else "elle"
        dlui = "de lui" if m else "d'elle"
        qlui = "que lui" if m else "qu'elle"
        seul = "seul" if m else "seule"
        vu = "vu" if m else "vue"
        inst = "installé" if m else "installée"
        if t == "en_sala":
            R = cl["sala"]
            return tria(t, [f"{pr} était {sala(R, 'dins')}.", f"{pr} se trouvait {sala(R, 'dins')}.",
                            f"On l'a {vu} {sala(R, 'dins')}.", f"{pr} a passé le temps {sala(R, 'dins')}."])
        if t == "no_en_sala":
            R = cl["sala"]
            return tria(t, [f"{pr} n'était pas {sala(R, 'dins')}.", f"{pr} ne se trouvait pas {sala(R, 'dins')}.",
                            f"Personne ne l'a {vu} {sala(R, 'dins')}."])
        if t == "sobre_obj":
            o = cl["obj"]
            return tria(t, [f"{pr} était sur {objecte(o, 'def')}.", f"{pr} était {inst} sur {objecte(o, 'def')}.",
                            f"{pr} se tenait sur {objecte(o, 'def')}."])
        if t == "prop_obj":
            o = cl["obj"]
            return tria(t, [f"{pr} était à côté {dindef(o)}.", f"{pr} avait {indef(o)} tout près.",
                            f"{pr} se tenait près {dindef(o)}."])
        if t == "fila_obj":
            o = cl["obj"]
            return tria(t, [f"Sur sa ligne se trouvait {indef(o)}.", f"{pr} partageait sa ligne avec {indef(o)}.",
                            f"{cap(indef(o))} se trouvait sur sa ligne."])
        if t == "col_obj":
            o = cl["obj"]
            return tria(t, [f"Dans sa colonne se trouvait {indef(o)}.", f"{pr} partageait sa colonne avec {indef(o)}.",
                            f"{cap(indef(o))} se trouvait dans sa colonne."])
        if t == "raco":
            return tria(t, [f"{pr} était dans un coin d'une pièce.", f"{pr} occupait un coin d'une pièce.",
                            f"{pr} se tenait dans un angle d'une pièce."])
        if t == "vora":
            L = de_lloc(esc["lloc"][lang], lang)
            return tria(t, [f"{pr} était contre un mur extérieur {L}.", f"{pr} touchait un mur extérieur {L}.",
                            f"{pr} avait un mur extérieur {L} tout contre {lui}."])
        if t == "sol":
            return tria(t, [f"{pr} ne partageait sa pièce avec personne, pas même avec la victime.",
                            f"{pr} était {seul} dans sa pièce.",
                            "Dans sa pièce, il n'y avait personne d'autre, pas même la victime."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return tria(t, [f"{pr} était juste à côté {de_nom(nq)}, dans la même pièce.",
                            f"{pr} se trouvait tout à côté {de_nom(nq)}, dans la même pièce.",
                            f"{nq} était juste à côté {dlui}, dans la même pièce."])
        if t == "nord":
            return tria(t, [f"{pr} était au nord {de_nom(nq)}.", f"{pr} se trouvait plus au nord {que(nq)}.",
                            f"{nq} était au sud {dlui}."])
        if t == "sud":
            return tria(t, [f"{pr} était au sud {de_nom(nq)}.", f"{pr} se trouvait plus au sud {que(nq)}.",
                            f"{nq} était au nord {dlui}."])
        if t == "est":
            return tria(t, [f"{pr} était à l'est {de_nom(nq)}.", f"{pr} se trouvait plus à l'est {que(nq)}.",
                            f"{nq} était à l'ouest {dlui}."])
        if t == "oest":
            return tria(t, [f"{pr} était à l'ouest {de_nom(nq)}.", f"{pr} se trouvait plus à l'ouest {que(nq)}.",
                            f"{nq} était à l'est {dlui}."])
        if t == "diag":
            return tria(t, [f"{pr} était sur la même diagonale {que(nq)}.", f"{pr} partageait une diagonale avec {nq}.",
                            f"{nq} et {lui} étaient sur une même ligne diagonale."])
        if t == "cavall":
            return tria(t, [f"{pr} était à un saut de cavalier {de_nom(nq)} (comme aux échecs).",
                            f"{pr} se trouvait à un saut de cavalier {de_nom(nq)}.",
                            f"Par rapport à {nq}, {pr.lower()} était à un mouvement de cavalier."])
        if t == "mateixa_sala":
            return tria(t, [f"{pr} était dans la même pièce {que(nq)}.", f"{pr} partageait sa pièce avec {nq}.",
                            f"{nq} et {lui} étaient dans la même pièce."])
        if t == "altra_sala":
            return tria(t, [f"{pr} n'était pas dans la même pièce {que(nq)}.",
                            f"{pr} ne partageait pas sa pièce avec {nq}.",
                            f"{pr} se trouvait dans une autre pièce {que(nq)}."])
        if t == "sol_amb":
            return tria(t, [f"Seuls {lui} et {nq} étaient dans sa pièce.",
                            f"Dans sa pièce, il n'y avait {qlui} et {nq}.",
                            f"{pr} ne partageait sa pièce qu'avec {nq}."])
    raise ValueError(t)


def _indef(lang, nom):
    return det(lang, nom, "indef")


def _de_indef(lang, nom):
    return "d'" + det(lang, nom, "indef")


def descriu(lang, esc, pistes, rng):
    """Llista de frases (una per pista). Dins d'un cas no es repeteix la mateixa plantilla mentre n'hi hagi d'altres."""
    usades = {}

    def tria(clau, variants):
        fetes = usades.setdefault(clau, set())
        lliures = [i for i in range(len(variants)) if i not in fetes]
        if not lliures:
            fetes.clear()
            lliures = list(range(len(variants)))
        i = rng.choice(lliures)
        fetes.add(i)
        return variants[i]
    return [frase(lang, esc, cl, tria) for cl in pistes]
