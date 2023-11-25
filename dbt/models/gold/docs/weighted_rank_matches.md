{% docs weighted_rank_matches %}

This column calculates the score based on the players' ranking on the game, the numbers of players, plus the weight of the game.

The formula is calculated by:

- If player is the ranked first, then they scores game weight.
- If the player is ranked last, they scores 0 points.
- Otherwise, the player scores (1 - (rank/quantity of players)) * game weight

{% enddocs %}