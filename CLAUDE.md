# Projecte: joc de misteri (puzles de lògica de crims, per al mòbil)

Document de context per continuar el projecte des de Claude Code. Resumeix el que l'usuari ha decidit, el que està fet i el que és obert. Les coses marcades com a **proposta** les va suggerir Claude i **l'usuari encara no les ha confirmades**.

L'usuari (Ferran) parla català: respon-li en català. Entorn: Windows, Python instal·lat. El codi només usa la biblioteca estàndard (cal Python 3.9 o superior); no cal xarxa ni instal·lar res.

## 1. Què és

Joc de puzles de lògica de crims. Cada cas és una graella n×n amb forats, dividida en sales amb objectes. S'han de col·locar n persones (n-1 sospitosos + la víctima, que és l'última) **una per fila i una per columna**, només en caselles utilitzables, seguint les pistes. **L'assassí és l'únic sospitós que queda a la mateixa sala que la víctima.** Cada persona té una pista i hi ha unes poques pistes generals. Cada cas té una única solució que es pot trobar per deducció.

El gènere el representa Murdoku (murdoku.com, de Manuel Garand; vist en versió alfa, 40 casos, 5 nivells, mides 6×6 a 9×9) i una app anomenada Roomers. L'usuari vol que el joc **s'assembli molt a Murdoku** en estructura, pantalles i maneres de jugar (vegeu §8), però **sense reutilitzar els seus noms, textos, dibuixos, personatges ni escenaris**: tot el contingut i l'art han de ser propis. No es copien imatges ni es fa servir el nom «Murdoku». Les mecàniques de joc en general no estan protegides, però els noms, textos i art sí (no és assessorament legal). A `referencia/` hi ha captures de Murdoku que l'usuari va enviar per entendre el gènere (no per reproduir-les).

## 2. Decisions de l'usuari

