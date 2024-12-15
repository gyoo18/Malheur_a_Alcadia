# Malheur à Alcadia
Le mal envahis votre cité! Saurez-vous diriger vos golems et l'écraser? Ou serez-vous emportés par les ombres?

## Qu'est-ce que c'est?
Malheur à Alcadia est un petit jeu console de combat stratégique en tour-par-tour, à la *Fire Emblem* ou *X-COM*, dans lequel vous pouvez invoquer des golems composés des matériaux du sol sur lesquels vous les faîtes apparaîtres. Il compose le projet final du cours de programmation 1 au baccalauréat en informatique de l'Université du Québec en Outaouais.

## Comment Jouer?
1. Assurez-vous d'avoir **python d'installé**. Si vous êtes sur linux, vous devriez déjà l'avoir. Pour vérifier si vous l'avez, ouvrez une invite de commande et tapez `python --version`,`py --version` ou `python3 --version`. Si l'une d'entre elles fonctionnes, python est installé. Si vous n'avez pas python, vous pouvez l'installer ici : https://www.python.org/downloads/
3. Cliquez sur le lien suivant : https://github.com/gyoo18/Prog1_jeu/releases
4. Téléchargez la version la plus récente
5. Vous trouverez un fichier .zip, dézippez-le
6. Cliquez sur `Jouer-Windows.bat` ou `Jouer-Linux.sh`, tout dépedant du système que vous possédez. *Il se peut que vous ayez à changer les permissions du fichier*.

## Structure générale
### Dossier principal
Contient : 
 - `Jouer-Linux.sh` et `Jouer-Windows.bat` Simple script exécutant les commandes de démarrage.
 - `Main.py` L'entrée principale du programme. Initialise les ressources, fait rouler la boucle et détruit les ressources
 - `Jeu.py` Classe singleton qui décrit l'état actuel du jeu. S'occupe de mettre à jour toutes les composante
 - `Ressources.py` Classe singleton qui s'occupe de gérer les ressources du jeu.
 - `menu.py` Ensemble de fonctions qui impriment les menus et qui se charge d'accepter et interpréter les commandes en appeleant les autres composantes
 - `dialogue.py` Contient un ensemble de fonctions responsable de gérer les dialogues à afficher selon la situation.
 - `TFX.py` Contient un ensemble de fonctions utilitaires servant à produire différents effets dans le terminal
### Maths
Contient :
 - `Vec2.py, Vec3.py, Vec4.py` Classes décrivants des vecteurs et des fonctions utiles à leur manipulation
### InclusionsCirculaires
Contient des fichier `.py` qui contournent les problèmes d'inclusions circulaires de certaines classes
### Entités
Contient :
 - `Entité.py` Classe générale décrivant une entité dans un niveau. Peut se déplacer sur une carte grâce à l'algorithme A*, attaquer d'autres entitées et possède quelques autres habiletées.
 - `Paysan.py` Ensemble de classes décrivant l'ennemi principal du jeu : le paysan. Implémente sa classe parente `Entité`
 - `Golem.py` Ensemble de classes décrivant le pion principal du jeu : le golem. Peut être créé sur la carte, reçevoir des commandes du joueur et effectuer des attaques spéciales
 - `Attaque.py` Classe décrivant une attaque à être passée entre deux entitées
### Carte
Contient : 
 - `class_carte.py` Classe décrivant une carte. Une carte décrit l'entièreté du niveau, incluant les entitées et les moments scriptés.
 - `Tuile.py` Classe décrivant une tuile sur une carte. Peut être de différents types et fait apparaître des golems.

## Contributeurs :
Merci à :
 - gyoo18 https://github.com/gyoo18
 - Camicey https://github.com/Camicey
 - Dreamod4 https://github.com/Dreamod4
 - Frankydud3 https://github.com/Frankydud3
 - mario0393 https://github.com/mario0393
 - MoCa55 https://github.com/MoCa55
 - MrCarnaval https://github.com/MrCarnaval
 - ris1294 https://github.com/ris1294
 - Stang-Boy https://github.com/Stang-Boy
 - Stephanemba --- https://github.com/Stephanemba
