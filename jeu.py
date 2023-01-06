from interface import *
from os import system

class Jeu() :
    """Class Jeu, gère la logique du jeu est son initialisation
    
    Attributs :
        nombreJoueurs (int) : le nombre de joueurs dans la partie
        listJoueur ([]Joueur) : list des joueurs dans la partie
        nbManche (int) : nombre de la manche actuelle
        nombreChercheur (int) : nombre de chercheurs d'or dans la partie
        Deck ([]Carte) : Cartes restantes dans la pioche
        Gold ([]Or) : Cartes d'or restantes
        t (Table) : La table du jeu
    
    Méthodes :
        getPlayers() : demande un input de l'utilisateur qui donnera le nombre de joueurs, et le nom de chacun
        giveRoles() : attribue un rôle à chaque joueur aléatoirement 
        printRules() : affiche les rêgles du jeu
        printInterface() : premier affichage de l'interface du jeu
        refreshInterface() : update de l'interface du jeu
        gameLoop() : lance la boucle du jeu principale
        printLeaderboard() : affiche les joueurs par ordre du score finale
        printGold(orPioche : []Or) : affiche les cartes d'or piochées
        getGold() : récupère la liste des cartes d'or issue d'un fichier text
        initDeck() : récupère les cartes du jeu issue d'un fichier text
        giveCards() : donne à chaque joueur un certain nombre de cartes au début de la manche
        printCards(j : Joueur) : affiche les cartes d'un joueur j
        printJoueurs() : affiche les joueurs du jeu ainsi que les états de leurs outils
        checkWin() : vérifie si la manche est finie
        printWinner(result : bool, j : Joueur) affiche le joueur qui a posé la carte gagnante
    """
    def __init__(self) :
        self.nombreJoueurs = 0
        self.listJoueurs = []
        self.nombreChercheur = 0
        self.Deck = []
        self.Gold = []
        self.nbManche = 0
        self.t = Table()
        self.getPlayers()
        self.getGold()
        self.printRules()
        while self.nbManche < 3 :
            self.giveRoles()
            self.initDeck()
            self.giveCards()
            self.printInterface()
            self.t = Table()
            minerWin, j = self.gameloop()
            self.nbManche +=1
            self.refreshInterface(j)
            self.printWinner(minerWin,j)
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
            for i  in range(self.nombreChercheur) :
                c = choice(self.Gold)
                orPioche.append(c)
                self.Gold.remove(c)
            i = j.id
            p = 0
            while p < self.nombreChercheur :
                if i == self.nombreJoueurs :
                    i = 0
                j = self.listJoueurs[i]
                if j.Role == "Mineur" :
                    p += 1
                    self.printGold(orPioche)
                    s = input(f"Joueur {j.id}, choisissez une carte : ")
                    try :
                        n = int(s) 
                    except :
                        print("Veuillez donner un nombre valide")
                        continue
                    if n > len(orPioche)-1 :
                        print("Veuillez donner un nombre de carte valide")
                        continue
                    j.Score += orPioche[n].Value
                    orPioche.remove(orPioche[n])
                i +=1
            self.Deck = []
            for j in self.listJoueurs :
                j.Cards = []
        self.printLeaderboard()

    def printLeaderboard(self) :
        self.listJoueurs.sort(key=lambda j: j.Score, reverse=True)
        system("cls")
        print("Résulats finaux :")
        for i, j in enumerate(self.listJoueurs) :
            print(f"{i+1}. Joueur {j.id}, {j.name}...........{j.Score}")
         
    def printGold(self, orPioche) :
        for y in range(4) :
            for i, card in enumerate(orPioche) :
                for x in range(3) :
                    if y == 0 or y == 2 :
                        print(u"\u2588"*2, end="")
                    if y == 1 :
                        print(f"  {card.Value}G  ", end="")
                        break
                if y == 3 :
                    print(f"  ({i}) ", end="")
                print(" "*5, end="")
            print(" ")
                        
    def getPlayers(self) :
        print("Bienvenue a SabOOters, ou des loutres essaient de trouver de l'or")
        n = 0
        while True :
            s = input("Veuillez donner le nombre de joueurs : ")
            try :
                n = int(s)
            except :
                print("Veuillez donner un nombre.")
                continue
            if n < 3 or n > 10 :
                print("Veuillez donner un nombre entre 3 et 10. ")
                continue
            break
        self.nombreJoueurs = n
        for i  in range(n) :
            s = input(f"Nom du joueur n°{i} : ")
            j = Joueur(i)
            j.creerJoueur(s)
            self.listJoueurs.append(j)
            
    def printRules(self) :
        system("cls")
        print("Dans ce jeu, il existe des loutres mineurs, et des loutres sabotteurs")
        print("Le but du jeu pour les mineurs est d'arriver a la carte a face cachee qui contient l'or")
        print("Le but des saboteurs est d'empêcher cela")
        self.t.affTable()
        print("Il existe trois type de cartes :")
        print("     - les cartes Chemins : elles sont utilisees pour 'miner' vers les cartes d'arrivee, chaque carte contient un dessin qui designe le chemin qu'elle definit")
        print("     - les cartes Action : elles sont utilisees pour appliquer des buff (ou des debuff) aux autres joueurs. Elles sont representees par un A (pour action), puis le type de buff (P pour pioche, L pour lampe, et C pour chariot), puis si c'est un buff (+) ou un debuff (-)")
        print("     Aussi, les carte eboulement (EBOU), et MAP permettent de retirer une carte de la table, ou regarder une des cartes a face cachee")
        print("     - les cartes OR : elles designent la quantite d'or que chaque joueur recois a chaque fin de manche. Le jeu est composee de trois manches")
        print("Si vous avez fini de lire les regles, appuyer sur une touche")
        input()
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
        
    def printCards(self,j: Joueur) :

        for y in range(3) :
            for i, card in enumerate(j.Cards) :
                for x in range(3) :

                    if isinstance(card, Action) :
                        if y == 0 and x == 1 :
                            print(f" A", end="")
                            continue
                        if y == 1 :
                            if x == 1 :
                                print(f"{card.Code}"+" "*(4-len(card.Code)), end="")
                                break
                        if y ==2 and x == 1 :
                            print(f"{card.Type} ", end="")
                            continue
                    if card.Mat[y][x] == 1 :
                        print(u"\u2588"*2, end="")
                        continue
                    if card.Mat[y][x] == 0 :
                        print("  ", end="")
                print(" "*5, end="")
            print(" ")
        for i, card in enumerate(j.Cards) :
            print(f" ({i})       ", end="")
        print(" ")
    
    def printJoueurs(self) :
        for i, j in enumerate(self.listJoueurs) :
            print(f"Joueur {i} : {j.name}      ", end="")
        print(" ")
        for j in self.listJoueurs :
            print(f"pioche : {j.state['pioche']}        " + " "*len(j.name), end= "" )
        print(" ")
        for j in self.listJoueurs :
            print(f"lampe : {j.state['lampe']}         " + " "*len(j.name), end= "" )
        print(" ")
        for j in self.listJoueurs :
            print(f"chariot : {j.state['chariot']}       " + " "*len(j.name), end= "" )
        print(" ")
    
    def printInterface(self) :
        print("Tour")
        self.t.affTable()
        self.printJoueurs()
        self.printCards(self.listJoueurs[0])
        
    def refreshInterface(self, j) :
        system("cls")
        print(f"Tour du Joueur {j.id} : {j.name}, {j.Role}")
        print(f"Nombre de cartes restantes : {len(self.Deck)}")
        self.t.affTable()
        self.printJoueurs()
        self.printCards(j)
        
    def gameloop(self) :
        i = 0
        lostFlag = 0
        while True :
            win = self.checkWin()
            if win :
                return win, j
            if i >= self.nombreJoueurs :
                i = 0
            j = self.listJoueurs[i]
            self.refreshInterface(j)
            if len(j.Cards) == 0 and len(self.Deck) == 0 :
                input("Pas de cartes restantes, veuillez appuyer sur ENTRER pour passer le tour")
                lostFlag += 1
                if lostFlag == self.nombreJoueurs:
                    return False, j
            
            s = input("Quelle carte à jouer ? 'P' pour passer ")
            if s == "P" or s == "p" :
                s = input("Quelle carte à céder pour passer le tour ?")
                try :
                    n = int(s)
                except :
                    print("Veuillez donner un nombre de carte valide")
                    input()
                    continue
                if n >= len(j.Cards) :
                    print("Veuillez donner un nombre de carte valide")
                    input()
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
                print("Veuillez donner un nombre de carte valide")
                input()
                continue
            if n >= len(j.Cards) :
                print("Veuillez donner un nombre de carte valide")
                input()
                continue
            c = j.Cards[n]
            if isinstance(c, Action) :
                if c.Code == "MAP" :
                    s = input("Choisir la carte arrivée que vous voulez voir : UP, MID, ou DOWN ")
                    loc = self.t.getArrivee()
                    mat = self.t.Mat
                    x, y = loc[0]
                    if s == "MID" :
                        x, y = loc[1]
                    if s == "DOWN" :
                        x, y = loc[2]
                    mat[y][x].reveal()
                    self.refreshInterface(j)
                    input()
                    mat[y][x].hide()
                    j.Cards.remove(c)
                    if len(self.Deck) > 0 :
                        c = choice(self.Deck)
                        self.Deck.remove(c)
                        j.piocher(c)
                    i += 1
                    continue
                    
                if c.Code == "EBOU" :
                    s = input("Choisir la carte que vous voulez enlever :")
                    try :
                        pos= int(s)
                    except :
                        print("Veuillez donner une position valide")
                        input()
                        continue

                    y = int((pos/self.t.dimX))
                    x = pos%self.t.dimX
                    if not self.t.Mat[y][x].posee :

                        print("Veuillez donner une position valide")
                        input()
                        continue
                    if isinstance(self.t.Mat[y][x], Arrivee) or isinstance(self.t.Mat[y][x], Depart) :
                        print("Les cartes de depart et arrivee ne peuvent pas etre enlevées")
                        input()
                        continue
                        
                    self.t.Mat[y][x] = Carte()
                    j.Cards.remove(c)
                    if len(self.Deck) > 0 :
                        c = choice(self.Deck)
                        self.Deck.remove(c)
                        j.piocher(c)
                    i += 1
                    continue

                s = input("Veuillez donner le nombre du joueur sur lequel vous voulez utiliser la carte Action : ")
                
                try :
                    n = int(s)
                except :
                    print("Veuillez donner un nombre de joueur valide")
                    input()
                    continue
                if n >= self.nombreJoueurs :
                    print(f"Veuillez donner un nombre de joueur entre 0 et {self.nombreJoueurs-1}")
                    input()
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
            s = input("Veuillez donner l'emplace de la carte :")
            try :
                pos = int(s)
            except :
                print("Veuillez donner un emplacement valide")
                input()
                continue
            validPos = self.t.verifChemin(c, pos)
            canPlay = j.checkState()
            if validPos and canPlay :
                self.t.putCard(c, pos)
                j.Cards.remove(c)

                self.t.affTable()
                #parce que sinon ça affiche un truc bizarre 
                if len(self.Deck) > 0 :
                    c = choice(self.Deck)
                    self.Deck.remove(c)
                    j.piocher(c)
                i += 1
                continue

            if not validPos :
                print("Veuillez donner un emplacement valide")
            if not canPlay :
                print("Vous ne pouvez pas jouer, un outil est cassé")
        
            input()
            
            
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
                    if mat[y][x-1].Mat[1][2] == 0 :
                        mat[y][x].reveal()
            if x+1 < self.t.dimX :
               
                if mat[y][x+1].posee and mat[y][x+1].Type == "+":
                    if mat[y][x+1].Mat[1][0] == 0 :
                        mat[y][x].reveal()
            if mat[y][x].Type == "G" and mat[y][x].State != "Hidden" :
                return True
        return False
        
    def printWinner(self, result, j) :
        if result :
            print("Les mineurs ont gagné !")
            print(f"Le joueur qui a posé la carte gagnate : Joueur {j.id} {j.name}, {j.Role}")
            input()
            return
        print("Les saboteurs ont gagné !")
        return
                     
    
j = Jeu()