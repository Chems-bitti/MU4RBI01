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
        if x > self.dimY or x < 0 :
            print("x invalide ?", x, self.dimY)
            return False
        if y > self.dimX or y < 0 :
            print("y invalid ?", y, self.dimX)
            return False
        posValid = []
        if self.Mat[x][y].posee :
            print(f"mat",x, y)
            return False
        if x-1 > 0 :
            if not self.Mat[x-1][y].posee :
                print(f"mat",x-1, y)
                posValid.append(False)
        if x+1 < self.dimY :
            if not self.Mat[x+1][y].posee :
                print(f"mat",x+1, y)
                posValid.append(False)
        if y-1 > 0 :
    
            if not self.Mat[x][y-1].posee :
                print(f"mat",x, y-1)
                posValid.append(False)

        if y+1 < self.dimX :
            if not self.Mat[x][y+1].posee :
                print(f"mat",x, y+1)
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
    def putCard(self, c, pos) :
        print("Valid")
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

class Jeu() :
    def __init__(self) :
        self.scr = StartMenu()
        self.nombreJoueurs = self.scr.nombreJoeurs #juste pour ne pas écrire scr à chaque fois
        self.listJoueurs = []
        self.Deck = []
        self.getPlayers()
        self.giveRoles()
        self.initDeck()
        self.giveCards()
        self.t = Table()
        interface = self.printInterface(self.listJoueurs[0])
        self.gameLoop(interface)
    def getPlayers(self) :
        uni.clear()
        startx = int(0.2*self.scr.MaxX) 
        starty = int(0.2*self.scr.MaxY)
        startHeight = int(0.6*self.scr.MaxY)
        startWidth = int(0.6*self.scr.MaxX)
        info = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(info, 0, 0)
        for i in range(self.nombreJoueurs) :
            j = Joueur(i)
            uni.echo()
            uni.mvwaddstr(info, starty+1, startx-10, f"Nom du joueur {i} :")
            uni.wclrtoeol(info)
            uni.box(info, 0, 0)
            uni.wrefresh(info)
            uni.curs_set(1)
            s = uni.mvwgetstr(info, starty+1, startx-10+18)
            uni.curs_set(0)
            uni.noecho()
            j.name = s
            self.listJoueurs.append(j)
    def giveRoles(self) :
        #copie locale de la liste des joueurs car on en aura besoin
        listJoueurs = self.listJoueurs.copy()
        # copie locale du nombre de joueur car j'ai la flemme d'écrire self à chaque fois
        n = self.nombreJoueurs
        N = 1
        if 5 <= n <= 6 :
            N = 2
        if 7 <=n <=9  :
            N = 3
        if n == 10 :
            N = 4
        for i in range(N) :
            j = choice(listJoueurs)
            j.Role = "Saboteur"
            listJoueurs.remove(j)
        for j in listJoueurs :
            j.Role = "Mineur"
        
    def initDeck(self) :
        with open("chemin.txt") as f :
            lines = f.readlines()
            for line in lines :
                s = line.split()
                #sert à rien de vérifier mais bon au cas
                #où l'utilisateur change le fichier
                if len(s) < 3 :
                    continue
                for i in range(int(s[0])) :
                    self.Deck.append(Chemin(s[1], s[2]))
        with open("action.txt") as f :
            lines = f.readlines()
            for line in lines :
                s=line.split()
                if len(s) < 3 :
                    continue
                for i in range(int(s[0])) :
                    self.Deck.append(Action(s[1], s[2]))
        # je viens vraiment d'écrire cette monstruosité...
    def giveCards(self) :
        N = 6
        if 6 <= self.nombreJoueurs <= 7 :
            N = 5
        if self.nombreJoueurs > 7 :
            N = 4
        for j in self.listJoueurs :
            for _ in range(N) :
                c = choice(self.Deck)
                j.piocher(c)
                self.Deck.remove(c)

    def printInterface(self, j : Joueur) :
        uni.clear()
        startx = 0
        starty = 0
        startHeight = self.scr.MaxY
        startWidth = self.scr.MaxX
        interface = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(interface, 0, 0)
        self.refreshInterface(interface, j)
        return interface
    def refreshInterface(self, interface, j : Joueur) :
        uni.clear()
        startx = 0
        starty = 0
        uni.box(interface, 0, 0)
        uni.mvwaddstr(interface, starty+1, startx+int(self.scr.MaxX*0.4), f"Tour du joueur {j.id} : {j.name} , {j.Role}" )
        uni.wclrtoeol(interface)
        uni.mvwaddstr(interface, starty+2, startx+int(self.scr.MaxX*0.4), f"Pioche : {len(self.Deck)}")
        uni.wclrtoeol(interface)
        self.printTable(interface)
        self.printJoueurs(interface)
        self.printCards(interface, j)
        uni.wrefresh(interface)
        
    
    def printTable(self, interface) :
        startx = int(0.3*self.scr.MaxX)
        starty = int(0.1*self.scr.MaxY)
        #bouger le curseur à la position de départ
        uni.mvwaddch(interface,starty, startx, " ")
        q = 0
        for j, line in enumerate(self.t.Mat) :
            for i, card in enumerate(line) :
                if j == 0 and card.posee :
                    self.t.addLine("up")
                if j == self.t.dimY-1 and card.posee :
                    self.t.addLine("down")
                if i == 0 and card.posee :
                    self.t.addCollumn("left")
                if i == self.t.dimX-1 and card.posee :
                    self.t.addCollumn("right")
                if isinstance(card, Arrivee) :
                    if card.State != "Hidden" :
                        card.reveal()
                startx = int(0.3*self.scr.MaxX)+i*6
                for y in range(3) :
                    for x in range(3) :
                        if card.Mat[y][x] == 1:
                            uni.mvwaddstr(interface, starty+y, startx+x*2, u"\u2588"*2 )
                            uni.wclrtoeol(interface)

                        if y == x == 1  and not card.posee and not isinstance(card, Arrivee):
                            uni.mvwaddstr(interface, starty+y, startx+x*2, f"{q}")
                            uni.wclrtoeol(interface)
                            #print(q,' ', sep='', end='')
                            continue
                            
                        if card.Mat[y][x] == 2:
                            uni.mvwaddstr(interface, starty+y, startx+x*2, "D")
                            uni.wclrtoeol(interface)
                            continue
        
                        if card.Mat[y][x] == 3:
                            uni.mvwaddstr(interface, starty+y, startx+x*2, "G")
                            uni.wclrtoeol(interface)
                            continue
        
                        if card.Mat[y][x] == 4:
                            uni.mvwaddstr(interface, starty+y, startx+x*2, "C")
                            uni.wclrtoeol(interface)
                            continue
                q +=1
            starty += 3
    def printCards(self,interface, j: Joueur) :
        startx = int(0.35*self.scr.MaxX)
        starty = int(0.8*self.scr.MaxY)
        uni.mvwaddch(interface,starty, startx, " ")
        for i, card in enumerate(j.Cards) :
            startx = int(0.35*self.scr.MaxX)+i*13
            for y in range(3) :
                for x in range(3) :
                    if isinstance(card, Action) :
                        if y == 0 and x == 1 :
                            uni.mvwaddstr(interface, starty+y, startx+x*2, "A")
                            uni.wclrtoeol(interface)
                            continue
                        if y == 1 :
                            if x == 1 :
                                uni.mvwaddstr(interface, starty+y, startx+x*2, card.Code)
                                uni.wclrtoeol(interface)
                                break
                        if y ==2 and x == 1 :
                            uni.mvwaddstr(interface, starty+y, startx+x*2, card.Type)
                            uni.wclrtoeol(interface)
                            continue
                    if card.Mat[y][x] == 1:
                        uni.mvwaddstr(interface, starty+y, startx+x*2, u"\u2588"*2 )
                        uni.wclrtoeol(interface)
                    if card.Mat[y][x] == 0:
                        uni.mvwaddstr(interface, starty+y, startx+x*2, "  " )
                        uni.wclrtoeol(interface)
                        
            uni.mvwaddstr(interface, starty+4,startx+2, f"({i})")
            uni.wclrtoeol(interface)
    def printJoueurs(self, interface) :
        for i, j in enumerate(self.listJoueurs) :
            starty = int(0.1*self.scr.MaxY)+5*int(i/2)
            startx = 3
            if i%2 != 0 :
                startx = self.scr.MaxX-30
            p = j.state["pioche"]
            l = j.state["lampe"]
            c = j.state["chariot"]
            uni.mvwaddstr(interface, starty, startx+11, f"Cards : {len(j.Cards)}")
            uni.mvwaddstr(interface, starty+1, startx+1, f"J{i}")
            uni.mvwaddstr(interface, starty+1, startx+11, f"pioche : {p}")
            uni.mvwaddstr(interface, starty+2, startx+11, f"lampe : {l}")
            uni.mvwaddstr(interface, starty+3, startx+11, f"chariot : {c}")
            
            
    def gameLoop(self, interface) :
        i = 0
        lostFlag = 0
        while True :
            if i >= self.nombreJoueurs :
                i = 0
            j = self.listJoueurs[i]
            if len(j.Cards) == 0 and len(self.Deck) == 0 :
                uni.mvwaddstr(interface, starty, startx, "Pas de cartes restantes, veuillez appuyer sur une touche pour passer le tour")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.wgetch(interface)
                lostFlag += 1
                if lostFlag == self.nombreJoueurs:
                    return False
            
            startx = int(0.35*self.scr.MaxX)
            starty = int(0.9*self.scr.MaxY)
            uni.mvwaddstr(interface, starty, startx, "Quelle carte à jouer ? 'P' pour passer  ")
            uni.wclrtoeol(interface)
            self.refreshInterface(interface, j)
            uni.curs_set(1)
            uni.echo()
            s = uni.mvwgetstr(interface, starty, startx+43)
            uni.wclrtoeol(interface)
            uni.noecho()
            uni.curs_set(0)
            if s == "P" :
                uni.mvwaddstr(interface, starty, startx, "Quelle carte céder pour passer le tour ? ")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.curs_set(1)
                uni.echo()
                s = uni.mvwgetstr(interface, starty, startx+43)
                uni.wclrtoeol(interface)
                uni.noecho()
                uni.curs_set(0)
                try :
                    n = int(s)
                except :
                    uni.mvwaddstr(interface, starty, startx, "Veuillez donner un nombre de carte valide")
                    uni.wclrtoeol(interface)
                    self.refreshInterface(interface, j)
                    uni.wgetch(interface)
                    continue
                if n >= len(j.Cards) :
                    uni.mvwaddstr(interface, starty, startx, "Veuillez donner un nombre de carte valide")
                    uni.wclrtoeol(interface)
                    self.refreshInterface(interface, j)
                    uni.wgetch(interface)
                    continue
                    
                j.passerTour(n)
                if len(self.Deck) > 0 :
                    c = choice(self.Deck)
                    self.Deck.remove(c)
                    j.piocher(c)
                i += 1
                continue
            try :
                n = int(s)
            except :
                uni.mvwaddstr(interface, starty, startx, "Veuillez donner un nombre de carte valide")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.wgetch(interface)
                continue
            if n >= len(j.Cards) :
                uni.mvwaddstr(interface, starty, startx, "Veuillez donner un nombre de carte valide")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.wgetch(interface)
                continue
            c = j.Cards[n]
            if isinstance(c, Action) :
                if c.Code == "MAP" or c.Code == "EBOU" :
                    pass
                uni.mvwaddstr(interface, starty, startx, "Veuillez donner le nombre du joueur sur lequel vous voulez utiliser la carte Action : ")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.curs_set(1)
                uni.echo()
                s = uni.mvwgetstr(interface, starty, startx+88)
                uni.wclrtoeol(interface)
                uni.noecho()
                uni.curs_set(0)
                
                try :
                    n = int(s)
                except :
                    uni.mvwaddstr(interface, starty, startx, "Veuillez donner un nombre de joueur valide")
                    uni.wclrtoeol(interface)
                    self.refreshInterface(interface, j)
                    uni.wgetch(interface)
                    continue
                if n >= self.nombreJoueurs :
                    uni.mvwaddstr(interface, starty, startx, f"Veuillez donner un nombre de joueur entre 0 et {self.nombreJoueurs-1}")
                    uni.wclrtoeol(interface)
                    self.refreshInterface(interface, j)
                    uni.wgetch(interface)
                    continue
                jtemp = self.listJoueurs[n]
                jtemp.Action(c)
                j.Cards.remove(c)
                if len(self.Deck) > 0 :
                    c = choice(self.Deck)
                    self.Deck.remove(c)
                    j.piocher(c)
                i += 1
                continue
            uni.mvwaddstr(interface, starty, startx, "Veuillez donner l'emplacement de la carte")
            uni.wclrtoeol(interface)
            self.refreshInterface(interface, j)
            uni.curs_set(1)
            uni.echo()
            s = uni.mvwgetstr(interface, starty, startx+43)
            uni.wclrtoeol(interface)
            uni.noecho()
            uni.curs_set(0)
            try :
                pos = int(s)
            except :
                uni.mvwaddstr(interface, starty, startx, "Veuillez donner un emplacement valide")
                uni.wclrtoeol(interface)
                self.refreshInterface(interface, j)
                uni.wgetch(interface)
                continue
            res = self.t.verifChemin(c, pos)
            if res == True :
                self.t.putCard(c, pos)
                j.Cards.remove(c)
                if len(self.Deck) > 0 :
                    c = choice(self.Deck)
                    self.Deck.remove(c)
                    j.piocher(c)
                i += 1
                res = self.checkWin()
                if res == True :
                    break
                continue
            
            uni.mvwaddstr(interface, starty, startx, "Veuillez donner un emplacement valide")
            uni.wclrtoeol(interface)
            self.refreshInterface(interface, j)
            uni.wgetch(interface)
            continue
            
            
    def checkWin(self) :
        loc = []
        mat = self.t.Mat
        for y in range(self.t.dimY) :
            for x in range(self.t.dimX) :
                if isinstance(mat[y][x], Arrivee) :
                    loc.append((x,y))
        print(loc)
        for x,y in loc :
            if y-1 < self.t.dimX :
                if mat[y-1][x].posee :
                    if mat[y-1][x].Mat[2][1] == 0 :
                        mat[y][x].reveal()
            if y+1 < self.t.dimX :
                if mat[y+1][x].posee :
                    if mat[y+1][x].Mat[0][1] == 0 :
                        mat[y][x].reveal()
            if x-1 < self.t.dimX :
                if mat[y][x-1].posee :
                    if mat[y][x-1].Mat[1][2] == 0 :
                        mat[y][x].reveal()
            if x+1 < self.t.dimX :
                if mat[y][x+1].posee :
                    if mat[y][x+1].Mat[1][0] == 0 :
                        mat[y][x].reveal()
            if mat[y][x].Code == "G" and mat[y][x].State != "Hidden" :
                return True
        return False
        
                
            
                
                
            
                
            

j = Jeu()