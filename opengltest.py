from Dessin.Peintre import Peintre
from tkinter import Tk, Label

root = Tk()
label = Label(root,text="test")
label.pack()
peintre = Peintre(root,width=100,height=100)
peintre.pack(fill="both",expand=True)

while True:
    root.update_idletasks()
    root.update()
