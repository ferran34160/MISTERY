"""Escenaris: sales, objectes i personatges (originals, en català i francès).

Cada nom és (gènere, text). Gènere: "m" o "f".
"""

ESCENARIS = {
    "mas": {
        "titol": {"ca": "El crim del mas", "fr": "Le crime du mas"},
        "lloc": {"ca": "la finca", "fr": "la propriété"},
        "sales": {
            "cuina": {"nom": {"ca": ("f", "cuina"), "fr": ("f", "cuisine")},
                      "objs": ["taula", "llar", "cadira"]},
            "celler": {"nom": {"ca": ("m", "celler"), "fr": ("m", "cellier")},
                       "objs": ["barril", "armari"]},
            "porxo": {"nom": {"ca": ("m", "porxo"), "fr": ("m", "porche")},
                      "objs": ["banc", "carro"]},
            "hort": {"nom": {"ca": ("m", "hort"), "fr": ("m", "potager")},
                     "objs": ["figuera", "pou"]},
            "sala": {"nom": {"ca": ("f", "sala"), "fr": ("m", "salon")},
                     "objs": ["balanci", "armari", "cadira"]},
            "corral": {"nom": {"ca": ("m", "corral"), "fr": ("f", "basse-cour")},
                       "objs": ["carro", "pou"]},
        },
        "objectes": {
            "taula": {"bloqueja": True, "nom": {"ca": ("f", "taula"), "fr": ("f", "table")}},
            "llar": {"bloqueja": True, "nom": {"ca": ("f", "llar de foc"), "fr": ("f", "cheminée")}},
            "barril": {"bloqueja": True, "nom": {"ca": ("m", "barril"), "fr": ("m", "tonneau")}},
            "armari": {"bloqueja": True, "nom": {"ca": ("m", "armari"), "fr": ("f", "armoire")}},
            "figuera": {"bloqueja": True, "nom": {"ca": ("f", "figuera"), "fr": ("m", "figuier")}},
            "pou": {"bloqueja": True, "nom": {"ca": ("m", "pou"), "fr": ("m", "puits")}},
            "banc": {"bloqueja": False, "nom": {"ca": ("m", "banc"), "fr": ("m", "banc")}},
            "carro": {"bloqueja": False, "nom": {"ca": ("m", "carro"), "fr": ("f", "charrette")}},
            "balanci": {"bloqueja": False, "nom": {"ca": ("m", "balancí"), "fr": ("m", "fauteuil à bascule")}},
            "cadira": {"bloqueja": False, "nom": {"ca": ("f", "cadira"), "fr": ("f", "chaise")}},
        },
        "persones": [("Marçal", "m"), ("Rosa", "f"), ("Quim", "m"), ("Neus", "f"),
                     ("Blai", "m"), ("Remei", "f"), ("Teo", "m"), ("Elna", "f"),
                     ("Jaume", "m"), ("Aina", "f")],
    },
    "estacio": {
        "titol": {"ca": "Crim a l'estació", "fr": "Crime à la gare"},
        "lloc": {"ca": "l'estació", "fr": "la gare"},
        "sales": {
            "andana": {"nom": {"ca": ("f", "andana"), "fr": ("f", "quai")},
                   "objs": ['banc', 'fanal', 'carreto']},
            "taquilla": {"nom": {"ca": ("f", "taquilla"), "fr": ("m", "guichet")},
                   "objs": ['finestreta', 'cadira']},
            "espera": {"nom": {"ca": ("f", "sala d'espera"), "fr": ("f", "salle d'attente")},
                   "objs": ['banc', 'estufa', 'maleta']},
            "cafeteria": {"nom": {"ca": ("f", "cafeteria"), "fr": ("f", "buvette")},
                   "objs": ['barra', 'tamboret']},
            "magatzem": {"nom": {"ca": ("m", "magatzem"), "fr": ("m", "entrepôt")},
                   "objs": ['caixa', 'carreto']},
            "despatx": {"nom": {"ca": ("m", "despatx"), "fr": ("m", "bureau")},
                   "objs": ['escriptori', 'arxivador', 'cadira']},
        },
        "objectes": {
            "banc": {"bloqueja": False, "nom": {"ca": ("m", "banc"), "fr": ("m", "banc")}},
            "fanal": {"bloqueja": True, "nom": {"ca": ("m", "fanal"), "fr": ("m", "lampadaire")}},
            "carreto": {"bloqueja": False, "nom": {"ca": ("m", "carretó"), "fr": ("m", "chariot")}},
            "finestreta": {"bloqueja": True, "nom": {"ca": ("f", "finestreta"), "fr": ("m", "guichet")}},
            "cadira": {"bloqueja": False, "nom": {"ca": ("f", "cadira"), "fr": ("f", "chaise")}},
            "estufa": {"bloqueja": True, "nom": {"ca": ("f", "estufa"), "fr": ("m", "poêle")}},
            "maleta": {"bloqueja": False, "nom": {"ca": ("f", "maleta"), "fr": ("f", "valise")}},
            "barra": {"bloqueja": True, "nom": {"ca": ("f", "barra"), "fr": ("m", "comptoir")}},
            "tamboret": {"bloqueja": False, "nom": {"ca": ("m", "tamboret"), "fr": ("m", "tabouret")}},
            "caixa": {"bloqueja": True, "nom": {"ca": ("f", "caixa"), "fr": ("f", "caisse")}},
            "escriptori": {"bloqueja": True, "nom": {"ca": ("m", "escriptori"), "fr": ("m", "bureau")}},
            "arxivador": {"bloqueja": True, "nom": {"ca": ("m", "arxivador"), "fr": ("m", "classeur")}},
        },
        "persones": [('Oriol', 'm'), ('Carla', 'f'), ('Biel', 'm'), ('Mireia', 'f'), ('Pau', 'm'), ('Laia', 'f'), ('Arnau', 'm'), ('Berta', 'f'), ('Nil', 'm'), ('Gal·la', 'f')],
    },
    "teatre": {
        "titol": {"ca": "Mort al teatre", "fr": "Mort au théâtre"},
        "lloc": {"ca": "l'edifici", "fr": "l'édifice"},
        "sales": {
            "escenari": {"nom": {"ca": ("m", "escenari"), "fr": ("f", "scène")},
                   "objs": ['piano', 'tel']},
            "platea": {"nom": {"ca": ("f", "platea"), "fr": ("m", "parterre")},
                   "objs": ['butaca', 'sofa']},
            "camerino": {"nom": {"ca": ("m", "camerino"), "fr": ("f", "loge")},
                   "objs": ['mirall', 'maniqui', 'tamboret']},
            "vestibul": {"nom": {"ca": ("m", "vestíbul"), "fr": ("m", "foyer")},
                   "objs": ['sofa', 'bagul']},
            "bambolines": {"nom": {"ca": ("f", "tramoia"), "fr": ("f", "coulisse")},
                   "objs": ['escala', 'bagul']},
            "cabina": {"nom": {"ca": ("f", "cabina de llum"), "fr": ("f", "cabine technique")},
                   "objs": ['reflector', 'tamboret']},
        },
        "objectes": {
            "piano": {"bloqueja": True, "nom": {"ca": ("m", "piano"), "fr": ("m", "piano")}},
            "tel": {"bloqueja": True, "nom": {"ca": ("m", "teló"), "fr": ("m", "rideau")}},
            "butaca": {"bloqueja": False, "nom": {"ca": ("f", "butaca"), "fr": ("m", "fauteuil")}},
            "sofa": {"bloqueja": False, "nom": {"ca": ("m", "sofà"), "fr": ("m", "canapé")}},
            "mirall": {"bloqueja": True, "nom": {"ca": ("m", "mirall"), "fr": ("m", "miroir")}},
            "maniqui": {"bloqueja": True, "nom": {"ca": ("m", "maniquí"), "fr": ("m", "mannequin")}},
            "tamboret": {"bloqueja": False, "nom": {"ca": ("m", "tamboret"), "fr": ("m", "tabouret")}},
            "bagul": {"bloqueja": False, "nom": {"ca": ("m", "bagul"), "fr": ("f", "malle")}},
            "escala": {"bloqueja": True, "nom": {"ca": ("f", "escala"), "fr": ("f", "échelle")}},
            "reflector": {"bloqueja": True, "nom": {"ca": ("m", "reflector"), "fr": ("m", "projecteur")}},
        },
        "persones": [('Xavi', 'm'), ('Mercè', 'f'), ('Roc', 'm'), ('Júlia', 'f'), ('Eudald', 'm'), ('Dolors', 'f'), ('Lluc', 'm'), ('Maia', 'f'), ('Ivo', 'm'), ('Violant', 'f')],
    },
}


