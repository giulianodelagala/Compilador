#Definicion de Clases Gramatica

import abc
from Errores import Log
from Traduccion import *

dic_clases = {'Num' : 'Num',
                'lambda' : 'Lambda',
             '+' : "Add", 
             '-' : "Rest",
             '*' : "Mult",
              '/' : "Divi",
              '(':'AbreParentesis',
              ')':'CierraParentesis',
              'int':'integer',
              '->' :'flecha',
              'if' :'if_sta'
                        }

dic_variables = {}

log = Log.getInstance()
#Rutinas en C++
Trad = Traduccion()

class AbstractExpresion(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def interpret(self):
        pass

class NodoNoTerminal(AbstractExpresion):
    def __init__(self, expression):
        self.expression = expression
        self.prod = {}
        
    def interpret(self):
        self.expression.interpret()

class NodoTerminal(AbstractExpresion):
    def interpret(self):
        pass

class Program (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Program')
        self.linea = linea
        self.prod['Data_decs'] = None
        self.prod['Block'] = None
        self.header = Trad.header

    def interpret(self):
        valorData = self.prod['Data_decs'].interpret()
        valorBlock = self.prod['Block'].interpret()
        
        return self.header + valorData + 'void main()\n'+ valorBlock

class Block (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Block')
        self.linea = linea
        self.prod['abrellave'] = None
        self.prod['Statements'] = None
        self.prod['cierrallave'] = None

    def interpret(self):
        valorStatements = self.prod['Statements'].interpret()       
        return '{' + valorStatements + '}'

class Statements (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Statements')
        self.linea = linea
        self.prod['Statement'] = None
        self.prod['StP'] = None

    def interpret(self):
        valorStatement = self.prod['Statement'].interpret()
        return self.prod['StP'].interpret(valorStatement)

class Data_decs (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Data_decs')
        self.linea = linea
        self.prod['Data_dec'] = None
        self.prod['DataP'] = None

    def interpret(self):
        valorDec = self.prod['Data_dec'].interpret()
        return self.prod['DataP'].interpret(valorDec)

class DataP (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Data_P')
        self.linea = linea
        self.prod['lambda'] = None
        self.prod['Data_decs'] = None

    def interpret(self, anterior):
        if (self.prod['Data_decs'] != None):
            valorDecs = self.prod['Data_decs'].interpret()
            return anterior + valorDecs
        elif (self.prod['lambda'] != None):
            return anterior + ''

class Data_dec (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Data_dec')
        self.linea = linea
        self.prod['int'] = None
        self.prod['Var'] = None
        self.prod['semicolon'] = None
        self.prod['node'] = None
        self.prod['edge'] = None

    def interpret(self):
        valorVar = self.prod['Var'].interpret()
        valorSemic = self.prod['semicolon'].interpret()
        if (self.prod['int'] != None):
            dic_variables[valorVar] = 'int' #Agregando dic de vars
            valorInt = self.prod['int'].interpret()
            return valorInt + valorVar + valorSemic
        elif (self.prod['node'] != None):
            dic_variables[valorVar] = 'node' #Agregando dic de vars
            valorNode = self.prod['node'].interpret()
            return valorNode + valorVar  + valorSemic
        elif (self.prod['edge'] != None):
            dic_variables[valorVar] = 'edge' #Agregando dic de vars
            valorEdge = self.prod['edge'].interpret()
            return valorEdge + valorVar + valorSemic
 
class StP (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('StP')
        self.linea = linea
        self.prod['lambda'] = None
        self.prod['Statements'] = None

    def interpret(self, anterior):
        if (self.prod['Statements'] != None):
            valorSts = self.prod['Statements'].interpret()
            return anterior + valorSts
        elif (self.prod['lambda'] != None):
            if (anterior != None):
                return anterior + ''
           

class Assignment (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Assignment')
        self.linea = linea
        self.prod['Var'] = None
        self.prod['AssP'] = None
        self.prod['if_sta'] = None
        self.prod['Expression'] = None
        self.prod['semicolon'] = None
        self.prod['Block'] = None

    def interpret(self):
        if (self.prod['Var'] != None):
            valorVar = self.prod['Var'].interpret() 
            return self.prod['AssP'].interpret(valorVar)

        elif (self.prod['if_sta'] != None) :
            valorIf = self.prod['if_sta'].interpret()
            valorExp = self.prod['Expression'].interpret()
            #valorSemic = self.prod['semicolon']
            valorBlock = self.prod['Block'].interpret()
            return valorIf + '(' + valorExp + ')' + valorBlock

class AssP (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('AssP')
        self.linea = linea
        self.prod['equal'] = None
        self.prod['Expression'] = None
        self.prod['semicolon'] = None
        self.prod['flecha'] = None
        self.prod['Var'] = None

    def interpret(self, anterior):
        #Asignacion de variable
        if (self.prod['equal'] != None):
            #valorVar = self.prod['Var'].interpret() 
            valorEqual = self.prod['equal'].interpret()
            valorExp = self.prod['Expression'].interpret()
            valorSemicolon = self.prod['semicolon'].interpret()
            if (dic_variables[anterior] == 'int'):
                return anterior + valorEqual + valorExp + valorSemicolon
            elif (dic_variables[anterior] == 'node'):
                return anterior + '.data = ' + valorExp + valorSemicolon
        elif (self.prod['flecha'] != None):
            valorFlecha = self.prod['flecha'].interpret()
            valorVar = self.prod['Var'].interpret() 
            valorSemicolon = self.prod['semicolon'].interpret()
            if (dic_variables[anterior] == 'node' and dic_variables[valorVar] == 'edge'):
                return anterior + valorFlecha + '(' +valorVar +')' + valorSemicolon + \
                        valorVar + '.vec_nodes.push_back' + '(' + anterior + ')' + valorSemicolon

class Statement (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Statement')
        self.linea = linea
        self.prod['Assignment'] = None

    def interpret(self):
        valorA = self.prod['Assignment'].interpret() 
        return valorA


class Expression (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Expression')
        self.linea = linea
        self.prod['Term'] = None
        self.prod['ExpressionP'] = None

    def interpret(self):
        valorT = self.prod['Term'].interpret()
        return self.prod['ExpressionP'].interpret(valorT)

class PosDBI (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('PosDBI')
        self.linea = linea
        self.col = col
        self.prod['AbreParentesis'] = None
        self.prod['Expression'] = None
        self.prod['CierraParentesis'] = None
        self.prod['ConfDBI'] = None
    
    def interpret(self):
        if (self.prod['AbreParentesis'] != None):
            #print("Error DBI")
            log.addError(200, self.linea, self.col)
            #Recuperacion de Error
            valorConfDBI = self.prod['ConfDBI'].interpret()
            return valorConfDBI
        else:
            valorConfDBI = self.prod['ConfDBI'].interpret()
            return valorConfDBI

class ConfDBI (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('ConfDBI')
        self.linea = linea
        self.col = col
        self.prod['Expression'] = None
        self.prod['DBD'] = None
        self.prod['CierraParentesis'] = None
    
    def interpret(self):
        if (self.prod['DBD'].interpret() != None):
            #print("Error DBD")
            log.addError(201, self.linea, self.col)
        #Recuperacion de Errores
        valorE = self.prod['Expression'].interpret()
        return valorE


class DBD (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('DBD')
        self.linea = linea
        self.prod['lambda'] = None
        self.prod['CierraParentesis'] = None
    
    def interpret(self):
        if (self.prod['CierraParentesis'] != None):
            return self.prod['CierraParentesis'].interpret()
        else:
            return None      


class Term (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Term')
        self.linea = linea
        self.prod['Factor'] = None
        self.prod['TermP'] = None
    
    def interpret(self, anterior = None):
        valorF = self.prod['Factor'].interpret()
        return self.prod['TermP'].interpret(valorF)


class ExpressionP (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('ExpressionP')
        self.linea = linea
        self.prod['Add'] = None
        self.prod['Rest'] = None
        self.prod['Term'] = None
        self.prod['ExpressionP'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior = None):
        if (self.prod['Add'] != None):
            valorT = self.prod['Term'].interpret()
            suma = anterior + self.prod['Add'].interpret() + valorT
            return self.prod['ExpressionP'].interpret(suma)

        elif (self.prod['Rest'] != None):
            valorT = self.prod['Term'].interpret()
            resta = anterior + self.prod['Rest'].interpret() + valorT
            return self.prod['ExpressionP'].interpret(resta)
        
        elif (self.prod['lambda'] != None):
            return anterior

class Factor (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('Factor')
        self.linea = linea
        self.prod['AbreParentesis'] = None
        self.prod['PosDBI'] = None
        self.prod['Num'] = None
        self.prod['Var'] = None

    def interpret(self, anterior = None):
        if (self.prod['Num'] != None):
            valorId = self.prod['Num'].interpret()
            return valorId
        elif (self.prod['Var'] != None):
            valorVar = self.prod['Var'].interpret()
            return valorVar
        else:
            valorZ =self.prod['PosDBI'].interpret()
            return valorZ


class TermP (NodoNoTerminal):
    def __init__(self, linea, col):
        super().__init__('TermP')
        self.linea = linea
        self.prod['Mult'] = None
        self.prod['Factor'] = None
        self.prod['TermP'] = None
        self.prod['lambda'] = None
    
    def interpret(self, anterior = None):
        if (self.prod['Mult']!= None):
            valorF = self.prod['Factor'].interpret()
            multiplica = anterior + self.prod['Mult'].interpret() + valorF
            return self.prod['TermP'].interpret(multiplica)
        elif (self.prod['lambda'] != None):
            return anterior

#####################################
class Add (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '+'

class Rest (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '-'

class Mult (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '*'

class AbreParentesis(NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '('

class CierraParentesis(NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return ')'

class Lambda (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return self

class semicolon (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return ';\n'

class equal (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '='

class abrellave (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '{'

class cierrallave (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '}'

class integer (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return 'int '

class node (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return 'node '

class edge (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return 'edge '

class flecha (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return '.vec_edges.push_back'

class if_sta (NodoTerminal):
    def __init__(self, linea, col):
        super().__init__()

    def interpret(self):
        return 'if '

######################################
class Num (NodoTerminal):
    def __init__(self, value):
        self.value = value
    
    def interpret(self):
        return self.value

class Var (NodoTerminal):
    def __init__(self, value):
        self.value = value
    
    def interpret(self):
        return self.value

####################################

