{% docs weighted_rank %}

This column calculated the score based on the players' ranking on the game, the numbers of players, plus the weighted of the game.

The formula is calculated by:

- Players individual score: Weight of the Game * (Total of Players on the Match - Ranking of the player on that game + 1). The sum of one is to avoid division by zero.
- Match possible score: Weight of the Game * Total of Players on the Match. Evaluates the maximum score possible for each match based on the first on the rank and the number of players. 
- Final score: sum(Players individual score)/sum(Match possible score)

The result is given in %. 

Example: Kanagawa has weight 2. In a match with 4 players the score would be calculated as

- Max score: 4 (total players) * 2 (game weight) = 8
- First player:  2 (weight) * [4 (total players) - 1 (player's ranking) + 1] = 8 
- Second player: 2 (weight) * [4 (total players) - 2 (player's ranking) + 1] = 6
- Third player:  2 (weight) * [4 (total players) - 3 (player's ranking) + 1] = 4
- Fourth player: 2 (weight) * [4 (total players) - 4 (player's ranking) + 1] = 2

{% enddocs %}