# Noms de persona per lletra (A..J i V): el sospitós A té un nom que comença per A, etc.
# Servei per a tots els escenaris; cada cas en tria un a l'atzar per lletra. (nom, gènere)
NOMS_LLETRA = {
    "A": [("Aleix", "m"), ("Anna", "f"), ("Arnau", "m"), ("Aina", "f")],
    "B": [("Biel", "m"), ("Berta", "f"), ("Blai", "m"), ("Bruna", "f")],
    "C": [("Carles", "m"), ("Clara", "f"), ("Cesc", "m"), ("Carla", "f")],
    "D": [("Dídac", "m"), ("Dolors", "f"), ("David", "m"), ("Delfina", "f")],
    "E": [("Eudald", "m"), ("Elna", "f"), ("Enric", "m"), ("Eulàlia", "f")],
    "F": [("Ferran", "m"), ("Francesca", "f"), ("Felip", "m"), ("Fina", "f"), ("Fabiola", "f"), ("Fanny", "f")],
    "G": [("Gerard", "m"), ("Griselda", "f"), ("Guerau", "m"), ("Guillem", "m"), ("Glòria", "f"), ("Gemma", "f")],
    "H": [("Hug", "m"), ("Helena", "f"), ("Hèctor", "m"), ("Heura", "f")],
    "I": [("Ivo", "m"), ("Irene", "f"), ("Ignasi", "m"), ("Isidre", "m"), ("Isabel", "f"), ("Imma", "f")],
    "J": [("Jaume", "m"), ("Júlia", "f"), ("Jordi", "m"), ("Judit", "f")],
    "V": [("Valentí", "m"), ("Violant", "f"), ("Vicenç", "m"), ("Vera", "f")],
}


