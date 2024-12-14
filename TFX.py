from Maths.Vec3 import Vec3
from Maths.Vec2 import Vec2

EFL = "\033[2K" # Efface la ligne

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
        ret = "\033[48;2;" + str(int(Scoul.x*256)) + ';' + str(int(Scoul.y*256)) + ';' + str(int(Scoul.z*256)) + 'm' + ret
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

def bgcr(translation : Vec2):
    """
    Bouge le curseur sur l'écran de « translation » caractères

    Args:
        translation (Vec2): translation à effectuer
    """
    if translation.x > 0:
        print("\033[" + str(int(translation.x)) + "C",end='')
    else:
        print("\033[" + str(int(-translation.x)) + "D",end='')
    
    if translation.y > 0:
        print("\033[" + str(int(translation.y)) + "A",end='')
    else:
        print("\033[" + str(int(-translation.y)) + "B",end='')

def markDownFormattage(texte : str):
    résultat = ""
    string = ""
    ouvert_italique = False
    ouvert_gras = False
    ouvert_souligné = False
    ouvert_barré = False
    ouvert_espaces = False
    ouvert_RL = False
    ouvert_liste_points = False
    ouvert_liste_nombres = False
    ouvert_header = False
    ouvert_code = False
    ouvert_code_grand = False
    ouvert_couleur_avant = False
    ouvert_couleur_arrière = False
    n_citation = 0
    n_espaces = 0
    n_RL = 0
    n_header = 0

    n_marqeurs = 0
    n_étoiles = 0
    n_soul = 0
    échap = False

    couleur_avant : Vec3 = None
    couleur_arrière : Vec3 = None

    sauter_paramètre_couleur = ''

    traité = False
    ajouter_caractère = True

    for i in range(len(texte)):
        c = texte[i]
        traité = False
        ajouter_caractère = True
        if c == '*' and n_étoiles == 0 and not échap:
            n_étoiles = 1
        elif c == '*' and n_étoiles == 1 and not échap:
            n_étoiles = 2
        elif c == '*' and n_étoiles == 2 and not échap:
            n_étoiles = 3
        elif i>1 and texte[i-1] == '*' and c != '*' and (ouvert_italique or c != ' ') and n_étoiles == 1 and not échap:
            # marqueur italique
            n_étoiles = 0
            
            string = string[:-1]
            if ouvert_italique:
                ouvert_italique = False
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=True,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
            elif len(string) == 0:
                ouvert_italique = True
            else:
                ouvert_italique = True
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=False,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
        elif i>1 and texte[i-1] == '*' and c != '*' and (ouvert_gras or c != ' ') and n_étoiles == 2 and not échap:
            # marqueur gras
            n_étoiles = 0
            
            string = string[:-2]
            if ouvert_gras:
                ouvert_gras = False
                
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=True,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
            elif len(string) == 0:
                ouvert_gras = True
            else:
                ouvert_gras = True
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=False,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
        elif i>1 and texte[i-1] == '*' and c != '*' and n_étoiles == 3 and not échap:
            résultat += string[:-3] + '\n'+"="*50+'\n'
            string = ''
            n_étoiles = 0
            ajouter_caractère = False
        
        if c == '_' and n_soul == 0 and not échap:
            n_soul = 1
        elif c == '_' and n_soul == 1 and texte[i-1] == c and not échap:
            n_soul = 2
        elif c == '_' and n_soul == 2 and texte[i-1] == c and not échap:
            n_soul = 3
        elif i>1 and texte[i-1] == '_' and c != '_' and n_soul == 1 and not échap:
            # marqueur italique
            n_soul = 0
            
            string = string[:-1]
            if ouvert_italique:
                ouvert_italique = False
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=True,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
            elif len(string) == 0:
                ouvert_italique = True
            else:
                ouvert_italique = True
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=False,soul=ouvert_souligné,barré=ouvert_barré)
                résultat += string
                string = ''
        elif i>1 and texte[i-1] == '_' and c != '_' and n_soul == 2 and not échap:
            # marqueur gras
            n_soul = 0
            
            string = string[:-2]
            if ouvert_souligné:
                ouvert_souligné = False
                
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=ouvert_italique,soul=True,barré=ouvert_barré)
                résultat += string
                string = ''
            elif len(string) == 0:
                ouvert_souligné = True
            else:
                ouvert_souligné = True
                if ouvert_header:
                    string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=ouvert_italique,soul=False,barré=ouvert_barré)
                résultat += string
                string = ''
        elif i>1 and texte[i-1] == '_' and c != '_' and n_soul == 3 and not échap:
            résultat += string[:-3] + '\n'+"="*50+'\n'
            string = ''
            n_soul = 0
            ajouter_caractère = False

        if c == '~' and len(string) == 0 and not échap:
            ouvert_barré = True
            ajouter_caractère = False
        elif c == '~' and not ouvert_barré and len(string) != 0 and not échap:
            ouvert_barré = True
            ajouter_caractère = False
            
            if ouvert_header:
                string = 'h'+str(n_header)+' '+string
            string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=ouvert_italique,soul=ouvert_souligné,barré=False)
            résultat += string
            string = ''
        elif c == '~' and ouvert_barré and not échap:
            ouvert_barré = False
            ajouter_caractère = False
            
            if ouvert_header:
                string = 'h'+str(n_header)+' '+string
            string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=ouvert_italique,soul=ouvert_souligné,barré=True)
            résultat += string
            string = ''
        
        if c == '#' and not échap:
            n_marqeurs += 1
        elif i>0 and texte[i-1] == '#' and c == ' ' and not échap:
            n_header = n_marqeurs
            n_marqeurs = 0
            ouvert_header = True
            string = string[:-n_header]
            string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré)
            résultat += string
            string = ''
            ajouter_caractère = False
        elif i>1 and texte[i-1] == '#' and c != ' ' and not échap:
            n_marqeurs = 0
            n_header = 0
        elif ouvert_header and c == '\n' and not échap:
            ouvert_header = False
            
            if len(string) > 0:
                string = 'h'+str(n_header)+' '+string
                string = TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=True,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré)
            résultat += string
            string = ''
        
        if not ouvert_liste_nombres and c in "123456789" and not échap:
            estPremier = False
            j = 1
            while True:
                if i-j >= 0 and texte[i-j] == '\n':
                    estPremier = True 
                    break
                elif i-j >= 0 and texte[i-j] != ' ':
                    estPremier = False
                    break
                j+=1
            if estPremier:
                j = 1
                while True:
                    if len(texte)-1 >= i+j+1 and texte[i+j] == '.' and texte[i+j+1] == ' ':
                        ouvert_liste_nombres = True
                        résultat += string
                        string = ''
                        if texte[i-1] == ' ':
                            string = ''
                        else:
                            string = ''
                        
                        break
                    elif len(texte)-1 >= i+j+1 and not texte[i+j] in "123456789":
                        break
                    j+=1
        elif ouvert_liste_nombres and c == '\n' and not échap:
            ouvert_liste_nombres = False

        if c == '-' and n_marqeurs == 0 and not échap:
            n_marqeurs = 1
        elif c == '-' and n_marqeurs == 1 and not échap:
            n_marqeurs = 2
        elif c == '-' and n_marqeurs ==2 and not échap:
            n_marqeurs = 3
        if not ouvert_liste_points and c in "*-" and c != '' and len(texte)-1 >= i+1 and texte[i+1] == ' ' and not échap:
            estPremier = False
            j = 1
            while True:
                if i-j >= 0 and texte[i-j] == '\n':
                    estPremier = True 
                    break
                elif i-j >= 0 and texte[i-j] != ' ':
                    estPremier = False
                    break
                j+=1
            if estPremier:
                ouvert_liste_points = True
                résultat += string
                string = ''
                
                n_marqeurs = 0
        elif ouvert_liste_points and c == '\n' and not échap:
            ouvert_liste_points = False
        elif c != '-' and n_marqeurs == 3 and texte[i-1] == '-' and not échap:
            résultat += string[:-3] + '\n'+'='*50+'\n'
            string = ''
            n_marqeurs = 0
            ajouter_caractère = False
        
        if c == '>' and not échap:
            valide = False
            j = 1
            while True:
                if len(texte)-1 >= i+j and texte[i+j] == ' ' and ((i>0 and (texte[i-1]=='\n' or texte[i-1]=='>')) or i==0):
                    valide = True
                    break
                elif len(texte)-1 >= i+j and texte[i+j] != '>':
                    valide = False
                    break
                if len(texte)-1 < i+j:
                    break
                j+=1
            if valide:
                n_citation +=1
                résultat += string
                string = '|'
                ajouter_caractère = False
                
        if n_citation > 0 and c == '\n' and not échap:
            n_citation = 0
            if n_citation == 0 and len(texte)-1 >= i+1 and texte[i+1] != '>':
                string += '\n'

        if c == '`' and n_marqeurs == 0 and not échap:
            n_marqeurs = 1
        elif c == '`' and n_marqeurs == 1 and not échap:
            n_marqeurs = 2
        elif c == '`' and n_marqeurs == 2 and not échap:
            n_marqeurs = 3
        elif i > 0 and c != '`' and texte[i-1] == '`' and n_marqeurs == 1 and not échap:
            ouvert_code = not ouvert_code
            string = string[:-1]
            
            n_marqeurs = 0
        elif i > 0 and c != '`' and texte[i-1] == '`' and n_marqeurs==3 and not échap:
            string = string[:-3]+ '\n'
            ouvert_code_grand = not ouvert_code_grand
            
            n_marqeurs = 0

        if c=='<' or c=='{':
            couleur : Vec3 = None
            token = c
            fermeCouleurAvant = False
            fermeCouleurArrière = False
            j = 1
            while True:
                if len(texte)-1 >= i+j and texte[i+j] != ('>'if c=='<'else'}'):
                    token += texte[i+j]
                elif len(texte)-1 >= i+j and texte[i+j] == ('>'if c=='<'else'}'):
                    token += texte[i+j]
                    break
                if len(texte)-1 < i+j:
                    break
                j+=1
            token = token[1:-1].lower().split(';')
            if len(token) == 1:
                if token[0] == "/":
                    if c == '<':
                        fermeCouleurAvant = True
                    if c == '{':
                        fermeCouleurArrière = True
                elif token[0][0] == '#' and len(token[0])==7:
                    couleur = Vec3(int(token[0][1:3],16)/255,int(token[0][3:5],16)/255,int(token[0][5:],16)/255)
                else:
                    estPâle = False
                    estFoncé = False
                    if token[0][-1] == 'p':
                        estPâle = True
                        token[0] = token[:-1]
                    elif token[0][-5:]==" pâle":
                        estPâle = True
                        token[0] = token[:-5]
                    if token[0][-1] == 'f':
                        estFoncé = True
                        token[0] = token[:-1]
                    elif token[0][-6:]==" foncé":
                        estFoncé = True
                        token[0] = token[:-6]
                    match token[0]:
                        case 'r'|"rouge":
                            if estPâle:
                                couleur = ROUGE_PÂLE
                            elif estFoncé:
                                couleur = ROUGE_FONCÉ
                            else:
                                couleur = ROUGE
                        case 'o'|"orange":
                            if estPâle:
                                couleur = ORANGE_PÂLE
                            elif estFoncé:
                                couleur = ORANGE_FONCÉ
                            else:
                                couleur = ORANGE
                        case 'br'|"brun":
                            couleur = BRUN
                        case 'v'|"vert":
                            if estPâle:
                                couleur = VERT_PÂLE
                            elif estFoncé:
                                couleur = VERT_FONCÉ
                            else:
                                couleur = VERT
                        case 'b'|"bleu":
                            if estPâle:
                                couleur = BLEU_PÂLE
                            elif estFoncé:
                                couleur = BLEU_FONCÉ
                            else:
                                couleur = BLEU
                        case 'n'|"noir":
                            couleur = NOIR
                        case 'bl'|"blanc":
                            couleur = BLANC
                        case 'j'|"jaune":
                            if estPâle:
                                couleur = JAUNE_PÂLE
                            elif estFoncé:
                                couleur = JAUNE_FONCÉ
                            else:
                                couleur = JAUNE
                        case 'vi'|"violet":
                            if estPâle:
                                couleur = VIOLET_PÂLE
                            elif estFoncé:
                                couleur = VIOLET_FONCÉ
                            else:
                                couleur = VIOLET
                        case 'ma'|"magenta":
                            if estPâle:
                                couleur = MAGENTA_PÂLE
                            elif estFoncé:
                                couleur = MAGENTA_FONCÉ
                            else:
                                couleur = MAGENTA
                        case 'c'|"cyan":
                            if estPâle:
                                couleur = CYAN_PÂLE
                            elif estFoncé:
                                couleur = CYAN_FONCÉ
                            else:
                                couleur = CYAN
                        case 'tu'|"turquoise":
                            if estPâle:
                                couleur = TURQUOISE_PÂLE
                            elif estFoncé:
                                couleur = TURQUOISE_FONCÉ
                            else:
                                couleur = TURQUOISE
                        case 'be'|"beige":
                            couleur = BEIGE
                        case 'g'|"gris":
                            if estPâle:
                                couleur = GRIS_PÂLE
                            elif estFoncé:
                                couleur = GRIS_FONCÉ
                            else:
                                couleur = GRIS
                        case 'ro'|"rose":
                            couleur = ROSE
                        case 'or':
                            couleur = OR
            elif len(token) == 3:
                couleur = Vec3(float(token[0]),float(token[1]),float(token[2]))
        
            if couleur != None or fermeCouleurAvant or fermeCouleurArrière:
                if len(string) != 0:
                    if ouvert_header:
                        string = 'h'+str(n_header)+' '+string
                    résultat += TFX(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=(ouvert_gras or ouvert_header),ital=ouvert_italique,barré=ouvert_barré,soul=ouvert_souligné)
                    string = ''
                if fermeCouleurAvant:
                    ouvert_couleur_avant = False
                    couleur_avant = None
                elif c == '<':
                    ouvert_couleur_avant = True
                    couleur_avant = couleur
                if fermeCouleurArrière:
                    ouvert_couleur_arrière = False
                    couleur_arrière = None
                elif c == '{':
                    ouvert_couleur_arrière = True
                    couleur_arrière = couleur
                sauter_paramètre_couleur = c
        
        if sauter_paramètre_couleur != '':
            ajouter_caractère = False
            if sauter_paramètre_couleur == '<' and c=='>':
                sauter_paramètre_couleur = ''
            elif sauter_paramètre_couleur == '{' and c=='}':
                sauter_paramètre_couleur = ''
        
        if c=='\\' and not échap:   
            échap = True
            ajouter_caractère = False
        elif échap:
            échap = False

        if c == ' ' and not (ouvert_code or ouvert_code_grand):
            n_espaces +=1
            if not ouvert_espaces:
                ouvert_espaces = True
        if c != ' ' and ouvert_espaces and not (ouvert_code or ouvert_code_grand):
            ouvert_espaces = False
            
            if n_espaces != 1:
                if n_espaces < 4:
                    string = string[:-n_espaces] + " "
                elif n_espaces%4 == 0:
                    pass
                else:
                    string = string[:-(n_espaces%4)]
            else:
                pass
            n_espaces = 0

        if c == '\n' and not ouvert_code_grand:
            n_RL +=1
            if not ouvert_RL:
                ouvert_RL = True
        if c != '\n' and ouvert_RL  and not ouvert_code_grand:
            ouvert_RL = False
            
            garder = False
            défaut = False
            match c:
                case '#':
                    j = 1
                    while True:
                        if len(texte)-1 >= i+j and texte[i+j] == ' ':
                            garder = True
                            break
                        elif len(texte)-1 >= i+j and texte[i+j] != '#':
                            garder = False
                            break
                        if len(texte)-1 < i+j:
                            break
                        j+=1
                case '*'|'-'|'_':
                    if ( ( (c == '*' or c == '-') and len(texte)-1 >= i+1 and texte[i+1] == ' ') or
                        (len(texte)-1 >= i+2 and texte[i+1] == c and texte[i+2] == c) ):
                        garder = True
                case '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
                    j = 1
                    while True:
                        if len(texte)-1 >= i+j+1 and texte[i+j] == '.' and texte[i+j+1] == ' ':
                            garder = True
                            break
                        elif len(texte)-1 >= i+j and not texte[i+j] in '123456789':
                            garder = False
                            break
                        if len(texte)-1 < i+j:
                            break
                        j+=1
                case ' ':
                    j = 1
                    while True:
                        if len(texte)-1 >= i+j+1 and texte[i+j] in '*-.' and texte[i+j+1] == ' ':
                            garder = True
                            break
                        elif len(texte)-1 >= i+j and not texte[i+j] in ' 123456789':
                            garder = False
                            break
                        if len(texte)-1 < i+j:
                            break
                        j+=1
                case '>':
                    j = 1
                    while True:
                        if len(texte)-1 >= i+j and texte[i+j] == ' ':
                            garder = True
                            break
                        elif len(texte)-1 >= i+j and texte[i+j] != '>':
                            garder = False
                            break
                        if len(texte)-1 < i+j:
                            break
                        j+=1
                case _:
                    if n_RL == 1:
                        string = string[:-1] + ' '
                    elif not échap: 
                        string = string[:-1]
                    n_RL = 0
                    défaut = True
            if not défaut and not garder:
                string = string[:-1]
        
        if ajouter_caractère:
            string += c
    if len(string) != 0:
        résultat += string
    return résultat