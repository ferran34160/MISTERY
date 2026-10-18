"""Escenaris addicionals (només canvien noms de sales, objectes i colors; la lògica del cas no depèn de l'escenari).

Format de cada línia: clau ; etiqueta ca ; etiqueta fr ; lloc ca ; lloc fr ; sales
Sala: "g nom ca|g nom fr|obj,obj,obj" (g = m/f). Els objectes són claus d'escenaris._OBJ (cada una té la seva icona).
"""

DADES = """
far;El far;Le phare;l'edifici;l'édifice;f sala de la llanterna|f salle de la lanterne|reflector,escala,tamboret
 ;;;;;f cuina|f cuisine|taula,estufa,cadira
 ;;;;;m dormitori|f chambre|llit,armari,bagul
 ;;;;;m magatzem|f réserve|caixa,barril,carreto
 ;;;;;f plataforma|f plateforme|banc,fanal,planta
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
port;El port;Le port;la dàrsena;le bassin;m moll|m quai|carreto,caixa,fanal
 ;;;;;m magatzem|m entrepôt|barril,caixa,escala
 ;;;;;f taverna|f taverne|barra,tamboret,taula
 ;;;;;f oficina|m bureau|escriptori,arxivador,cadira
 ;;;;;f coberta|m pont|timo,ancora,bagul
 ;;;;;m passeig|f promenade|banc,fanal,planta
mina;La mina;La mine;la galeria;la galerie;f galeria|f galerie|torxa,carreto,caixa
 ;;;;;f sala de màquines|f salle des machines|estufa,escala,barril
 ;;;;;m campament|m campement|llit,taula,cadira
 ;;;;;m magatzem|m dépôt|caixa,bagul,carro
 ;;;;;f oficina|m bureau|escriptori,arxivador,cadira
 ;;;;;f entrada|f entrée|fanal,banc,carreto
observatori;L'observatori;L'observatoire;l'edifici;l'édifice;f cúpula|f coupole|reflector,escala,tamboret
 ;;;;;f biblioteca|f bibliothèque|llibreria,butaca,taula
 ;;;;;m taller|m atelier|taula,caixa,escala
 ;;;;;m dormitori|f chambre|llit,armari,cadira
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m jardí|m jardin|planta,banc,figuera
taverna;La taverna;La taverne;la taverna;la taverne;f sala|f salle|taula,banc,llar
 ;;;;;f barra|m comptoir|barra,tamboret,barril
 ;;;;;f cuina|f cuisine|estufa,taula,caixa
 ;;;;;m celler|m cellier|barril,caixa,escala
 ;;;;;f habitació|f chambre|llit,armari,bagul
 ;;;;;m pati|f cour|pou,banc,carro
cinema;El cinema;Le cinéma;l'edifici;l'édifice;f sala|f salle|butaca,sofa,reflector
 ;;;;;m vestíbul|m hall|banc,planta,mirall
 ;;;;;f taquilla|f billetterie|finestreta,cadira,banc
 ;;;;;f cabina|f cabine|reflector,escala,tamboret
 ;;;;;m magatzem|m entrepôt|caixa,bagul,maniqui
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
banc;El banc;La banque;l'edifici;l'édifice;m vestíbul|m hall|banc,planta,finestreta
 ;;;;;f cambra cuirassada|f chambre forte|caixa,bagul,arxivador
 ;;;;;m despatx del director|m bureau du directeur|escriptori,butaca,llibreria
 ;;;;;f sala de reunions|f salle de réunion|taula,cadira,pissarra
 ;;;;;f sala d'espera|f salle d'attente|sofa,butaca,planta
 ;;;;;m arxiu|f archive|arxivador,escala,caixa
joieria;La joieria;La bijouterie;l'edifici;l'édifice;f botiga|f boutique|vitrina,barra,tamboret
 ;;;;;m taller|m atelier|taula,estufa,caixa
 ;;;;;f caixa forta|m coffre|bagul,caixa,arxivador
 ;;;;;m despatx|m bureau|escriptori,cadira,llibreria
 ;;;;;f sala de proves|m salon d'essayage|mirall,sofa,planta
 ;;;;;m magatzem|f réserve|armari,caixa,carreto
pastisseria;La pastisseria;La pâtisserie;l'establiment;l'établissement;m obrador|m laboratoire|taula,estufa,barril
 ;;;;;f botiga|f boutique|vitrina,barra,tamboret
 ;;;;;f terrassa|f terrasse|taula,planta,cadira
 ;;;;;m magatzem|f réserve|caixa,armari,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;f cambra freda|f chambre froide|caixa,barril,carreto
botiga de llibres;La llibreria;La librairie;l'establiment;l'établissement;f botiga|f boutique|llibreria,taula,escala
 ;;;;;m magatzem|f réserve|caixa,llibreria,carreto
 ;;;;;f sala de lectura|f salle de lecture|butaca,sofa,planta
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m soterrani|m sous-sol|barril,bagul,escala
 ;;;;;m aparador|f vitrine|vitrina,mirall,tamboret
spa;El balneari;Le spa;l'edifici;l'édifice;f piscina|f piscine|banc,planta,pou
 ;;;;;f sauna|m sauna|banc,estufa,barril
 ;;;;;f recepció|f réception|barra,sofa,planta
 ;;;;;f sala de massatges|f salle de massage|llit,mirall,tamboret
 ;;;;;m bar|m bar|barra,tamboret,taula
 ;;;;;m vestuari|m vestiaire|armari,banc,mirall
casino;El casino;Le casino;l'edifici;l'édifice;f sala de joc|f salle de jeu|taula,tamboret,estatua
 ;;;;;m bar|m bar|barra,tamboret,mirall
 ;;;;;f caixa|f caisse|finestreta,caixa,arxivador
 ;;;;;m despatx|m bureau|escriptori,butaca,llibreria
 ;;;;;m vestíbul|m hall|planta,sofa,quadre
 ;;;;;f sala privada|m salon privé|piano,sofa,butaca
convent;El convent;Le couvent;el claustre;le cloître;m claustre|m cloître|pou,banc,figuera
 ;;;;;f capella|f chapelle|estatua,banc,torxa
 ;;;;;f cuina|f cuisine|llar,taula,barril
 ;;;;;f biblioteca|f bibliothèque|llibreria,taula,escala
 ;;;;;m dormitori|m dortoir|llit,armari,bagul
 ;;;;;m hort|m potager|planta,carro,figuera
esglesia;L'església;L'église;l'edifici;l'édifice;f nau|f nef|banc,estatua,torxa
 ;;;;;f sagristia|f sacristie|armari,bagul,taula
 ;;;;;m campanar|m clocher|escala,torxa,caixa
 ;;;;;f cripta|f crypte|bagul,estatua,torxa
 ;;;;;f rectoria|m presbytère|escriptori,cadira,llibreria
 ;;;;;m hort|m jardin|planta,banc,pou
biblioteca;La biblioteca;La bibliothèque;l'edifici;l'édifice;f sala de lectura|f salle de lecture|taula,cadira,llibreria
 ;;;;;m taulell|m comptoir|barra,tamboret,arxivador
 ;;;;;f sala infantil|f salle des enfants|pupitre,pilota,planta
 ;;;;;m arxiu|f archive|arxivador,escala,caixa
 ;;;;;f sala d'estudi|f salle d'étude|pupitre,pissarra,cadira
 ;;;;;m despatx|m bureau|escriptori,butaca,planta
plato;El plató de televisió;Le plateau de télévision;l'edifici;l'édifice;m plató|m plateau|reflector,sofa,butaca
 ;;;;;f sala de control|f régie|escriptori,arxivador,tamboret
 ;;;;;m camerino|f loge|mirall,maniqui,cadira
 ;;;;;m magatzem|m entrepôt|caixa,bagul,carreto
 ;;;;;f cafeteria|f cafétéria|barra,tamboret,taula
 ;;;;;f recepció|f réception|finestreta,sofa,planta
radio;L'emissora de ràdio;La station de radio;l'edifici;l'édifice;m estudi|m studio|escriptori,tamboret,piano
 ;;;;;f sala de control|f régie|arxivador,escala,tamboret
 ;;;;;f discoteca|f discothèque|llibreria,caixa,escala
 ;;;;;f recepció|f réception|barra,sofa,planta
 ;;;;;m despatx|m bureau|escriptori,cadira,quadre
 ;;;;;f cuina|f cuisine|estufa,taula,cadira
diari;La redacció del diari;La rédaction du journal;l'edifici;l'édifice;f redacció|f rédaction|escriptori,cadira,arxivador
 ;;;;;f impremta|f imprimerie|barril,caixa,carreto
 ;;;;;m arxiu|f archive|arxivador,escala,llibreria
 ;;;;;m despatx del director|m bureau du directeur|escriptori,butaca,planta
 ;;;;;f sala de reunions|f salle de réunion|taula,pissarra,cadira
 ;;;;;f recepció|f réception|barra,sofa,quadre
taller;El taller mecànic;Le garage;el taller;le garage;m taller|m atelier|taula,caixa,carreto
 ;;;;;m magatzem|m entrepôt|barril,caixa,escala
 ;;;;;f oficina|m bureau|escriptori,arxivador,cadira
 ;;;;;f sala d'espera|f salle d'attente|sofa,planta,tamboret
 ;;;;;m pati|f cour|carro,barril,fanal
 ;;;;;m fossat|f fosse|escala,torxa,caixa
vinya;La vinya;Le vignoble;la finca;le domaine;m celler|m chai|barril,caixa,escala
 ;;;;;f vinya|f vigne|planta,carro,figuera
 ;;;;;f sala de tast|f salle de dégustation|taula,tamboret,barra
 ;;;;;m trull|m pressoir|barril,carreto,estufa
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;f casa|f maison|llar,taula,llit
moli;El molí;Le moulin;el molí;le moulin;f sala de les moles|f salle des meules|barril,caixa,carreto
 ;;;;;m graner|m grenier|caixa,escala,bagul
 ;;;;;f cuina|f cuisine|llar,taula,cadira
 ;;;;;m dormitori|f chambre|llit,armari,bagul
 ;;;;;f resclosa|f écluse|pou,banc,carro
 ;;;;;m hort|m potager|planta,figuera,banc
xocolata;La fàbrica de xocolata;La chocolaterie;l'edifici;l'édifice;f cuina|f cuisine|estufa,taula,barril
 ;;;;;m magatzem|m entrepôt|caixa,carreto,escala
 ;;;;;f botiga|f boutique|vitrina,barra,tamboret
 ;;;;;f sala de màquines|f salle des machines|estufa,escala,barril
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;f sala de tast|f salle de dégustation|taula,sofa,planta
refugi;El refugi de muntanya;Le refuge de montagne;el refugi;le refuge;f sala comuna|f salle commune|llar,taula,banc
 ;;;;;f cuina|f cuisine|estufa,taula,barril
 ;;;;;m dormitori|m dortoir|llit,armari,bagul
 ;;;;;m magatzem|f réserve|caixa,carreto,escala
 ;;;;;f terrassa|f terrasse|banc,planta,fanal
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
golf;El club de golf;Le club de golf;el club;le club;m restaurant|m restaurant|taula,cadira,planta
 ;;;;;m vestuari|m vestiaire|armari,banc,mirall
 ;;;;;f botiga|f boutique|vitrina,barra,tamboret
 ;;;;;f terrassa|f terrasse|banc,planta,fanal
 ;;;;;m despatx|m bureau|escriptori,butaca,llibreria
 ;;;;;m magatzem|m entrepôt|bagul,carreto,caixa
nautic;El club nàutic;Le club nautique;el club;le club;m moll|m ponton|ancora,carreto,fanal
 ;;;;;m bar|m bar|barra,tamboret,mirall
 ;;;;;m taller|m atelier|taula,caixa,escala
 ;;;;;m vestuari|m vestiaire|armari,banc,bagul
 ;;;;;f terrassa|f terrasse|banc,planta,timo
 ;;;;;f oficina|m bureau|escriptori,arxivador,cadira
tren;El tren d'època;Le train d'époque;el tren;le train;m vagó restaurant|m wagon-restaurant|taula,cadira,barra
 ;;;;;m vagó llit|m wagon-lit|llit,armari,maleta
 ;;;;;m vagó saló|m wagon-salon|sofa,butaca,piano
 ;;;;;m vagó d'equipatges|m wagon à bagages|maleta,caixa,bagul
 ;;;;;f locomotora|f locomotive|estufa,escala,carreto
 ;;;;;f cabina del revisor|f cabine du contrôleur|escriptori,cadira,arxivador
dirigible;El dirigible;Le dirigeable;la nau;le dirigeable;f cabina de comandament|f cabine de pilotage|timo,escriptori,cadira
 ;;;;;m saló|m salon|sofa,butaca,piano
 ;;;;;m menjador|m restaurant|taula,cadira,barra
 ;;;;;f cabina|f cabine|llit,armari,maleta
 ;;;;;f bodega|f soute|caixa,barril,bagul
 ;;;;;f sala de motors|f salle des moteurs|estufa,escala,carreto
submari;El submarí;Le sous-marin;la nau;le sous-marin;f sala de control|f salle de contrôle|timo,escriptori,tamboret
 ;;;;;f sala de màquines|f salle des machines|estufa,escala,carreto
 ;;;;;m camarot|f cabine|llit,armari,bagul
 ;;;;;f cuina|f cuisine|taula,estufa,cadira
 ;;;;;m magatzem|f soute|caixa,barril,carreto
 ;;;;;f sala de torpedes|f salle des torpilles|caixa,ancora,escala
palau;El palau;Le palais;el palau;le palais;f sala del tron|f salle du trône|tron,torxa,taula
 ;;;;;m saló de ball|f salle de bal|piano,mirall,sofa
 ;;;;;f cuina|f cuisine|llar,taula,barril
 ;;;;;f biblioteca|f bibliothèque|llibreria,butaca,escala
 ;;;;;m jardí|m jardin|estatua,pou,banc
 ;;;;;f cambra reial|f chambre royale|llit,armari,bagul
monestir;El monestir;Le monastère;el monestir;le monastère;m claustre|m cloître|pou,banc,figuera
 ;;;;;f biblioteca|f bibliothèque|llibreria,taula,escala
 ;;;;;m refectori|m réfectoire|taula,banc,llar
 ;;;;;f capella|f chapelle|estatua,torxa,banc
 ;;;;;m scriptorium|m scriptorium|escriptori,pupitre,cadira
 ;;;;;m celler|m cellier|barril,caixa,bagul
ranxo;El ranxo;Le ranch;el ranxo;le ranch;m corral|m enclos|carro,barril,pou
 ;;;;;f quadra|f écurie|caixa,carro,escala
 ;;;;;f cuina|f cuisine|estufa,taula,cadira
 ;;;;;m saló|m salon|llar,sofa,butaca
 ;;;;;f porxada|f véranda|banc,planta,tamboret
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
saloon;El saloon;Le saloon;l'edifici;l'édifice;f sala|f salle|taula,piano,tamboret
 ;;;;;f barra|m comptoir|barra,tamboret,barril
 ;;;;;f cuina|f cuisine|estufa,taula,caixa
 ;;;;;f habitació|f chambre|llit,armari,bagul
 ;;;;;f presó|f prison|banc,caixa,torxa
 ;;;;;m pati|f cour|pou,carro,banc
temple;El temple;Le temple;el temple;le temple;f sala de les estàtues|f salle des statues|estatua,torxa,banc
 ;;;;;f cambra del tresor|f chambre du trésor|bagul,caixa,vitrina
 ;;;;;m santuari|m sanctuaire|tron,torxa,estatua
 ;;;;;m passadís|m couloir|torxa,carreto,caixa
 ;;;;;m pati|f cour|pou,planta,banc
 ;;;;;f biblioteca|f bibliothèque|llibreria,escala,taula
campament;El campament;Le campement;el campament;le campement;f tenda gran|f grande tente|taula,banc,llar
 ;;;;;f cuina|f cuisine|estufa,taula,barril
 ;;;;;m magatzem|f réserve|caixa,carro,bagul
 ;;;;;m dormitori|m dortoir|llit,armari,maleta
 ;;;;;f foguera|m feu de camp|banc,llar,barril
 ;;;;;m estable|f écurie|carro,caixa,escala
parc;El parc d'atraccions;Le parc d'attractions;el parc;le parc;f sala dels miralls|f palais des glaces|mirall,maniqui,tamboret
 ;;;;;f taquilla|f billetterie|finestreta,cadira,banc
 ;;;;;m carrusel|m manège|bola,banc,planta
 ;;;;;f sala de control|f salle de contrôle|escriptori,arxivador,cadira
 ;;;;;m magatzem|m entrepôt|caixa,bagul,carreto
 ;;;;;m bar|m bar|barra,tamboret,taula
estudi;L'estudi d'artista;L'atelier d'artiste;l'edifici;l'édifice;m taller|m atelier|quadre,estatua,taula
 ;;;;;f galeria|f galerie|quadre,vitrina,banc
 ;;;;;m dormitori|f chambre|llit,armari,mirall
 ;;;;;f cuina|f cuisine|estufa,taula,cadira
 ;;;;;m magatzem|m entrepôt|caixa,bagul,escala
 ;;;;;m jardí|m jardin|planta,figuera,banc
antiguitats;La botiga d'antiguitats;La boutique d'antiquités;l'establiment;l'établissement;f botiga|f boutique|vitrina,mirall,sofa
 ;;;;;m magatzem|m entrepôt|bagul,armari,caixa
 ;;;;;m taller|m atelier|taula,escala,caixa
 ;;;;;f sala de subhastes|f salle des ventes|tron,butaca,quadre
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m soterrani|m sous-sol|barril,bagul,escala
tapes;El bar de tapes;Le bar à tapas;l'establiment;l'établissement;f barra|m comptoir|barra,tamboret,barril
 ;;;;;f sala|f salle|taula,cadira,planta
 ;;;;;f cuina|f cuisine|estufa,taula,caixa
 ;;;;;f terrassa|f terrasse|taula,tamboret,planta
 ;;;;;m celler|m cellier|barril,caixa,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
pizzeria;La pizzeria;La pizzeria;l'establiment;l'établissement;m forn|m four|estufa,taula,escala
 ;;;;;f sala|f salle|taula,cadira,planta
 ;;;;;f barra|m comptoir|barra,tamboret,mirall
 ;;;;;f terrassa|f terrasse|banc,taula,planta
 ;;;;;m magatzem|f réserve|caixa,barril,carreto
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
poble;La casa de poble;La maison de village;la casa;la maison;f cuina|f cuisine|llar,taula,cadira
 ;;;;;m menjador|f salle à manger|taula,banc,armari
 ;;;;;f golfa|m grenier|bagul,caixa,escala
 ;;;;;m celler|f cave|barril,caixa,escala
 ;;;;;m dormitori|f chambre|llit,armari,mirall
 ;;;;;m pati|f cour|pou,figuera,banc
aeroport;L'aeroport;L'aéroport;l'edifici;l'édifice;f terminal|m terminal|banc,maleta,planta
 ;;;;;f consigna|f consigne|armari,maleta,carreto
 ;;;;;f torre de control|f tour de contrôle|escriptori,reflector,tamboret
 ;;;;;m hangar|m hangar|caixa,carreto,escala
 ;;;;;f cafeteria|f cafétéria|barra,tamboret,taula
 ;;;;;f oficina|m bureau|escriptori,arxivador,cadira
oficines;El gratacels;La tour de bureaux;l'edifici;l'édifice;f recepció|f réception|barra,sofa,planta
 ;;;;;f sala de reunions|f salle de réunion|taula,pissarra,cadira
 ;;;;;m despatx del director|m bureau du directeur|escriptori,butaca,quadre
 ;;;;;m arxiu|f archive|arxivador,escala,caixa
 ;;;;;f cafeteria|f cafétéria|barra,tamboret,taula
 ;;;;;f terrassa|f terrasse|banc,planta,fanal
titelles;El teatre de titelles;Le théâtre de marionnettes;l'edifici;l'édifice;m escenari|f scène|tel,maniqui,reflector
 ;;;;;f platea|m parterre|butaca,banc,sofa
 ;;;;;m taller|m atelier|taula,caixa,escala
 ;;;;;m camerino|f loge|mirall,tamboret,armari
 ;;;;;m magatzem|m entrepôt|bagul,maniqui,caixa
 ;;;;;f taquilla|f billetterie|finestreta,cadira,planta
xalet;El xalet de muntanya;Le chalet;el xalet;le chalet;m saló|m salon|llar,sofa,butaca
 ;;;;;f cuina|f cuisine|estufa,taula,barril
 ;;;;;m dormitori|f chambre|llit,armari,bagul
 ;;;;;m garatge|m garage|carro,caixa,escala
 ;;;;;f terrassa|f terrasse|banc,planta,fanal
 ;;;;;m estudi|m bureau|escriptori,llibreria,cadira
hipodrom;L'hipòdrom;L'hippodrome;el recinte;l'enceinte;f pista|f piste|banc,fanal,carro
 ;;;;;f tribuna|f tribune|banc,butaca,planta
 ;;;;;f quadra|f écurie|caixa,carro,barril
 ;;;;;f taquilla|f billetterie|finestreta,cadira,banc
 ;;;;;m bar|m bar|barra,tamboret,mirall
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
fira;La fira;La foire;la fira;la foire;f carpa|f tente|taula,banc,llar
 ;;;;;f parada|m stand|vitrina,barra,tamboret
 ;;;;;m carrusel|m manège|bola,banc,planta
 ;;;;;f taquilla|f billetterie|finestreta,cadira,banc
 ;;;;;m magatzem|m entrepôt|caixa,carro,bagul
 ;;;;;m bar|m bar|barra,tamboret,barril
cafe;El cafè antic;Le vieux café;el cafè;le café;f sala|f salle|taula,cadira,piano
 ;;;;;f barra|m comptoir|barra,tamboret,mirall
 ;;;;;f cuina|f cuisine|estufa,taula,caixa
 ;;;;;f terrassa|f terrasse|taula,tamboret,planta
 ;;;;;m celler|f cave|barril,caixa,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
cabaret;El cabaret;Le cabaret;l'edifici;l'édifice;m escenari|f scène|tel,piano,reflector
 ;;;;;f sala|f salle|taula,butaca,tamboret
 ;;;;;m camerino|f loge|mirall,maniqui,sofa
 ;;;;;f barra|m comptoir|barra,tamboret,barril
 ;;;;;m magatzem|m entrepôt|caixa,bagul,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
farmacia;La farmàcia;La pharmacie;l'establiment;l'établissement;f botiga|f officine|barra,vitrina,tamboret
 ;;;;;m laboratori|m laboratoire|taula,estufa,caixa
 ;;;;;m magatzem|f réserve|armari,caixa,escala
 ;;;;;f sala d'espera|f salle d'attente|sofa,planta,banc
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m soterrani|m sous-sol|barril,bagul,carreto
ferreteria;La ferreteria;La quincaillerie;l'establiment;l'établissement;f botiga|f boutique|barra,armari,tamboret
 ;;;;;m magatzem|m entrepôt|caixa,barril,escala
 ;;;;;m taller|m atelier|taula,estufa,carreto
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m pati|f cour|carro,barril,fanal
 ;;;;;m soterrani|m sous-sol|caixa,bagul,escala
sastreria;La sastreria;La couturière;l'establiment;l'établissement;f botiga|f boutique|mirall,maniqui,vitrina
 ;;;;;m taller|m atelier|taula,maniqui,tamboret
 ;;;;;m emprovador|f cabine d'essayage|mirall,sofa,cadira
 ;;;;;m magatzem|f réserve|armari,caixa,bagul
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;f golfa|m grenier|bagul,escala,caixa
perruqueria;La perruqueria;Le salon de coiffure;l'establiment;l'établissement;f sala|m salon|mirall,butaca,tamboret
 ;;;;;m rentat|m bac|banc,barril,tamboret
 ;;;;;f recepció|f réception|barra,sofa,planta
 ;;;;;m magatzem|f réserve|armari,caixa,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m pati|f cour|planta,banc,pou
jardi;El jardí botànic;Le jardin botanique;el recinte;l'enceinte;m hivernacle|f serre|planta,figuera,banc
 ;;;;;f entrada|f entrée|finestreta,banc,planta
 ;;;;;m cobert|f remise|caixa,carro,escala
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;f cafeteria|f cafétéria|barra,tamboret,taula
 ;;;;;f font|f fontaine|pou,banc,estatua
atic;L'àtic;L'attique;l'edifici;l'édifice;m saló|m salon|sofa,piano,butaca
 ;;;;;f cuina|f cuisine|estufa,taula,cadira
 ;;;;;m dormitori|f chambre|llit,armari,mirall
 ;;;;;f terrassa|f terrasse|banc,planta,fanal
 ;;;;;m estudi|m bureau|escriptori,llibreria,arxivador
 ;;;;;m vestidor|m dressing|armari,mirall,bagul
galeria;La galeria d'art;La galerie d'art;l'edifici;l'édifice;f sala principal|f salle principale|quadre,banc,estatua
 ;;;;;m magatzem|f réserve|caixa,bagul,carreto
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m taller|m atelier|taula,escala,caixa
 ;;;;;m jardí d'escultures|m jardin de sculptures|estatua,banc,planta
 ;;;;;f cafeteria|f cafétéria|barra,tamboret,taula
hostal;L'hostal;L'auberge;l'edifici;l'édifice;m saló|f salle commune|llar,taula,banc
 ;;;;;f cuina|f cuisine|estufa,taula,barril
 ;;;;;f habitació|f chambre|llit,armari,bagul
 ;;;;;m celler|f cave|barril,caixa,escala
 ;;;;;f quadra|f écurie|carro,caixa,carreto
 ;;;;;m pati|f cour|pou,banc,figuera
gimnas;El gimnàs;La salle de sport;l'edifici;l'édifice;f sala|f salle|pilota,banc,mirall
 ;;;;;m vestuari|m vestiaire|armari,banc,mirall
 ;;;;;f recepció|f réception|barra,sofa,planta
 ;;;;;m bar|m bar|barra,tamboret,taula
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
 ;;;;;m magatzem|m entrepôt|caixa,pilota,escala
concerts;La sala de concerts;La salle de concert;l'edifici;l'édifice;m escenari|f scène|piano,reflector,tel
 ;;;;;f platea|m parterre|butaca,banc,sofa
 ;;;;;m camerino|f loge|mirall,tamboret,armari
 ;;;;;m vestíbul|m hall|banc,planta,quadre
 ;;;;;m bar|m bar|barra,tamboret,taula
 ;;;;;m despatx|m bureau|escriptori,arxivador,cadira
"""


def llegeix():
    """Retorna una llista d'escenaris: (clau, etiqueta, lloc, sales)."""
    out = []
    cur = None
    for lin in DADES.strip().split("\n"):
        parts = lin.split(";")
        clau = parts[0].strip()
        sala = parts[5]
        if clau:
            cur = {"clau": clau, "tag": (parts[1], parts[2]), "lloc": (parts[3], parts[4]), "sales": []}
            out.append(cur)
        ca, fr, objs = sala.split("|")
        cur["sales"].append(((ca[0], ca[2:]), (fr[0], fr[2:]), objs.split(",")))
    return out