# ---------------------------------------------------------------------------
# Escenaris addicionals (definits de forma compacta). Cada objecte té un nom
# genèric (ca, gènere ca, fr, gènere fr, bloqueja) i una icona a index.html.
# ---------------------------------------------------------------------------
_OBJ = {
    "taula": ("taula", "f", "table", "f", True), "cadira": ("cadira", "f", "chaise", "f", False),
    "banc": ("banc", "m", "banc", "m", False), "barril": ("barril", "m", "tonneau", "m", True),
    "caixa": ("caixa", "f", "caisse", "f", True), "bagul": ("bagul", "m", "malle", "f", False),
    "escala": ("escala", "f", "échelle", "f", True), "armari": ("armari", "m", "armoire", "f", True),
    "estufa": ("estufa", "f", "poêle", "m", True), "llar": ("llar de foc", "f", "cheminée", "f", True),
    "escriptori": ("escriptori", "m", "bureau", "m", True), "arxivador": ("arxivador", "m", "classeur", "m", True),
    "maleta": ("maleta", "f", "valise", "f", False), "sofa": ("sofà", "m", "canapé", "m", False),
    "butaca": ("butaca", "f", "fauteuil", "m", False), "mirall": ("mirall", "m", "miroir", "m", True),
    "piano": ("piano", "m", "piano", "m", True), "tamboret": ("tamboret", "m", "tabouret", "m", False),
    "barra": ("barra", "f", "comptoir", "m", True), "carreto": ("carretó", "m", "chariot", "m", False),
    "carro": ("carro", "m", "charrette", "f", False), "reflector": ("reflector", "m", "projecteur", "m", True),
    "finestreta": ("finestreta", "f", "guichet", "m", True), "pou": ("pou", "m", "puits", "m", True),
    "figuera": ("arbre", "m", "arbre", "m", True), "maniqui": ("maniquí", "m", "mannequin", "m", True),
    "fanal": ("fanal", "m", "lampadaire", "m", True), "tel": ("teló", "m", "rideau", "m", True),
    "timo": ("timó", "m", "barre", "f", True), "ancora": ("àncora", "f", "ancre", "f", True),
    "llit": ("llit", "m", "lit", "m", False), "planta": ("planta", "f", "plante", "f", True),
    "llibreria": ("llibreria", "f", "bibliothèque", "f", True), "quadre": ("quadre", "m", "tableau", "m", True),
    "vitrina": ("vitrina", "f", "vitrine", "f", True), "estatua": ("estàtua", "f", "statue", "f", True),
    "tron": ("tron", "m", "trône", "m", False), "torxa": ("torxa", "f", "torche", "f", True),
    "armadura": ("armadura", "f", "armure", "f", True), "pupitre": ("pupitre", "m", "pupitre", "m", False),
    "pissarra": ("pissarra", "f", "tableau noir", "m", True), "pilota": ("pilota", "f", "ballon", "m", False),
    "bola": ("bola d'equilibri", "f", "boule d'équilibre", "f", False),
    # segon lot d'objectes (24)
    "nevera": ("nevera", "f", "frigo", "m", True), "forn": ("forn", "m", "four", "m", True),
    "pica": ("pica", "f", "évier", "m", True), "banyera": ("banyera", "f", "baignoire", "f", True),
    "vater": ("vàter", "m", "W.-C.", "m", True), "rentadora": ("rentadora", "f", "lave-linge", "m", True),
    "bascula": ("bàscula", "f", "balance", "f", False), "cafetera": ("cafetera", "f", "machine à café", "f", True),
    "billar": ("billar", "m", "billard", "m", True), "escacs": ("tauler d'escacs", "m", "échiquier", "m", False),
    "caixareg": ("caixa registradora", "f", "caisse enregistreuse", "f", True), "celler": ("rac de vins", "m", "casier à vins", "m", True),
    "fogata": ("fogata", "f", "feu de camp", "m", True), "tenda": ("tenda de campanya", "f", "tente", "f", True),
    "motxilla": ("motxilla", "f", "sac à dos", "m", False), "caiac": ("canoa", "f", "canoë", "m", False),
    "cistell": ("cistell de fruita", "m", "panier de fruits", "m", False), "bicicleta": ("bicicleta", "f", "vélo", "m", False),
    "tractor": ("tractor", "m", "tracteur", "m", True), "bustia": ("bústia", "f", "boîte aux lettres", "f", True),
    "rellotge": ("rellotge de peu", "m", "horloge", "f", True), "gabia": ("gàbia", "f", "cage", "f", True),
    "telefon": ("telèfon", "m", "téléphone", "m", True), "globus": ("globus terraqüi", "m", "globe", "m", True),
}


