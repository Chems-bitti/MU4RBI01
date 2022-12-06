from interface import *

class Jeu() :
    def __init__(self) :
        self.scr = StartMenu()
        self.nombreJoueurs = self.scr.nombreJoeurs #juste pour ne pas écrire scr à chaque fois
        self.listJoueurs = []
        self.nombreChercheur = 0
        self.Deck = []
        self.Gold = []
        self.nbManche = 0
        self.getPlayers()
        self.giveRoles()
        self.getGold()
        self.initDeck()
        self.giveCards()
        self.t = Table()
        interface = self.printInterface(self.listJoueurs[0])
        while self.nbManche < 3 :
            minerWin, j = self.gameLoop(interface)
            self.printWinner(interface, minerWin, j)
            self.nbManche += 1
            
            if not minerWin :
                if self.nombreJoueurs < 4 :
                    gold =  4
                elif self.nombreJoueurs < 10 :
                    gold = 3
                else :
                    gold = 2
                    
                for j in self.listJoueurs :
                    if j.Role == "Saboteur" :
                        j.Score += gold
                continue
            orPioche = []
            print(self.Gold)
            for i  in range(self.nombreChercheur) :
                c = choice(self.Gold)
                orPioche.append(c)
                self.Gold.remove(c)
            startx = int(0.35*self.scr.MaxX)
            starty = int(0.7*self.scr.MaxY)
            i = j.id
            p = 0
            while p < self.nombreChercheur :
                if i == self.nombreJoueurs :
                    i = 0
                j = self.listJoueurs[i]
                if j.Role == "Mineur" :
                    p += 1
                    uni.clear()
                    self.printGold(interface, orPioche)
                    uni.mvwaddstr(interface, starty, startx, f"Joueur {j.id}, choisissez une carte : ")
                    uni.wclrtoeol(interface)
                    uni.wrefresh(interface)
                    uni.curs_set(1)
                    uni.echo()
                    s = uni.mvwgetstr(interface, starty, startx+40)
                    uni.wclrtoeol(interface)
                    uni.noecho()
                    uni.curs_set(0)
                    j.Score += orPioche[int(s)]
                    orPioche.remove(orPioche[int[s]])
            
            

    def printLeaderboard(self) :
        startx = int(0.2*self.scr.MaxX)
        starty = int(0.2*self.scr.MaxY)
        startHeight = int(0.3*self.scr.MaxY)
        startWidth = int(0.3*self.scr.MaxX)
        leaderBoard = uni.newwin(startHeight, startWidth, starty, startx)
        uni.box(leaderBoard, 0, 0)
        i = 0
        sortedJoueurs = sorted(self.listJoueurs, key=lambda j : j.Score)
        starty = starty+startHeight-3
        for i, j in enumerate(sortedJoueurs) :
            starty -= i*2 
            uni.mvwaddstr(leaderBoard, starty, startx, f"Joueur {j.id} : {j.name}   {j.Score}G")
        uni.wrefresh(leaderBoard)
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
        self.nombreChercheur  = self.nombreJoueurs - N
        if 5 <= n <= 6 :
            N = 2
            self.nombreChercheur  = self.nombreJoueurs - N
        if 7 <=n <=9  :
            N = 3
            self.nombreChercheur  = self.nombreJoueurs - N
        if n == 10 :
            N = 4
            self.nombreChercheur  = self.nombreJoueurs - N
        for i in range(N) :
            j = choice(listJoueurs)
            j.Role = "Saboteur"
            listJoueurs.remove(j)
        for j in listJoueurs :
            j.Role = "Mineur"
        
    def getGold(self) :
        with open("gold.txt") as f :
            lines = f.readlines()
            for line in lines :
                s = line.split()
                #sert à rien de vérifier mais bon au cas
                #où l'utilisateur change le fichier
                if len(s) < 2 :
                    continue
                for i in range(int(s[0])) :
                    self.Gold.append(Or(int(s[1])))
                
    
    def printGold(self,interface, Gold) :
        startx = int(0.35*self.scr.MaxX)
        starty = int(0.5*self.scr.MaxY)
        uni.mvwaddch(interface,starty, startx, " ")
        for i, card in enumerate(self.Gold) :
            startx = int(0.35*self.scr.MaxX)+i*13
            for y in range(3) :
                for x in range(3) :
                    if y == 0 or y == 2 :
                        uni.mvwaddstr(interface, starty+y, startx+2*x, u"\u2588"*2)
                        uni.wclrteol(interface)
                    if y == 1 :
                        uni.mvwaddstr(interface, starty+y, startx, f"  {card.Value}G")
                        uni.wclrteol(interface)
                        
            uni.mvwaddstr(interface, starty+4,startx+2, f"({i})")
            uni.wclrtoeol(interface)
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
            win = self.checkWin()
            if win :
                return win, j
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
                    return False, j
            
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
                if c.Code == "MAP" :
                    uni.mvwaddstr(interface, starty, startx, "Choisir la carte arrivée que vous voulez voir : UP, MID, ou DOWN")
                    uni.wclrtoeol(interface)
                    uni.curs_set(1)
                    uni.echo()
                    s = uni.mvwgetstr(interface, starty, startx+88)
                    uni.wclrtoeol(interface)
                    uni.noecho()
                    uni.curs_set(0)
                    loc = self.t.getArrivee()
                    mat = self.t.Mat
                    x, y = loc[0]
                    if s == "MID" :
                        x, y = loc[1]
                    if s == "DOWN" :
                        x, y = loc[2]
                    mat[y][x].reveal()
                    self.refreshInterface(interface, j)
                    uni.wgetch(interface)
                    mat[y][x].hide()
                    j.Cards.remove(c)
                    if len(self.Deck) > 0 :
                        c = choice(self.Deck)
                        self.Deck.remove(c)
                        j.piocher(c)
                    i += 1
                    continue
                    
                if c.Code == "EBOU" :
                    uni.mvwaddstr(interface, starty, startx, "Choisir la carte que vous voulez enlever :")
                    uni.wclrtoeol(interface)
                    uni.curs_set(1)
                    uni.echo()
                    s = uni.mvwgetstr(interface, starty, startx+48)
                    uni.wclrtoeol(interface)
                    uni.noecho()
                    uni.curs_set(0)
                    try :
                        pos= int(s)
                    except :
                        uni.mvwaddstr(interface, starty, startx, "Veuillez donner une position valide")
                        uni.wclrtoeol(interface)
                        self.refreshInterface(interface, j)
                        uni.wgetch(interface)
                        continue

                    y = int((pos/self.t.dimX))
                    x = pos%self.t.dimX
                    if not self.t.Mat[y][x].posee :
                        uni.mvwaddstr(interface, starty, startx, "Veuillez donner la position d'une carte posee")
                        uni.wclrtoeol(interface)
                        self.refreshInterface(interface, j)
                        uni.wgetch(interface)
                        continue
                    if isinstance(self.t.Mat[y][x], Arrivee) or isinstance(self.t.Mat[y][x], Depart) :
                        uni.mvwaddstr(interface, starty, startx, "Les cartes de depart et arrivee ne peuvent pas être retirees")
                        uni.wclrtoeol(interface)
                        self.refreshInterface(interface, j)
                        uni.wgetch(interface)
                        continue
                        
                    self.t.Mat[y][x] = Carte()
                    j.Cards.remove(c)
                    if len(self.Deck) > 0 :
                        c = choice(self.Deck)
                        self.Deck.remove(c)
                        j.piocher(c)
                    i += 1
                    continue

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
            validPos = self.t.verifChemin(c, pos)
            canPlay = j.checkState()
            if validPos and canPlay :
                self.t.putCard(c, pos)
                j.Cards.remove(c)
                if len(self.Deck) > 0 :
                    c = choice(self.Deck)
                    self.Deck.remove(c)
                    j.piocher(c)
                i += 1
                self.refreshInterface(interface, j)
                continue

            if not validPos :
                uni.mvwaddstr(interface, starty, startx, "Veuillez donner un emplacement valide")
            if not canPlay :
                uni.mvwaddstr(interface, starty, startx, "Vous ne pouvez pas jouer, un outil est cassé")
            uni.wclrtoeol(interface)
            self.refreshInterface(interface, j)
            uni.wgetch(interface)
            
            
    def checkWin(self) :
        loc = self.t.getArrivee()
        mat = self.t.Mat
        for x,y in loc :
            if y-1 > 0 :
                if mat[y-1][x].posee and mat[y-1][x].Type == "+" :
                    if mat[y-1][x].Mat[2][1] == 0 :
                        mat[y][x].reveal()
            if y+1 < self.t.dimX :
                if mat[y+1][x].posee and mat[y+1][x].Type == "+":
                    if mat[y+1][x].Mat[0][1] == 0 :
                        mat[y][x].reveal()
            if x-1 > 0 :
                if mat[y][x-1].posee and mat[y][x-1].Type == "+":
                    if mat[y][x-1].Mat[1][0] == 0 :
                        mat[y][x].reveal()
            if x+1 < self.t.dimX :
               
                if mat[y][x+1].posee and mat[y][x+1].Type == "+":
                    if mat[y][x+1].Mat[1][2] == 0 :
                        mat[y][x].reveal()
            if mat[y][x].Type == "G" and mat[y][x].State != "Hidden" :
                return True
        return False
        
    def printWinner(self, interface, result, j) :
        uni.clear()
        startx = int(0.4*self.scr.MaxX)
        starty = int(0.5*self.scr.MaxY)
        if result :
            uni.mvwaddstr(interface, starty, startx, "Les mineurs ont gagné !")
            uni.mvwaddstr(interface, starty+2, startx, f"Joueur qui a posé la carte gagnante : Joueur{j.id} {j.name}")
            uni.wrefresh(interface)
            uni.wgetch(interface)
            return
        uni.mvwaddstr(interface, starty, startx, "Les saboteurs ont gagné !")
        uni.wrefresh(interface)
        uni.wgetch(interface)
        return
            
j = Jeu()