@echo off
::Tester si l'environnement virtuel est déjà installé
%cd%/.venv/Scripts/python.exe --version 3>NUL

::Si non, exécuter en installant
if errorlevel 1 goto installer

::Si oui, lancer le programme
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

gcc --version || clang --version || "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if errorlevel 1 goto installercompilateur

goto:installer

:installercompilateur
echo !==== AUCUN COMPILATEUR N'A ETE DETECTE SUR VOTRE SYSTEME ====!
echo Veuillez installer gcc, clang ou msvc. Vous pouvez cliquer sur le lien suivant pour installer ce dernier : https://visualstudio.microsoft.com/fr/downloads/#build-tools-for-visual-studio-2022
goto:fin

:installer
::Détection de 

::Détection de python sous la commande 'python'
python --version 3>NUL

::Si cette commande échoue, qu'il soit sous 'py'
if errorlevel 1 goto essais2

::Exécuter le script avec 'python'
python -m venv .venv
%cd%/.venv/Scripts/python.exe -m pip install -r requirements_windows.txt
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp313-cp313-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp313-cp313pwin_amd64.whl
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

::On essaie de détecter python sous 'py'
:essais2
py --version 3>NUL

::Si on ne trouve toujours pas python, montrer un message d'erreur
if errorlevel 1 goto erreur

::Exécuter le script avec 'py'
py -m venv .venv
%cd%/.venv/Scripts/python.exe -m pip install -r requirements_windows.txt
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp313-cp313-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp313-cp313pwin_amd64.whl
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

::Message d'erreur, python n'est pas installé
:erreur
echo !!====PYTHON N'A PAS ETE DETECTE SUR VOTRE ORDINATEUR.====!!
echo Veuillez installer python au lien suivant : https://www.python.org/downloads/

:fin
echo Merci d'avoir joue :)
set /p DUMMY=Tapez entre pour quitter...