def _registra(clau, titol, lloc, sales):
    """sales: llista de (clau, (gca, ca), (gfr, fr), [objectes])."""
    usats = {o for s in sales for o in s[3]}
    ESCENARIS[clau] = {
        "titol": {"ca": titol[0], "fr": titol[1]},
        "lloc": {"ca": lloc[0], "fr": lloc[1]},
        "sales": {k: {"nom": {"ca": ca, "fr": fr}, "objs": objs} for k, ca, fr, objs in sales},
        "objectes": {k: {"bloqueja": _OBJ[k][4],
                         "nom": {"ca": (_OBJ[k][1], _OBJ[k][0]), "fr": (_OBJ[k][3], _OBJ[k][2])}}
                     for k in sorted(usats)},
        "persones": [],
    }


_registra("vaixell", ("Crim al vaixell", "Crime sur le navire"), ("la nau", "la nef"), [
    ("coberta", ("f", "coberta"), ("m", "pont"), ["timo", "ancora", "barril"]),
    ("camarot", ("m", "camarot"), ("f", "cabine"), ["llit", "bagul", "cadira"]),
    ("galera", ("f", "galera"), ("f", "cambuse"), ["taula", "estufa", "caixa"]),
    ("bodega", ("f", "bodega"), ("f", "cale"), ["barril", "caixa", "bagul"]),
    ("passarella", ("f", "passarel·la"), ("f", "passerelle"), ["timo", "escriptori", "cadira"]),
    ("maquines", ("f", "sala de màquines"), ("f", "salle des machines"), ["estufa", "escala", "carreto"])])