- **Format: col·lecció de casos** amb diferents dificultats, mides i escenaris. No un sol cas diari.
- **Per jugar al mòbil** (pàgina web que s'adapti bé a una pantalla de mòbil).
- **Idiomes: català i francès**, des del principi.
- Experiment personal; no associar-lo a cap institució. Sense diners reals.
- **Vol que s'assembli molt més a Murdoku** (17-10-2026): mateixes pantalles, controls i organització, amb contingut propi (§8).

## 3. Propostes de Claude (pendents de confirmar)

- ~~Controls alternatius~~ (substituït: l'usuari vol que s'assembli més al joc de referència, vegeu §8).
- Pàgina estàtica que carrega els casos des d'un JSON, instal·lable (PWA) i sense connexió; progrés i temps a `localStorage`.
- Tocar una pista il·lumina les caselles afectades; temporitzador opcional; mode fosc.
- Mides de 6×6 fins a 9×9 i 5 nivells de dificultat (com a referència; l'usuari no n'ha triat).
- Escenari inicial «El mas» (original); més escenaris després. **No** escenari de laboratori (l'usuari no ho vol associar a cap institució). No usar persones reals com a sospitosos o víctimes. No usar escenaris ni noms de Murdoku.
- Atributs ocults com a pistes generals (un sospitós que menteix, un amagat...): **no implementat**.
- Art propi en SVG senzill.

## 4. Com és el joc de referència (de les captures de `referencia/`)

- Graella amb forats; sales amb nom escrit sobre el plànol i amb textura pròpia; objectes (cactus, roques, cavall, butaca, taula). Els objectes bloquegen la casella, llevat d'alguns que es poden ocupar (el cavall).
- Targetes de sospitós (lletra A, B, C... i V per a la víctima) amb retrat i **una pista cadascuna**, més «pistes generals».
- Paraules clau: *al costat* (esquerra, dreta, amunt o avall, i a la mateixa sala), *sol* (ningú més a la sala, ni la víctima), *sol amb*, *àrea buida*, *cantonada* (dues parets d'una sala), *diagonal* (línia sencera), *fila*, *columna*, *a l'est/oest de* (qualsevol casella en aquella direcció).
- Tècniques «avançades» que explica el joc: (1) fila o columna amb una sola casella lliure; (2) files o columnes sobrecarregades (dues persones només caben a dues files → ningú més); (3) eliminar la casella alineada amb totes les opcions d'una persona.
- Llista de casos amb dificultat (Molt fàcil, Fàcil, Mitjà, Difícil, Expert), mida, millor temps i segell de «cas resolt».

## 5. Estat del codi (carpeta misteri/)

| Fitxer | Què fa |
|---|---|
| `motor.py` | Plantilla (graella amb forats, sales, objectes), catàleg de pistes, solucionador que compta solucions, regla implícita de la víctima, valoració de dificultat, generador de casos. |
| `escenaris.py` | Escenari `mas` (sales, objectes i personatges en ca/fr). |
| `textos.py` | Frases de les pistes en ca/fr: articles, contraccions (al/del, au/du), elisions, gènere. |
| `generador.py` | Genera casos i els desa en JSON. |
| `verifica.py` | Comprovador **independent** per força bruta (no usa `motor.py`). |
| `prova.py` | Prova de tot el flux: genera 3 casos i els verifica. |
| `casos_prova.json`, `casos_n3.json` | 13 casos 6×6 de mostra (10 aleatoris, 3 de nivell 3). |

### Comandes
```
python generador.py --quantitat 10 --llavor 7 --sortida casos.json
python generador.py --quantitat 3 --nivell 3 --veure
python verifica.py casos.json
python prova.py
```
`--veure` imprimeix el plànol, la solució i les pistes en català i francès.

### Pistes implementades (`motor.py`, camp `t`)
Per persona: `en_sala`, `no_en_sala`, `sobre_obj`, `prop_obj` (al costat d'un objecte, a la mateixa sala), `raco`, `vora` (a la vora de la finca), `fila_obj`, `col_obj`, `sol`, `costat` (ortogonal i a la mateixa sala), `nord`, `sud`, `est`, `oest` (qualsevol casella en aquella direcció), `diag`, `cavall` (salt de cavall d'escacs), `mateixa_sala`, `altra_sala`, `sol_amb`. Generals: `compte_sala` (k persones a una sala; k=0 és «sala buida»). Regla implícita `victima`: un únic sospitós a la sala de la víctima.
`costat` i `mateixa_sala` amb la víctima s'exclouen perquè revelarien l'assassí.

### Dificultat (`valora`)
Un solucionador «humà» aplica tècniques en ordre i el nivell és la més alta necessària: 1 consistència de pistes + únic nu; 2 + fila/columna amb una sola opció; 3 + parelles sobrecarregades; 4 + interseccions i trios; 5 cal provar una casella i veure la contradicció. Si no es resol per deducció, el cas es descarta. És una definició pròpia i no s'ha validat amb jugadors.

### Format del JSON d'un cas
`id`, `escenari`, `n`, `nivell`, `pla` (matriu 0/1; 0 = forat), `sala` (matriu d'índexs; -1 fora del plànol), `sales` (índex → nom ca/fr), `obj` (matriu amb clau d'objecte o `null`), `persones` (`id` A.. i V, `nom`, `genere`), `pistes` (dades estructurades), `textos` (`ca` i `fr`, una frase per pista, en el mateix ordre), `solucio` (id → [fila, columna]), `assassi` (id).
Les claus d'objecte (`taula`, `barril`, `carro`...) i si bloquegen són a `escenaris.py`; **el JSON no porta els noms dels objectes ni si bloquegen**: la pàgina haurà de rebre'ls (afegir-los al JSON és el primer canvi lògic).

### Verificat
`verifica.py` ha comprovat 13 casos: tots tenen exactament una solució i és la correcta. De 10 casos aleatoris, 8 van sortir de nivell 5 (poca mostra).

## 6. Problemes coneguts i preguntes obertes

1. **Distribució de nivells:** els casos aleatoris surten sobretot de nivell 5. Es poden demanar per nivell (`--nivell`), però un cas de nivell 3 triga ~50 s. Cal ajustar el generador (menys intents descartats) o revisar la valoració.
2. **Només s'ha provat 6×6.** 7×7 a 9×9 poden ser molt més lents (el solucionador compta per backtracking).
3. **Textos:** les frases en francès les ha revisat només Claude; les hauria de repassar algú que parli francès. Alguns textos són una mica repetitius (cal més variants). «sala» és tant una sala del mas com la paraula genèrica: a les frases genèriques s'usa «habitació/pièce».
4. **El JSON no porta els objectes** (vegeu §5).
5. Atributs ocults i més tipus de pista per variar.
6. Art (SVG propi), més escenaris, noms dels casos, retrats dels personatges.
7. Pàgina del joc per al mòbil i com es publica.
8. Tutorial dins del joc (regles, paraules clau, tècniques) en ca/fr.

## 7. Propers passos (proposta)

1. Afegir al JSON els objectes (nom ca/fr i si bloquegen) perquè la pàgina no depengui de `escenaris.py`.
2. Fer la **pàgina web per al mòbil** (HTML/CSS/JS sense dependències): graella amb forats, sales amb color, objectes en SVG, targetes de sospitós amb la seva pista, controls tàctils, desfés, comprovació, selector ca/fr, llista de casos amb nivell i temps, progrés a `localStorage`.
3. Ajustar el generador (equilibri de nivells, mides 7 a 9) i generar una col·lecció de 40 casos o més.
4. Més escenaris, art i tutorial.

## 8. Disseny de la interfície (objectiu: molt semblant en estructura i interaccions)

Base: les captures de `referencia/`. **Es reprodueix l'organització i el comportament, no els recursos**: dibuixos, retrats, noms, textos i escenaris propis.

### Pantalla de la llista de casos (captura 03 i 07)
- Capçalera amb el nom del joc (propi), botó d'inici de sessió (opcional, pot ser només local), selector d'idioma (Català/Français), botó de notícies/novetats amb marcador, botó de mode fosc, i una etiqueta «ALPHA».
- Resum: «40 enigmes · N completats».
- Filtres per dificultat en pestanyes: Tots, Molt fàcil, Fàcil, Mitjà, Difícil, Expert (la seleccionada ressaltada).
- «Ordena per:» (Dificultat...) i botó «Amaga els completats».
- Quadrícula de dues columnes de **sobres**: un cas disponible és un sobre tancat amb un tros del plànol que s'entreveu i el text «CAS DISPONIBLE! FES CLIC PER REVELAR»; en tocar-lo s'obre. Un cas resolt és una targeta amb la miniatura del plànol amb les X i les lletres, el segell «CAS RESOLT», el nom del cas, la dificultat, la mida (6×6) i el millor temps; els no començats mostren el nombre de pistes o una lupa.
- Cada cas té nom propi i escenari/tema (en el joc de referència, amb una etiqueta de color; aquí, escenaris propis).

### Pantalla de joc (captures 01 i 02)
- Barra superior: fletxa enrere, nom del cas, temporitzador, botó d'ajuda (?) i de configuració.
- Plànol a dalt, amb forats, sales amb textura/color propis i el **nom de cada sala escrit sobre el plànol**, objectes dibuixats (alguns bloquegen la casella).
- A sota, secció «Pistes generals» (targetes) i després les **targetes dels sospitosos** en dues columnes: lletra, nom, retrat i la seva pista, amb els mots clau en negreta; la víctima (V) hi surt també.
- Barra inferior fixa amb: botó X (marcar caselles impossibles), goma (mantenir premut per buidar-ho tot), Desfés, pista (bombeta) i «Envia» (desactivat fins que tots els sospitosos són col·locats: «col·loca'ls tots primer»).

### Controls (captura 05)
- Tocar un sospitós: el selecciona.
- Tocar una casella: afegeix/treu una nota (lletra minúscula).
- Mantenir premuda la casella: col·loca el sospitós (lletra majúscula).
- Arrossegar: pinta notes per diverses caselles.
- Les caselles descartades per fila/columna es marquen soles (opcional, desactivable).

### Ajuda (captures 04, 05, 06)
Finestra amb quatre pestanyes: Com es juga, Paraules clau (mini-diagrames per a cada pista), Avançat (tècniques amb exemples) i FAQ.

### Què ha de ser propi
Nom del joc, logotip, tipografia i paleta, il·lustracions (plànols, objectes, retrats), noms dels casos, escenaris, textos de les pistes i de l'ajuda. L'escenari actual és «El mas»; s'han d'afegir més escenaris amb personalitat pròpia (colors i textures per escenari).
