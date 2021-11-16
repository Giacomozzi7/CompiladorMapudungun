import ply.lex as lex
from instrucciones import *
from analizadorlexico import *
import TabSimbolos
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
    ('left','PAREIZQ','PAREDER')
)

def p_INIT(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_LISTA_INSTRUCCIONES(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_DEFINICION_INSTRUCCION(t) :
    '''definicion_instr   : RAKIN ID
                          | NEMEL ID'''
    if   t[1] == "rakin": t[0] = DefVar(t[2],t[1])
    elif t[1] == "nemel": t[0] = DefVar(t[2],t[1])

def p_INSTRUCCIONES_INSTRUCCION(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_INSTRUCCION(t) :
    '''instruccion      : pekenun_instr
                        | definicion_instr
                        | asignacion_instr
                        | tuntentu_instr
                        | may_instr
                        | kmay_instr'''
    t[0] = t[1]

def p_PEKENUN_INSTRUCCCION(t) :
    'pekenun_instr     : PEKENUN PAREIZQ expresion_cadena PAREDER'
    t[0] =Pekenun(t[3])

def p_ASIGNAVARIABLE_INSTRUCCION(t) :
    '''asignacion_instr   : ID ASIGNACION expresion_numerica
                          | ID ASIGNACION expresion_cadena '''
    if   (type(t[3].val)==int) : 
        t[0] = AsignaVariable(t[1], t[3], 0)

    elif (type(t[3].val)==str) : 
        t[0]  = AsignaVariable(t[1], t[3],1)

def p_TUNTENTU_INSTRUCCION(t) :
    'tuntentu_instr     : TUNTENTU PAREIZQ expresion_logica PAREDER ANTU instrucciones KUYEN'
    t[0] =Tuntentu(t[3], t[6])

def p_MAY_INSTRUCCION(t) :
    'may_instr           : MAY PAREIZQ expresion_logica PAREDER ANTU instrucciones KUYEN'
    t[0] =May(t[3], t[6])

def p_KMAY_INSTRUCCION(t) :
    'kmay_instr      : MAY PAREIZQ expresion_logica PAREDER ANTU instrucciones KUYEN KMAY ANTU instrucciones KUYEN'
    t[0] =KMay(t[3], t[6], t[10])


#Definicion de expresiones  para el analizador sintactico
#--------------------------------------------------------------------------------------------
def p_BIN_EXPRESION(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        '''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], "+")
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], "-")
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], "*")
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], "/")

def p_AGRUP_EXPRESION(t):
    'expresion_numerica : PAREIZQ expresion_numerica PAREDER'
    t[0] = t[2]

def p_NUMERO_EXPRESION(t):
    '''expresion_numerica : INT
                          | FLOTANTE'''
    t[0] = ExpresionNumero(t[1])

def p_ID_EXPRESION(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionIdentificador(t[1])

def p_CADENATEXTO_EXPRESION(t) :
    'expresion_cadena     : CADENA_TEXTO'
    t[0] = ExpresionDobleComilla(t[1])

def p_CADENANUM_EXPRESION(t) :
    'expresion_cadena     : expresion_numerica'
    t[0] = ExpresionCadenaNumerico(t[1])

def p_CONCAT_EXPRESION(t) :
    'expresion_cadena     : expresion_cadena CONCAT expresion_cadena'
    t[0] = ExpresionConcatenar(t[1], t[3])

def p_LOGICO_EXPRESION(t) :
    '''expresion_logica : expresion_numerica MAYOR expresion_numerica
                        | expresion_numerica MENOR expresion_numerica
                        | expresion_numerica IGUALQUE expresion_numerica
                        | expresion_numerica DISTINTO expresion_numerica'''
    if t[2] == '>'    : t[0] = ExpresionLogica(t[1], t[3], '>')
    elif t[2] == '<'  : t[0] = ExpresionLogica(t[1], t[3], '<')
    elif t[2] == '==' : t[0] = ExpresionLogica(t[1], t[3], '=')
    elif t[2] == '!=' : t[0] = ExpresionLogica(t[1], t[3], '<>')

def p_error(t):
    global nFlag
    if t: 
        resultado = f">> ERROR: sintaxis incorrecta de tipo {t.type} cerca de {t.value}"
        nFlag=1
        aResultado.append(resultado)


parser = yacc.yacc()
def resolverTuntentu(instr, ts) :
    while operacionLogica(instr.expLogica, ts) :
        ts_local = TabSimbolos.TablaDeSimbolos(ts.simbolos)
        generarInstrucciones(instr.instrucciones, ts_local)

def resolverMay(instr, ts) :
    if operacionLogica(instr.expLogica, ts) :
        ts_local = TabSimbolos.TablaDeSimbolos(ts.simbolos)
        generarInstrucciones(instr.instrucciones, ts_local)

def resolverKMay(instr, ts) :
    if operacionLogica(instr.expLogica, ts):
        ts_local = TabSimbolos.TablaDeSimbolos(ts.simbolos)
        generarInstrucciones(instr.instrliVerdadero, ts_local)
    else :
        ts_local = TabSimbolos.TablaDeSimbolos(ts.simbolos)
        generarInstrucciones(instr.instrliFalso, ts_local)

def procesarString(expCad, ts) :
    if isinstance(expCad, ExpresionConcatenar) :
        exp1 = procesarString(expCad.exp1, ts)
        exp2 = procesarString(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionDobleComilla) :
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico) :
        return str(operacionAritmetica(expCad.exp, ts))
    else : 
        print('>> ERROR: Cadena no válida')

def procesarDef(instr, ts) :
    if instr.tipo == "rakin": simbolo = TabSimbolos.Simbolo(instr.id, TabSimbolos.TIPO_DATO.RAKIN, 0)
    if instr.tipo == "nemel": simbolo = TabSimbolos.Simbolo(instr.id, TabSimbolos.TIPO_DATO.NEMEL, "")
    ts.addSimbolo(simbolo)

def procesarAsign(instr, ts) :
    if instr.n == 0:
        simbolo = TabSimbolos.Simbolo(instr.id, TabSimbolos.TIPO_DATO.RAKIN, operacionAritmetica(instr.exp, ts))
    if instr.n == 1:
        simbolo = TabSimbolos.Simbolo(instr.id, TabSimbolos.TIPO_DATO.NEMEL, procesarString(instr.exp, ts))
    ts.UpdSimbolo(simbolo)

#Procesamiento de operaciones lógicas
def operacionLogica(expLog, ts) :
    exp1 = operacionAritmetica(expLog.exp1, ts)
    exp2 = operacionAritmetica(expLog.exp2, ts)
    if expLog.operador == '>' : return exp1 > exp2
    if expLog.operador == '<' : return exp1 < exp2
    if expLog.operador == '=' : return exp1 == exp2
    if expLog.operador == '<>' : return exp1 != exp2

def operacionAritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        exp1 = operacionAritmetica(expNum.exp1, ts)
        exp2 = operacionAritmetica(expNum.exp2, ts)
        if expNum.operador == '+' : return exp1 + exp2
        if expNum.operador == '-' : return exp1 - exp2
        if expNum.operador == '*' : return exp1 * exp2
        if expNum.operador == '/' : return exp1 / exp2

    elif isinstance(expNum, ExpresionNegativo) :
        exp = operacionAritmetica(expNum.exp, ts)
        return exp * -1

    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val

    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.getSimbolo(expNum.id).valor

#Fase de prueba y generacion de instrucciones para ser mostradas en la interfaz
def prueba_sintactica(data):
    global nFlag
    instrucciones = parser.parse(data)
    nFlag = 0
    ts_global = TabSimbolos.TablaDeSimbolos()
    return generarInstrucciones(instrucciones, ts_global)

def generarInstrucciones(instrucciones, ts) :
    global aResultado
    global nFlag
    try:
        for instr in instrucciones :
            if (nFlag!=0): break
            if isinstance(instr, Pekenun) : 
                sP = '>> %s'%(procesarString(instr.cad, ts))
                aResultado.append(sP)
            elif isinstance(instr, DefVar) : procesarDef(instr, ts)
            elif isinstance(instr, AsignaVariable) : procesarAsign(instr, ts)
            elif isinstance(instr, Tuntentu) : resolverTuntentu(instr, ts)
            elif isinstance(instr, May) : resolverMay(instr, ts)
            elif isinstance(instr, KMay) : resolverKMay(instr, ts)
            else : aResultado.append('>> ERROR: La instrucción es inválida')
    except: pass
    return aResultado