_registra("hotel", ("Crim a l'hotel", "Crime à l'hôtel"), ("l'hotel", "l'hôtel"), [
    ("recepcio", ("f", "recepció"), ("f", "réception"), ["barra", "maleta", "sofa"]),
    ("habitacio", ("f", "habitació"), ("f", "chambre"), ["llit", "armari", "cadira"]),
    ("bar", ("m", "bar"), ("m", "bar"), ["barra", "tamboret", "mirall"]),
    ("cuina", ("f", "cuina"), ("f", "cuisine"), ["taula", "estufa", "caixa"]),
    ("terrassa", ("f", "terrassa"), ("f", "terrasse"), ["banc", "planta", "taula"]),
    ("biblioteca", ("f", "biblioteca"), ("f", "bibliothèque"), ["llibreria", "butaca", "escala"])])
_registra("museu", ("Crim al museu", "Crime au musée"), ("l'edifici", "l'édifice"), [
    ("vestibul", ("m", "vestíbul"), ("m", "hall"), ["banc", "planta", "finestreta"]),
    ("galeria", ("f", "galeria"), ("f", "galerie"), ["quadre", "vitrina", "banc"]),
    ("estatues", ("f", "sala d'estàtues"), ("f", "salle des statues"), ["estatua", "banc", "vitrina"]),
    ("taller", ("m", "taller de restauració"), ("m", "atelier"), ["taula", "escala", "caixa"]),
    ("magatzem", ("m", "magatzem"), ("f", "réserve"), ["caixa", "bagul", "carreto"]),
    ("despatx", ("m", "despatx"), ("m", "bureau"), ["escriptori", "arxivador", "cadira"])])
_registra("castell", ("Crim al castell", "Crime au château"), ("la fortalesa", "la forteresse"), [
    ("tron", ("f", "sala del tron"), ("f", "salle du trône"), ["tron", "taula", "torxa"]),
    ("cuina", ("f", "cuina"), ("f", "cuisine"), ["llar", "taula", "barril"]),
    ("calabos", ("m", "calabós"), ("m", "cachot"), ["torxa", "banc", "caixa"]),
    ("torre", ("f", "torre"), ("f", "tour"), ["escala", "torxa", "bagul"]),
    ("jardi", ("m", "jardí"), ("m", "jardin"), ["pou", "banc", "figuera"]),
    ("armeria", ("f", "armeria"), ("f", "armurerie"), ["armadura", "caixa", "taula"])])
_registra("escola", ("Crim a l'escola", "Crime à l'école"), ("l'escola", "l'école"), [
    ("aula", ("f", "aula"), ("f", "classe"), ["pupitre", "pissarra", "cadira"]),
    ("gimnas", ("m", "gimnàs"), ("m", "gymnase"), ["pilota", "banc", "caixa"]),
    ("biblioteca", ("f", "biblioteca"), ("f", "bibliothèque"), ["llibreria", "taula", "escala"]),
    ("menjador", ("m", "menjador"), ("m", "réfectoire"), ["taula", "banc", "barra"]),
    ("pati", ("m", "pati"), ("f", "cour"), ["figuera", "banc", "pou"]),
    ("despatx", ("m", "despatx"), ("m", "bureau"), ["escriptori", "arxivador", "cadira"])])
