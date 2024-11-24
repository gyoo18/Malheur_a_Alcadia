from Entités.Entité import *

class Ennemi(Entité):

    def __init__(self):
        super().__init__()

    def _AttaquerEnnemi(self):
        match self.étatCombat.v:
            case ÉtatCombat.CHARGER:
                self.chargement += 1
                if self.chargement >= self.TEMP_CHARGEMENT:
                    attaque = Attaque()
                    attaque.dégats = 1.0*self.attaque_chargée
                    self.ennemi.Attaquer(attaque)

            case ÉtatCombat.DÉFENSE:
                if self.ennemi.étatCombat.v != ÉtatCombat.CHARGER:
                    self.étatCombat.v = ÉtatCombat.LIBRE

            case ÉtatCombat.LIBRE:
                match self.ennemi.étatCombat.v:
                    case ÉtatCombat.LIBRE:
                        attaque = Attaque()
                        attaque.dégats = 1.0
                        self.ennemi.Attaquer(attaque)

                    case ÉtatCombat.DÉFENSE:
                        self.étatCombat = ÉtatCombat.CHARGER

                    case ÉtatCombat.CHARGER:
                        self.étatCombat = ÉtatCombat.DÉFENSE