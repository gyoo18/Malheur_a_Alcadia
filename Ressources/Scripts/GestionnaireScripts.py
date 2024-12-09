from Ressources.Scripts import Script1
from Ressources.Scripts import Script2

def InitialiserScript(nom : str):
    match nom:
        case "Script1":
            Script1.initialiser()
        case "Script2":
            Script2.initialiser()
        case _:
            raise ValueError("[Gestionnaire de Scripts] Le script " + nom + " n'est pas un script reconnus.")
        
def MettreÀJourScript(nom : str):
    match nom:
        case "Script1":
            Script1.mettreÀJour()
        case "Script2":
            Script2.mettreÀJour()
        case _:
            raise ValueError("[Gestionnaire de Scripts] Le script " + nom + " n'est pas un script reconnus.")

def Terminer(nom : str):
    match nom:
        case "Script1":
            Script1.Terminer()
        case "Script2":
            Script2.Terminer()
        case _:
            raise ValueError("[Gestionnaire de Scripts] Le script " + nom + " n'est pas un script reconnus.")