"""Quins objectes encaixen a cada tipus de sala (per a `reskin.py`): evita taules a un vaixell on no toquen,
sofàs en un magatzem, etc. El tipus de sala es deriva del nom català de la sala."""
import re

# (tipus, expressió regular sobre el nom de la sala en minúscules)
TIPUS = [
    ("cuina", r"cuina|obrador|forn\b|fleca|peixateria|galera"),
    ("bany", r"vestuari|sauna|massatges|solàrium|bany|lavabo|emprovador|vestidor"),
    ("celler", r"celler|bodega|trull|cambra freda|vinya"),
    ("menjador", r"menjador|restaurant|refectori|cafeteria|cafè|\bbar\b|barra|taverna|sala de tast"),
    ("dormitori", r"dormitori|habitació|camarot|cambra reial|cambra\b|caravana|vagó llit|campament"),
    ("biblioteca", r"biblioteca|arxiu|scriptorium|lectura|sala d'estudi"),
    ("oficina", r"despatx|oficina|redacció|rectoria|reunions|control|comandament|cabina del revisor|\bestudi\b"),
    ("escola", r"aula|gimnàs|sala infantil"),
    ("teatre", r"escena|escenari|platea|golfa|camerino|tribuna|pista|carpa|carrusel|plató|discoteca|tramoia|sala de joc|estudi de gravació|sala d'assaig"),
    ("antic", r"calabós|presó|torre\b|capella|santuari|sagristia|cripta|armeria|tron|campanar|cambra del tresor|caixa forta|cambra cuirassada|claustre"),
    ("museu", r"estàtues|miralls|subhastes|taller de restauració|aparador|sala de proves"),
    ("botiga", r"botiga|taquilla|taulell|parada|consigna|terminal|caixa\b|cabina|sala de la llanterna"),
    ("nautic", r"coberta|passarel|moll\b|fossat|nau\b|cúpula|plataforma"),
    ("exterior", r"jardí|terrassa|terrat|pati|porxo|porxada|passeig|hort|\bera\b|mirador|plaça|parc|hivernacle|foguera|tenda gran|corral|estable|quadra|solàrium|\bcasa\b"),
    ("magatzem", r"magatzem|soterrani|garatge|hangar|taller|cobert|graner|impremta|laboratori|màquines|motors|torpedes|locomotora|vagó d'equipatges|andana"),
    ("saló", r"saló|vestíbul|recepció|galeria|\bsala\b|passadís|entrada|sala principal|sala comuna|sala privada|sala d'espera|santuari|vagó saló|sala de|piscina"),
]

# objectes que hi encaixen (a més dels que ja té la sala a l'escenari)
POOL = {
    "cuina": "taula estufa forn pica nevera cafetera armari caixa barril tamboret cadira cistell planta rellotge",
    "bany": "banyera vater pica rentadora bascula mirall banc armari planta tamboret",
    "celler": "barril caixa celler escala bagul tamboret taula torxa",
    "menjador": "catifa taula cadira tamboret barra cafetera planta mirall quadre rellotge celler banc llar",
    "dormitori": "catifa llit armari cadira bagul mirall maleta escriptori butaca quadre planta rellotge telefon estufa",
    "biblioteca": "catifa llibreria escala butaca taula escriptori globus planta quadre rellotge pupitre arxivador tamboret",
    "oficina": "catifa escriptori arxivador cadira butaca maleta telefon planta globus quadre armari llibreria rellotge caixa",
    "escola": "pupitre pissarra pilota bola balanci banc escala planta armari cadira",
    "teatre": "catifa reflector tel tamboret piano butaca sofa maniqui mirall bola pilota balanci banc planta",
    "antic": "torxa armadura tron banc bagul caixa barril escala estatua taula cadira vitrina quadre",
    "museu": "catifa vitrina estatua quadre banc maniqui escala mirall armadura planta",
    "botiga": "caixareg finestreta barra banc maleta carreto caixa rellotge bustia cadira tamboret bascula",
    "nautic": "timo ancora caiac barril caixa bagul escala fanal carreto banc",
    "exterior": "banc planta figuera fanal pou estatua torxa taula cadira tamboret bicicleta caiac fogata tenda motxilla carro tractor",
    "magatzem": "caixa barril bagul escala carreto carro armari taula tamboret estufa arxivador rentadora maleta",
    "saló": "catifa sofa butaca mirall quadre vitrina estatua planta rellotge piano taula cadira banc maleta bustia telefon escacs billar gabia",
}
GENERIC = "planta caixa banc taula cadira armari quadre tamboret"
_RE = [(t, re.compile(r)) for t, r in TIPUS]


def tipus_sala(nom_ca):
    n = nom_ca.lower()
    for t, rx in _RE:
        if rx.search(n):
            return t
    return None


def permesos(nom_ca, objs_sala):
    """Conjunt d'objectes que hi encaixen: els de la sala segons l'escenari + el seu tipus."""
    t = tipus_sala(nom_ca)
    return set(objs_sala) | set((POOL.get(t) or GENERIC).split())

# objectes del mode K-pop (només s'usen als casos K-pop)
KPOP = set("micro lightstick enceinte projecteur ampli synthe console miroirloge valise peluche ramen bubble photocards "
           "affiche camera canape cadeau lanterne eventail epee chapeau cerisier distributeur".split())

# objectes que s'agrupen en una sola peça de diverses caselles (taules, escriptoris, barres, catifes…)
MERGE = {"taula", "escriptori", "barra", "catifa"}
