#Instrucciones
class Instruccion:
    "Clase abstracta para instrucciones"

class Pekenun(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

class Tuntentu(Instruccion) :
    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class DefVar(Instruccion) :
    def __init__(self, id,tipo) :
        self.id = id
        self.tipo = tipo

class AsignaVariable(Instruccion) :
    def __init__(self, id, exp,n) :
        self.id = id
        self.exp = exp
        self.n = n

class May(Instruccion) : 
    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class KMay(Instruccion) : 
    def __init__(self, expLogica, instrliVerdadero = [], instrliFalso = []) :
        self.expLogica = expLogica
        self.instrliVerdadero = instrliVerdadero
        self.instrliFalso = instrliFalso

#EXPRESIONES    
class ExpresionNumerica:
        "Expresiones numericas"  
class ExpresionBinaria(ExpresionNumerica) :
    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.val = 0
class ExpresionNegativo(ExpresionNumerica) :
    def __init__(self, exp) :
        self.exp = exp
class ExpresionNumero(ExpresionNumerica) :
    def __init__(self, val = 0) :
        self.val = val
class ExpresionIdentificador(ExpresionNumerica) :
    def __init__(self, id = "") :
        self.id = id
class ExpresionCadena :
    "Cadena de texto"
class ExpresionConcatenar(ExpresionCadena) :
    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2
class ExpresionDobleComilla(ExpresionCadena) :
    def __init__(self, val) :
        self.val = val
class ExpresionCadenaNumerico(ExpresionCadena) :
    def __init__(self, exp) :
        self.exp = exp
class ExpresionLogica() :
    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador