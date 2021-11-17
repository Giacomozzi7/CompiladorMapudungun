from clases_exp import *
from analizadorlexico import *
from tablasimbolos import Simbolo,TablaDeSimbolos
import ply.yacc as yacc
nFlag = 0
aResultado=[]

#Se define la precedencia de los tokens
#Right indica que la precedencia es por la derecha
#Left indica que la precedencia es por la izquierda
precedence = (
    ('right','ASIGNACION'),
    ('left','DISTINTO'),
    ('left','MENOR','MAYOR'),
    ('left','MAS', 'MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','PARENTESISIZQ','PARENTESISDER')
)

def p_INIT(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_LISTA_INSTRUCCIONES(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_DEFINICION_INSTRUCCION(t) :
    '''instDefinicion   : RAKIN ID
                          | NEMEL ID'''
    if   t[1] == "rakin": t[0] = DefVar(t[2],t[1])
    elif t[1] == "nemel": t[0] = DefVar(t[2],t[1])

def p_INSTRUCCIONES_INSTRUCCION(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_INSTRUCCION(t) :
    '''instruccion      : instPekenun
                        | instDefinicion
                        | instAsignacion
                        | instTuntentu
                        | instMay
                        | instKMay'''
    t[0] = t[1]

def p_PEKENUN_INSTRUCCCION(t) :
    'instPekenun     : PEKENUN PARENTESISIZQ expString PARENTESISDER'
    t[0] =Pekenun(t[3])

def p_ASIGNAVARIABLE_INSTRUCCION(t) :
    '''instAsignacion   : ID ASIGNACION expNumero
                          | ID ASIGNACION expString '''
    if   (type(t[3].valor)==int) : 
        t[0] = AsignaVariable(t[1], t[3], 0)

    elif (type(t[3].valor)==str) : 
        t[0]  = AsignaVariable(t[1], t[3],1)

def p_TUNTENTU_INSTRUCCION(t) :
    'instTuntentu     : TUNTENTU PARENTESISIZQ eL PARENTESISDER ANTU instrucciones KUYEN'
    t[0] =Tuntentu(t[3], t[6])

def p_MAY_INSTRUCCION(t) :
    'instMay           : MAY PARENTESISIZQ eL PARENTESISDER ANTU instrucciones KUYEN'
    t[0] =May(t[3], t[6])

def p_KMAY_INSTRUCCION(t) :
    'instKMay      : MAY PARENTESISIZQ eL PARENTESISDER ANTU instrucciones KUYEN KMAY ANTU instrucciones KUYEN'
    t[0] =KMay(t[3], t[6], t[10])


#Definicion de expresiones  para el analizador sintactico
#--------------------------------------------------------------------------------------------
def p_BIN_EXPRESION(t):
    '''expNumero : expNumero MAS expNumero
                        | expNumero MENOS expNumero
                        | expNumero POR expNumero
                        | expNumero DIVIDIDO expNumero
                        '''
    if   t[2] == '+': t[0] = EXP_BIN(t[1], t[3], "+")
    elif t[2] == '-': t[0] = EXP_BIN(t[1], t[3], "-")
    elif t[2] == '*': t[0] = EXP_BIN(t[1], t[3], "*")
    elif t[2] == '/': t[0] = EXP_BIN(t[1], t[3], "/")

def p_AGRUP_EXPRESION(t):
    'expNumero : PARENTESISIZQ expNumero PARENTESISDER'
    t[0] = t[2]

def p_NUMERO_EXPRESION(t):
    '''expNumero : INT
                          | FLOTANTE'''
    t[0] = EXP_NUM(t[1])

def p_ID_EXPRESION(t):
    'expNumero   : ID'
    t[0] = EXP_ID(t[1])

def p_CADENATEXTO_EXPRESION(t) :
    'expString     : CADENA_TEXTO'
    t[0] = EXP_DOBLE(t[1])

def p_CADENANUM_EXPRESION(t) :
    'expString     : expNumero'
    t[0] = EXP_CAD(t[1])

def p_CONCAT_EXPRESION(t) :
    'expString     : expString CONCAT expString'
    t[0] = EXP_CONCAT(t[1], t[3])

def p_LOGICO_EXPRESION(t) :
    '''eL : expNumero MAYOR expNumero
                        | expNumero MENOR expNumero
                        | expNumero IGUALQUE expNumero
                        | expNumero DISTINTO expNumero'''
    if   t[2] == '>'  : t[0] = EXP_LOGICA(t[1], t[3], '>')
    elif t[2] == '<'  : t[0] = EXP_LOGICA(t[1], t[3], '<')
    elif t[2] == '==' : t[0] = EXP_LOGICA(t[1], t[3], '=')
    elif t[2] == '!=' : t[0] = EXP_LOGICA(t[1], t[3], '<>')

def p_error(t):
    global nFlag
    if t: 
        sError = f">> ERROR: sintaxis incorrecta de tipo {t.type} cerca de {t.value}"
        nFlag=1
        aResultado.append(sError)

#Se resuelven las palabras reservadas Tuntentu, May y KMay
parser = yacc.yacc()
def resolverTuntentu(objInstruccion, objTS) :
    while operacionLogica(objInstruccion.eL, objTS) :
        generarInstrucciones(objInstruccion.aInst, TablaDeSimbolos(objTS.simbolos))

def resolverMay(objInstruccion, objTS) :
    if operacionLogica(objInstruccion.eL, objTS) :
        generarInstrucciones(objInstruccion.aInst, TablaDeSimbolos(objTS.simbolos))

def resolverKMay(objInstruccion, objTS) :
    if operacionLogica(objInstruccion.eL, objTS):
        generarInstrucciones(objInstruccion.aInstMayV, TablaDeSimbolos(objTS.simbolos))
    else :
        generarInstrucciones(objInstruccion.aInstMayF, TablaDeSimbolos(objTS.simbolos))

def procesarString(expCad, objTS) :
    if type(expCad) == EXP_CONCAT      : return procesarString(expCad.expresion_1, objTS) + procesarString(expCad.expresion_2, objTS)
    elif type(expCad) == EXP_DOBLE     : return expCad.valor #Expresion para cadena con doble comilla
    elif type(expCad) == EXP_CAD       : return str(operacionAritmetica(expCad.exp, objTS))

def procesarDef(objInstruccion, objTS) :
    if objInstruccion.tipo == "rakin": simbolo = Simbolo(objInstruccion.id, "RAKIN", 0)
    if objInstruccion.tipo == "nemel": simbolo = Simbolo(objInstruccion.id, "NEMEL", "")
    objTS.addSimbolo(simbolo)

def procesarAsign(objInstruccion, objTS) :
    if objInstruccion.nVal == 0:
        simbolo = Simbolo(objInstruccion.id, "RAKIN", operacionAritmetica(objInstruccion.exp, objTS))
    if objInstruccion.nVal == 1:
        simbolo = Simbolo(objInstruccion.id, "NEMEL", procesarString(objInstruccion.exp, objTS))
    objTS.UpdSimbolo(simbolo)

#Procesamiento de operaciones lógicas
def operacionLogica(expresionLogica, objTS) :
    aExp = [operacionAritmetica(expresionLogica.expresion_1, objTS),operacionAritmetica(expresionLogica.expresion_2, objTS)]
    if expresionLogica.op == '>'  : return aExp[0] > aExp[1]
    if expresionLogica.op == '<'  : return aExp[0] < aExp[1]
    if expresionLogica.op == '='  : return aExp[0] == aExp[1]
    if expresionLogica.op == '<>' : return aExp[0] != aExp[1]

#Procesamiento de operaciones aritmeticas
def operacionAritmetica(expresionNumerica, objTS) :
    if type(expresionNumerica) == EXP_BIN:
        aExp = [operacionAritmetica(expresionNumerica.expresion_1, objTS),operacionAritmetica(expresionNumerica.expresion_2, objTS)]
        if expresionNumerica.op == '+' : return aExp[0] + aExp[1]
        if expresionNumerica.op == '-' : return aExp[0] - aExp[1]
        if expresionNumerica.op == '*' : return aExp[0] * aExp[1]
        if expresionNumerica.op == '/' : return aExp[0] / aExp[1]

    elif type(expresionNumerica) == EXP_NEG:        return operacionAritmetica(expresionNumerica.exp, objTS) * -1
    elif type(expresionNumerica) == EXP_NUM:        return expresionNumerica.valor
    elif type(expresionNumerica) == EXP_ID:         return objTS.getSimbolo(expresionNumerica.id).valor

#Fase de prueba y generacion de instrucciones para ser mostradas en la interfaz
def analizadorSintactico(sData):
    global nFlag
    aInstrucciones = parser.parse(sData)
    nFlag = 0
    return generarInstrucciones(aInstrucciones, TablaDeSimbolos())

def generarInstrucciones(aInstrucciones, objTS) :
    global aResultado
    global nFlag
    try:
        for objInstruccion in aInstrucciones :
            print(f'instrucciones : {aInstrucciones}')
            if (nFlag!=0): break
            if isinstance(objInstruccion, Pekenun) : 
                sP = '>> %s'%(procesarString(objInstruccion.cad, objTS))
                aResultado.append(sP)
            elif type(objInstruccion) == DefVar:          procesarDef(objInstruccion, objTS)
            elif type(objInstruccion) == AsignaVariable:  procesarAsign(objInstruccion, objTS)
            elif type(objInstruccion) == Tuntentu:        resolverTuntentu(objInstruccion, objTS)
            elif type(objInstruccion) == May :            resolverMay(objInstruccion, objTS)
            elif type(objInstruccion) == KMay :           resolverKMay(objInstruccion, objTS)
            else : aResultado.append('>> ERROR: La instrucción es inválida')
    except: pass
    return aResultado