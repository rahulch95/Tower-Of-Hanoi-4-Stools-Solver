# Copyright 2013 Gary Baumgartner, Samuel Richard Holett Earle, Rahul Chaudhary 
# and Aayush Agarwal. Done as part of CSC148 Assignment 1.
# Distributed under the terms of the GNU General Public License.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
SolvingController: GUI window for automatically recursively (using memoization) solving Anne Hoy's problems,
while animating it.
"""

import tkinter as TI
import time
from tkinter import Canvas
from tkinter import Event
import sys

class DomainStools:    
    """Model Anne Hoy's stools holding cheese.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """
    
    def __init__(self: 'DomainStools', number_of_stools: int) -> None:
        """Initialize a new DomainStools.
        """
        
        self.num_stools = number_of_stools
        self.moves = 0
        self.layout = {}
        
        for stool in range(self.num_stools):
            self.layout[stool] = []        
        
    def number_of_stools(self: 'DomainStools') -> int:
        """Return the number of stools."""
    
        return self.num_stools
    
    def number_of_moves(self: 'DomainStools') -> int:
        """Return the number of moves so far."""
        
        return self.moves
    
    def add(self: 'DomainStools', 
            stool: float, 
            cheese: 'CheeseView' or 'Cheese') -> None:
        
        cheese.stool = stool  
        if stool in self.layout:
            self.layout[stool].append(cheese)            
        else:            
            self.layout[stool] = [cheese]
        
    def move(self: 'DomainStool', 
             cheese_to_move: 'CheeseView', 
             cheese: 'CheeseView') -> None:
        
        """
        Moving Cheeses
        """
        # for debugging
        #print(self.layout)
        #print(cheese_to_move.x_center)
        #print(cheese_to_move.size)
        #print(cheese.x_center)
        #print(cheese.y_center)
        #print(cheese.size)
        
        if (cheese_to_move.size < cheese.size and 
            self.layout[cheese_to_move.stool][-1] == cheese_to_move and 
            self.layout[cheese.stool][-1] == cheese): 
            
            self.moves += 1
            self.layout[cheese.stool].append(
                self.layout[cheese_to_move.stool].pop())

            cheese_to_move.stool = cheese.stool
        
                
        else:
            raise Exception
    
    def move_stools(self: 'DomainStools', 
                    start_stool: 'Starting stool', 
                    end_stool: 'End Stool') -> None:
        
        if ((self.layout[end_stool] == []) or (self.layout[start_stool][-1].size
                                               < self.layout[end_stool][-1].size
                                               )):
            self.moves += 1
            cheese_to_move = self.layout[start_stool][-1]
            self.layout[end_stool].append(self.layout[start_stool].pop())

class Cheese:
    
    def __init__(self: 'Cheese', size: float) -> None:
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        
        self.size = size
        
class CheeseView(Cheese):
    def __init__(self: 'CheeseView',
                 size: float,
                 click_handler: (lambda Event: None),
                 canvas: Canvas,
                 thickness: float,
                 x_center: float, y_center: float) -> None:
        """
        Initialize a new CheeseView.

        size - horizontal extent of this cheese
        click_handler - function to react to mouse clicks
        canvas - space to draw a representation of this cheese
        thickness - vertical extent of this cheese
        x_center - center of this cheese horizontally
        y_center - center of this cheese vertically
        """
        # Call the superclass constructor appropriately.

        super().__init__(size)

        # Store canvas, thickness, x_center and y_center in instance variables.
        
        self.canvas = canvas
        self.thickness = thickness
        self.x_center = x_center
        self.y_center = y_center

        # Create a rectangle on the canvas, and record the index that tkinter
        # uses to refer to it.
        
        self.index = canvas.create_rectangle(0, 0, 0, 0)

        # Initial placement.
        self.place(x_center, y_center)

        # Initially unhighlighted.
        self.highlight(False)

        # Tell the canvas to report when the rectangle is clicked.
        # The report is a call to click_handler, passing it this CheeseView
        # instance so the controller knows which one was clicked.
        
        self.canvas.tag_bind(self.index,
                             '<ButtonRelease>',
                             lambda _: click_handler(self))

    def highlight(self: 'CheeseView', highlighting: bool):
        """Set this CheeseView's colour to highlighted or not.

           highlighting - whether to highlight"""

        self.canvas.itemconfigure(self.index,
                                  fill=('red' if highlighting else 'orange'))

    def place(self: 'CheeseView', x_center: 'float', y_center: 'float'):
        """
        Place the cheese at particular coordinates
        (in the form of a rectangle)
        """
        
        self.canvas.coords(self.index, (x_center - self.size / 2, 
                                        y_center + self.thickness / 2, 
                                        x_center + self.size / 2, 
                                        y_center - self.thickness / 2))
        
        self.x_center = x_center
        self.y_center = y_center     

