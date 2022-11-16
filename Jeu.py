from Cards import *
from random import choice
class Table() :
    def __init__(self) :
        self.Mat = []
        self.resetMat()
        #Mettre la carte de départ et les cartes d'arrivée
        self.Mat[2][0] = Depart()
        self.randomArrivee()
    def randomArrivee(self) :
        l = [0, 1, 2]
        # random choice pour l'or
        goldIdx = choice(l)
        self.Mat[goldIdx*2][-1] = Arrivee(1, '', 'G')
        # le reste
        l.remove(goldIdx)
        self.Mat[l[0]*2][-1] = Arrivee(1, "LD", 'C')
        self.Mat[l[1]*2 ][-1] = Arrivee(1, 'UR', 'C')       
    def resetMat(self) :
        for i in range(5) :
            line = []
            for j in range(9) :
                line.append(Carte(1))
            self.Mat.append(line)
            
    """ Fonction d'affichage de la table"""
    def affTable(self) :
        
        q = 0
        for line in self.Mat :
            for j in range(3) :
                for card in line :
                    for i in range(3) :
                        if card.Mat[j][i] != 0 :
                            if card.Mat[j][i] == 2 :
                                print(u" D", end='')
                                continue
                            if card.Mat[j][i] == 3 :
                                print(u" G", end='')
                            if card.Mat[j][i] == 4 :
                                print(u" C", end='')
                            if i == j == 1  and not card.posee:
                                if q < 10 :
                                    print(q,' ', sep='', end='')
                                    continue
                                        
                                print(q, sep='', end='')
                                continue
                            if card.Mat[j][i] == 1 :
                                print(u"\u2588"*2, end='')
                            continue
                        print(' '*2, end='')
                    if j == 1 :
                        q += 1
                print(' ')
                
            
    def checkPosValid(self, c, x, y) :
        # Vérifier si c'est à coté d'une carte posée
        posValid = []
        if self.Mat[x][y].posee :
            return False
        if not self.Mat[x-1][y].posee :
            posValid.append(False)
        
        if not self.Mat[x+1][y].posee :
            posValid.append(False)
    
        if not self.Mat[x][y-1].posee :
            posValid.append(False)

        if not self.Mat[x][y-1].posee :
            posValid.append(False)
        if len(posValid) == 4 :
            return False
        posValid = []
        # Vérifier le chemin par rapports aux cartes posées 
        if (self.Mat[x-1][y].Mat[1][2] != c.Mat[1][0]) and self.Mat[x-1][y].posee :
            posValid.append(False)
        
        if (self.Mat[x+1][y].Mat[1][0] != c.Mat[1][2]) and self.Mat[x+1][y].posee :
            posValid.append(False)
    
        if (self.Mat[x][y-1].Mat[2][1] != c.Mat[0][1]) and self.Mat[x][y-1].posee :
            posValid.append(False)

        if (self.Mat[x][y+1].Mat[0][1] != c.Mat[2][1]) and self.Mat[x][y+1].posee :
            posValid.append(False)
        if False in posValid :
            return False
        return True
    
t = Table()
t.affTable()

c = Chemin(1, 'ULR', '+')
print(t.checkPosValid(c, 2, 1))

t.Mat[2][1] = c
t.affTable()
c = Chemin(1, 'ULR', '+')
print(t.checkPosValid(c, 2, 1))

t.Mat[2][1] = c
t.affTable()