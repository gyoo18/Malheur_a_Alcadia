@echo off
::Tester si l'environnement virtuel est déjà installé
%cd%/.venv/Scripts/python.exe --version 3>NUL

::Si non, exécuter en installant
if errorlevel 1 goto venv

::Si oui, lancer le programme
goto:demarrer

gcc --version || clang --version || "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if errorlevel 1 goto installercompilateur

goto:venv

:installercompilateur
echo !==== AUCUN COMPILATEUR C/C++ N'A ETE DETECTE SUR VOTRE SYSTEME ====!
echo Veuillez installer gcc, clang ou msvc. Vous pouvez cliquer sur le lien suivant pour installer ce dernier : https://visualstudio.microsoft.com/fr/downloads/#build-tools-for-visual-studio-2022
goto:fin

:venv
::Détection de python sous la commande 'python'
python --version 3>NUL

::Si cette commande échoue, qu'il soit sous 'py'
if errorlevel 1 goto essais2

::Exécuter le script avec 'python'

::Détection de la version de python
FOR /F "delims=" %%i IN ('python --version') DO set version=%%i
:boucle1
set version=%version:~0,-1%
IF "%version:~-1%" NEQ "." goto boucle1
set version=%version:~0,-1%

::Création de l'environnement virtuel
echo installation des dependances
python -m venv .venv
goto:installer

::On essaie de détecter python sous 'py'
:essais2
py --version 3>NUL

::Si on ne trouve toujours pas python, montrer un message d'erreur
if errorlevel 1 goto erreur

::Exécuter le script avec 'py'

::Détection de la version de python
FOR /F "delims=" %%i IN ('py --version') DO set version=%%i
:boucle2
set version=%version:~0,-1%
IF "%version:~-1%" NEQ "." goto boucle2
set version=%version:~0,-1%

::Création de l'environnement virtuel
echo installation des dependances
py -m venv .venv
goto:installer

::Message d'erreur, python n'est pas installé
:erreur
echo !!====PYTHON N'A PAS ETE DETECTE SUR VOTRE ORDINATEUR.====!!
echo Veuillez installer python au lien suivant : https://www.python.org/downloads/
goto:fin

:installer
%cd%/.venv/Scripts/python.exe -m pip install -r requirements_windows.txt

IF "%version%" == "Python 3.9" goto installerp39
IF "%version%" == "Python 3.10" goto installerp310
IF "%version%" == "Python 3.11" goto installerp311
IF "%version%" == "Python 3.12" goto installerp312
IF "%version%" == "Python 3.13" goto installerp313
::else
echo Votre version de python - %version% - n'est pas supportee. Veuillez installer Python 3.9, 3.10, 3.11, 3.12 ou 3.13.
goto:fin

:installerp39
IF %PROCESSOR_ARCHITECTURE%==x86 goto installerp39x86
IF %PROCESSOR_ARCHITECTURE%==ARM64 goto installerp39arm64
::else
goto:installerp39amd64
:installerp39x86
echo installation de PyOpenGL. Python 3.9 sur x86
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp39-cp39-win32.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp39-cp39-win32.whl
goto:demarrer
:installerp39arm64
echo !==== PYOPENGL N'EST PAS SUPPORTE POUR VOTRE VERSION DE PYTHON (3.9) SUR VOTRE PLATEFORME (ARM64) ====!
echo Veuillez installer l'une des versions de Python supportee parmis les suivantes : 3.11, 3.12, 3.13.
goto:demarrer
:installerp39amd64
IF %PROCESSOR_ARCHITECTURE% NEQ AMD64 echo ATTENTION votre architecture CPU est %PROCESSOR_ARCHITECTURE%. Seulle AMD64 est officiellement supportee. Il se peut que vous ayez des problemes.
echo installation de PyOpenGL. Python 3.9 sur AMD64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp39-cp39-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp39-cp39-win_amd64.whl
goto:demarrer

