from Cards import *
from random import choice

class Table() :
    """Table du jeu, contient la matrice des cartes posées et gère la pose et l'enlèvement des cartes
    
    Attributs :
        Mat ([][]Carte) : Matrice d'objets abstraits de type Carte, va contenir toutes les cartes posées par les joueurs
        dimX (int) : taille horizontale de la table, auguementera quand les joueurs posent une carte sur les bords
        dimY (int) : taille verticale de la table, auguementera quand les joueurs posent une carte sur les bords
        
    Méthodes :
        randomArrivee() : génère un emplacement aléatoire pour chaque carte d'arrivée
        resetMat() : reset la table
        addLine(pos) : rajoute une ligne à la table au haut (up) ou en bas (other)
        addCollumn(pos) : rajoute une colonne à la table à droite (right) ou à gauche (other)
        getArrivee() : renvoie la position des cartes arrivee sur la table
        affTable() : affiche la table
        verifChemin(carteChemin, pos) : vérifie si la position proposée et la carte sont compatibles
        checkPosValid() : fonction utilisée par verifChemin
        putCard(c, pos) : remplacer la carte à la position pos dans la matrice par c 
    """
    def __init__(self) :
        """Constructeur de la classe Table
        """
        self.Mat = []
        self.dimX = 11
        self.dimY = 7
        self.resetMat()
        #Mettre la carte de départ et les cartes d'arrivée
        self.Mat[3][1] = Depart()
        self.randomArrivee()
        
    def randomArrivee(self) :
        """Mets les cartes d'arrivée en position
        """
        l = [1, 3, 5]
        # random choice pour l'or
        goldIdx = choice(l)
        self.Mat[goldIdx][-1] = Arrivee('G')
        # le reste
        l.remove(goldIdx)
        self.Mat[l[0]][-1] = Arrivee('C')
        self.Mat[l[1]][-1] = Arrivee('C')       
    def resetMat(self) :
        """reset la matrice de la table
        """
        for i in range(self.dimY) :
            line = []
            for j in range(self.dimX) :
                line.append(Carte())
            self.Mat.append(line)
            
    def addLine(self, pos) :
        """Ajoute une ligne à la matrice des cartes

        Args:
            pos (int): position de la ligne "up" pour la placer en haut, sinon en bas
        """
        vec = [Carte()]*self.dimX
        if pos == "up" :
            self.Mat.insert(0,vec)
        else :
            self.Mat.append(vec)
        self.dimY +=1
        
    def addCollumn(self, pos) :
        """Ajoute une colonne à la matrice des cartes

        Args:
            pos (int): position de la ligne "right" pour la placer à droite, sinon à gauche
        """
        for line in self.Mat :
            if pos == "right" :
                line.append(Carte())
            else : 
                line.insert(0,Carte())
        self.dimX += 1
        
    def getArrivee(self) :
        """Renvoie la position des cartes d'arrivée 
        """
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
        """Affiche la matrice des cartes de la table du jeu
        """
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
                                    print(q, end=' ')
                                    continue
                                        
                                print(q, end='')
                                continue
                            if card.Mat[j][i] == 1 :
                                if q >= 100 and i == 2 and j == 1 :
                                    print(u"\u2588", end='')
                                    continue
                                print(u"\u2588"*2, end='')
                                continue
                        if q >= 100 and i > 1 and j == 1 :
                            print(' ', end='')
                        print(' '*2, end='')
                    if j == 1 :
                        q += 1
                print(' ')
                
            
    def checkPosValid(self, c, x, y) :
        """Vérifie si la position et la carte sont compatibles
        """
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
        """Mets la carte c à la position pos

        Args:
            c (Chemin): Carte chemin à poser
            pos (int): Position souhaitée
        """
        c.posee = True
        y = int(pos/self.dimX)
        x = pos%self.dimX
        self.Mat[y][x] = c
        


class Joueur():
    """Class joueur. Chaque joueur sera défini par un objet de type Joueur 
    
    Attributs :
        Role (str) : role du joueur, (saboteur) ou (mineur)
        name (str) : nom du joueur
        Score (int) : score du joueur
        id (int) : identificateur du joueur
        Cards ([]Carte) : vecteur contenant les cartes possédées par le joueur
        state (Map[string]{integer}) : un dictionnaire contennant l'état des outils du joueur
    
    Méthodes :
        creerJoueur(name) : attribue au joueur son nom
        Action(carteAction) : applique l'effect de la carte carteAction sur le joueur en fonction de son code et type
        checkState() : vérifie si le joueur peut jouer ou pas
        piocher(carte) : ajoute carte au vecteur Cards du joueur
        passerTour(n) : enlève la carte cédée pour passer le tour
    """
    
    def __init__(self, id):
        """Constructeur de la classe Joueur

        Args:
            id (int): identificateur du joueur
        """
        self.Role=""
        self.name = ""
        self.Score=0
        self.id=id
        self.Cards=[]
        self.state={"pioche":0, "lampe":0,"chariot":0}

    def creerJoueur(self, nom): # sert pas à grande chose mais osef
        """Attribue au joueur son nom

        Args:
            nom (str): nom du joueur
        """
        self.name=nom



    def Action(self,carteAction):
        """Applique l'effet décrit par carteAction su le joueur

        Args:
            carteAction (Action()): carte Action utilisée
        """
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
        """Vérifie si le joueur peut jouer

        Returns:
            bool: False si il peut pas jouer, True sinon
        """
        if self.state["pioche"] < 0 :
            return False
        if self.state["lampe"] < 0 :
            return False
        if self.state["chariot"] < 0 : 
            return False
        return True

    def piocher(self,carte):
        """Ajoute carte chez le joueur

        Args:
            carte (Carte): Carte piochée
        """
        self.Cards.append(carte)

    def passerTour(self, n):
        """Enlève la carte cédée pour passer son tour

        Args:
            n (integer): indice de la carte à céder
        """
        self.Cards.remove(self.Cards[n])