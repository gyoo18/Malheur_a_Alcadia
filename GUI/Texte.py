from tkinter import Text
from tkinter import font as tkFont
from tkinter.font import Font
from Maths.Vec3 import Vec3
from TFX import *

class Texte(Text):
    def __init__(self,parent):
        super().__init__(parent)

        self.police_défaut = tkFont.nametofont(self.cget("font"))
        self.police_défaut.configure(weight="normal",slant="roman",underline=False,overstrike=False,size=int(self.police_défaut.cget("size")))
        self.polices : list[Font] = [self.police_défaut]
        self.polices_caracs : list[tuple[Vec3|None,Vec3|None,bool,bool,bool,bool,int]] = [(None,None,False,False,False,False,0)]
        self.tag_configure("0",font=self.police_défaut)

    def i(index,chars,*args):
        super.insert("end",chars,args)

    def insérerFormatté(self,texte : str, Pcoul : Vec3 = None, Scoul : Vec3 = None, gras = False, ital = False, soul = False, barré = False,niveau_Titre : int = 0):
        caracs_police : tuple[Vec3|None,Vec3|None,bool,bool,bool,bool,int] = (Pcoul,Scoul,gras,ital,soul,barré,niveau_Titre)
        police : Font = None
        indexe = -1
        for i in range(len(self.polices_caracs)):
            if caracs_police == self.polices_caracs[i]:
                police = self.polices[i]
                indexe = i
                break
        
        if police == None:
            police = Font(**self.police_défaut.configure())
            indexe = len(self.polices)

            if Pcoul != None:
                self.tag_configure(str(indexe),foreground='#'+hex(int(Pcoul.x*255))[2:]+hex(int(Pcoul.y*255))[2:]+hex(int(Pcoul.z*255))[2:])
            if Scoul != None:
                self.tag_configure(str(indexe),background='#'+hex(int(Scoul.x*255))[2:]+hex(int(Scoul.y*255))[2:]+hex(int(Scoul.z*255))[2:])
            if gras:
                police.configure(weight="bold")
            if ital:
                police.configure(slant="italic")
            if soul:
                police.configure(underline=True)
            if barré:
                police.configure(overstrike=True)
            if niveau_Titre != 0:
                if niveau_Titre == 1:
                    police.configure(size=int(self.police_défaut.cget("size")*6),weight="bold")
                if niveau_Titre == 2:
                    police.configure(size=int(self.police_défaut.cget("size")*5),weight="bold")
                if niveau_Titre == 3:
                    police.configure(size=int(self.police_défaut.cget("size")*4),weight="bold")
                if niveau_Titre == 4:
                    police.configure(size=int(self.police_défaut.cget("size")*3),weight="bold")
                if niveau_Titre == 5:
                    police.configure(size=int(self.police_défaut.cget("size")*2),weight="bold")
                if niveau_Titre == 6:
                    police.configure(size=int(self.police_défaut.cget("size")*1.5),weight="bold")
            self.tag_configure(str(indexe),font=police)
            self.polices.append(police)
            self.polices_caracs.append(caracs_police)

        self.insert("end",texte,str(indexe))

    def markdownFormattage(self,texte : str):
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

        ajouter_caractère = True

        for i in range(len(texte)):
            c = texte[i]
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
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=True,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
                elif len(string) == 0:
                    ouvert_italique = True
                else:
                    ouvert_italique = True
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=False,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
            elif i>1 and texte[i-1] == '*' and c != '*' and (ouvert_gras or c != ' ') and n_étoiles == 2 and not échap:
                # marqueur gras
                n_étoiles = 0
                
                string = string[:-2]
                if ouvert_gras:
                    ouvert_gras = False
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=True,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
                elif len(string) == 0:
                    ouvert_gras = True
                else:
                    ouvert_gras = True
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=False,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
            elif i>1 and texte[i-1] == '*' and c != '*' and n_étoiles == 3 and not échap:
                self.insérerFormatté('\n'+'='*50+'\n',Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
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
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=True,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
                elif len(string) == 0:
                    ouvert_italique = True
                else:
                    ouvert_italique = True
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=False,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
            elif i>1 and texte[i-1] == '_' and c != '_' and n_soul == 2 and not échap:
                # marqueur gras
                n_soul = 0
                
                string = string[:-2]
                if ouvert_souligné:
                    ouvert_souligné = False
                    
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=True,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
                elif len(string) == 0:
                    ouvert_souligné = True
                else:
                    ouvert_souligné = True
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=False,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
            elif i>1 and texte[i-1] == '_' and c != '_' and n_soul == 3 and not échap:
                self.insérerFormatté(string[:-3] + '\n'+"="*50+'\n',Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                string = ''
                n_soul = 0
                ajouter_caractère = False

            if c == '~' and len(string) == 0 and not échap:
                ouvert_barré = True
                ajouter_caractère = False
            elif c == '~' and not ouvert_barré and len(string) != 0 and not échap:
                ouvert_barré = True
                ajouter_caractère = False
                self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=False,niveau_Titre=n_header)
                string = ''
            elif c == '~' and ouvert_barré and not échap:
                ouvert_barré = False
                ajouter_caractère = False
                self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=True,niveau_Titre=n_header)
                string = ''
            
            if c == '#' and not échap:
                n_marqeurs += 1
            elif i>0 and texte[i-1] == '#' and c == ' ' and not échap:
                n_header = n_marqeurs
                n_marqeurs = 0
                ouvert_header = True
                string = string[:-n_header]
                self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=0)
                string = ''
                ajouter_caractère = False
            elif i>1 and texte[i-1] == '#' and c != ' ' and not échap:
                n_marqeurs = 0
                n_header = 0
            elif ouvert_header and c == '\n' and not échap:
                ouvert_header = False
                self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                string = ''
                n_header = 0
            
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
                            self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
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
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
                    string = ''
                    
                    n_marqeurs = 0
            elif ouvert_liste_points and c == '\n' and not échap:
                ouvert_liste_points = False
            elif c != '-' and n_marqeurs == 3 and texte[i-1] == '-' and not échap:
                self.insérerFormatté(string[:-3] + '\n'+"="*50+'\n',Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
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
                    self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
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
                        self.insérerFormatté(string,Pcoul=couleur_avant,Scoul=couleur_arrière,gras=ouvert_gras,ital=ouvert_italique,soul=ouvert_souligné,barré=ouvert_barré,niveau_Titre=n_header)
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