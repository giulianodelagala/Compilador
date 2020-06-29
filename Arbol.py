from collections import deque

class Nodo:
    def __init__(self, etiqueta: str, padre = None, siguiente = None):
        self.etiqueta = etiqueta
        self.hijos = []
        self.padre = padre
        self.siguiente = siguiente
    
    def InsertHijo(self, new_hijo):
        self.hijos.append(new_hijo)

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



