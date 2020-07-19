#Archivo main Compilador LL1

from AST import *
#from Errores import Logico

log = Log.getInstance()

if __name__ == "__main__":
    arbol_sint = Arbol()

    Grammar = Gramatica()
    Grammar.Cargar("GramaticaGrafo.txt")

    print("Tabla Analisis Sintactico")
    Grammar.tabla.ImprimirTabla()

    print("\nVerificacion Cadenas")
    file = "CadenaOperacion.txt"
    
    output = open("output.cpp", "w")
    
    linea = AnalizadorLexico(file)
    correcto, arbol_sint = Grammar.Analiza(linea, arbol_sint)
    
    if (correcto):
        
        arbol_sint.Imprimir()
        arbol_sint.CrearArbolClases()
        arbol_sint.SetearProduccion()
   
        res = arbol_sint.raiz.clase_asociada.interpret()
        #proc = Logico(res)
        #print(res)
        output.write(res)
    log.Print()
    output.close()
    

 