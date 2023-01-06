# SabOOtters : le jeu où des loutres cherchent de l'or.
Le principe du jeu est le suivant :
 - Il existe des loutres qui cherchent de l'or, et des loutres qui veulent saboter la recherche
 - Les loutres utilisent des cartes Chemin pour tracer une mine entre la carte de départ et les 3 cartes d'arrivée. Une seule des 3 cartes d'arrivée contient de l'or.
 - Les loutres peuvent aussi utiliser des cartes ACTION pour réparer ou casser des outils, voir une des cartes d'arrivée, ou enlever une carte CHEMIN de la table.
 - Si les mineurs arrivent à l'or, ils gagnent. S'il ne reste plus de cartes et les mineurs n'ont toujours pas trouvé l'or, les saboteurs ont gagné.
 - A chaque fin de manche, l'or est distribué suivant entre les gagnant. Après 3 manches, la partie est finie et un classement des joueurs est affiché.


Afin de lancer le jeu, lancer le fichier `jeu.py` avec python3.

# Extensions

Il est possible de rajouter des cartes au jeu en modifiant les fichiers action.txt (cartes Action), chemin.txt (cartes Chemin), gold.txt (cartes Or).
 - Pour les cartes actions, suivre la syntaxe du fichier : `<nombre de carte> outil_touché positif(+)/negatif(-)`
 - Pour les cartes chemin, suivre la syntaxe du fichier : `<nombre de carte> Chemin_décrit(URLD) Type`
 - Pour les cartes Or, suivre la syntaxe du fichier : `<nombre de cartes> <nombre de lingots d'or>`

lien du github : https://github.com/Chems-bitti/MU4RBI01