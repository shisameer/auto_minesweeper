# auto_minesweeper
Beating the existing record in Minesweeper game (https://minesweeperonline.com/)

Algorithm:
- Divide the playarea into 9*9 matrix
- maintain a list of available positions to click
- click randomly, and pop out the clicked cell
- Check emoji above for each itteration, if is "happy emoji" continue, else, click on the emoji to restart the game

Result:
- Achieved 1-second record time in beginner's difficulty.
