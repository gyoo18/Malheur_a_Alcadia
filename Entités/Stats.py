import random
#Exemple de stats que l'on pourrait faire
def Stats_earth_golems():
    HP=150
    print(f"HP: {HP}")
    ATT=int(random.choice(range(10,16)))
    print(f"Attaque: {ATT}")
    DEF=int(random.choice(range(39,46)))
    print(f'Défence: {DEF}')
    return ATT and DEF and HP
    
Stats_earth_golems()
def Damage(ATT,DEF):
    Dm=ATT-ATT*DEF/100
    return Dm