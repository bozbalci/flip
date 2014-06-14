flip
----

Attempts to solve any Flip puzzle (from [Simon Tatham's puzzle collection][sgt]) in the least number of moves. *Still in development!*

Usage
-----

**TODO:** make this easier

Open the source code, and go to the `main()` function, and configure the grid `g`. An example configuration has been provided. The following functions are yours to use, in the grid configuration:

* `g = Grid(x, y)` will create a blank `x` by `y` grid named `g`
* `g.random()` will make `g` a random (solvable) grid
* `g.refresh()` will set every light on `g` to zero
* `g.invert(x, y)` will invert a single block `(x, y)` on `g` (neighbors are not affected). Remember that this may lead to unsolvable games.
* `g.toggle(x, y)` will toggle a single block `(x, y)` on `g` and its neighbors. 
* `print g` will print the grid `g`.

The Solver object `s = Solver(g)` will then solve the Grid `g` (read the source code for further information)

Standards
---------

* The lights which are turned on is denoted by a `1`, and the lights that are off are denoted by a `0`.
 
* The moves are in the format `(x, y)` where +x is from left to right, and +y is from the top to the bottom. The first column is `x=0`, and the first row is `y=0`.
 
* The solution table is in the `bottom row => top row` format.

How it works
------------

It uses the [light chasing][lc] algorithm to solve the puzzle. The solving procedure is as follows:

1. Use the light chasing algorithm on a blank board to observe the result of bringing particular lights from the top row to the bottom row, and generate a dictionary for later reference
2. Use the light chasing algorithm on the given board
3. Compare the bottom row configuration to the ones in the dictionary, and find the according top row lights, turn them on
4. Use the light chasing algorithm once more to solve the puzzle.
5. If a move has been made twice, undo the move, minimalising the moves required for solution.

Performance
-----------

Solves a 5x5 puzzle (the standard) in 0.01 seconds, and ten random 12x12 puzzles in 34.8 seconds (in a pretty old machine). Can solve 14x14 puzzles, and in a very long time 15x15 puzzles, crashes on 16x16 and up.

Example output
--------------

    Initial board
    *-----------*
    
     0 1 1 1 1
     0 1 1 1 1
     1 0 0 1 1
     1 1 1 0 1
     1 0 0 1 0
    
    Solved in 12 moves!
    
    List of moves
    *-----------*
    
    (0, 2)
    (0, 3)
    (0, 3)
    (1, 1)
    (1, 2)
    (1, 2)
    (1, 4)
    (2, 1)
    (2, 1)
    (2, 4)
    (3, 0)
    (4, 2)
    
    Solution table (7 entries)
    *------------*
    
    00111 => 00010
    01010 => 00111
    01101 => 10000
    10001 => 00011
    10110 => 00001
    11011 => 00100
    11100 => 01000

Requirements
------------
* Tested on Python 2.7.6

License
-------

    Copyright (c) 2014, Berk Özbalcı
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:
    
    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    
    * Redistributions in binary form must reproduce the above copyright notice, this
      list of conditions and the following disclaimer in the documentation and/or
      other materials provided with the distribution.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Links
-----

* [Flip, playable Java version][java]
* [Flip, playable JS version][js]
* [Flip, playable Windows executable][exe]
* [Manual to the puzzle][man]
* [Download links to Simon Tatham's puzzle collection][dl]

[sgt]: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/
[java]: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/java/flip.html
[js]: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html
[exe]: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/flip.exe
[dl]: http://www.chiark.greenend.org.uk/~sgtatham/puzzles/#download
[lc]: http://en.wikipedia.org/wiki/Lights_Out_%28game%29#Light_chasing