_registra("restaurant", ("Crim al restaurant", "Crime au restaurant"), ("l'establiment", "l'établissement"), [
    ("menjador", ("m", "menjador"), ("f", "salle"), ["taula", "cadira", "planta"]),
    ("cuina", ("f", "cuina"), ("f", "cuisine"), ["estufa", "taula", "caixa"]),
    ("terrassa", ("f", "terrassa"), ("f", "terrasse"), ["tamboret", "taula", "planta"]),
    ("celler", ("m", "celler"), ("m", "cellier"), ["barril", "caixa", "escala"]),
    ("bar", ("m", "bar"), ("m", "bar"), ["barra", "tamboret", "mirall"]),
    ("despatx", ("m", "despatx"), ("m", "bureau"), ["escriptori", "arxivador", "cadira"])])
_registra("circ", ("Crim al circ", "Crime au cirque"), ("la carpa", "la tente"), [
    ("pista", ("f", "pista"), ("f", "piste"), ["bola", "reflector", "tamboret"]),
    ("tribuna", ("f", "tribuna"), ("f", "tribune"), ["banc", "butaca", "planta"]),
    ("caravana", ("f", "caravana"), ("f", "roulotte"), ["llit", "armari", "taula"]),
    ("quadra", ("f", "quadra"), ("f", "écurie"), ["caixa", "carro", "barril"]),
    ("taquilla", ("f", "taquilla"), ("f", "billetterie"), ["finestreta", "cadira", "banc"]),
    ("magatzem", ("m", "magatzem"), ("m", "entrepôt"), ["bagul", "maniqui", "escala"])])
_registra("mansio", ("Crim a la mansió", "Crime au manoir"), ("la mansió", "la demeure"), [
    ("vestibul", ("m", "vestíbul"), ("m", "vestibule"), ["mirall", "planta", "banc"]),
    ("menjador", ("m", "menjador"), ("f", "salle à manger"), ["taula", "cadira", "llar"]),
    ("saloo", ("m", "saló"), ("m", "salon"), ["piano", "sofa", "butaca"]),
    ("cuina", ("f", "cuina"), ("f", "cuisine"), ["estufa", "taula", "caixa"]),
    ("estudi", ("m", "estudi"), ("m", "cabinet"), ["escriptori", "llibreria", "arxivador"]),
    ("jardi", ("m", "jardí d'hivern"), ("m", "jardin d'hiver"), ["planta", "figuera", "banc"])])
_registra("mercat", ("Crim al mercat", "Crime au marché"), ("la plaça", "la place"), [
    ("fruita", ("f", "parada de fruita"), ("m", "étal de fruits"), ["caixa", "taula", "tamboret"]),
    ("peix", ("f", "peixateria"), ("f", "poissonnerie"), ["barra", "barril", "caixa"]),
    ("forn", ("m", "forn"), ("f", "boulangerie"), ["estufa", "taula", "cadira"]),
    ("cafe", ("m", "cafè"), ("m", "café"), ["barra", "tamboret", "mirall"]),
    ("magatzem", ("m", "magatzem"), ("m", "entrepôt"), ["carro", "caixa", "bagul"]),
    ("oficina", ("f", "oficina"), ("m", "bureau"), ["escriptori", "arxivador", "cadira"])])


# --- escenaris definits a escenaris_extra.py ---------------------------------
def _prep(tag, lang):
    """'El castell' -> 'al castell' (ca) / 'au château' (fr), per fer el títol «Crim al castell»."""
    art, _, resta = tag.partition(" ") if not tag.startswith(("L'", "l'")) else (tag[:2], "", tag[2:])
    if lang == "ca":
        return {"El": "al " + resta, "La": "a la " + resta, "L'": "a l'" + resta}[art]
    return {"Le": "au " + resta, "La": "à la " + resta, "L'": "à l'" + resta}[art]


