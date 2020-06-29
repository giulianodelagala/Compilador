#Gramatica
#Practica 7
#Alexander Pinto
from collections import deque
from Tabla import Tabla
from Arbol import *

class Produccion:
    def __init__(self, izq : ""):
        # La produccion solo contendra ids
        # par[0] : non/ter  par[1] : indice en el array   
        self.izq = izq
        self.der = []
        
    def AgregarDer(self,der :[]):
        self.der.append(der)


class Gramatica:
    def __init__(self):
        self.produccion = []
        self.terminal_d = {} 
        self.noterminal_d = {} 
        self.dolar = "$"
        self.primeros_d = {}
        self.siguientes_d = {}
        self.tabla = [] 

    def Cargar(self, file : str):
        f = open(file, "r")
        self.cont_non = 0 #generar id de no terminales
        self.cont_ter = 0 #generar id de terminales

        #Creacion de array No terminales
        for line in f:           
            izq, dumb = self.SepararProduccion(line)
            
            if (self.InsertarNoTerminal(izq)):
                self.cont_non += 1

        # Preparar produccion
        f.seek(0)
        for line in f:
            izq, der = self.SepararProduccion(line)
            derecho = self.ProcesarDerecho(der)
            # Mejorar si noterminal ya existe solo append
            existe, pr = self.BuscarProduccion(izq)
                #Existe izq de Produccion
            if (existe):
                #for item in derecho:
                    #self.produccion[pr].AgregarDer(item)
                self.produccion[pr].der += derecho
            else:
                a = Produccion(izq)
                #for item in derecho:
                #    a.AgregarDer(derecho)
                a.der += derecho
                self.produccion.append(a)   
        
        self.Primeros()
        self.GetSiguientes()
        self.CrearTabla()

    def BuscarProduccion(self, izq : str):
        for pr in range (0, len(self.produccion)):
                if (self.produccion[pr].izq == izq):
                    return True, pr
        return False, -1

    def SepararProduccion(self, prod : str):
        index = prod.find(":=")       
        izq = prod[0:index].strip()
        der = prod[(index+2):].strip()
        return izq, der

    def InsertarNoTerminal(self, izq : str):                      
        if (self.noterminal_d.get(izq) != None):
            # Insertado anterioridad
            return False       
        # Se procede insercion
        self.noterminal_d[izq] = self.cont_non
        return True

    def InsertarTerminal(self, der: str):        
        if (self.terminal_d.get(der) != None):
            # Insertado anterioridad
            return False         
        # Se procede insercion
        self.terminal_d[der] = self.cont_ter
        return True

    def ProcesarDerecho(self, der : str):
        lista = der.split()
        derecha = [] #Array de literales en derecha
        tot_derecha = []
        for item in lista:
            if (item == '|'):
                #Fin de Produccion
                if (len(derecha) != 0):
                    tot_derecha.append(derecha.copy())
                    derecha.clear()

            elif (self.noterminal_d.get(item) != None):
                #Generamos su par
                par = [0,item]
                derecha.append(par)

            else:
                #Es Terminal
                #Verificar si esta en lista de terminales
                if (self.InsertarTerminal(item)):
                    self.cont_ter += 1
                par = [1, item]
                derecha.append(par)
        if (len(derecha)!= 0):
            tot_derecha.append(derecha)
            
        return tot_derecha             

    def GetProduccion(self, izq : str):
        for pr in self.produccion:
            res = []
            if (pr.izq == izq):
                der = []
                for p in pr.der:
                    for item in p:
                        der.append(item[1])
                    res.append(der.copy())
                    der.clear()
                return res
      
        return ("None")

    def Primeros(self):
        self.primeros_d = {}
        for nodo in self.noterminal_d:
            self.primeros_d[nodo] = self.GetPrimero(nodo)
        return self.primeros_d

    def GetPrimero(self, nodo : str):
        prods = self.GetProduccion (nodo)
        primeros = []
        for item in prods:
            #Si item es terminal
            index = self.terminal_d.get(item[0])
            if (index != None):
                primeros.append(item[0])
            elif (self.noterminal_d.get(item[0]) != None):
                #Es no terminal.. consulta recursiva
                temp = self.GetPrimero(item[0])
                for t in temp:
                    primeros.append(t)
            else:
                return ("None")
        return primeros
    
    def GetSiguientes(self):
        self.siguientes_d[next(iter(self.noterminal_d))] = [self.dolar]

        for nodo in self.produccion:
            existe = False
            padre = False
            index_padre = ""
            for n in self.produccion:
                for item in n.der:
                    for d in range(0, len(item)):
                        if (item[d][1] == nodo.izq):
                            if (not padre):
                                #Guardamos indice de padre
                                #en caso no tengamos siguiente derecha
                                index_padre = n.izq
                                padre = True

                            if (d < len(item)-1 and item[d+1][0] == 1):                          
                                #Existe un siguiente y es terminal
                                #print (nodo.izq , item[d+1][1])
                                self.siguientes_d[nodo.izq].append(item[d+1][1])
                                existe = True
                                break
                            elif (d < len(item)-1 and item[d+1][0] == 0):
                                #El siguiente es no terminal
                                #Agregamos primeros de su derecha
                                # y revisamos si existe valor lambda
                                for p in self.primeros_d[item[d+1][1]]:
                                    if (p != "lambda"):
                                        try: 
                                            self.siguientes_d[nodo.izq].index(p)
                                        except:
                                            try:
                                                self.siguientes_d[nodo.izq].append(p)
                                            except: 
                                                self.siguientes_d[nodo.izq] = [p]
                                    else:
                                        for i in self.siguientes_d[index_padre]:
                                            try:
                                                self.siguientes_d[nodo.izq].index(i)
                                            except:
                                                try:
                                                    self.siguientes_d[nodo.izq].append(i)
                                                except:
                                                    self.siguientes_d[nodo.izq] =  [i]
                                existe = True                      
                                break

                    if (existe):
                        break

            if (not existe):
                #No tuvo siguientes
                self.siguientes_d[nodo.izq] = self.siguientes_d[index_padre]

    def SearchProduccion(self, nodo_nt, nodo_t):
        prod = self.GetProduccion(nodo_nt)
        for p in prod:
            try:
                ind = p.index(nodo_t)
                return p
            except:
                continue
        return p

    def CrearTabla(self):
        self.terminal_d['$'] = len(self.terminal_d)
        self.tabla = Tabla(self.noterminal_d, self.terminal_d)
        for nodo_nt in self.noterminal_d:
            for nodo_t in self.primeros_d[nodo_nt]:
                if (nodo_t != "lambda"):
                   
                    self.tabla.Insertar(nodo_nt, nodo_t, self.SearchProduccion(nodo_nt, nodo_t))
                else:
                    for nodo_t2 in self.siguientes_d[nodo_nt]:
                        self.tabla.Insertar(nodo_nt, nodo_t2, ["lambda"]) 

    def Opera1(self, pivote, arbol):
        arbol.ActualizarHermanos(pivote)
        return pivote.hijos[0]

    def Opera2(self, pivote, arbol):
        if (pivote == arbol.raiz or pivote == None):
            return None

        if (pivote.siguiente != None):
            if (pivote.siguiente.etiqueta != "lambda"):
                return pivote.siguiente
            
        return self.Opera2(pivote.padre, arbol)

    #def Opera3(self, pivote, arbol):


    def Analiza(self, cadena : str, arbol: Arbol):
        #Algoritmo de Validacion de Cadena       
        entrada = deque()
        for i in cadena.split():
            entrada.append(i)

        pila = deque()
        
        pila.appendleft('$')
        pila.appendleft(next(iter(self.noterminal_d)))
        #Creacion de Raiz de Arbol
        arbol = Arbol( Nodo(pila[0]) )
        arbol.InsertNodo( Nodo(pila[0]))
        pivote = arbol.raiz
        entrada.append('$')
        no_lambda = False
        try:
            while( len(entrada) != 0 and len(pila) != 0):
                if (entrada[0] == pila[0]):
                    entrada.popleft()
                    pila.popleft()
                    pivote = self.Opera2(pivote, arbol)

                else:
                    tmp = pila.popleft()
                    #Ubicacion de pivote
                    
                    #arbol.InsertNodo(pivote)
                    for x in reversed(self.tabla[tmp,entrada[0]]):
                        if (x != 'lambda'):
                            #pivote = arbol.BuscarNodo(tmp)
                            pila.appendleft(x)
                            #Opera1
                            #Crear Nuevo Nodo e Insertar como hijo
                            hijo = Nodo(x, pivote)
                            pivote.InsertHijo(hijo)
                            arbol.InsertNodo(hijo)
                            no_lambda = True

                        else:
                            #x == lambda
                            hijo = Nodo(x, pivote)
                            pivote.InsertHijo(hijo)
                            arbol.InsertNodo(hijo)
                            pivote = self.Opera2(pivote, arbol)
                            no_lambda = False
                            
                    #Actualizar siguientes(hermanos)
                    if (no_lambda):
                        pivote = self.Opera1(pivote, arbol)
                                   
            return len(entrada) == 0 and len(pila) == 0, arbol
        except:       
            return False, arbol


if __name__ == "__main__":
    arbol_sint = Arbol()

    Grammar = Gramatica()
    Grammar.Cargar("prueba_arbol.txt")

    print("Tabla Analisis Sintactico")
    Grammar.tabla.ImprimirTabla()

    print("\nVerificacion Cadenas")
    f = open("cadena_arbol.txt", "r")
    for line in f:
        correcto, arbol_sint = Grammar.Analiza(line, arbol_sint)
        if (correcto):
            print (line, 'OK')
        else:
            print (line, 'FALSE')

    arbol_sint.Imprimir()
    
     