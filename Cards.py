class Carte() :
    def __init__(self) :
        self.posee = False
        self.Mat = [[1,1,1],[1,1,1],[1,1,1]]

class Depart(Carte) :
    def __init__(self) :
        super().__init__()
        self.Mat = [[1,0,1],[0,2,0],[1,0,1]]
        self.posee = True
    def affMat(self) :
        for i in self.Mat :
            for j in i :
                if j != 0 :
                    print(u"\u2588"*2, end='')
                    continue
                print(' '*2, end='')
            print(' ')

class Arrivee(Carte) :
    def __init__(self, Code, Type) :
        super().__init__()
        self.Code = Code
        self.Type = Type
        #Bloquée au début
        self.Mat = [[1,1,1],[1,1,1],[1,1,1]]
        self.State = "Hidden"
    def reveal(self) :
        if self.Type == "G" :
            self.Mat = [[1,0,1],[0,3,0],[1,0,1]]
        if self.Type == "C" :
            self.Mat = [[1,0,1],[0,4,0],[1,0,1]]
        self.posee = True
    
        
class Chemin(Carte) :
    def __init__(self, Code, Type) :
        super().__init__()
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
    def __init__(self, Code, Type) :
        super().__init__()
        self.Code = Code
        self.Type = Type

class Nain(Carte) :
    def __init__(self, Type) :
        super().__init__()
        self.Type = Type

class Or(Carte) :
    def __init__(self, value) :
        super().__init__()
        self.Value = value        