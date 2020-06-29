#Tabla prediccion
#Alexander Pinto

class Tabla:
    def __init__(self, noterminal_d, terminal_d):
        self.tabla = []
        self.noterminal_d = noterminal_d
        self.terminal_d = terminal_d

        self.tabla = [None]* len(self.noterminal_d)
        for i in range(0, len(self.noterminal_d)):
            self.tabla[i] = [None]* len(self.terminal_d)

    def __getitem__(self, index):        
        i = self.noterminal_d.get(index[0])
        j = self.terminal_d.get(index[1])
        return self.tabla[i][j]

    def Insertar(self, ind1: str, ind2:str, prod : []):
        i = self.noterminal_d.get(ind1)
        j = self.terminal_d.get(ind2)
        self.tabla[i][j] = prod
    
    def ImprimirTabla(self):
        for i in range(0, len(self.tabla)):
            row = []
            for j in range(0, len(self.tabla[0])):
                if (self.tabla[i][j] != None):
                    row += self.tabla[i][j]
                else:
                    row += ['None']
            print(row)
    