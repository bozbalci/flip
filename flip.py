#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# flip.py - attempts to solve any flip puzzle (from Simon Tatham's puzzle collection)
#           in the least number of moves
#
# Copyright (c) 2014, Berk Özbalcı
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, random, itertools

class GridError(Exception):
   """ An error in the nature of the grid """

# The grid will hold the lights
class Grid:
   def __init__(self, width, height):
      if width <= 0:
         raise GridError("Grid width must be a positive integer")
      if height <= 0:
         raise GridError("Grid height must be a positive integer")
      if not (isinstance(width, (int, long)) and isinstance(height, (int, long))):
         raise GridError("Grid width/height must be integers")

      # Initialize all to zero
      grid = [[0 for i in range(width)] for j in range(height)]

      self.width = width
      self.height = height
      self.grid = grid

   # Turn on a few lights to generate a random grid.
   def random(self):
      for y, i in enumerate(self.grid):
         for x, j in enumerate(i):
            if random.choice([True, False]):
               self.toggle(x, y)

   # Reinitialize all to zero
   def refresh(self):
      for y, i in enumerate(self.grid):
         for x, j in enumerate(i):
            self.grid[y][x] = 0

   # Returns 0 or 1 depending on the light's state
   def get(self, x, y):
      if x > self.width - 1 or y > self.height - 1:
         raise GridError("Block index out of grid size")

      return self.grid[y][x]

   # Gets the bottom row as a sequence of ones and zeroes
   def get_bottom_row(self):
      m = ""
      for i in self.grid[self.height - 1]:
         m += str(i)
      return m
   
   # Returns a neighboring block
   def get_above(self, x, y):
      if y != 0:
         return (x, y - 1)
      else: raise IndexError
   def get_below(self, x, y):
      if y != self.height - 1:
         return (x, y + 1)
      else: raise IndexError
   def get_left(self, x, y):
      if x != 0:
         return (x - 1, y)
      else: raise IndexError
   def get_right(self, x, y):
      if x != self.width - 1:
         return (x + 1, y)
      else: raise IndexError

   # Toggles a single block
   def invert(self, x, y):
      if x > self.width - 1 or y > self.height - 1:
         raise GridError("Block index out of grid size")

      self.grid[y][x] = 1 - self.grid[y][x]

   # Operate a single move on (x, y)
   def toggle(self, x, y):
      if x > self.width - 1 or y > self.height - 1:
         raise GridError("Block index out of grid size")

      self.invert(x, y)
      try:
         a = self.get_above(x, y)
         self.invert(*a)
      except IndexError: pass
      try:
         a = self.get_below(x, y)
         self.invert(*a)
      except IndexError: pass
      try:
         a = self.get_left(x, y)
         self.invert(*a)
      except IndexError: pass
      try:
         a = self.get_right(x, y)
         self.invert(*a)
      except IndexError: pass

   # Print the grid neatly.
   def __repr__(self):
      output = ""
      for i in self.grid:
         for j in i:
            output += " " + str(j)
         output += "\n"
      return output[:-1]

