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
            return ("sur " if t in _SUR_FR else "dans ") + d
    raise ValueError(cas)


_SUR_FR = {"toit", "terrasse", "pont", "passerelle", "plateforme", "quai", "mirador", "piste", "scène"}


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
                                      f"No hi havia ànima {sala(R, 'a')}, ni la víctima.",
                                      f"{cap(sala(R, 'def'))} es va quedar sense ningú, víctima inclosa."])
            if k == 1:
                return tria(t + "1", [f"Només hi havia una persona {sala(R, 'a')}, víctima inclosa.",
                                      f"{cap(sala(R, 'def'))} només tenia una persona, comptant la víctima.",
                                      f"{cap(sala(R, 'def'))} era gairebé buida: una sola persona, víctima inclosa."])
            return tria(t + "n", [f"Hi havia exactament {k} persones {sala(R, 'a')}, víctima inclosa.",
                                  f"{cap(sala(R, 'def'))} acollia {k} persones, comptant la víctima.",
                                  f"Comptant la víctima, {k} persones eren {sala(R, 'a')}.",
                                  f"Si hi sumes la víctima, {sala(R, 'a')} hi havia {k} persones.",
                                  f"{cap(sala(R, 'def'))} va tenir {k} persones aquell vespre, víctima inclosa."])
        if k == 0:
            return tria(t + "0", [f"Personne n'était {sala(R, 'dins')}, pas même la victime.",
                                  f"{cap(sala(R, 'def'))} était vide : pas une âme.",
                                  f"Pas âme qui vive {sala(R, 'dins')}, la victime non plus.",
                                  f"{cap(sala(R, 'def'))} est restée sans personne, victime comprise."])
        if k == 1:
            return tria(t + "1", [f"Il n'y avait qu'une personne {sala(R, 'dins')}, victime comprise.",
                                  f"{cap(sala(R, 'def'))} ne comptait qu'une personne, victime comprise.",
                                  f"{cap(sala(R, 'def'))} était presque vide : une seule personne, victime comprise."])
        return tria(t + "n", [f"Il y avait exactement {k} personnes {sala(R, 'dins')}, victime comprise.",
                              f"{cap(sala(R, 'def'))} accueillait {k} personnes, victime comprise.",
                              f"Victime comprise, {k} personnes se trouvaient {sala(R, 'dins')}.",
                              f"En ajoutant la victime, {k} personnes étaient {sala(R, 'dins')}.",
                              f"{cap(sala(R, 'def'))} abritait {k} personnes ce soir-là, victime comprise."])

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
                            f"{el} van veure {sala(R, 'a')}.", f"Va passar l'estona {sala(R, 'a')}.",
                            f"Havia estat {sala(R, 'a')} tota l'estona.", f"Va entrar {sala(R, 'a')} i no en va sortir.",
                            f"Ningú no dubta que era {sala(R, 'a')}.", f"Tenia el seu lloc {sala(R, 'a')}.",
                            f"Es va deixar veure {sala(R, 'a')}."])
        if t == "no_en_sala":
            R = cl["sala"]
            return tria(t, [f"No era {sala(R, 'a')}.", f"No es trobava {sala(R, 'a')}.",
                            f"Ningú no {el.lower()} va veure {sala(R, 'a')}.", f"No va posar els peus {sala(R, 'a')}.",
                            f"Va mantenir-se lluny {sala(R, 'de')}.", f"Es va quedar fora {sala(R, 'de')}.",
                            f"Va evitar {sala(R, 'def')}.", f"{cap(sala(R, 'def'))} no era el seu lloc aquella nit."])
        if t == "sobre_obj":
            o = cl["obj"]
            return tria(t, [f"Era sobre {objecte(o, 'def')}.", f"Estava damunt {objecte(o, 'def')}.",
                            f"Es va deixar caure sobre {objecte(o, 'def')}.", f"Va quedar-se sobre {objecte(o, 'def')}.",
                            f"Va ocupar {objecte(o, 'def')}.", f"Es va situar sobre {objecte(o, 'def')}.",
                            f"El seu lloc era sobre {objecte(o, 'def')}.", f"Reposava sobre {objecte(o, 'def')}."])
        if t == "prop_obj":
            o = cl["obj"]
            return tria(t, [f"Era al costat {dindef(o)}.", f"Tenia {indef(o)} a tocar.",
                            f"Prop seu hi havia {indef(o)}.", f"Estava vora {indef(o)}.",
                            f"A pocs passos hi havia {indef(o)}.", f"{cap(indef(o))} era el seu veí més proper.",
                            f"Tenia {indef(o)} ben a prop.", f"No es va separar gaire {dindef(o)}."])
        if t == "fila_obj":
            o = cl["obj"]
            return tria(t, [f"A la seva fila hi havia {indef(o)}.", f"Compartia fila amb {indef(o)}.",
                            f"Tenia {indef(o)} a la mateixa fila.", f"{cap(indef(o))} era a la seva fila.",
                            f"Seguint la seva fila, es topava amb {indef(o)}.", f"{cap(indef(o))} es feia notar a la seva fila."])
        if t == "col_obj":
            o = cl["obj"]
            return tria(t, [f"A la seva columna hi havia {indef(o)}.", f"Compartia columna amb {indef(o)}.",
                            f"Tenia {indef(o)} a la mateixa columna.", f"{cap(indef(o))} era a la seva columna.",
                            f"Seguint la seva columna, es topava amb {indef(o)}.", f"{cap(indef(o))} es feia notar a la seva columna."])
        if t == "raco":
            return tria(t, ["Era en un racó d'una habitació.", "Va quedar-se en un racó d'una habitació.",
                            "Ocupava un racó d'una habitació.", "Estava en una cantonada d'una habitació.",
                            "Tenia dues parets d'una habitació a l'esquena.", "Va trobar refugi en un racó d'una habitació.",
                            "Se'l podia trobar arraconat en una habitació." if m else "Se la podia trobar arraconada en una habitació."])
        if t == "vora":
            L = de_lloc(esc["lloc"][lang], lang)
            return tria(t, [f"Era al costat d'una paret exterior {L}.", f"Tocava una paret exterior {L}.",
                            f"Tenia una paret exterior {L} just al costat.",
                            f"Tenia l'exterior {L} a tocar, només separat per una paret.", f"Es va recolzar prop d'una paret exterior {L}."])
        if t == "sol":
            return tria(t, ["No compartia habitació amb ningú, ni tan sols amb la víctima.",
                            f"Era {sol_} a la seva habitació.",
                            "A la seva habitació no hi havia ningú més, ni la víctima.",
                            "Ningú més, ni tan sols la víctima, no compartia la seva habitació.",
                            f"Va estar {sol_} a la seva habitació: ni la víctima hi era."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return tria(t, [f"Era just al costat {de_nom(nq)}, a la mateixa habitació.",
                            f"Es trobava tot just al costat {de_nom(nq)}, dins la mateixa habitació.",
                            f"{nq} era el seu veí immediat, a la mateixa habitació.",
                            f"Estava a tocar {de_nom(nq)}, dins la mateixa habitació.",
                            f"No hi havia cap casella entre {ell} i {nq}, dins la mateixa habitació."])
        if t == "nord":
            return tria(t, [f"Era al nord {de_nom(nq)}.", f"Estava més al nord que {nq}.", f"Tenia {nq} al seu sud.",
                            f"Al plànol, estava per sobre {de_nom(nq)}.", f"{nq} quedava més avall que {ell} al plànol."])
        if t == "sud":
            return tria(t, [f"Era al sud {de_nom(nq)}.", f"Estava més al sud que {nq}.", f"Tenia {nq} al seu nord.",
                            f"Al plànol, estava per sota {de_nom(nq)}.", f"{nq} quedava més amunt que {ell} al plànol."])
        if t == "est":
            return tria(t, [f"Era a l'est {de_nom(nq)}.", f"Estava més a l'est que {nq}.", f"Tenia {nq} al seu oest.",
                            f"Al plànol, quedava a la dreta {de_nom(nq)}.", f"{nq} quedava a la seva esquerra."])
        if t == "oest":
            return tria(t, [f"Era a l'oest {de_nom(nq)}.", f"Estava més a l'oest que {nq}.", f"Tenia {nq} al seu est.",
                            f"Al plànol, quedava a l'esquerra {de_nom(nq)}.", f"{nq} quedava a la seva dreta."])
        if t == "diag":
            return tria(t, [f"Era a la mateixa diagonal {que(nq)}.", f"Compartia diagonal amb {nq}.",
                            f"{nq} i {ell} eren en una mateixa línia diagonal.",
                            f"Si traçaves una diagonal des {de_nom(nq)}, hi arribaves a {ell}.",
                            f"{nq} i {ell} formaven una diagonal."])
        if t == "cavall":
            return tria(t, [f"Era a un salt de cavall {de_nom(nq)} (com als escacs).",
                            f"Estava a un salt de cavall {de_nom(nq)}.",
                            f"Respecte a {nq}, estava a un moviment de cavall.",
                            f"Només un salt de cavall {'el' if m else 'la'} separava {de_nom(nq)}."])
        if t == "mateixa_sala":
            return tria(t, [f"Era a la mateixa habitació {que(nq)}.", f"Compartia habitació amb {nq}.",
                            f"{nq} i {ell} eren a la mateixa habitació.",
                            f"Va coincidir amb {nq} a la mateixa habitació.", f"{nq} i {ell} es van trobar sota el mateix sostre."])
        if t == "altra_sala":
            return tria(t, [f"No era a la mateixa habitació {que(nq)}.", f"No compartia habitació amb {nq}.",
                            f"Era en una altra habitació que {nq}.",
                            f"{nq} i {ell} no es van creuar: eren a habitacions diferents.",
                            f"Entre {ell} i {nq} hi havia almenys una paret."])
        if t == "sol_amb":
            return tria(t, [f"Només {ell} i {nq} eren a la seva habitació.",
                            f"A la seva habitació només hi havia {nq} amb {ell}.",
                            f"Compartia habitació només amb {nq}.",
                            f"{nq} era l'única companyia en aquella habitació.",
                            f"A la seva habitació, ningú més que {nq}."])
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
                            f"On l'a {vu} {sala(R, 'dins')}.", f"{pr} a passé le temps {sala(R, 'dins')}.",
                            f"{pr} n'a pas quitté {sala(R, 'def')} de la soirée.", f"{pr} est entré {sala(R, 'dins')} et n'en est pas ressorti." if m else f"{pr} est entrée {sala(R, 'dins')} et n'en est pas ressortie.",
                            f"Personne ne doute qu'{pr.lower()} était {sala(R, 'dins')}.", f"{pr} avait sa place {sala(R, 'dins')}."])
        if t == "no_en_sala":
            R = cl["sala"]
            return tria(t, [f"{pr} n'était pas {sala(R, 'dins')}.", f"{pr} ne se trouvait pas {sala(R, 'dins')}.",
                            f"Personne ne l'a {vu} {sala(R, 'dins')}.",
                            f"{pr} est resté à l'écart {sala(R, 'de')}." if m else f"{pr} est restée à l'écart {sala(R, 'de')}.",
                            f"{pr} a évité {sala(R, 'def')}.", f"{cap(sala(R, 'def'))} n'était pas sa place ce soir-là."])
        if t == "sobre_obj":
            o = cl["obj"]
            return tria(t, [f"{pr} était sur {objecte(o, 'def')}.", f"{pr} était {inst} sur {objecte(o, 'def')}.",
                            f"{pr} se tenait sur {objecte(o, 'def')}.",
                            f"{pr} a pris place sur {objecte(o, 'def')}.", f"Sa place était sur {objecte(o, 'def')}.",
                            f"{pr} reposait sur {objecte(o, 'def')}."])
        if t == "prop_obj":
            o = cl["obj"]
            return tria(t, [f"{pr} était à côté {dindef(o)}.", f"{pr} avait {indef(o)} tout près.",
                            f"{pr} se tenait près {dindef(o)}.",
                            f"À quelques pas se trouvait {indef(o)}.", f"{cap(indef(o))} était son plus proche voisin.",
                            f"{pr} ne s'est guère éloigné {dindef(o)}." if m else f"{pr} ne s'est guère éloignée {dindef(o)}."])
        if t == "fila_obj":
            o = cl["obj"]
            return tria(t, [f"Sur sa ligne se trouvait {indef(o)}.", f"{pr} partageait sa ligne avec {indef(o)}.",
                            f"{cap(indef(o))} se trouvait sur sa ligne.",
                            f"En suivant sa ligne, on tombait sur {indef(o)}.", f"{cap(indef(o))} se remarquait sur sa ligne."])
        if t == "col_obj":
            o = cl["obj"]
            return tria(t, [f"Dans sa colonne se trouvait {indef(o)}.", f"{pr} partageait sa colonne avec {indef(o)}.",
                            f"{cap(indef(o))} se trouvait dans sa colonne.",
                            f"En suivant sa colonne, on tombait sur {indef(o)}.", f"{cap(indef(o))} se remarquait dans sa colonne."])
        if t == "raco":
            return tria(t, [f"{pr} était dans un coin d'une pièce.", f"{pr} occupait un coin d'une pièce.",
                            f"{pr} se tenait dans un angle d'une pièce.",
                            f"{pr} avait deux murs d'une pièce dans le dos.", f"{pr} avait trouvé refuge dans un coin d'une pièce."])
        if t == "vora":
            L = de_lloc(esc["lloc"][lang], lang)
            return tria(t, [f"{pr} était contre un mur extérieur {L}.", f"{pr} touchait un mur extérieur {L}.",
                            f"{pr} avait un mur extérieur {L} tout contre {lui}.",
                            f"{pr} avait l'extérieur {L} tout près, derrière un simple mur.",
                            f"{pr} s'est appuyé près d'un mur extérieur {L}." if m else f"{pr} s'est appuyée près d'un mur extérieur {L}."])
        if t == "sol":
            return tria(t, [f"{pr} ne partageait sa pièce avec personne, pas même avec la victime.",
                            f"{pr} était {seul} dans sa pièce.",
                            "Dans sa pièce, il n'y avait personne d'autre, pas même la victime.",
                            "Personne d'autre, même pas la victime, ne partageait sa pièce.",
                            f"{pr} est resté {seul} dans sa pièce : la victime n'y était pas non plus."])
        q = cl["q"]
        nq = noms[q][0]
        if t == "costat":
            return tria(t, [f"{pr} était juste à côté {de_nom(nq)}, dans la même pièce.",
                            f"{pr} se trouvait tout à côté {de_nom(nq)}, dans la même pièce.",
                            f"{nq} était juste à côté {dlui}, dans la même pièce.",
                            f"{pr} était collé à {nq}, dans la même pièce." if m else f"{pr} était collée à {nq}, dans la même pièce.",
                            f"Il n'y avait aucune case entre {lui} et {nq}, dans la même pièce."])
        if t == "nord":
            return tria(t, [f"{pr} était au nord {de_nom(nq)}.", f"{pr} se trouvait plus au nord {que(nq)}.",
                            f"{nq} était au sud {dlui}.",
                            f"Sur le plan, {pr.lower()} était au-dessus {de_nom(nq)}.", f"{nq} se trouvait plus bas {qlui} sur le plan."])
        if t == "sud":
            return tria(t, [f"{pr} était au sud {de_nom(nq)}.", f"{pr} se trouvait plus au sud {que(nq)}.",
                            f"{nq} était au nord {dlui}.",
                            f"Sur le plan, {pr.lower()} était au-dessous {de_nom(nq)}.", f"{nq} se trouvait plus haut {qlui} sur le plan."])
        if t == "est":
            return tria(t, [f"{pr} était à l'est {de_nom(nq)}.", f"{pr} se trouvait plus à l'est {que(nq)}.",
                            f"{nq} était à l'ouest {dlui}.",
                            f"Sur le plan, {pr.lower()} était à droite {de_nom(nq)}.", f"{nq} se trouvait à sa gauche."])
        if t == "oest":
            return tria(t, [f"{pr} était à l'ouest {de_nom(nq)}.", f"{pr} se trouvait plus à l'ouest {que(nq)}.",
                            f"{nq} était à l'est {dlui}.",
                            f"Sur le plan, {pr.lower()} était à gauche {de_nom(nq)}.", f"{nq} se trouvait à sa droite."])
        if t == "diag":
            return tria(t, [f"{pr} était sur la même diagonale {que(nq)}.", f"{pr} partageait une diagonale avec {nq}.",
                            f"{nq} et {lui} étaient sur une même ligne diagonale.",
                            f"En traçant une diagonale depuis {nq}, on arrivait à {lui}.",
                            f"{nq} et {lui} formaient une diagonale."])
        if t == "cavall":
            return tria(t, [f"{pr} était à un saut de cavalier {de_nom(nq)} (comme aux échecs).",
                            f"{pr} se trouvait à un saut de cavalier {de_nom(nq)}.",
                            f"Par rapport à {nq}, {pr.lower()} était à un mouvement de cavalier.",
                            f"Un seul saut de cavalier séparait {nq} {dlui}."])
        if t == "mateixa_sala":
            return tria(t, [f"{pr} était dans la même pièce {que(nq)}.", f"{pr} partageait sa pièce avec {nq}.",
                            f"{nq} et {lui} étaient dans la même pièce.",
                            f"{pr} a croisé {nq} dans la même pièce.", f"{nq} et {lui} ont fini sous le même toit."])
        if t == "altra_sala":
            return tria(t, [f"{pr} n'était pas dans la même pièce {que(nq)}.",
                            f"{pr} ne partageait pas sa pièce avec {nq}.",
                            f"{pr} se trouvait dans une autre pièce {que(nq)}.",
                            f"{nq} et {lui} n'ont pas pu se croiser : ils étaient dans des pièces différentes.",
                            f"Entre {lui} et {nq}, il y avait au moins un mur."])
        if t == "sol_amb":
            return tria(t, [f"Seuls {lui} et {nq} étaient dans sa pièce.",
                            f"Dans sa pièce, il n'y avait {qlui} et {nq}.",
                            f"{pr} ne partageait sa pièce qu'avec {nq}.",
                            f"{nq} était sa seule compagnie dans cette pièce.", f"Dans sa pièce, personne d'autre que {nq}."])
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
    noms = {n[0].lower() for n in esc["_noms"].values()}
    ca = lang == "ca"
    enquadra = (["", "", "", "Segons un testimoni, ", "Un convidat recorda que ", "L'inspector va anotar que ",
                 "Algú va jurar que ", "A la llibreta de l'inspector consta que ", "Diuen que "] if ca else
                ["", "", "", "Selon un témoin, ", "Un invité se souvient que ", "L'inspecteur a noté que ",
                 "Quelqu'un a juré que ", "Dans le carnet de l'inspecteur, on lit que ", "On dit que "])
    out = []
    for cl in pistes:
        f = frase(lang, esc, cl, tria)
        if cl["t"] != "compte_sala" and f.split()[0].lower().strip(",") not in noms:
            w = tria("enquadra", enquadra)
            if w:
                f = f[0].lower() + f[1:]
                if not ca and w.endswith("que ") and f[0] in "aeiouhéèêàâîô":
                    w = w[:-4] + "qu'"
                f = w[0].upper() + w[1:] + f if False else w + f
                f = f[0].upper() + f[1:]
        out.append(f)
    return out


