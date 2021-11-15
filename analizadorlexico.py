import ply.lex as lex
import re
import codecs
import os
import sys

#Palabras reservadas y Tokens

aRes = [
    'BEGIN', #Begin
    'FOR',   #For
    'END',   #End
    'IF',    #If
    'ELSE',  #Else
    'NOT',   #Not
    'WHILE', #While
    'IN',    #In
    'PRINT', #Print
    'NUM',   #Int
    'STRING' #String
]

tokens = aRes + ['ID','INT','FLOTANTE','MAS','MENOS','POR','DIVIDIDO','ASIGNACION',
                 'DISTINTO','MENOR','MAYOR','PAREIZQ','PAREDER','COMENTARIO','POTENCIA',
                 'COMENTARIO_MULTILINEA','IGUALQUE','CADENA_TEXTO','CONCAT','COMA']

aResultado = []

#Expresiones regulares para los tokens
t_ignore = '\t'
t_MAS =   r'\+'
t_MENOS = r'\-'
t_POR =   r'\*'
t_DIVIDIDO = r'/'
t_ASIGNACION = r'='
t_DISTINTO = r'<>'
t_MENOR = r'<'
t_MAYOR = r'>'
t_PAREIZQ = r'\('
t_PAREDER = r'\)'
t_COMA = r','
t_POTENCIA = r'\^'
t_IGUALQUE = r'=='
t_CONCAT = r'&'

#Se definen funciones con expresiones regulares complejas
#-----------------------------------------------------------------------
#FUNCION PARA EXPRESION IDENTIFICADOR
def t_ID(t):
    r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    if t.value in aRes: t.type = t.value.upper()
    else: t.type = 'ID'
    return t

#FUNCION PARA EXPRESION NUEVA LINEA
def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#FUNCION PARA EXPRESION STRING
def t_CADENA_TEXTO(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t 

#FUNCION PARA EXPRESION COMENTARIO
def t_COMENTARIO(t):
    r'\@.*'
    pass

#FUNCION PARA EXPRESION FLOAT
def t_FLOTANTE(t):
    r'\d+\.\d+'
    try: t.value = float(t.value)
    except:
        print(f'Valor flotante invalido {t.value}')
        t.value = 0
    return t

#FUNCION PARA EXPRESION INT
def t_INT(t):
    r'\d+'
    try: t.value = int(t.value)
    except:
        print(f'Valor entero invalido {t.value}')
        t.value = 0
    return t

#FUNCION PARA EXPRESION ESPACIOS
def t_NONSPACE(t):
    r'\s+'
    pass

def t_error(t):
    global aResultado
    estado = [t.lineno,t.lexpos,'TOKEN INVALIDO', t.value]
    aResultado.append(estado)
    t.lexer.skip(1)

def prueba(sData):
    global aResultado
    an = lex.lex()
    an.input(sData)
    aResultado.clear()
    while True:
        token = an.token()
        if not token: break
        estado = [token.lineno,token.lexpos,token.type,token.value]
        aResultado.append(estado)
    return aResultado
































# def buscarFicheros(directorio):
#     ficheros = []
#     numArchivo = ''
#     respuesta = False
#     cont = 1

#     for base, dirs, files in os.walk(directorio):
#         ficheros.append(files)

#     for file in files:
#         print(str(cont)+". "+file)
#         cont = cont+1
    
#     while respuesta == False:
#         numArchivo = input('\nNumero del test:')
#         for file in files:
#             if file == files[int(numArchivo)-1]:
#                 respuesta = True
#                 break
#     print(f"Has escogido {files[int(numArchivo)-1]}")

#     return files[int(numArchivo)-1]



# directorio = 'D://Documentos//GitHub//CompiladorMapudungun//data//pruebas//'
# archivo = buscarFicheros(directorio)
# test = directorio+archivo
# fp = codecs.open(test,"r","utf-8")
# cadena = fp.read()
# fp.close()

# analizador = lex.lex()

# analizador.input(cadena)

# while True:
#     tok = analizador.token()
#     if not tok: break
#     print (tok)








