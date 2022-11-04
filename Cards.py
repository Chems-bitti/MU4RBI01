class Carte() :
    def __init__(self, Nombre) :
        self.Nombre = Nombre
        self.posee = False

class Depart(Carte) :
    def __init__(self) :
        super().__init__(1)
        self.Mat = [[1,0,1],[0,0,0],[1,0,1]]

class Arrivee(Carte) :
    def __init__(self, Nombre, Code, Type) :
        super().__init__(Nombre)
        self.Code = Code
        self.Type = Type
        self.getMat()
    
    def getMat(self) :
        if self.Type == 'G' :
            self.Mat = [[1,0,1], [0,0,0],[1,0,1]]
        elif self.Code == "LD" :
            self.Mat = [[1,1,1],[0,0,1],[1,0,1]]
        elif self.Code == "UR" :
            self.Mat = [[1,0,1],[1,0,0],[1,1,1]]
        else :
            pass
        
class Chemin(Carte) :
    def __init__(self, Nombre, Code, Type) :
        super().__init__(Nombre)
        self.Code = Code
        self.Type = Type
        self.getMat()
    def getMat(self) :
        self.Mat = [[1,1,1],[1,1,1],[1,1,1]]
        if 'U' in self.Code :
            self.Mat[0][1] = 0
        if 'D' in self.Code :
            self.Mat[2][1] = 0
        if 'L' in self.Code : 
            self.Mat[1][0] = 0
        if 'R' in self.Code : 
            self.Mat[1][2] = 0
        if self.Type == '+' :
            self.Mat[1][1] = 0
    def affMat(self) :
        for i in self.Mat :
            for j in i :
                if j != 0 :
                    print(u"\u2588"*2, end='')
                    continue
                print(' '*2, end='')
            print(' ')

class Action(Carte) :
    def __init__(self, Nombre, Code, Type) :
        super().__init__(Nombre)
        self.Code = Code
        self.Type = Type

class Nain(Carte) :
    def __init__(self, Nombre, Type) :
        super().__init__(Nombre)
        self.Type = Type

class Or(Carte) :
    def __init__(self, Nombre, value) :
        super().__init__(Nombre)
        self.Value = value        