def _carrega_extra():
    from escenaris_extra import llegeix
    for e in llegeix():
        tag_ca, tag_fr = e["tag"]
        _registra(e["clau"],
                  ("Crim " + _prep(tag_ca, "ca"), "Crime " + _prep(tag_fr, "fr")),
                  e["lloc"],
                  [("s%d" % i, ca, fr, objs) for i, (ca, fr, objs) in enumerate(e["sales"])])
        ESCENARIS[e["clau"]]["tag"] = {"ca": tag_ca, "fr": tag_fr}


_carrega_extra()


# --- mode K-pop (només per a ús personal; no entra a la col·lecció normal) ---------------------
_OBJ.update({
    "micro": ("micròfon", "m", "micro", "m", False), "lightstick": ("bastó lluminós", "m", "light stick", "m", False),
    "enceinte": ("altaveu", "m", "enceinte", "f", True), "projecteur": ("projector d'escena", "m", "projecteur", "m", True),
    "ampli": ("amplificador", "m", "ampli", "m", True), "synthe": ("sintetitzador", "m", "synthé", "m", True),
    "console": ("taula de DJ", "f", "console DJ", "f", True), "miroirloge": ("mirall de camerino", "m", "miroir de loge", "m", True),
    "valise": ("maleta de gira", "f", "valise", "f", False), "peluche": ("peluix de tigre", "m", "peluche", "f", False),
    "ramen": ("bol de ramen", "m", "bol de ramen", "m", False), "bubble": ("bubble tea", "m", "bubble tea", "m", False),
    "photocards": ("expositor de fotocards", "m", "présentoir", "m", True), "affiche": ("pòster", "m", "affiche", "f", True),
    "camera": ("càmera", "f", "caméra", "f", True), "canape": ("sofà rosa", "m", "canapé rose", "m", False),
    "cadeau": ("caixa de regal", "f", "boîte cadeau", "f", False), "lanterne": ("llanterna coreana", "f", "lanterne", "f", True),
    "eventail": ("ventall", "m", "éventail", "m", False), "epee": ("espasa màgica", "f", "épée magique", "f", False),
    "chapeau": ("barret gat", "m", "chapeau gat", "m", False), "cerisier": ("cirerer en flor", "m", "cerisier", "m", True),
    "distributeur": ("màquina de snacks", "f", "distributeur", "m", True),
})
_registra("kpop", ("Missió K-pop", "Mission K-pop"), ("l'escenari", "la scène"), [
    ("escena", ("f", "escena"), ("f", "scène"), ["projecteur", "micro", "enceinte"]),
    ("camerinos", ("m", "camerino"), ("f", "loge"), ["miroirloge", "canape", "valise", "peluche", "photocards"]),
    ("estudi", ("m", "estudi de gravació"), ("m", "studio"), ["console", "synthe", "ampli", "camera"]),
    ("assaig", ("f", "sala d'assaig"), ("f", "salle de danse"), ["eventail", "epee", "lightstick", "affiche"]),
    ("terrat", ("m", "terrat"), ("m", "toit"), ["cerisier", "lanterne", "chapeau"]),
    ("cuina", ("f", "cuina"), ("f", "cuisine"), ["ramen", "bubble", "distributeur", "cadeau"])])
ESCENARIS["kpop"]["tag"] = {"ca": "El K-pop", "fr": "Le K-pop"}
ESCENARIS["kpop"]["especial"] = True

# personatges (nom, gènere) per inicial; en un cas no se'n repeteix cap inicial
KPOP_PERSONATGES = {"R": [("Rumi", "f"), ("Romance", "m")], "M": [("Mira", "f"), ("Mystery", "m")],
                    "Z": [("Zoey", "f")], "J": [("Jinu", "m")], "A": [("Abby", "m")],
                    "B": [("Baby", "m"), ("Bobby", "m")], "G": [("Gwi-Ma", "m")],
                    "D": [("Derpy", "m")], "S": [("Sussie", "f")]}


