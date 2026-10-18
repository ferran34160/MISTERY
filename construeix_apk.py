#!/usr/bin/env python3
"""Construeix l'APK d'Android (un WebView amb la pàgina del joc).

Requisits: JDK 17+, Gradle i l'SDK d'Android (plataforma 34 i build-tools 34.0.0).
Ús: python construeix_apk.py        -> escriu misteri.apk a la carpeta del projecte
Abans cal tenir `casos.js` al dia (python construeix.py).
"""
import os
import shutil
import subprocess
import sys

ARREL = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ARREL, "android", "app", "src", "main", "assets")
FITXERS = ["index.html", "casos.js", "logo.png", "sobre.png", "paper.png"]
CARPETES = ["retrats", "objectes", "terres"]


def main():
    shutil.rmtree(ASSETS, ignore_errors=True)
    os.makedirs(ASSETS)
    for f in FITXERS:
        shutil.copy(os.path.join(ARREL, f), ASSETS)
    for d in CARPETES:
        shutil.copytree(os.path.join(ARREL, d), os.path.join(ASSETS, d))
    # configuració de la classificació (amb el token, si hi ha ranking_secret.js)
    sys.path.insert(0, ARREL)
    os.chdir(ARREL)
    from construeix import config_classificacio
    with open(os.path.join(ASSETS, "ranking_config.js"), "w", encoding="utf-8") as fh:
        fh.write(config_classificacio())
    env = dict(os.environ)
    env.setdefault("ANDROID_HOME", os.path.expanduser("~/android-sdk"))
    env.setdefault("ANDROID_SDK_ROOT", env["ANDROID_HOME"])
    cmd = ["gradle", "-p", os.path.join(ARREL, "android"), "assembleRelease", "--no-daemon", "-q"]
    r = subprocess.run(cmd, env=env)
    if r.returncode:
        sys.exit(r.returncode)
    apk = os.path.join(ARREL, "android", "app", "build", "outputs", "apk", "release", "app-release.apk")
    shutil.copy(apk, os.path.join(ARREL, "misteri.apk"))
    print("misteri.apk creat (%d KB)" % (os.path.getsize(apk) // 1024))


if __name__ == "__main__":
    main()