def tour_of_four_stools(n: int, stools: DomainStools) -> None:
    """Move an n cheese tower from the first stool in stools to the fourth.

       n - number of cheeses on the first stool of stools
       stools - a DomainStools with a tower of cheese on the first stool
                and three other empty stools
    """
    
    four_stool(n, stools, 0, 1, 2, 3)   



cached = {}

def determine_split(n: 'int') -> int:
    """
    Determining where the cheeses should be split so as to 
    solve it faster
    """
    def det_split(n: 'int') -> int:
        if not n in cached:
            if n > 1:
                min_moves = 2 ** n + 1
                for i in range(1, n):
                    moves = 2 * det_split(n - i)[0] + 2 ** i - 1
                    if moves < min_moves:
                        min_moves = moves
                        split = i
            else:
                min_moves = 1
                split = 1
            cached[n] = min_moves, split
        return cached[n]
    return det_split(n)
    

def four_stool(n: int, 
               stools: 'DomainStools', 
               start: 'Start stool', 
               inter_1: 'Intermediate Stool 1', 
               inter_2: 'Intermediate Stool 2', 
               end: 'End Stool') -> None:
    """
    A method to move n cheeses from the starting stool to the final stools 
    with the help of 2 intermediate stools (or total of 4 stools) 
    (this method calls the 3 stool method)
    """
    
    if n > 3:    
        i = determine_split(n)[1]
        four_stool(n - i, stools, start, inter_1, end, inter_2)
        three_stool(i, stools, start, inter_1, end)
        four_stool(n - i, stools, inter_2, start, inter_1, end)
    
    elif n == 3:
        stools.move_stools(start, inter_1)
        stools.move_stools(start, inter_2)
        stools.move_stools(start, end)
        stools.move_stools(inter_2, end)
        stools.move_stools(inter_1, end)
        
    elif n == 2:
        stools.move_stools(start, inter_2)
        stools.move_stools(start, end)
        stools.move_stools(inter_2, end)
        
    else:
        stools.move_stools(start, end)
    
    
def three_stool(n: int, 
                stools: 'DomainStools', 
                start: 'Starting Stool', 
                inter: 'Intermediate Stool 1', 
                end: 'End Stool') -> None:
    """
    A method to move n cheeses from the starting stool to the final stool
    with the help of 1 intermediate stool (or total of 3 stools) 
    """
    
    if n > 1:
        three_stool(n - 1, stools, start, end, inter)
        stools.move_stools(start, end)
        three_stool(n - 1, stools, inter, start, end)
        
    if n == 1:
        stools.move_stools(start, end)


