# Classificació entre amics (base de dades gratuïta)

El joc guarda els temps i els punts de cada jugador en una base de dades de **Firebase** (de Google, gratuïta per a un ús com aquest). No cal publicar el joc en cap web: cada amic pot rebre el fitxer `joc.html` (o l'APK) i tots comparteixen la mateixa classificació.

**Només cal fer-ho una vegada, i només la persona que organitza el grup.**

## 1. Crear la base de dades

1. Entra a <https://console.firebase.google.com> amb un compte de Google.
2. **Afegeix un projecte** (per exemple «misteri-amics»). Pots desactivar Google Analytics.
3. Al menú de l'esquerra: **Compilació → Realtime Database → Crea la base de dades**.
   - Tria la ubicació que et surti (per exemple Bèlgica, `europe-west1`).
   - Tria **«Inicia en mode de prova»**.
4. A la pestanya **Regles**, substitueix el contingut per això i prem **Publica**:

```json
{
  "rules": {
    "ranking": {
      ".read": true,
      ".write": true
    }
  }
}
```

   Així la classificació no caduca (el mode de prova s'apaga als 30 dies) i només s'obre la part `ranking`.
5. A la pestanya **Dades**, copia l'adreça que surt a dalt, del tipus
   `https://misteri-amics-default-rtdb.europe-west1.firebasedatabase.app`

## 2. Posar l'adreça al joc

Obre `ranking_config.js` i canvia-hi la línia per:

```js
window.RANKING_URL = "https://misteri-amics-default-rtdb.europe-west1.firebasedatabase.app";
```

Després cal tornar a construir el joc (`python construeix.py`) i passar el fitxer nou als amics. Si m'envies l'adreça, ho faig jo.

## 3. Com funciona

- Cada jugador es posa un **sobrenom** (al botó 🏆). No hi ha comptes ni contrasenyes.
- En resoldre un cas, el temps i els punts pugen sols. Si no hi ha connexió, es guarden i es tornen a enviar la propera vegada.
- **Punts d'un cas:** depèn del nivell (10, 20, 35, 55, 80) i de la mida (×1, ×1,25, ×1,5, ×1,8), amb un **bonus de fins al doble** si el resols ràpid respecte a un temps de referència. Cada jugador només compta el seu millor resultat de cada cas.
- 🏆 **General:** suma de punts i casos resolts. 🏆 **Per cas:** els temps de tothom en un cas.

## Seguretat (què cal saber)

Les regles deixen escriure a qualsevol persona que tingui l'adreça de la base de dades. Entre amics és suficient, però:
- Qui conegui l'adreça pot esborrar o canviar resultats; no la publiquis.
- Dos jugadors amb el mateix sobrenom compartirien resultats.
- El joc no pot saber si algú fa trampes.
- Si algun dia vols esborrar-ho tot, ho pots fer des de la pestanya **Dades** de Firebase.
