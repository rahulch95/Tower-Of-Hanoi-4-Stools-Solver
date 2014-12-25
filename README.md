Tower-Of-Hanoi-4-Stools-Solver
==============================

## What is it?
Solves the tower of hanoi problem recursively for four stools and visualizes it for you. 
It uses memoization to enhance the speed, so it works for more than 1000 pieces instantly.

## How do I run it?
To run it you will need Python (tested in Python 3.3). Once you install python:
```
python SolvingController.py
```
to run the program. It will ask for your input, as to how many pieces do you want to play this game with and whether you want it to be solved automatically or whether you want to do it manually.
If you plan to use the automatic solver, you can customize the time each step takes by changing the variable "timeTakeForEachStep" on line 582 in SolvingController.py

## Software Stack
- Python
- Tkinter
