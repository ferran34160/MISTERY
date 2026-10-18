# Classificació entre amics

La classificació es guarda en **un fitxer (`ranking.json`) dins d'una branca d'aquest mateix repositori de GitHub**. Cada vegada que algú acaba un cas, el joc llegeix el fitxer, hi afegeix el resultat i el torna a pujar; el botó 🏆 el llegeix per mostrar la classificació. No cal cap servei extern ni publicar el joc: els amics reben el `joc.html` o l'APK.

GitHub no deixa escriure a ningú sense identificar-se, així que cal un **token** (una clau d'accés) dins de l'app. **Només cal fer-ho una vegada, i només la persona que organitza el grup.**

## 1. Crear el token

1. A GitHub: la teva foto (a dalt a la dreta) → **Settings** → baixa fins a **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. **Token name:** `misteri-classificacio`. **Expiration:** la més llarga que et deixi (per exemple 1 any).
3. **Repository access → Only select repositories →** tria `MISTERY`.
4. **Permissions → Repository permissions → Contents → Read and write.** No cal cap altre permís.
5. **Generate token** i **copia'l** (comença per `github_pat_…`). Només el veuràs una vegada.

## 2. Posar el token al joc

El token **no es pot pujar al repositori** (GitHub el detectaria i el desactivaria). Per això només va dins del fitxer que es reparteix:

- Si em passes el token pel xat, jo el poso en un fitxer local que no es puja (`ranking_secret.js`) i construeixo l'`joc.html` i l'APK amb el token inclòs.
- Si ho fas tu: crea el fitxer `ranking_secret.js` al costat de `ranking_config.js` amb una sola línia i torna a construir (`python construeix.py` i `python construeix_apk.py`):

```js
window.RANKING_GH.token = "github_pat_…el_teu_token…";
```

Amb això la classificació ja funciona. El joc crea sol la branca `ranking` la primera vegada que algú acaba un cas.

## 3. Com funciona

- Cada jugador es posa un **sobrenom** (al botó 🏆). No hi ha comptes.
- En resoldre un cas, el temps i els punts pugen sols. Si no hi ha connexió, es guarden i es tornen a enviar la propera vegada.
- **Punts d'un cas:** depèn del nivell (10, 20, 35, 55, 80) i de la mida (×1, ×1,25, ×1,5, ×1,8), amb un **bonus de fins al doble** si el resols ràpid respecte a un temps de referència. Cada jugador només compta el seu millor resultat de cada cas.
- 🏆 **General:** suma de punts i casos resolts. 🏆 **Per cas:** els temps de tothom en un cas.
- Si dos jugadors acaben alhora, el joc reintenta fins a 5 vegades.
- Tens l'historial complet a GitHub: a la branca `ranking`, fitxer `ranking.json`, cada resultat és un canvi. Si cal corregir alguna cosa, pots editar el fitxer a mà.

## Seguretat (què cal saber)

- **El token queda dins de l'app**, i qui tingui el `joc.html` o l'APK pot treure'l. Amb aquest token es pot escriure a **qualsevol branca** del repositori `MISTERY`, també al codi. Entre família ho veig acceptable, però **no passis el fitxer a gent de fora del grup**.
- **Protecció recomanada (2 minuts):** a GitHub → el repositori → **Settings → Branches → Add branch ruleset / rule** per a la branca `main` (i la teva de treball), amb **«Require a pull request before merging»** i sense permetre ometre les regles ni a administradors. Així el token no pot canviar el codi, només la branca `ranking`.
- Si el token es filtra o vols tancar-ho: a GitHub → Settings → Developer settings → **Revoke** el token. Cap altre accés s'ha compartit.
- El joc no pot saber si algú fa trampes.

## Alternativa: Firebase

Si algun dia prefereixes una base de dades en lloc de GitHub, posa l'adreça d'una Realtime Database de Firebase a `RANKING_URL` de `ranking_config.js` (i deixa el token buit). El format de les dades és el mateix.