:installerp310
IF %PROCESSOR_ARCHITECTURE%==x86 goto installerp310x86
IF %PROCESSOR_ARCHITECTURE%==ARM64 goto installerp310arm64
::else
goto:installerp310amd64
:installerp310x86
echo installation de PyOpenGL. Python 3.10 sur x86
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp310-cp310-win32.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp310-cp310-win32.whl
goto:demarrer
:installerp310arm64
echo !==== PYOPENGL N'EST PAS SUPPORTE POUR VOTRE VERSION DE PYTHON (3.10) SUR VOTRE PLATEFORME (ARM64) ====!
echo Veuillez installer l'une des versions de Python supportee parmis les suivantes : 3.11, 3.12, 3.13.
goto:demarrer
:installerp310amd64
IF %PROCESSOR_ARCHITECTURE% NEQ AMD64 echo ATTENTION votre architecture CPU est %PROCESSOR_ARCHITECTURE%. Seulle AMD64 est officiellement supportée. Il se peut que vous ayez des problèmes.
echo installation de PyOpenGL. Python 3.10 sur AMD64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp310-cp310-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp310-cp310-win_amd64.whl
goto:demarrer

:installerp311
IF %PROCESSOR_ARCHITECTURE%==x86 goto installerp311x86
IF %PROCESSOR_ARCHITECTURE%==ARM64 goto installerp311arm64
::else
goto:installerp311amd64
:installerp311x86
echo installation de PyOpenGL. Python 3.11 sur x86
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp311-cp311-win32.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp311-cp311-win32.whl
goto:demarrer
:installerp311arm64
echo installation de PyOpenGL. Python 3.11 sur ARM64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp311-cp311-win_arm64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp311-cp311-win_arm64.whl
goto:demarrer
:installerp311amd64
IF %PROCESSOR_ARCHITECTURE% NEQ AMD64 echo ATTENTION votre architecture CPU est %PROCESSOR_ARCHITECTURE%. Seulle AMD64 est officiellement supportée. Il se peut que vous ayez des problèmes.
echo installation de PyOpenGL. Python 3.11 sur AMD64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp311-cp311-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp311-cp311-win_amd64.whl
goto:demarrer

:installerp312
IF %PROCESSOR_ARCHITECTURE%==x86 goto installerp312x86
IF %PROCESSOR_ARCHITECTURE%==ARM64 goto installerp312arm64
::else
goto:installerp312amd64
:installerp312x86
echo installation de PyOpenGL. Python 3.12 sur x86
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp312-cp312-win32.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp312-cp312-win32.whl
goto:demarrer
:installerp312arm64
echo installation de PyOpenGL. Python 3.12 sur ARM64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp312-cp312-win_arm64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp312-cp312-win_arm64.whl
goto:demarrer
:installerp312amd64
IF %PROCESSOR_ARCHITECTURE% NEQ AMD64 echo ATTENTION votre architecture CPU est %PROCESSOR_ARCHITECTURE%. Seulle AMD64 est officiellement supportée. Il se peut que vous ayez des problèmes.
echo installation de PyOpenGL. Python 3.12 sur AMD64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp312-cp312-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp312-cp312-win_amd64.whl
goto:demarrer

:installerp313
IF %PROCESSOR_ARCHITECTURE%==x86 goto installerp313x86
IF %PROCESSOR_ARCHITECTURE%==ARM64 goto installerp313arm64
::else
goto:installerp313amd64
:installerp313x86
echo installation de PyOpenGL. Python 3.13 sur x86
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp313-cp313-win32.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp313-cp313-win32.whl
goto:demarrer
:installerp313arm64
echo installation de PyOpenGL. Python 3.13 sur ARM64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp313-cp313-win_arm64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp313-cp313-win_arm64.whl
goto:demarrer
:installerp313amd64
IF %PROCESSOR_ARCHITECTURE% NEQ AMD64 echo ATTENTION votre architecture CPU est %PROCESSOR_ARCHITECTURE%. Seulle AMD64 est officiellement supportée. Il se peut que vous ayez des problèmes.
echo installation de PyOpenGL. Python 3.13 sur AMD64
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL-3.1.8-cp313-cp313-win_amd64.whl
%cd%/.venv/Scripts/python.exe -m pip install Win_PyOpenGL_whl/PyOpenGL_accelerate-3.1.8-cp313-cp313-win_amd64.whl
goto:demarrer

::Démarrer 
:demarrer
%cd%/.venv/Scripts/python.exe Main.py
goto:fin

:fin
echo Merci d'avoir joue :)
set /p DUMMY=Tapez 'entre' pour quitter...
