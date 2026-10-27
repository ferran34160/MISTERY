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
- **Retrats:** imatges de l'usuari (carpeta `retrats/`, 50): fotogràfics per a les lletres A-E, H, J i V i d'estil il·lustrat per a F, G i I (6 noms per aquestes tres lletres; la resta en tenen 4). Si un nom no té imatge es dibuixa una cara SVG.
- **Objectes:** il·lustracions (carpeta `objectes/`, 44 imatges que l'usuari va aportar, retallades i amb el fons tret); si un objecte no té imatge es fa servir la icona SVG de `index.html`.
- **Terres de les sales:** 9 textures fotogràfiques (carpeta `terres/`, aportades per l'usuari) que `index.html` tria segons el nom de la sala (`TEX`) i barreja amb el color de la sala.
- **Logotip, sobre i targeta de paper:** imatges aportades per l'usuari (`logo.png`, `sobre.png`, `paper.png`; la xinxeta és un SVG propi). El logotip diu «MISTERY MURDER» (amb «Mistery», que és una errada d'«Mystery»): **l'usuari ha decidit deixar-lo així**.
- **Classificació entre amics:** només amb **GitHub**, al **mateix repositori** (decisió de l'usuari; juga amb 3-4 familiars): un fitxer `ranking.json` en una branca `ranking` que el joc crea sol, escrit des de l'app amb un token fi de GitHub (Contents: read/write). El token **no es puja mai al repositori** (GitHub el revocaria): va a `ranking_secret.js` (ignorat per git), que `construeix.py` i `construeix_apk.py` incrusten només a `joc.html` i a l'APK. `joc.html` i `misteri.apk` ja no es versionen (poden dur el token). Punts per cas = base segons nivell × mida × (1 + bonus de temps, fins a ×2). Firebase queda com a alternativa (`RANKING_URL`). Vegeu `RANKING.md`. **Pendent:** l'usuari ha de crear el token; probat només amb un servidor GitHub simulat.
- **Distribució als amics:** un **APK** d'Android (`python construeix_apk.py`), construït al núvol amb l'SDK baixat a `~/android-sdk`; no s'ha pogut provar en un mòbil. Només Android; cal permetre instal·lar d'orígens desconeguts.
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
| `retrats/` | 50 retrats (jpg) dels personatges. |
| `objectes/` | 44 imatges (png transparent) dels objectes. |
| `terres/` | 9 textures (jpg) dels terres de les sales. |
| `android/`, `construeix_apk.py` | Projecte d'Android (un WebView que carrega `index.html` des d'`assets/`) i script que copia els fitxers i construeix `misteri.apk` (cal JDK 17+, Gradle i l'SDK d'Android; clau de signatura fixa `android/debug.keystore`, la de depuració estàndard, no és secreta). |
| `ranking_config.js`, `RANKING.md` | Configuració de la classificació (repositori i branca; el token no hi va) i guia per crear el token. |
| `PROMPTS_IMATGES.md` | Textos per demanar a un generador d'imatges els objectes, terres, logotip, sobre, targeta i retrats F/G/I. |
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
210 casos a la pàgina (més els 18 K-pop i el cas de la casa d'estiu): mides 21 de 6x6, 32 de 7x7, 52 de 8x8 i 105 de 9x9 (`PER_MIDA`), tots amb 5 o 6 sales; nivells (després de `dificultat.py`) ~12 Molt fàcil, 24 Fàcil, 47 Mitjà, 60 Difícil, 67 Expert. Difícil = nivell 4 del motor o nivell 5 amb ≤2 proves d'hipòtesi (`PROVES_DIFICIL`).

## 6. Problemes coneguts i feina oberta

1. **9x9:** el generador en fa ara un lot de 3 en ~2 minuts; a la pàgina n'hi ha 25 (tots verificats, també de nivells 1-3).
2. **Francès:** els textos i els noms de sales/escenaris els ha revisat només Claude; caldria que algú que parli francès els repassés.
3. **Estil dels retrats:** els de F, G i I són il·lustrats i la resta fotogràfics; si es vol coherència caldria tornar a generar-los amb el mateix estil.
4. **Retrats F, G, I:** fet; els 18 són ja fotogràfics (substituïts a `retrats/`).
5. **Objectes de reserva:** si un escenari té pocs objectes d'un tipus, `reskin.py` en pren un d'un altre escenari (pot quedar poc coherent).
6. **Publicació:** no s'ha publicat res (GitHub Pages no està activat; cal preguntar abans). L'usuari prova la versió amb `joc.html`.
7. Atributs ocults i més tipus de pista; tutorial més complet; el mode fosc i el francès només s'han provat poc.
8. Els identificadors dels casos conserven el prefix de l'escenari original (`mas-6-7-3`...) tot i que ara el cas es mostra en un altre escenari; el progrés es guarda per aquest identificador.

## 7. Propers passos (proposta)

1. Generar més 9x9 (i més casos en general) i tornar a executar `reskin.py` i `construeix.py`.
2. Revisió del francès per una persona nativa.
3. Retrats per a F, G, I i, si es vol, imatges d'objectes de més qualitat.
4. Decidir com publicar-ho (GitHub Pages o altre); confirmar-ho amb l'usuari abans.

## 8. Notes de manteniment
- `assignacions.json` recorda quin escenari té cada cas (id d'estructura → escenari) perquè no canviï en tornar a executar `reskin.py`. Per fer lloc a casos nous, treu-ne entrades i passa un fitxer de preferits: `python reskin.py ids.txt casos_final.json preferits.txt`.
- Els `id` de cas són estables (`escenari-mida-hash`); `font` guarda l'id antic i `index.html` hi migra el progrés.
- Objectes: 67 (43 + 24 del segon lot); `escenaris._amplia()` els afegeix a les sales pel nom.
- **Mode K-pop (ús personal, per a la filla de 6 anys):** `kpop.py` genera `casos_kpop.json` (12 casos 5×5 + 6 de 6×6, nivell 1-2, només pistes simples via `motor.TIPUS_PERMESOS`, sense pistes repetides) amb l'escenari `kpop` (marcat `especial`, fora de `reskin.py`) i els personatges de la pel·lícula (`escenaris.KPOP_PERSONATGES`, inicials diferents; la insígnia del retrat és `ins`). `construeix.py` els afegeix a `casos.js` (camp `kpop`) i, si existeix la carpeta `kpop/retrats/` (**ignorada per git**: són imatges amb drets d'autor), n'incrusta els retrats a `joc.html` i a l'APK. A `index.html`: botó «⭐ K-POP» (canvia a francès), sense temporitzador ni classificació, 💡 dóna directament la casella i 🔊 llegeix la pista en francès (speechSynthesis).
- **Textos de les pistes:** `textos.py` té 5-9 variants per tipus de pista i, a més, un «enquadrament» aleatori (testimoni, convidat, llibreta de l'inspector…) que s'aplica a ~2/3 de les pistes (`descriu`). `kpop.py` i `cas_meu.py` només tornen a redactar els casos ja existents (les pistes no canvien: la tria no és determinista entre execucions); `--nous` / `--nou` en regeneren de nous.
- **Taulell sempre quadrat (només aspecte):** els forats del plànol (`pla` = 0) es dibuixen com a caselles plenes de pedra amb un objecte decoratiu (`decor()` a `index.html`: planta, arbre, estàtua, fanal, pou… o cirerer/llanterna/pòster als casos K-pop), triat entre els que NO surten al cas per no crear ambigüitat amb les pistes. Per a la lògica (parets, `vora`, `raco`, solució) continuen sent forats.
- **Història de cada cas:** `textos.intro()` genera (ca/fr, estable per id) 3 frases d'introducció que `construeix.py` desa a `c["intro"]`; a `index.html` surten al desplegable «📜 La història» sobre les pistes (variants pròpies pel mode K-pop). Pendent: 12 textures de terra noves (`PROMPTS_IMATGES.md` §7) quan l'usuari les passi.