# ----------------------------------------------------------------- història d'introducció de cada cas
_INTRO = {
    "ca": {
        "s1": ["Una nit de tempesta {A}, {N} va ser {trobat} sense vida.",
               "Era gairebé mitjanit {A} quan van trobar {N} sense vida.",
               "Tot just havia sortit el sol {A} quan es va descobrir que {N} ja no respirava.",
               "Després d'una llarga vetllada {A}, ningú no va tornar a veure {N} amb vida.",
               "La festa acabava d'acabar-se {A} quan {N} va aparèixer {estes} a terra.",
               "Una tarda qualsevol {A}, un crit va trencar el silenci: {N} era {mort}.",
               "Les llums van parpellejar {A} i, quan van tornar, {N} ja era {mort}.",
               "Ningú no havia sentit res {A}, però {N} va ser {trobat} sense vida.",
               "L'endemà d'una nit sense lluna {A}, van descobrir {N} sense vida.",
               "Va ser un matí ben estrany {A}: {N} no responia, i ja no ho faria mai més."],
        "s2": ["Les portes eren tancades i només els sospitosos eren dins.",
               "Tots tenien una excusa, però només un deia la veritat.",
               "La policia va acordonar la zona i va prendre declaració a tothom.",
               "Ningú no podia marxar fins que s'aclarís el misteri.",
               "Cada testimoni recordava una cosa diferent, i les peces havien d'encaixar.",
               "L'inspector va obrir la llibreta i va començar a fer preguntes.",
               "Hi havia moltes declaracions, i cap de sola no ho explicava tot.",
               "Els sospitosos van repetir la seva història, cadascú a la seva manera."],
        "s3": ["Col·loca cada sospitós al seu lloc i descobreix qui era a la mateixa sala que {N}.",
               "Qui era a la mateixa sala que {N}? Les pistes ho diuen tot.",
               "Ordena les declaracions i troba l'assassí: l'únic que va quedar a la sala de {N}.",
               "L'assassí és qui va quedar tancat amb {N}. Ho pots deduir?",
               "Encaixa les pistes: només un sospitós era amb {N} quan va passar."],
    },
    "fr": {
        "s1": ["Par une nuit d'orage {A}, {N} a été {trouve} sans vie.",
               "Il était presque minuit {A} quand on a retrouvé {N} sans vie.",
               "Le soleil venait à peine de se lever {A} quand on a découvert que {N} ne respirait plus.",
               "Après une longue soirée {A}, personne n'a revu {N} en vie.",
               "La fête venait de se terminer {A} quand {N} est apparu{e} {etendu} par terre.",
               "Un après-midi tranquille {A}, un cri a déchiré le silence : {N} était {mort}.",
               "Les lumières ont clignoté {A} et, quand elles sont revenues, {N} était {mort}.",
               "Personne n'avait rien entendu {A}, mais {N} a été {trouve} sans vie.",
               "Au lendemain d'une nuit sans lune {A}, on a découvert {N} sans vie.",
               "Ce fut un matin étrange {A} : {N} ne répondait plus, et ne répondrait jamais plus."],
        "s2": ["Les portes étaient fermées et seuls les suspects se trouvaient à l'intérieur.",
               "Tous avaient une excuse, mais un seul disait la vérité.",
               "La police a bouclé les lieux et pris la déposition de chacun.",
               "Personne ne pouvait partir avant que le mystère ne soit éclairci.",
               "Chaque témoin se souvenait d'une chose différente, et les pièces devaient s'emboîter.",
               "L'inspecteur a ouvert son carnet et s'est mis à poser des questions.",
               "Il y avait beaucoup de témoignages, et aucun ne disait tout.",
               "Les suspects ont répété leur histoire, chacun à sa façon."],
        "s3": ["Place chaque suspect et découvre qui se trouvait dans la même pièce que {N}.",
               "Qui était dans la même pièce que {N} ? Les indices disent tout.",
               "Remets les déclarations en ordre et trouve le coupable : le seul resté dans la pièce de {N}.",
               "Le coupable est celui qui est resté enfermé avec {N}. Peux-tu le déduire ?",
               "Assemble les indices : un seul suspect était avec {N} au moment des faits."],
    },
}
_INTRO_K = {
    "ca": {"s1": ["Just abans del concert, {N} va desaparèixer sense deixar rastre.",
                  "A l'últim assaig, {N} va quedar-se sense veu i ningú no sabia per què.",
                  "Les llums de l'escenari es van apagar de cop i {N} ja no hi era.",
                  "Quan va acabar la cançó, {N} havia desaparegut entre bastidors."],
           "s2": ["Les amigues i els amics van buscar a totes les sales.",
                  "Tothom tenia una pista, i només una era la bona.",
                  "El concert havia de començar aviat, i calia resoldre-ho ràpid."],
           "s3": ["Col·loca cada amic al seu lloc i descobreix qui era a la mateixa sala que {N}.",
                  "Qui era amb {N}? Mira bé les pistes!"]},
    "fr": {"s1": ["Juste avant le concert, {N} a disparu sans laisser de trace.",
                  "À la dernière répétition, {N} a perdu sa voix et personne ne savait pourquoi.",
                  "Les lumières de la scène se sont éteintes d'un coup et {N} n'était plus là.",
                  "Quand la chanson s'est terminée, {N} avait disparu dans les coulisses."],
           "s2": ["Les amis ont cherché dans toutes les pièces.",
                  "Chacun avait un indice, et un seul était le bon.",
                  "Le concert allait bientôt commencer, il fallait vite résoudre l'énigme."],
           "s3": ["Place chaque ami à sa place et découvre qui était dans la même pièce que {N}.",
                  "Qui était avec {N} ? Regarde bien les indices !"]},
}


def intro(lang, titol, nom_v, genere_v, id_cas, kpop=False):
    """Petita història de tres frases per a un cas (estable per id). `titol` és el títol de l'escenari
    («Crim al far»); en treu el lloc («al far»)."""
    import random
    import zlib
    rng = random.Random(zlib.crc32((id_cas + lang).encode()))
    d = (_INTRO_K if kpop else _INTRO)[lang]
    lloc = titol.split(" ", 1)[1] if " " in titol else titol
    m = genere_v == "m"
    if lang == "ca":
        w = {"A": lloc, "N": nom_v, "trobat": "trobat" if m else "trobada", "estes": "estès" if m else "estesa",
             "mort": "mort" if m else "morta"}
    else:
        w = {"A": lloc, "N": nom_v, "trouve": "retrouvé" if m else "retrouvée", "etendu": "étendu" if m else "étendue",
             "mort": "mort" if m else "morte", "e": "" if m else "e"}
        w["trouve"] = "trouvé" if m else "trouvée"
    out = []
    for k in ("s1", "s2", "s3"):
        s = rng.choice(d[k]).format(**w)
        out.append(s[0].upper() + s[1:])
    return " ".join(out)
