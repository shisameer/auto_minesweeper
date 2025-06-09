# auto_minesweeper
Beating the existing record in the Minesweeper game (https://minesweeperonline.com/)

Algorithm:
- Divide the play area into a 9*9 matrix
- Maintain a list of available positions to click
- click randomly, and pop out the clicked cell
- Check the emoji above in each iteration, if it is a "happy emoji", continue, else, click on the emoji to restart the game

Result:
- Achieved a 1-second record time in beginner's difficulty.
