# Projecte: joc de misteri (puzles de lògica de crims, per al mòbil)

Document de context per continuar el projecte des de Claude Code. Resumeix el que l'usuari ha decidit, el que està fet i el que és obert. Les coses marcades com a **proposta** les va suggerir Claude i **l'usuari encara no les ha confirmades**.

L'usuari (Ferran) parla català: respon-li en català. Entorn: Windows, Python instal·lat. El codi només usa la biblioteca estàndard (cal Python 3.9 o superior); no cal xarxa ni instal·lar res.

## 1. Què és

Joc de puzles de lògica de crims. Cada cas és una graella n×n amb forats, dividida en sales amb objectes. S'han de col·locar n persones (n-1 sospitosos + la víctima, que és l'última) **una per fila i una per columna**, només en caselles utilitzables, seguint les pistes. **L'assassí és l'únic sospitós que queda a la mateixa sala que la víctima.** Cada persona té una pista i hi ha unes poques pistes generals. Cada cas té una única solució que es pot trobar per deducció.

El gènere el representa Murdoku (murdoku.com, de Manuel Garand; vist en versió alfa, 40 casos, 5 nivells, mides 6×6 a 9×9) i una app anomenada Roomers. **No s'ha de copiar**: noms, textos, dibuixos, escenaris i interfície han de ser propis. Les mecàniques de joc en general no estan protegides, però els noms, textos i art sí (no és assessorament legal). A `referencia/` hi ha captures de Murdoku que l'usuari va enviar per entendre el gènere (no per reproduir-les).

## 2. Decisions de l'usuari