class Cheese:
    
    def __init__(self: 'Cheese', size: float) -> None:
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """

        self.size = size

class SolvingController:
    
    def __init__(self: 'SolvingController',
                 number_of_cheeses: int, 
                 content_width: float, 
                 content_height: float, 
                 cheese_scale: float, 
                 seconds: float) -> None:
        """
        Initialize a new SolvingController.

        number_of_cheeses - number of cheese to tower on the first stool,
                            not counting the bottom cheese acting as stool
        content_width - width in pixels of the working area
        content_height - height in pixels of the working area
        cheese_scale - height in pixels for showing cheese thicknesses,
                       and to scale cheese diameters
        seconds - time in seconds for which cheese is highlighted before
                  being moved.
        """

        self.domain = DomainStools(4)

        self.cheese_to_move = None
        self.blinking = False
        
        self.highlight_time = seconds

        self.cheese_scale = cheese_scale
        self.cheese_num = number_of_cheeses

        self.root = TI.Tk()
        
        canvas = TI.Canvas(self.root,
                           background="blue",
                           width=content_width, 
                           height=content_height)
        
        canvas.pack(expand=True, fill=TI.BOTH)

        self.moves_label = TI.Label(self.root)
        self.show_number_of_moves()
        self.moves_label.pack()

        for stool in range(1 + self.domain.number_of_stools()):
            total_size = 0
            for size in range(1 + (number_of_cheeses if stool == 0 else 0)):
                cheese = CheeseView(self.cheese_scale *
                                    (number_of_cheeses + 1 - size),
                                    None,
                                    canvas,
                                    0 if size == 0 else self.cheese_scale,
                                    content_width * (stool + 1) /
                                    (self.domain.number_of_stools() + 1.0),
                                    content_height if size == 0 else 
                                    (content_height - cheese_scale / 2
                                    - total_size))
                
                self.domain.add(stool, cheese)
                if size != 0:
                    total_size += self.cheese_scale
                   

    def show_number_of_moves(self: 'SolvingController') -> None:
        """Show the number of moves so far."""

        self.moves_label.config(text='Number of moves: ' +
                                str(self.domain.number_of_moves()))
        

    def select(self: 'SolvingController', cheese) -> None:
        
        """If no cheese is selected to move, select cheese and highlight it.
           Otherwise try moving the currently selected cheese onto cheese:
           if that's not a valid move, blink the currently selected cheese.

           cheese - cheese to select for moving, or to try moving onto.
        """
        
        self.root.update()
        
        if self.cheese_to_move is None:
            self.cheese_to_move = cheese
            self.cheese_to_move.highlight(True)
            self.root.update()
            time.sleep(self.highlight_time)

        else:
            if cheese is not self.cheese_to_move:
                try:
                    self.domain.move(self.cheese_to_move, cheese)
                    self.cheese_to_move.place(cheese.x_center, 
                                              cheese.y_center - 
                                              self.cheese_scale / 2 
                                              if cheese.thickness == 0 
                                              else (cheese.y_center - 
                                                    self.cheese_scale))
                    
                    self.show_number_of_moves()
                    
                except:
                    self.blinking = True
                    for i in range(10):
                        self.cheese_to_move.highlight(i % 2 != 0)
                        self.root.update()
                        time.sleep(0.1)
                    self.blinking = False
            self.cheese_to_move.highlight(False)
            self.cheese_to_move = None
            
              
    def four_stool(self: 'SolvingController', 
                   n: int, 
                   start: 'Start Stool', 
                   inter_1: 'Intermediate Stool 1', 
                   inter_2: 'Intermediate Stool 2', 
                   end: 'End Stool') -> None:
        """
        A method to move n cheeses from the starting stool to the final stools 
        with the help of 2 intermediate stools (or total of 4 stools) 
        (this method uses the 3 stool method)
        
        """
        if n > 3: 
            
            i = determine_split(n)[1]
            self.four_stool(n - i, start, inter_1, end, inter_2)
            self.three_stool(i, start, inter_1, end)
            self.four_stool(n - i, inter_2, start, inter_1, end)
    
        elif n == 3:
            
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[inter_1][-1])
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[inter_2][-1])
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[end][-1])
            self.select(self.domain.layout[inter_2][-1])
            self.select(self.domain.layout[end][-1])
            self.select(self.domain.layout[inter_1][-1])
            self.select(self.domain.layout[end][-1])
        
        elif n == 2:
            
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[inter_2][-1])
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[end][-1])            
            self.select(self.domain.layout[inter_2][-1])
            self.select(self.domain.layout[end][-1])
        
        else:
            
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[end][-1])
    
    
    def three_stool(self: 'SolvingController', 
                    n: int, 
                    start: 'Starting Stool', 
                    inter: 'Intermediate Stool', 
                    end: 'End Stool') -> None:
        """
        A method to move n cheeses from the starting stool to the final stool
        with the help of 1 intermediate stool (or total of 3 stools) 
        
        """
    
        if n > 1:
            self.three_stool(n - 1, start, end, inter)
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[end][-1])
            self.three_stool(n - 1, inter, start, end)
       
        if n == 1:
            self.select(self.domain.layout[start][-1])
            self.select(self.domain.layout[end][-1])    

class ManualController:
    def __init__(self: 'ManualController',
                 number_of_cheeses: int, number_of_stools: int,
                 content_width: float, content_height: float,
                 cheese_scale: float):
        """
        Initialize a new ManualController.

        number_of_cheeses - number of cheese to tower on the first stool,
                            not counting the bottom cheese acting as stool
        number_of_stools - number of stools, to be shown as large cheeses
        content_width - width in pixels of the working area
        content_height - height in pixels of the working area
        cheese_scale - height in pixels for showing cheese thicknesses,
                       and to scale cheese diameters
        """

        self.domain = DomainStools(number_of_stools)

        self.cheese_to_move = None
        self.blinking = False

        self.cheese_scale = cheese_scale

        self.root = TI.Tk()
        canvas = TI.Canvas(self.root,
                           background="blue",
                           width=content_width, height=content_height)
        canvas.pack(expand=True, fill=TI.BOTH)

        self.moves_label = TI.Label(self.root)
        self.show_number_of_moves()
        self.moves_label.pack()

        for stool in range(self.domain.number_of_stools()):
            total_size = 0
            for size in range(1 + (number_of_cheeses if stool == 0 else 0)):
                cheese = CheeseView(self.cheese_scale *
                                    (number_of_cheeses + 1 - size),
                                    lambda cheese: self.clicked(cheese),
                                    canvas,
                                    self.cheese_scale,
                                    content_width *
                                    (stool + 1) /
                                    (self.domain.number_of_stools() + 1.0),
                                    content_height - cheese_scale / 2
                                    - total_size)
                self.domain.add(stool, cheese)
                total_size += self.cheese_scale

    def show_number_of_moves(self: 'ManualController'):
        """Show the number of moves so far."""

        self.moves_label.config(text='Number of moves: ' +
                                str(self.domain.number_of_moves()))

    def clicked(self: 'ManualController', cheese: CheeseView):
        """React to cheese being clicked: if not in the middle of blinking
           then select cheese for moving, or for moving onto.

           cheese - clicked cheese
        """
        if not self.blinking:
            self.select(cheese)

    def select(self: 'ManualController', cheese: CheeseView):
        """If no cheese is selected to move, select cheese and highlight it.
           Otherwise try moving the currently selected cheese onto cheese:
           if that's not a valid move, blink the currently selected cheese.

           cheese - cheese to select for moving, or to try moving onto.
        """

        if self.cheese_to_move is None:
            self.cheese_to_move = cheese
            self.cheese_to_move.highlight(True)
        else:
            if cheese is not self.cheese_to_move:
                try:
                    self.domain.move(self.cheese_to_move, cheese)
                    self.cheese_to_move.place(cheese.x_center,
                                              cheese.y_center
                                              - self.cheese_scale)
                    self.show_number_of_moves()
                except:
                    self.blinking = True
                    for i in range(10):
                        self.cheese_to_move.highlight(i % 2 != 0)
                        self.root.update()
                        time.sleep(0.1)
                    self.blinking = False
            self.cheese_to_move.highlight(False)
            self.cheese_to_move = None
            
if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    number_of_cheese = 6
    while(True):
        try:            
            #to change the number of cheese you want the animated solution for
            #change the variable number_of_cheese            
            number_of_cheese = int(input("\n--Animation opens in a new window--\nEnter number of cheeses to be moved: "))
            option = int(input("\n1. Solve Manually\n2. Solve Automatically in shortest possible number of moves\nEnter Option: "))
        except ValueError:
            print("The value inputed is not a number!")
        else:
            if option == 2:    
                # to change the amount of time taken for each step by the automatic solver
                # change the following variable
                timeTakenForEachStep = 0.3
                a = SolvingController(number_of_cheese, 1024, 320, 20, timeTakenForEachStep)
                a.four_stool(number_of_cheese, 0, 1, 2, 3)
            elif option == 1:
                ManualController(number_of_cheese, 4, 1024, 320, 20)
            else:
                print('Wrong Option! Try Again') 
            TI.mainloop()
    