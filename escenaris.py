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
}
