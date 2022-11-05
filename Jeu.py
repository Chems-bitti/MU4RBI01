from Cards import *
from random import choice
class Table() :
    def __init__(self) :
        self.Mat = []
        self.initMat()
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
    def initMat(self) :
        for i in range(5) :
            line = []
            for j in range(9) :
                line.append(Carte(1))
            self.Mat.append(line)
            
    """ Fonction d'affichage de la table"""
    def affTable(self) :
        for line in self.Mat :
            for j in range(3) :
                for card in line :
                    for i in range(3) :
                        if card.Mat[j][i] != 0 :
                            if card.Mat[j][i] == 1 :
                                print(u"\u2588"*2, end='')
                            if card.Mat[j][i] == 2 :
                                print(u" D", end='')
                            if card.Mat[j][i] == 3 :
                                print(u" G", end='')
                            if card.Mat[j][i] == 4 :
                                print(u" C", end='')
                            continue
                        print(' '*2, end='')
                print(' ')
t = Table()
t.affTable()