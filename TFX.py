from Maths.Vec3 import Vec3

ROUGE = Vec3(0.90,0.12,0.12)
ORANGE = Vec3(0.90,0.52,0.12)
BRUN = Vec3(0.36,0.19,0.06)
VERT = Vec3(0.23,0.77,0.11)
BLEU = Vec3(0.18,0.24,0.80)
NOIR = Vec3(0,0,0)
BLANC = Vec3(1,1,1)
JAUNE = Vec3(0.93,0.87,0.12)
VIOLET = Vec3(0.62,0.13,0.86)
MAGENTA = Vec3(0.86,0.12,0.77)
CYAN = Vec3(0.09,0.82,0.88)
TURQUOISE = Vec3(0.08,0.88,0.55)
BEIGE = Vec3(0.93,0.71,0.52)
GRIS = Vec3(0.5,0.5,0.5)
ROSE = Vec3(0.85,0.33,0.48)
OR = Vec3(0.86,0.66,0.15)

ROUGE_PÂLE = Vec3(0.95,0.38,0.38)
ORANGE_PÂLE = Vec3(0.96,0.61,0.33)
VERT_PÂLE = Vec3(0.54,0.93,0.52)
JAUNE_PÂLE = Vec3(0.92,0.89,0.52)
BLEU_PÂLE = Vec3(0.52,0.62,0.91)
VIOLET_PÂLE = Vec3(0.77,0.52,0.91)
MAGENTA_PÂLE = Vec3(0.93,0.52,0.89)
CYAN_PÂLE = Vec3(0.50,0.91,0.93)
TURQUOISE_PÂLE = Vec3(0.38,0.89,0.73)
GRIS_PÂLE = Vec3(0.75,0.75,0.75)

ROUGE_FONCÉ = Vec3(0.64,0.08,0.08)
ORANGE_FONCÉ = Vec3(0.70,0.32,0)
VERT_FONCÉ = Vec3(0.18,0.48,0.08)
JAUNE_FONCÉ = Vec3(0.57,0.52,0.05)
BLEU_FONCÉ = Vec3(0.07,0.09,0.55)
VIOLET_FONCÉ = Vec3(0.30,0.07,0.46)
MAGENTA_FONCÉ = Vec3(0.41,0.04,0.37)
CYAN_FONCÉ = Vec3(0,0.51,0.51)
TURQUOISE_FONCÉ = Vec3(0.04,0.52,0.38)
GRIS_FONCÉ = Vec3(0.25,0.25,0.25)


def coul(s : str, coul : Vec3):
    return "\033[38;2;" + str(int(coul.x*256)) + ';' + str(int(coul.y*256)) + ';' + str(int(coul.z*256)) + 'm' + s + "\033[0m"
def surl(s : str, coul : Vec3):
    return "\033[48;2;" + str(int(coul.x*256)) + ';' + str(int(coul.y*256)) + ';' + str(int(coul.z*256)) + 'm' + s + "\033[0m"
def gras(s : str):
    return "\033[1m" + s + "\033[0m"
def pâle(s : str):
    return "\033[2m" + s + "\033[0m"
def ital(s : str):
    return "\033[3m" + s + "\033[0m"
def soul(s : str):
    return "\033[4m" + s + "\033[0m"
def cliL(s : str):
    return "\033[5m" + s + "\033[0m"
def cliR(s : str):
    return "\033[6m" + s + "\033[0m"
def TFX(s : str, Pcoul : Vec3 = None, Scoul : Vec3 = None, gras = False, pâle = False, ital = False, soul = False, cliL = False, cliR = False):
    ret = s
    if Pcoul != None:
        ret = "\033[38;2;" + str(int(Pcoul.x*256)) + ';' + str(int(Pcoul.y*256)) + ';' + str(int(Pcoul.z*256)) + 'm' + ret
    if Scoul != None:
        ret = "\033[48;2;" + str(int(Pcoul.x*256)) + ';' + str(int(Pcoul.y*256)) + ';' + str(int(Pcoul.z*256)) + 'm' + ret
    if gras:
        ret = "\033[1m" + ret
    if pâle:
        ret = "\033[2m" + ret
    if ital:
        ret = "\033[3m" + ret
    if soul:
        ret = "\033[4m" + ret
    if cliL:
        ret = "\033[5m" + ret
    if cliR:
        ret = "\033[6m" + ret
    return ret + "\033[0m"