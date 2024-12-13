import tkinter as tk
from tkinter import Frame, Label, Button, Tk, Widget

class TkFenetre:
    def __init__(self, frame : Frame):
        self.frame : Frame = frame
        self.widgets_enregistrés : dict[Widget] = {}
        self.initialisé : bool = False
        self.état = -1
    
    def enregistrerWidget(self, widget : Widget, nom : str):
        if nom in self.widgets_enregistrés.keys() or widget in self.widgets_enregistrés:
            raise ValueError("[etiquetterWidget] Soit le nom " + str(nom) + " soit le widget " + str(widget) + " sont déjà définis. Veuillez indiquer une paire widget:nom unique.")
        self.widgets_enregistrés[nom] = widget
        
    def obtenirWidget(self, nom : str) -> Widget:
        if not nom in self.widgets_enregistrés.keys():
            raise ValueError("[obtenirWidget] Le nom " + str(nom) + " n'est pas un nom de widget enregistré dans cette TkFenetre.")
        return self.widgets_enregistrés[nom]
    
