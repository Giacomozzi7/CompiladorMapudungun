#Instrucciones
class Instruccion:
    "Clase abstracta para aInst"

class Pekenun(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

class Tuntentu(Instruccion) :
    def __init__(self, eL, aInst = []) :
        self.eL = eL
        self.aInst = aInst

class DefVar(Instruccion) :
    def __init__(self, id,tipo) :
        self.id = id
        self.tipo = tipo

class AsignaVariable(Instruccion) :
    def __init__(self, id, exp,nVal) :
        self.id = id
        self.exp = exp
        self.nVal = nVal

class May(Instruccion) : 
    def __init__(self, eL, aInst = []) :
        self.eL = eL
        self.aInst = aInst

class KMay(Instruccion) : 
    def __init__(self, eL, aInstMayV = [], aInstMayF = []) :
        self.eL = eL
        self.aInstMayV = aInstMayV
        self.aInstMayF = aInstMayF

#EXPRESIONES    
class EXPNUMERICA:
        "Expresiones numericas"  
class EXP_BIN(EXPNUMERICA) :
    def __init__(self, expresion_1, expresion_2, op) :
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        self.op = op
        self.valor = 0
class EXP_NEG(EXPNUMERICA) :
    def __init__(self, exp) :
        self.exp = exp
class EXP_NUM(EXPNUMERICA) :
    def __init__(self, valor = 0) :
        self.valor = valor
class EXP_ID(EXPNUMERICA) :
    def __init__(self, id = "") :
        self.id = id

class EXPSTRING :
    "Cadena de texto"
class EXP_CONCAT(EXPSTRING) :
    def __init__(self, expresion_1, expresion_2) :
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
class EXP_DOBLE(EXPSTRING) :
    def __init__(self, valor) :
        self.valor = valor
class EXP_CAD(EXPSTRING) :
    def __init__(self, exp) :
        self.exp = exp

class EXP_LOGICA() :
    def __init__(self, expresion_1, expresion_2, op) :
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        self.op = op