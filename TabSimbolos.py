from enum import Enum

class TIPO_DATO(Enum) :
    RAKIN = 1
    NEMEL = 2
class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'
    def __init__(self, id, tipo, valor) :
        self.id = id
        self.tipo = tipo
        self.valor = valor

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'
    def __init__(self, simbolos = {}) :   self.simbolos = simbolos
    def addSimbolo(self, simbolo) :       self.simbolos[simbolo.id] = simbolo
    def getSimbolo(self, id) :            return self.simbolos[id]
    def UpdSimbolo(self, simbolo) : 
        if simbolo.id in self.simbolos :  self.simbolos[simbolo.id] = simbolo

        
