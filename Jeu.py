from Cards import *
from random import choice
import unicurses as uni
import sys
class Table() :
    def __init__(self) :
        self.Mat = []
        self.dimX = 11
        self.dimY = 7
        self.resetMat()
        #Mettre la carte de départ et les cartes d'arrivée
        self.Mat[3][1] = Depart()
        self.randomArrivee()
    def randomArrivee(self) :
        l = [1, 3, 5]
        # random choice pour l'or
        goldIdx = choice(l)
        self.Mat[goldIdx][-1] = Arrivee(1, '', 'G')
        # le reste
        l.remove(goldIdx)
        self.Mat[l[0]][-1] = Arrivee(1, "LD", 'C')
        self.Mat[l[1]][-1] = Arrivee(1, 'UR', 'C')       
    def resetMat(self) :
        for i in range(self.dimY) :
            line = []
            for j in range(self.dimX) :
                line.append(Carte(1))
            self.Mat.append(line)
            
    def addLine(self, pos) :
        vec = [Carte(1)]*self.dimX
        if pos == "up" :
            self.Mat.insert(0,vec)
        else :
            self.Mat.append(vec)
        self.dimY +=1
    def addCollumn(self, pos) :
        for line in self.Mat :
            if pos == "right" :
                line.append(Carte(1))
            else : 
                line.insert(0,Carte(1))
            self.dimX += 1
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
        if (self.Mat[x-1][y].Mat[2][1] != c.Mat[0][1]) and self.Mat[x-1][y].posee :
            print("test")
            posValid.append(False)
        
        if (self.Mat[x+1][y].Mat[0][1] != c.Mat[2][1]) and self.Mat[x+1][y].posee :
            print("test1")
            posValid.append(False)
    
        if (self.Mat[x][y-1].Mat[1][2] != c.Mat[1][0]) and self.Mat[x][y-1].posee :
            posValid.append(False)

        if (self.Mat[x][y+1].Mat[1][0] != c.Mat[1][2]) and self.Mat[x][y+1].posee :
            print("test3")
            posValid.append(False)
        if False in posValid :
            return False
        return True
    """Juste une couche d'abstraction pour checkPosValid, plus facile à utiliser"""
    def verifChemin(self, c, pos) :
        x = int(pos/self.dimX)
        y = pos%self.dimX
        res = self.checkPosValid(c, x, y)
        return res


class Joueur():
    def _init_(self, id):

        self.Role=None
        self.name = None
        self.Score=0
        self.id=id
        self.cartes=[]
        self.state={"pioche":0, "lampe":0,"chariot":0}

    def creerJoueur(self, nom):
        self.name=nom

    def poserCarte(self,carte):
        self.cartes.remove(carte)


    def Action(self,carteAction):
        if carteAction.code=="P":
            if carteAction.type=="+":
                self.state["pioche"]+=1
                return
        self.state["pioche"]-=1

        if carteAction.code=="L":
            if carteAction.type=="+":
                self.state["lampe"]+=1
                return
        self.state["lampe"]-=1

        if carteAction.code=="C":
            if carteAction.type=="+":
                self.state["chariot"]+=1
                return
        self.state["chariot"]-=1


    def piocher(self,carte):
        self.carte.append(carte)

    def passerTour(self):
        c=input("quelle carte pour passer le tour?:")

        return self.cartes[c+1]

