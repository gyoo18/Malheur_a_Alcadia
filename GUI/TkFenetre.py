import tkinter as tk
from Dessin.Peintre import Peintre

class TkFenetre:
    def __init__(self):
        self.root = tk.Tk()
        self.peintre = Peintre(self.root)
        self.peintre.pack(expand=True, fill='both', padx=50, pady=50)

    def démarrer(self):
        self.root.mainloop()