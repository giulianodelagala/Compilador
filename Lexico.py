#Analizador Lexico

from Errores import Log

DIC_TOKENS = {'+':'Add', 
                '-':'Rest',
                '*':'Mult',
                '/':'Divi',
                '=':'Asignar',
                '(':'AbreParentesis',
                ')':'CierraParentesis',
                '\n': 'semicolon',
                '{' : 'AbreLlave',
                '}' : 'CierraLlave',
                '=' : 'equal',
                'int': 'integer',
                'node': 'node',
                'edge': 'edge',
                '->' : 'flecha',
                '==' : 'igualdad',
                '<'  : 'menor',
                '>'  : 'mayor',
                '{'  : 'abrellave',
                '}'  : 'cierrallave',
                'if' : 'if',
                'then':'then'
                }

log = Log.getInstance()

def reconoceNumero(linea : str, num_linea:int, idx : int):
    token = ""
    while (idx < len(linea)):
        if (linea[idx].isnumeric()):
            token += linea[idx]
            idx += 1
        elif (linea[idx].isalpha()):
            #Caracter encontrado posible numero
            return token, idx, 100
        elif (linea[idx] not in DIC_TOKENS and linea[idx] != ' '):
            return token, idx, 101
        elif (linea[idx] in DIC_TOKENS or linea[idx] == ' '):
            break        
        else:
            return token, idx, 400
    return ['Num',token, num_linea, idx], idx, 0

def reconoceVariable(linea : str, num_linea:int, idx : int):
    token =""
    while (idx < len(linea)):
        if (linea[idx].isalnum()):
            token += linea[idx]
            idx += 1
        elif (linea[idx] not in DIC_TOKENS and linea[idx] != ' '):
            #Fin del token
            return token, idx, 101
        elif (linea[idx] in DIC_TOKENS or linea[idx] == ' '):
            break  
        else: 
            return token, idx, 400
    if (token in DIC_TOKENS):
        #token especial reconocido
        return [token,token, num_linea, idx], idx, 0
    else:
        #variable reconocida
        return ['Var',token, num_linea, idx], idx, 0

def reconoceToken(linea : str, num_linea:int, idx : int):
    token = ""
    temp = ""
    while (idx < len(linea)):
        temp = token + linea[idx] 
        if (temp in DIC_TOKENS):
            token = temp
            idx += 1
        else:
            break
    return [DIC_TOKENS[token], token, num_linea, idx], idx, 0

def AnalizadorLexico(file : str, ind_linea = 0):
    tokens = []
    f = open(file, "r")
    
    for linea in f:

        idx = 0
        while (idx < len(linea)):   
            #Verificando que clase de token tenemos
            if (linea[idx].isalpha()):
                token, idx, error = reconoceVariable(linea, ind_linea, idx)
            elif (linea[idx].isdigit()):
                token, idx, error = reconoceNumero(linea, ind_linea, idx)
            elif (linea[idx] in DIC_TOKENS):
                token, idx, error = reconoceToken (linea, ind_linea, idx)
            elif (linea[idx] == ' '):
                idx+=1
                continue
            else:
                error = 100
            
            #Captura de Errores
            if (error == 0):
                tokens.append(token)
            else:
                log.addError(error, linea, idx)
                idx+=1
        ind_linea+=1
    return tokens

if __name__ == "__main__":
    cadena = input("Cadena: ")
    print(AnalizadorLexico(cadena))
    log.Print()