- **Format: col·lecció de casos** amb diferents dificultats, mides i escenaris. No un sol cas diari.
- **Per jugar al mòbil** (pàgina web que s'adapti bé a una pantalla de mòbil).
- **Idiomes: català i francès**, des del principi.
- Experiment personal; no associar-lo a cap institució. Sense diners reals.
- **70 escenaris amb 3 casos cadascun** (210 casos). Només canvien el fons, els noms de les sales i els objectes.
- **Controls:** tocar una casella = nota; mantenir premut = col·locar; arrossegar = pintar notes; X (descarta), goma (premut = buida-ho tot), desfés, revisa. Les caselles de la fila i columna d'un sospitós es marquen soles amb una X suau (desactivable).
- **Retrats:** fotogràfics (carpeta `retrats/`, 32 imatges que l'usuari va aportar) per a les lletres A-E, H, J i V; les lletres F, G i I fan servir una cara SVG dibuixada fins que l'usuari aporti més retrats.
- Les persones tenen un nom que comença per la lletra del personatge (A, B, C... V) i canvia a cada cas.

## 3. Propostes de Claude (pendents de confirmar)

- **Controls al mòbil:** un toc fa cicle buit → X → nota; toc llarg col·loca el sospitós. (El joc de referència fa servir: tocar un sospitós per seleccionar-lo, tocar una casella per posar una nota, mantenir premut per col·locar, arrossegar per pintar notes; botons X, goma i desfés.)
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
| `motor.py` | Plantilla (graella amb forats, sales, objectes), catàleg de pistes, solucionador, valoració de dificultat, generador de casos. |
| `escenaris.py` | 12 escenaris definits aquí (`mas`, `estacio`, `teatre`, `vaixell`, `hotel`, `museu`, `castell`, `escola`, `restaurant`, `circ`, `mansio`, `mercat`) i 58 més carregats de `escenaris_extra.py` (70 en total). Catàleg d'objectes `_OBJ` i noms per lletra `NOMS_LLETRA`. |
| `escenaris_extra.py` | Dades compactes dels 58 escenaris addicionals (sales ca/fr i objectes). |
| `textos.py` | Frases de les pistes en ca/fr (articles, contraccions, elisions, gènere). |
| `generador.py` | Genera casos nous en JSON (`--escenari`, `--mida`, `--nivell`, `--quantitat`, `--llavor`, `--sortida`). |
| `verifica.py` | Comprovador **independent**. Per defecte cerca amb retrocés (dècimes de segon fins a 9x9); `--forca` fa la força bruta antiga (només per contrastar). Validat: dóna el mateix nombre de solucions que la força bruta. |
| `renom.py` | Posa a cada persona un nom que comença per la seva lletra i en refà els textos. |
| `reskin.py` | Reparteix casos verificats entre els escenaris (3 per escenari) i en canvia sales i objectes **sense tornar a verificar** (cada objecte nou bloqueja igual que l'antic). Escriu `casos_final.json`. |
| `construeix.py` | Llegeix `casos_final.json`, assigna noms de cas (`noms.json`), escriu `casos.js` (casos + `SCEN_META`) i `joc.html` (tot en un fitxer, amb les fotos incloses). |
| `index.html`, `sw.js` | La pàgina (carrega `casos.js`, sense dependències) i el service worker. |
| `retrats/` | 32 retrats (jpg) dels personatges. |
| `*.json` | Lots de casos generats (font d'estructures): `lot*.json`, `niv*.json`, `casos_*.json`. |

### Flux de treball
```
python generador.py --escenari mas --mida 7 --quantitat 6 --llavor 5 --sortida lot7_x.json
python renom.py lot7_x.json              # noms per lletra
python verifica.py lot7_x.json           # ràpid
# llista d'identificadors verificats (un per línia) -> ids.txt
python reskin.py ids.txt casos_final.json
python construeix.py                     # casos.js + joc.html
```
Un cas només depèn de la seva estructura (plànol, sales, pistes i si els objectes bloquegen); l'escenari és només l'aspecte.

### Pistes implementades (`motor.py`, camp `t`)
Per persona: `en_sala`, `no_en_sala`, `sobre_obj`, `prop_obj`, `raco`, `vora` (al costat d'una paret exterior de l'edifici o d'un forat), `fila_obj`, `col_obj`, `sol`, `costat`, `nord`, `sud`, `est`, `oest`, `diag`, `cavall`, `mateixa_sala`, `altra_sala`, `sol_amb`. Generals: `compte_sala`. Regla implícita `victima`.

### Dificultat (`valora`)
Un solucionador «humà» aplica tècniques en ordre i el nivell és la més alta necessària (1 a 5). Definició pròpia, no validada amb jugadors.

### Estat de la col·lecció
210 casos a la pàgina: 108 de 6x6, 63 de 7x7, 30 de 8x8 i 9 de 9x9, en 70 escenaris (3 per escenari). Els 429 casos dels fitxers `*.json` estan tots verificats.

## 6. Problemes coneguts i feina oberta

1. **9x9 nous:** el generador és molt lent a 9x9 (hores per cas) i només n'hi ha 9, tots de lots antics. Generar-ne més és el coll d'ampolla (la verificació ja no ho és).
2. **Francès:** els textos i els noms de sales/escenaris els ha revisat només Claude; caldria que algú que parli francès els repassés.
3. **Retrats F, G, I:** falten imatges fotogràfiques per a aquestes lletres (noms: Ferran, Francesca, Felip, Fina, Gerard, Griselda, Guerau, Glòria, Ivo, Irene, Ignasi, Isabel).
4. **Objectes:** només hi ha icones SVG pròpies; si l'usuari vol més qualitat pot aportar una imatge amb els objectes i es retallen com els retrats.
5. **Objectes de reserva:** si un escenari té pocs objectes d'un tipus, `reskin.py` en pren un d'un altre escenari (pot quedar poc coherent).
6. **Publicació:** no s'ha publicat res (GitHub Pages no està activat; cal preguntar abans). L'usuari prova la versió amb `joc.html`.
7. Atributs ocults i més tipus de pista; tutorial més complet; el mode fosc i el francès només s'han provat poc.
8. Els identificadors dels casos conserven el prefix de l'escenari original (`mas-6-7-3`...) tot i que ara el cas es mostra en un altre escenari; el progrés es guarda per aquest identificador.

## 7. Propers passos (proposta)

1. Generar més 9x9 (i més casos en general) i tornar a executar `reskin.py` i `construeix.py`.
2. Revisió del francès per una persona nativa.
3. Retrats per a F, G, I i, si es vol, imatges d'objectes de més qualitat.
4. Decidir com publicar-ho (GitHub Pages o altre); confirmar-ho amb l'usuari abans.
