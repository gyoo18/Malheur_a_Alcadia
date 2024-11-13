def Constructeur():
    pass

def Boucle():
    return True

def Destructeur():
    pass

def main():
    Constructeur()

    continuer = True
    while continuer:
        continuer = Boucle()
    
    Destructeur()

if __name__ == "__main__":
    main()