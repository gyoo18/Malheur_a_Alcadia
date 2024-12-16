from __future__ import annotations
from GUI.Texte import Texte
from TFX import *

class Log(Texte):
    logger : Log = None

    def __init__(self,parent,cnf={},**kw):
        super().__init__(parent,cnf,**kw)

    def initLogger(parent,cnf={},**kw):
        Log.logger = Log(parent,cnf,**kw)
    
    def log(texte : str,end="\n"):
        Log.logger.insérerFormatté(texte+end)
        print(texte,end=end)
    
    def mdwn(texte : str,end="\n"):
        Log.logger.markdownFormattage(texte+end)
        print(markDownFormattage(texte),end=end)