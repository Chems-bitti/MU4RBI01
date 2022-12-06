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
        self.Mat[goldIdx][-1] = Arrivee('ULDR', 'G')
        # le reste
        l.remove(goldIdx)
        self.Mat[l[0]][-1] = Arrivee("LD", 'C')
        self.Mat[l[1]][-1] = Arrivee('UR', 'C')       
    def resetMat(self) :
        for i in range(self.dimY) :
            line = []
            for j in range(self.dimX) :
                line.append(Carte())
            self.Mat.append(line)
            
    def addLine(self, pos) :
        vec = [Carte()]*self.dimX
        if pos == "up" :
            self.Mat.insert(0,vec)
        else :
            self.Mat.append(vec)
        self.dimY +=1
    def addCollumn(self, pos) :
        for line in self.Mat :
            if pos == "right" :
                line.append(Carte())
            else : 
                line.insert(0,Carte())
        self.dimX += 1
    def getArrivee(self) :
        loc = []
        mat = self.Mat
        for y in range(self.dimY) :
            for x in range(self.dimX) :
                if isinstance(mat[y][x], Arrivee) :
                    loc.append((x,y))
        return loc
    """ Fonction d'affichage de la table
        ça sert à rien si j'utilise ncurses
    """
    def affTable(self) :
        
        q = 0
        for y, line in enumerate(self.Mat) :
            for j in range(3) :
                for x, card in enumerate(line) :
                    if y == 0 and card.posee :
                        self.addLine("up")
                    if y == self.dimY-1 and card.posee :
                        self.addLine("down")
                    if x == 0 and card.posee :
                        self.addCollumn("left")
                    if x == self.dimX-1 and card.posee :
                        self.addCollumn("right")
                    if isinstance(card, Arrivee) :
                        if card.State != "Hidden" :
                            card.reveal()
                    for i in range(3) :
                        if card.Mat[j][i] != 0 :
                            if card.Mat[j][i] == 2 :
                                print(u" D", end='')
                                continue
                            if card.Mat[j][i] == 3 :
                                print(u" G", end='')
                            if card.Mat[j][i] == 4 :
                                print(u" C", end='')
                            if i == j == 1  and not card.posee and not isinstance(card, Arrivee):
                                if q < self.dimX :
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
        if x > self.dimY-1 or x < 0 :
            return False
        if y > self.dimX-1 or y < 0 :
            return False
        posValid = []
        if self.Mat[x][y].posee :
            return False
        if x-1 > 0 :
            if not self.Mat[x-1][y].posee :
                posValid.append(False)
        else :
            posValid.append(False)
        if x+1 < self.dimY :
            if not self.Mat[x+1][y].posee :
                posValid.append(False)
        else :
            posValid.append(False)
        if y-1 > 0 :
    
            if not self.Mat[x][y-1].posee :
                posValid.append(False)
        else :
            posValid.append(False)

        if y+1 < self.dimX :
            if not self.Mat[x][y+1].posee :
                posValid.append(False)
        else :
            posValid.append(False)
        if len(posValid) == 4 :
            return False
        posValid = []
        # Vérifier le chemin par rapports aux cartes posées 
        if x-1 > 0 :
            if (self.Mat[x-1][y].Mat[2][1] != c.Mat[0][1]) and self.Mat[x-1][y].posee :
                posValid.append(False)
        
        if x+1 < self.dimY :
            if (self.Mat[x+1][y].Mat[0][1] != c.Mat[2][1]) and self.Mat[x+1][y].posee :
                posValid.append(False)
    
        if y-1 > 0 :
            if (self.Mat[x][y-1].Mat[1][2] != c.Mat[1][0]) and self.Mat[x][y-1].posee :
                posValid.append(False)

        if y+1 < self.dimX :
            if (self.Mat[x][y+1].Mat[1][0] != c.Mat[1][2]) and self.Mat[x][y+1].posee :
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
    def putCard(self, c, pos) :
        c.posee = True
        y = int(pos/self.dimX)
        x = pos%self.dimX
        self.Mat[y][x] = c
        


class Joueur():
    def __init__(self, id):
        self.Role=None
        self.name = None
        self.Score=0
        self.id=id
        self.Cards=[]
        self.state={"pioche":0, "lampe":0,"chariot":0}

    def creerJoueur(self, nom):
        self.name=nom

    def poserCarte(self,carte):
        self.Cards.remove(carte)


    def Action(self,carteAction):
        if "P" in carteAction.Code:
            if carteAction.Type=="+":
                self.state["pioche"]+=1
            else :
                self.state["pioche"]-=1

        if "L" in carteAction.Code:
            if carteAction.Type=="+":
                self.state["lampe"]+=1
            else :
                self.state["lampe"]-=1

        if "C" in carteAction.Code:
            if carteAction.Type=="+":
                self.state["chariot"]+=1
            else :
                self.state["chariot"]-=1

    def checkState(self) :
        if self.state["pioche"] < 0 :
            return False
        if self.state["lampe"] < 0 :
            return False
        if self.state["chariot"] < 0 : 
            return False
        return True

    def piocher(self,carte):
        self.Cards.append(carte)

    def passerTour(self, n):
        self.Cards.remove(self.Cards[n])

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
        info = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(info, 0, 0)
        uni.mvwaddstr(info, starty+1, startx-5, "Nombre de Joueurs : ")
        uni.wrefresh(info)
        while True :
            uni.echo()
            uni.curs_set(1)
            nombreJoueurs = uni.mvwgetstr(info, starty+1, startx-5+21)
            uni.curs_set(0)
            uni.noecho()
            try :
                self.nombreJoeurs = int(nombreJoueurs)
            except :
                uni.mvwaddstr(info, starty+1, startx-5, "Nombre de Joueurs : ")
                uni.wclrtoeol(info)
                uni.mvwaddstr(info, starty+3, startx-10, "Veuillez donner un nombre valide")
                uni.wclrtoeol(info)
                uni.box(info, 0, 0)
                uni.wrefresh(info)
                continue
            if self.nombreJoeurs > 10 or self.nombreJoeurs < 3 :
                uni.mvwaddstr(info, starty+1, startx-5, "Nombre de Joueurs : ")
                uni.wclrtoeol(info)
                uni.mvwaddstr(info, starty+3, startx-10, "Veuillez donner un nombre entre 3 et 10")
                uni.wclrtoeol(info)
                uni.box(info, 0, 0)
                uni.wrefresh(info)
                continue
            break
