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
    """
    <p>Retourne un string dont la couleur de police sera spécifiée par `coul`</p>
    <p>Ex. :</p>
    <ul>
    <li>`coul( "Allô", Vec3(0.90,0.12,0.12))`</li>
    <li>`coul( "Allô", TFX.ROUGE)`</li>
    </ul>

    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**

    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[38;2;R;G;Bm[Texte]\\033[0m</p>

    À noter que VSCode n'affiche pas toutes les couleurs de textes dans son terminal.


    Args:
        s (str): String à colorier
        coul (Vec3): Couleur du string en format RGB décimal (0.0-1.0)

    Returns:
        str : Texte coloré
    """
    return "\033[38;2;" + str(int(coul.x*256)) + ';' + str(int(coul.y*256)) + ';' + str(int(coul.z*256)) + 'm' + s + "\033[0m"
def surl(s : str, coul : Vec3):
    """
    <p>Retourne un string surligné par la couleur spécifiée par `coul`</p>
    Ex. :
     - `coul( "Allô", Vec3(0.12,0.82,0.88))`
     - `coul( "Allô", TFX.JAUNE_PÂLE)`

    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[48;2;R;G;Bm[Texte]\\033[0m</p>

    Args:
        s (str): String à surligner
        coul (Vec3): Couleur du surlignage en format RGB décimal (0.0-1.0)

    Returns:
        str : Texte surligné
    """
    return "\033[48;2;" + str(int(coul.x*256)) + ';' + str(int(coul.y*256)) + ';' + str(int(coul.z*256)) + 'm' + s + "\033[0m"
def gras(s : str):
    """
    <p>Retourne un string en gras</p>
    <p>Ex. :</p>
    `gras( "Allô" ) ->` 
    
    **Allô**

    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[1m[Texte]\\033[0m</p>

    Args:
        s (str): String à mettre en gras

    Returns:
        str : Texte en gras
    """
    return "\033[1m" + s + "\033[0m"
def pâle(s : str):
    """
    <p>Retourne un string en pâle</p>
    <p>Ex. :</p>
    `pâle("Allô")`

    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[2m[Texte]\\033[0m</p>

    Returns:
        str : Texte en pâle
    """
    return "\033[2m" + s + "\033[0m"
def ital(s : str):
    """
    <p>Retourne un string en italique</p>
    <p>Ex. :</p>
     - `pâle("Allô") -> `
    
    *Allô*

    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[3m[Texte]\\033[0m</p>

    Returns:
        str : Texte en italique
    """
    return "\033[3m" + s + "\033[0m"
def soul(s : str):
    """
    <p>Retourne un string souligné</p>
    <p>Ex. :</p>
     - `pâle("Allô")`
    
    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[4m[Texte]\\033[0m</p>

    Returns:
        str : Texte en italique
    """
    return "\033[4m" + s + "\033[0m"
def cliL(s : str):
    """
    <p>Retourne un string qui clignote lentement</p>
    <p>Ex. :</p>
     - `cliL("Allô")`

    **Il se peut que cette fonctionalité ne soit pas supporté par votre terminal**
    
    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[5m[Texte]\\033[0m</p>

    Returns:
        str : Texte qui clignote
    """
    return "\033[5m" + s + "\033[0m"
def cliR(s : str):
    """
    <p>Retourne un string qui clignote rapidement</p>
    <p>Ex. :</p>
     - `cliR("Allô")`

    **Il se peut que cette fonctionalité ne soit pas supporté par votre terminal**
    
    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[6m[Texte]\\033[0m</p>

    Returns:
        str : Texte qui clignote
    """
    return "\033[6m" + s + "\033[0m"
def barré(s : str):
    """
    <p>Retourne un string barrét</p>
    <p>Ex. :</p>
     - `barré("Allô") ->`

    ~~Allô~~
    
    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[9m[Texte]\\033[0m</p>

    Returns:
        str : Texte barré
    """
    return "\033[9m" + s + "\033[0m"
def soul2(s : str):
    """
    <p>Retourne un string souligné avec deux barres</p>
    <p>Ex. :</p>
     - `soul2("Allô")`
    
    **Il se peut que l'utilisation composée de ces fonction ne donne pas le résultat escompté!**
    Veuillez utiliser TFX.TFX() pour vous assurer de l'effet voulus.

    <p>Renvoie un string qui contient les codes ANSI suivants : </p>
    <p>\\033[21m[Texte]\\033[0m</p>

    Returns:
        str : Texte double-souligné
    """
    return "\033[21m" + s + "\033[0m"
def TFX(s : str, Pcoul : Vec3 = None, Scoul : Vec3 = None, gras = False, pâle = False, ital = False, soul = False, cliL = False, cliR = False, barré = False, soul2 = False):
    """

    <p>Retourne un string auquel on a appliqué les effets indiqués</p>
    <p>Ex.:</p>
     - `TFX("Allô", Pcoul=TFX.ROUGE, Scoul=Vec3(0.23,0.77,0.11), gras=True, ital=True) ->`

     **_Allô_**

     **À noter que certains effets peuvent ne pas être compatible avec votre terminal**

     <p>Renvoie un string qui contient des codes ANSI comme suit : </p>
     <p>[CODE ANSI 1][CODE ANSI 2]...[TEXTE]\\033[0m</p>

    Args:
        s (str): String à affecter
        Pcoul (Vec3, optional): Couleur de police. Defaults to None.
        Scoul (Vec3, optional): Couleur de surlignage. Defaults to None.
        gras (bool, optional): En gras. Defaults to False.
        ital (bool, optional): En italique. Defaults to False.
        soul (bool, optional): Souligné. Defaults to False.
        cliL (bool, optional): Clignote lentement. Defaults to False.
        cliR (bool, optional): Clignote rapidement. Defaults to False.
        soul2 (bool, optional): Souligné avec duex barres. Defaults to False.

    Returns:
        str : Texte formatté
    """
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
    if barré:
        ret = "\033[9m" + ret
    if soul2:
        ret = "\033[21m" + ret
    return ret + "\033[0m"