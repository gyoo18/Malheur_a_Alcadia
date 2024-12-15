#!/bin/bash
gcc --version || clang --version
if [ $? -eq 0 ]
then
    clear
    echo Un compilateur a été détecté sur votre machine
else
    echo !==== AUCUN COMPILATEUR DÉTÉCTÉ ====!
    echo L\'installation de gcc est nécessaire. Veuillez entrer votre mot de passe.
    sudo apt install -y build-essential
fi

python3 --version
if [ $? -ne 0 ]
then
    echo !==== PYTHON 3.x N\'A PAS ÉTÉ DÉTECTÉ SUR VOTRE ORDINATEUR, VEUILLEZ INSTALLER PYTHON 3.x ====!
    exit
fi

if [ ! -e .venv ]
then
    echo !==== ENVIRONNEMENT VIRTUEL NON DÉTECTÉ, INSTALLATION DES DÉPENDANCES ====!
    python3 -m venv .venv
    ./.venv/bin/python3 -m pip install -r requirements_linux.txt
    clear
    ./.venv/bin/python3 Main.py
else
    clear
    ./.venv/bin/python3 Main.py
fi