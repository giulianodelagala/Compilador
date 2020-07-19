#Recuperacion de Errores

class DiccionarioError:
    def __init__(self):
        self.dic = {
            100 :'Caracter no reconocido, posible numero',
            101 :'Operador no reconocido',
            200 :'Desbalance Parentesis Izquierdo',
            201 :'Desbalance Parentesis Derecho',
            400 :'Desconocido',
            900 :'Valor Negativo',
            901 :'Valor Mayor a 65535'
        }

class Log:
    __instance = None
    @staticmethod
    def getInstance():
        #Acceso static
        if (Log.__instance == None):
            Log()
        return Log.__instance

    def __init__(self):
        if (Log.__instance != None):
            raise Exception("Un unico Log")
        else:
            Log.__instance = self
        self.DE = DiccionarioError()
        self.list_errors = []
        self.list_warnings = []

    def addError(self, codigo, linea, idx):
        self.list_errors.append([codigo,linea,idx])
    
    def addWarning(self, codigo, parametro):
        self.list_warnings.append([codigo, parametro])
    
    def Print(self):
        for i in self.list_errors:
            print(f"\nError: {self.DE.dic[i[0]]} en linea {i[1]}, col {i[2]}")
        for i in self.list_warnings:
            print(f"\nWarning: {self.DE.dic[i[0]]} en {i[1]}")

#log = Log.getInstance()

'''
class Logico:
    def __init__(self, output):
        self.output = output
        #self.log = log
        self.Procesar()

    def Procesar(self):
        if (self.output < 0):
            log.addWarning(900, "resultado")
        if (self.output > 65535):
            log.addWarning(901, "resultado")
'''      