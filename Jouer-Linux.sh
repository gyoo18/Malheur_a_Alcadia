#!/bin/bash
if [ ! -e .venv ]
then
    python3 -m venv .venv
    # source ./.venv/bin/activate
    ./.venv/bin/python3 -m pip install -r requirements.txt
    clear
    ./.venv/bin/python3 Main.py
else
    # source ./.venv/bin/activate
    clear
    ./.venv/bin/python3 Main.py
fi