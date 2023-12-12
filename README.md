# ChessBoardRiddle
visualization of a nice riddle

based on the awsome [video from 3Blue1Brown and StandUp Maths](https://www.youtube.com/watch?v=as7Gkm7Y7h4)

also based on the [site](https://datagenetics.com/blog/december12014/index.html)

rules:

* there is a board of size  2^n X 2^n
* on each tile on the board there is a coin (heads or tails <=> 0/1)

Variants:

1) each coin is determined randomly
2) each coin is determined by an adversary

**the game goes as follows:**
  
  after the board is decided, only player 1 can see the boardץ
  
  a tile is chosen by the adversary/randomly.
  
  player 1, after seeing which tile was chosen, must invert one of the tiles, and only one, such that player 2 will be able to distinguish which tile was chosen.