class StartMenu() :
    def __init__(self) :
        self.stdscr = uni.initscr()
        self.MaxY, self.MaxX = uni.getmaxyx(self.stdscr)
        uni.clear()
        uni.noecho()
        uni.cbreak()
        self.startHeight = int(0.5*self.MaxY)
        self.startWidth = int(0.5*self.MaxX)
        startx = int(0.25*self.MaxX) 
        starty = int(0.25*self.MaxY)
        self.Menu = uni.newwin(self.startHeight, self.startWidth, starty, startx)
        uni.keypad(self.Menu, True)
        self.startChoices = ["Start Game", "Rules", "Exit"]
        self.highlight = 1
        x = int(0.5*self.startWidth-10)
        uni.mvaddstr(starty-1,startx, "*"*x+"Welcome to SabOOters"+"*"*x)
        uni.refresh()
        self.printStart()
        uni.curs_set(0)
        self.inputLoop()
    def printStart(self) :
        x = 3
        y = int(self.startHeight/2)-3
        startx = int(0.25*self.MaxX) 
        starty = int(0.25*self.MaxY)
        X = int(0.5*self.startWidth-10)
        uni.mvaddstr(starty-1,startx, "*"*X+"Welcome to SabOOters"+"*"*X)
        uni.refresh()
        uni.box(self.Menu, 0, 0)
        for i in range(0, len(self.startChoices)):
            if (self.highlight == i + 1):
                uni.wattron(self.Menu, uni.A_REVERSE)
                uni.mvwaddstr(self.Menu, y, x,self.startChoices[i])
                uni.wattroff(self.Menu, uni.A_REVERSE)
            else:
                uni.mvwaddstr(self.Menu, y, x, self.startChoices[i])
            y += 2
        uni.wrefresh(self.Menu)
    def inputLoop(self) :
        while True :
            choice = 0
            c = uni.wgetch(self.Menu)
            if c == uni.KEY_UP:
                if self.highlight == 1:
                    self.highlight == len(self.startChoices)
                else:
                    self.highlight -= 1
            elif c == uni.KEY_DOWN:
                if self.highlight == len(self.startChoices):
                    self.highlight = 1
                else:
                    self.highlight += 1
            elif c == 10:   # ENTER is pressed
                choice = self.highlight
            else:
                uni.mvaddstr(22, 0, str.format("Please press ENTER to choose an option"))
                uni.clrtoeol()
                uni.refresh()
            self.printStart()
            if c == 10 :
                if choice == 1 :
                    self.renseignements()
                    break
                elif choice == 2 :
                    self.showRules()
                else:
                    sys.exit(1)
    def showRules(self) :
        uni.clear()     
        startx = int(0.1*self.MaxX) 
        starty = int(0.1*self.MaxY)
        startHeight = int(0.8*self.MaxY)
        startWidth = int(0.8*self.MaxX)
        self.Rules = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(self.Rules, 0, 0)
        uni.mvwaddstr(self.Rules,starty+6,startx+6, "blablabla")
        uni.wrefresh(self.Rules)

        # Ajouter les règles du jeu
        uni.wgetch(self.Rules)
        uni.clear()
        self.printStart()
    def renseignements(self) :
        uni.clear()
        startx = int(0.2*self.MaxX) 
        starty = int(0.2*self.MaxY)
        startHeight = int(0.6*self.MaxY)
        startWidth = int(0.6*self.MaxX)
        self.info = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(self.info, 0, 0)
        uni.mvwaddstr(self.info, starty+1, startx-5, "Nombre de Joueurs : ")
        uni.wrefresh(self.info)
        while True :
            uni.echo()
            nombreJoueurs = uni.mvwgetstr(self.info, starty+1, startx-5+21)
            uni.noecho()
            try :
                self.nombreJoeurs = int(nombreJoueurs)
            except :
                uni.mvwaddstr(self.info, starty+1, startx-5, "Nombre de Joueurs : ")
                uni.wclrtoeol(self.info)
                uni.mvwaddstr(self.info, starty+3, startx-10, "Veuillez donner un nombre valide")
                uni.wclrtoeol(self.info)
                uni.wrefresh(self.info)
                continue
            if self.nombreJoeurs > 10 or self.nombreJoeurs < 3 :
                uni.mvwaddstr(self.info, starty+3, startx-10, "Veuillez donner un nombre entre 3 et 10")
                uni.wclrtoeol(self.info)
                uni.wrefresh(self.info)
                continue
            break
                
            
        uni.wgetch(self.info)
        self.printStart()


        
scr = StartMenu()
"""
    
t = Table()
t.affTable()

c = Chemin(1, 'ULR', '+')
print(t.checkPosValid(c, 3, 2))

t.Mat[3][2] = c
t.affTable()
print(t.verifChemin(c,35))
t.addLine("")
t.affTable()
"""