# --- escenari de la casa d'estiu (el cas dissenyat per l'usuari; no entra a la col·lecció de 3 per escenari) ---
_registra("estiu", ("Crim a la casa d'estiu", "Crime à la maison d'été"), ("la casa", "la maison"), [
    ("cuina", ("f", "cuina d'estiu"), ("f", "cuisine d'été"), ["taula"]),
    ("menjador", ("m", "menjador"), ("f", "salle à manger"), ["taula", "cadira"]),
    ("passadis", ("m", "passadís"), ("m", "couloir"), []),
    ("porxo", ("m", "porxo"), ("m", "porche"), ["estatua"]),
    ("piscina", ("f", "piscina"), ("f", "piscine"), ["planta"]),
    ("terrassa", ("f", "terrassa"), ("f", "terrasse"), ["planta"])])
ESCENARIS["estiu"]["tag"] = {"ca": "La casa d'estiu", "fr": "La maison d'été"}
ESCENARIS["estiu"]["especial"] = True

# --- objectes del segon lot: s'afegeixen a les sales on encaixen pel nom -------------------------
_NOUS = [
    (("cuina",), ["nevera", "forn", "pica"]),
    (("forn", "obrador"), ["forn", "pica"]),
    (("cafeteria", "cafè", "bar", "restaurant", "menjador", "refectori"), ["cafetera"]),
    (("vestuari", "sauna", "massatges", "solàrium"), ["banyera", "bascula", "vater"]),
    (("soterrani", "garatge", "hangar"), ["rentadora", "bicicleta"]),
    (("sala de joc", "taverna", "saló", "sala comuna", "discoteca"), ["billar", "escacs"]),
    (("botiga", "taquilla", "recepció", "caixa", "taulell", "parada", "barra", "consigna"), ["caixareg"]),
    (("celler", "tast", "bodega", "trull", "vinya"), ["celler"]),
    (("campament", "foguera", "tenda gran", "carpa"), ["fogata", "tenda", "motxilla"]),
    (("hort", "hivernacle", "parada de fruita", "peixateria"), ["cistell", "tractor"]),
    (("era", "graner", "cobert", "corral", "estable", "quadra"), ["tractor"]),
    (("pati", "passeig", "mirador", "porxo"), ["bicicleta", "bascula"]),
    (("moll", "fossat", "hangar", "port"), ["caiac"]),
    (("entrada", "vestíbul", "passadís"), ["bustia", "rellotge"]),
    (("recepció", "oficina", "despatx", "redacció", "cabina", "sala de control"), ["telefon"]),
    (("sala d'espera", "terminal", "saló", "sala principal"), ["rellotge"]),
    (("estudi", "biblioteca", "lectura", "despatx del director", "sala de reunions", "scriptorium"), ["globus"]),
    (("casa", "sala infantil", "sala comuna", "saló"), ["gabia"]),
]


def _amplia():
    for e in ESCENARIS.values():
        if e.get("especial"):
            continue
        for s in e["sales"].values():
            nom = s["nom"]["ca"][1].lower()
            for claus, objs in _NOUS:
                if any(nom == k or nom.startswith(k + " ") or (len(k) > 4 and k in nom) for k in claus):
                    for o in objs:
                        if o not in s["objs"] and len(s["objs"]) < 6:
                            s["objs"].append(o)
        usats = {o for s in e["sales"].values() for o in s["objs"]}
        for k in usats:
            if k not in e["objectes"]:
                e["objectes"][k] = {"bloqueja": _OBJ[k][4],
                                    "nom": {"ca": (_OBJ[k][1], _OBJ[k][0]), "fr": (_OBJ[k][3], _OBJ[k][2])}}


_amplia()
