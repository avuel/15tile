# 15tile
This is a project to recreate an NxN tile sliding puzzle

i.e.

If you have a 3x3 puzzle, the solution is
1 2 3
4 5 6
7 8 

If you have a 4x4 puzzle, the solution is
1  2  3  4
5  6  7  8
9  10 11 12
13 14 15  

You can change the size of the grid by modifying the ROWS variable in the if __name__ == '__main__' statement
(ROWS = 3 produces a 3x3, ROWS = 4 produces a 4x4)

To play the game, you can either click on a tile next to the gray tile to move that tile over, or use the arrow keys
to move the blank tile in the direction of the arrow key (it felt more intuitive that way to me).

I would advise not going beyond a 10x10 as the size of the text is currently not scaled properly so displaying
3-digit numbers (10x10 only goes up to 99) on the smaller tiles is currently not fixed.

Futhermore, there is a 50/50 chance (I think) that the "randomized" layout of the board will be solvable
Once the board is solved, the player will not be able to move any tiles and will have to close the game and re-run the program.

Lastly, I aim to implement an algorithm (most likely iterative A*) to solve the game (and thus always make it solvable) and either
highlight the optimal tile to move to solve the puzzle, or maybe draw an arrow for while tile you should slide over
(I am thinking that highlighting the tile will be much easier as I would only need to change the color of the tile to yellow maybe)

The pygame code was mostly taken from this video
https://youtu.be/JtiK0DOeI4A

I did adapt the game but the tile generation and displaying (except for the numbers) is generally exactly what was shown in the video.

You must have Python and Pygame installed (I think my Python version is 3.8.8 64-bit and pygame 2.0.1)
I think all you need to do to run the game is drop the files all into one folder and then run test.py
Eventually I think I will create a game object and clean up the code in the test.py file