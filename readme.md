
Hex Game
--------
Ce projet presente l'arbitre du jeu [hex][1]. Il va faire jouer l'IA, Alice, contre votre implementation, Bob.

Travail demandé
---------------
Implementez le joueur Bob.
```py

from hexgame import AbstractPlayer, HORIZ, VERTI

class Player (AbstractPlayer):

    def play(self, board, direction, **options):
        print('Salut! C\'est moi, Bob.')
```
La méthode `play` recoit au moins deux arguments :

- le plâteau du jeu : `board[x][y]`
- la direction du joueur : `HORIZ` ou `VERTI`

Les tuiles/cases du plâteau sont organisés dans un tableau à deux dimensions. Chaque case est affecté une troisième coordonnée `z` qui est la somme de `x` et `y`. Cette troisième coordonnée permet une définition du voisinage. Vu que les cases sont des hexagones, ils auront six cases voisins. Ci-dessous un exemple d'un plâteau 4x4 avec les coordonnées `(x,y,z)` renseignées pour chaque case.

```
 /\  /\  /\  /\
/  \/  \/  \/  \
|000|101|202|303|
\  /\  /\  /\  /\
 \/  \/  \/  \/  \
  |011|112|213|314|
   \  /\  /\  /\  /\
    \/  \/  \/  \/  \
     |022|123|224|325|
     \  /\  /\  /\  /\
      \/  \/  \/  \/  \
       |033|134|235|336|
       \  /\  /\  /\  /
        \/  \/  \/  \/
```
La case `112` a les voisins `101`, `202`, `213`, `123`, `022`, `011`

[1]: https://en.wikipedia.org/wiki/Hex_%28board_game%29
