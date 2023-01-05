from abc import ABC
class Carte(ABC) :
    """Class mère de toutes nos cartes

    Attributs:
        posee (bool) : définit si la carte est posée ou pas
        Mat ([][]int) : définit les endroits où il y'un un mur (1), un chemin (0), un point de départ (2), de l'Or (3) ou du charbon (4)
        Type (str) : Positive (+) ou Négative (-)
    """
    def __init__(self) :
        self.posee = False
        self.Mat = [[1,1,1],[1,1,1],[1,1,1]]
        self.Type = ""

class Depart(Carte) :
    """Carte de départ unique, classe fille de Carte

    Attributs:
        Attributs de la classe mère Carte (voir Carte())
        Mat ([][]int) : définit les endroits où il y'un un mur (1) ou un chemin (0) ou un point de départ (2)
        posee (bool) : définit si la carte est posée ou pas
    """
    def __init__(self) :
        super().__init__()
        self.Mat = [[1,0,1],[0,2,0],[1,0,1]] #Redéfinition 
        self.posee = True

class Arrivee(Carte) :
    """Carte d'arrivée, classe fille de Carte

    Attributs:
        Attributs de la classe mère Carte (voir Carte())
        Type (str) : définit si la carte est une carte Or ou une carte Charbon
        State (str) : "Hidden" par défaut, définit si la carte est revélée au joueur ou pas
        
    Méthodes :
        reveal() : révele la carte d'arrivé
        hide() : cache la carte d'arrivé
    """
    def __init__(self, Type) :
        """Contructeur de la classe Arrivée

        Args:
            Type (str): définit si la carte est une carte Or (G) ou une carte Charbon (C)
        """
        super().__init__()
        self.Type = Type
        #Bloquée au début
        self.State = "Hidden"
    def reveal(self) :
        """Réveler la carte arrivé, sa vraie nature sera afficher sur le prochain affichage de la table
        """
        if self.Type == "G" :
            self.Mat = [[1,0,1],[0,3,0],[1,0,1]]
        if self.Type == "C" :
            self.Mat = [[1,0,1],[0,4,0],[1,0,1]]
        self.State = "Shown"
        self.posee = True
    def hide(self) :
        """Cacher la vraie nature de la carte
        """
        self.Mat = [[1,1,1],[1,1,1],[1,1,1]]
        self.posee = False
        self.State = "Hidden"
        
    
        
class Chemin(Carte) :
    """Cartes chemins, à jouer par le joueur

    Attributs :
        Attributs de la classe mère Carte (voir Carte())
        Code (str) : définit le chemin décrit par la carte en UP (U) , LEFT (L), RIGHT (R) et DOWN (D)
        Type (str) : définit si le centre de la carte est bloqué par un mur (-) ou passant (+)
       
    Méthodes :
        getMat() : modifie la matrice de la carte afin qu'elle soit cohérente avec le Code et le Type de la carte
    """
    def __init__(self, Code, Type) :
        """Contructeur de la classe

        Args:
            Code (str) : définit le chemin décrit par la carte en UP (U) , LEFT (L), RIGHT (R) et DOWN (D)
            Type (str) : définit si le centre de la carte est bloqué par un mur (-) ou passant (+)
        """
        super().__init__()
        self.Code = Code
        self.Type = Type
        self.getMat()
    def getMat(self) :
        """Set la matrice de la carte
        """
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

class Action(Carte) :
    """Carte Action, à jouer par le joueur pour appliquer des effets
    

    Attributs :
        Attributs de la classe mère Carte (voir Carte())
        Code (str) : définit l'outil touché par la carte : Pioche (P), Lampe (L) ou Chariot (C). Aussi ça peut prendre la valeur MAP pour réveler une carte d'arrivée ou EBOU pour enlever une carte de la table
        Type (str) : définit si la carte a un effet positif (+) ou négatif (-)
    """
    def __init__(self, Code, Type) :
        super().__init__()
        self.Code = Code
        self.Type = Type

class Or(Carte) :
    """Carte Or, à distribuer auprès des joueurs à chaque fin de manche

    Attributs: 
        Attributs de la classe mère Carte (voir Carte())
        Value : valeur de la carte, 3 lingots, 2 ou 1 seul
    """
    def __init__(self, value) :
        super().__init__()
        self.Value = value        