import os
from gramatica import Gramatica

class GenClases:
    def __init__(self, grammar : Gramatica, path_nt : str, path_t : str):
        self.path_ter = path_t
        self.path_noter = path_nt
        self.Grammar = grammar

        self.symbols = {'+' : "add", "-" : "rest",
                        '*' : "mult", '/' : "div"
                        }

        self.molde_nt = "class NodoNoTerminal(AbstractExpressionNT):\n\
    #diccionario<NombreClase, Objeto >\n\
    def interprets(val1,val2,val3):\n\
    return (0,0,0)"

        self.molde_t = "class Terminal(AbstractExpressionT):\n\
    #valor\n\
    def interprets():\n\
    return valor"

    def Generar(self):
        actual_path = os.getcwd()
        try:
            os.mkdir( actual_path + '/' + self.path_ter)
            os.mkdir( actual_path + '/' + self.path_noter)
        except:
            print("Directorio existente")

        for item in self.Grammar.terminal_d:
            #Creacion archivos clase de nodos terminales
            try:
                name = self.symbols[item]
            except:
                name = item

            file_t = actual_path + '/' + self.path_ter + "/Term_" + name
            f = open( file_t, "w")
            temp = self.molde_t
            
            f.write( temp.replace( "Terminal", "Term_" + name, 1))
            f.close

        for item in self.Grammar.noterminal_d:
            #Creacion de archivos clases de nodos no terminales
            file_t = actual_path + '/' + self.path_noter + "/NoTerm_" + item
            f = open( file_t, "w")
            temp = self.molde_nt
            
            f.write( temp.replace( "NodoNoTerminal", "NoTerm_" + item, 1))
            f.close
           

if __name__ == "__main__":
    Grammar = Gramatica()
    Grammar.Cargar("prueba_gram.txt")
    Generador = GenClases(Grammar, "noterminal", "terminal")
    Generador.Generar()


