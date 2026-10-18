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
    """Frase de la pista `cl` en `lang`. `tria(llista)` escull una variant."""
    ob = esc["objectes"]
    sa = esc["sales"]
    t = cl["t"]
    noms = esc["_noms"]

    def que(nom):
        if lang == "fr" and _elideix(nom):
            return "qu'" + nom
        return "que " + nom

    def sala(R, cas):
        return det(lang, sa[esc["_sales"][R]]["nom"][lang], cas)

    def objecte(o, cas):
        return det(lang, ob[o]["nom"][lang], cas)

    if t == "compte_sala":
        k = cl["k"]
        if lang == "ca":
            if k == 0:
                return tria([f"Ningú no era {sala(cl['sala'], 'a')}, ni tan sols la víctima.",
                             f"{sala(cl['sala'], 'def').capitalize()} estava buida: ni un sol cos."])
            if k == 1:
                return f"Només hi havia una persona {sala(cl['sala'], 'a')}, víctima inclosa."
            return f"Hi havia exactament {k} persones {sala(cl['sala'], 'a')}, víctima inclosa."
        if k == 0:
            return tria([f"Personne n'était {sala(cl['sala'], 'dins')}, pas même la victime.",
                         f"{sala(cl['sala'], 'def').capitalize()} était vide : pas une âme."])
        if k == 1:
            return f"Il n'y avait qu'une personne {sala(cl['sala'], 'dins')}, victime comprise."
        return f"Il y avait exactement {k} personnes {sala(cl['sala'], 'dins')}, victime comprise."

    p = cl["p"]
    g = noms[p][1]
    pr = _pron(lang, g)
    if lang == "ca":
        if t == "en_sala":
            return tria([f"Era {sala(cl['sala'], 'a')}.", f"Estava {sala(cl['sala'], 'a')}."])
        if t == "no_en_sala":
            return f"No era {sala(cl['sala'], 'a')}."
        if t == "sobre_obj":
            return f"Era sobre {objecte(cl['obj'], 'def')}."
        if t == "prop_obj":
            return tria([f"Era al costat {_de_indef(lang, ob[cl['obj']]['nom'][lang])}.",
                         f"Tenia {_indef(lang, ob[cl['obj']]['nom'][lang])} a tocar."])
        if t == "fila_obj":
            return f"A la seva fila hi havia {_indef(lang, ob[cl['obj']]['nom'][lang])}."
        if t == "col_obj":
            return f"A la seva columna hi havia {_indef(lang, ob[cl['obj']]['nom'][lang])}."
        if t == "raco":
            return "Era en un racó d'una habitació."
        if t == "vora":
            return f"Era al costat d'una paret exterior {de_lloc(esc['lloc'][lang], lang)}."
        if t == "sol":
            return tria(["No compartia habitació amb ningú, ni tan sols amb la víctima.",
                         "Era sol" + ("a" if g == "f" else "") + " a la seva habitació."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return f"Era just al costat {de_nom(nq)}, a la mateixa habitació."
        if t == "nord":
            return f"Era al nord {de_nom(nq)}."
        if t == "sud":
            return f"Era al sud {de_nom(nq)}."
        if t == "est":
            return f"Era a l'est {de_nom(nq)}."
        if t == "oest":
            return f"Era a l'oest {de_nom(nq)}."
        if t == "diag":
            return f"Era a la mateixa diagonal {que(nq)}."
        if t == "cavall":
            return f"Era a un salt de cavall {de_nom(nq)} (com als escacs)."
        if t == "mateixa_sala":
            return f"Era a la mateixa habitació {que(nq)}."
        if t == "altra_sala":
            return f"No era a la mateixa habitació {que(nq)}."
        if t == "sol_amb":
            return f"Només {'ell' if g == 'm' else 'ella'} i {nq} eren a la seva habitació."
    else:
        if t == "en_sala":
            return tria([f"{pr} était {sala(cl['sala'], 'dins')}.",
                         f"{pr} se trouvait {sala(cl['sala'], 'dins')}."])
        if t == "no_en_sala":
            return f"{pr} n'était pas {sala(cl['sala'], 'dins')}."
        if t == "sobre_obj":
            return f"{pr} était sur {objecte(cl['obj'], 'def')}."
        if t == "prop_obj":
            return tria([f"{pr} était à côté {_de_indef(lang, ob[cl['obj']]['nom'][lang])}.",
                         f"{pr} avait {_indef(lang, ob[cl['obj']]['nom'][lang])} tout près."])
        if t == "fila_obj":
            return f"Sur sa ligne se trouvait {_indef(lang, ob[cl['obj']]['nom'][lang])}."
        if t == "col_obj":
            return f"Dans sa colonne se trouvait {_indef(lang, ob[cl['obj']]['nom'][lang])}."
        if t == "raco":
            return f"{pr} était dans un coin d'une pièce."
        if t == "vora":
            return f"{pr} était contre un mur extérieur {de_lloc(esc['lloc'][lang], lang)}."
        if t == "sol":
            return tria([f"{pr} ne partageait sa pièce avec personne, pas même avec la victime.",
                         f"{pr} était seul{'e' if g == 'f' else ''} dans sa pièce."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return f"{pr} était juste à côté {de_nom(nq)}, dans la même pièce."
        if t == "nord":
            return f"{pr} était au nord {de_nom(nq)}."
        if t == "sud":
            return f"{pr} était au sud {de_nom(nq)}."
        if t == "est":
            return f"{pr} était à l'est {de_nom(nq)}."
        if t == "oest":
            return f"{pr} était à l'ouest {de_nom(nq)}."
        if t == "diag":
            return f"{pr} était sur la même diagonale {que(nq)}."
        if t == "cavall":
            return f"{pr} était à un saut de cavalier {de_nom(nq)} (comme aux échecs)."
        if t == "mateixa_sala":
            return f"{pr} était dans la même pièce {que(nq)}."
        if t == "altra_sala":
            return f"{pr} n'était pas dans la même pièce {que(nq)}."
        if t == "sol_amb":
            return f"Seuls {'lui' if g == 'm' else 'elle'} et {nq} étaient dans sa pièce."
    raise ValueError(t)


def _indef(lang, nom):
    return det(lang, nom, "indef")


def _de_indef(lang, nom):
    return "d'" + det(lang, nom, "indef")


def descriu(lang, esc, pistes, rng):
    """Llista de frases (una per pista)."""
    def tria(v):
        return rng.choice(v)
    return [frase(lang, esc, cl, tria) for cl in pistes]