class Solver:
   def __init__(self, grid):
      self.grid = grid
      self.solved = False

      # Transcript of moves
      self.toggles = []

      # Count of moves
      self.moves = 0

   # Light chasing algorithm (similar to Gaussian elimination)
   # If loud=True, then it will count moves
   def chase_lights(self, grid, loud=False):
      # For every line starting from the top
      for i in range(grid.height):
         for j in range(grid.width):
            # If it's black
            if grid.get(j, i) == 1:
               # Toggle the one below (except if it's the last line)
               try:
                  t = grid.get_below(j, i)
                  grid.toggle(*t)
                  if loud:
                     self.toggles.append(t)
               except IndexError:
                  pass

   # Okay, so this function is quite complicated.
   def generate_table(self):
      # This table is supposed to be filled by the end of this function.
      table = {}

      # Create a grid with the same size we're asked to solve.
      g = Grid(self.grid.width, self.grid.height)

      # Possible top row configurations
      configs = []
      # Combinations of 1, 2, 3, ... n
      for i in range(1, g.width):
         # E choose i
         for j in itertools.combinations(range(0, g.width), i):
            configs.append(j)

      for s in configs:
         # Dictionary entry for the lights in the top row
         top = "0" * g.width
         # Light the top row and add the string to the dictionary
         for c in s:
            g.toggle(c, 0)
            
            # Set cth char in top to 1
            top = top[:c] + '1' + top[c + 1:]
         self.chase_lights(g)
         bottom = g.get_bottom_row()
         if not all([c == "0" for c in bottom]):
            if bottom in table.keys():
               # Compare the amount of lights turned on in the top configurations
               n_deja = sum([1 for e in table[bottom] if e == "1"])
               n_current = sum([1 for e in top if e == "1"])
               if n_current <= n_deja:
                  table[bottom] = top
               else:
                  continue
            table[bottom] = top
         g.refresh()

      # Handle extreme cases
      # I.) If the board is 1x1, just turn off the light:
      if self.grid.width == 1 and self.grid.height == 1:
         table['1'] = '1'

      # II.) If the board is 2x2, the '11' case is simply '11':
      if self.grid.width == 2 and self.grid.height == 2:
         table['11'] = '11'

      self.table = table

   def solve(self):
      # First, generate the solution table for bottom row
      self.generate_table()

      # First chase of lights.
      self.chase_lights(self.grid, loud=True)

      # Get bottom row, and configure the top row accordingly
      bottom = self.grid.get_bottom_row()

      # If the bottom row isn't all zeroes, then it hasn't been solved
      if not bottom == '0' * self.grid.width:
         for i,j in enumerate(self.table[bottom]):
            if int(j) == 1:
               t = (i, 0)
               self.grid.toggle(*t)
               self.toggles.append(t)

         # Second chase of lights
         self.chase_lights(self.grid, loud=True)

      # Remove duplicate moves in self.toggles, set move count, etc.
      self.minimize()

      # Check if the puzzle has been solved
      self.check()

   def minimize(self):
      # Temporary variable to work on toggles
      work = self.toggles

      # If i is in the list an even number of times, remove it,
      # else, keep it
      for i in work:
         work.remove(i)
         if i in work:
            work.remove(i)
         else:
            work.append(i)

      self.toggles = work
      self.moves = len(work)

   # Returns true if every light is set to zero
   def check(self):
      self.solved = True
      for y in range(0, self.grid.height):
         for x in range(0, self.grid.width):
            if not self.grid.get(x, y) == 0:
               self.solved = False

def main():
   # Configure the grid here!
   # ------------------------
   
   g = Grid(5, 5)
   g.random()

   # ------------------------

   print "Initial board\n*-----------*\n\n%s\n" % g

   s = Solver(g)
   s.solve()

   if s.solved:
      print "Solved in " + str(s.moves) + " moves!\n"
   else:
      print "Could not solve the puzzle.\n\nFinal state\n*---------*\n\n%s\n" % g
   
   print "List of moves\n*-----------*\n"
   
   if len(s.toggles) == 0:
      print "None!"
   for k in sorted(sorted(s.toggles, key=lambda x: x[1]), key=lambda x: x[0]):
      print k

   print "\nSolution table (%s entries)\n*------------*\n" % str(len(s.table.keys()))
   
   if len(s.table.keys()) == 0:
      print "No entries!"
   for k in sorted(s.table.keys()):
      print k + " => " + s.table[k]

if __name__ == '__main__':
   try:
      main()
   except GridError as e:
      sys.stderr.write("Error: %s\n" % e)
      sys.exit(1)
   except Exception as e:
      sys.stderr.write("Unexpected exception: %s\n" % e)
      sys.exit(1)
   except:
      sys.exit(0)
