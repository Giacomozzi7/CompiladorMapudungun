'Corresponde a cada simbolo que compondra la tabla de simbolos'
class Simbolo() :
    def __init__(self, idSimbolo, tipoSimbolo, valorSimbolo) :
        self.id    = idSimbolo
        self.tipo  = tipoSimbolo
        self.valor = valorSimbolo

'Tabla de simbolos'
class TablaDeSimbolos() :
    def __init__(self, dictSimbolos = {}) :   
        self.simbolos = dictSimbolos
    def addSimbolo(self, simbolo) :       self.simbolos[simbolo.id] = simbolo
    def getSimbolo(self, id) :            return self.simbolos[id]
    def UpdSimbolo(self, simbolo) : 
        if simbolo.id in self.simbolos :  self.simbolos[simbolo.id] = simbolo

        
