from collections import deque
from DefClases import *

class Nodo:
    def __init__(self, etiqueta: str, padre = None, siguiente = None, value = None,
        linea = 0, col = 0):
        self.etiqueta = etiqueta
        self.hijos = []
        self.padre = padre
        self.siguiente = siguiente
        self.clase_asociada = None
        self.value = value
        self.linea = linea
        self.col = col
    
    def InsertHijo(self, new_hijo):
        self.hijos.append(new_hijo)
    
    def CompletarProd(self):
        for hijo in self.hijos:
            self.clase_asociada.prod[hijo.etiqueta] = hijo.clase_asociada

class Arbol:
    def __init__(self, raiz = None):
        self.raiz = raiz
        self.nodos = []
        #self.InsertNodo(raiz)
        

    def InsertNodo(self, new_nodo):
        self.nodos.append(new_nodo)
    
    def InsertHijo(self, nodo, new_hijo):
        idx = self.nodos.index(nodo)
        self.nodos[idx].InsertHijo(new_hijo)

    def ActualizarHermanos(self, padre):
        padre.hijos.reverse()
        num_hijos = len(padre.hijos)
        for i in range(0, num_hijos):
            if ( (i + 1) < num_hijos):
                padre.hijos[i].siguiente = padre.hijos[i+1]

    def BuscarNodo(self, etiqueta):
        for i in self.nodos:
            if (i.etiqueta == etiqueta):
                return i
        return -1

    def Imprimir(self):
        pila = deque()
        pila.appendleft(self.raiz)
        while (len(pila) != 0):
            node = pila.popleft()
            print(node.etiqueta)
            for hijo in node.hijos:
                pila.append(hijo)
                print ("padre: ", node.etiqueta, "Hijo", hijo.etiqueta)

    def CrearArbolClases (self):
        #Asociar cada nodo del AST con la clase adecuada
        pila = deque()
        pila.appendleft(self.raiz)
        while (len(pila) != 0):
            node = pila.popleft()
            #Obtener etiqueta apropiada para clase
            try:
                name = dic_clases[node.etiqueta]
            except:
                name = node.etiqueta
            clase = globals()[name]
            if (name == 'Num'):
                node.clase_asociada = clase(node.value) 
            elif (name == 'Var'):
                node.clase_asociada = clase(node.value) 
            else:
                node.clase_asociada = clase(node.linea, node.col)
            #node.CompletarProd()

            #Agregar siguientes hijos a la pila
            for hijo in node.hijos:
                pila.append(hijo)

    def SetearProduccion (self):
        #Asociar cada nodo del AST con la clase adecuada
        pila = deque()
        pila.appendleft(self.raiz)
        while (len(pila) != 0):
            node = pila.popleft()
            node.CompletarProd()

            #Agregar siguientes hijos a la pila
            for hijo in node.hijos:
                pila.append(hijo)


