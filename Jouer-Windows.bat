@echo off
::Tester si l'environnement virtuel est déjà installé
%cd%/.venv/Scripts/python.exe --version 3>NUL

::Si non, exécuter en installant
if errorlevel 1 goto installer

%cd%/.venv/Scripts/python.exe Main.py
goto:fin

:installer
::Détection de python sous la commande 'python'
python --version 3>NUL

::Si cette commande échoue, qu'il soit sous 'py'
if errorlevel 1 goto essais2

::Exécuter le script avec 'python'
python -m venv .venv
%cd%/.venv/Scripts/python.exe -m pip install -r requirements.txt
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

::On essaie de détecter python sous 'py'
:essais2
py --version 3>NUL

::Si on ne trouve toujours pas python, montrer un message d'erreur
if errorlevel 1 goto erreur

::Exécuter le script avec 'py'
py -m venv .venv
%cd%/.venv/Scripts/python.exe -m pip install -r requirements.txt
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

::Message d'erreur, python n'est pas installé
:erreur
echo !!====PYTHON N'A PAS ETE DETECTE SUR VOTRE ORDINATEUR. VEUILLEZ INSTALLER PYTHON.====!!


:fin
echo Merci d'avoir joue :)
set /p DUMMY=Tapez entre pour quitter...
