# sudoku_boards
Create solved boards first, then make puzzles. See puzzle_maker.py. 

## Introduction
Most programmers are familiar with building a Sudoku solver. I ran across a discussion thread on Reddit where someone was trying to create "completed" sudoku boards (an 9 X 9 grid of numbers with uniqueness across rows, columns, and "blocks"). That seemed fun. I also thought that if you can make a completed board, you could tweak the algorithm to develop puzzles (partially filled board that only have one solution). Here is what we are going to do:

    * Make a board builder
    * Make a solver
    * Make a puzzler (something that can make puzzles) 

## Mistakes were made
I made a lot of mistakes. I trying a cell by cell walk, with the idea that if I took a wrong path, just back up and choose a better one. I kept creating solutions where backtracking wasn't done correctly. Let's look at a simple first approach. 

```python

class Cell:
    def __init__(self):
        self.choice = None
        self.includes = set([str(i) for i in range(1,10)])
        self.excludes = set()

board = []
for r in range(9):
    row = []
    for c in range(9):
        row.append(Cell())
    board.append(row)
    
# For each cell, make a random choice
# Go to next cell and figure out what hasn't been chosen yet (cell.includes - picked)
# Make a random choice (board[i][j].choice = k)
# If you run out of choices, go back?
```  

What you'll discover is that it's hard to know how far to go back. If you do the analysis of where a series of choices go wrong, it's easy to find a case where the mistake needs to be corrected three or more cells before the one you are currently on. 

## Don't do that, do this
So I tried to think outside the box. For one, it's actually easier to solve the problem if your Sudoku board is one dimensional. The other major idea was to think about things in terms of "branches" and then take a "depth-first" approach to exploring the branching space. 

I thought about the board not as a 81 length array but as a string that joined all the numbers together. A "branch" is a series of consecutive number choices and the question is what is the next set of branches that I could explore? So for instance, let's start all the way at the beginning. You're at the first uppermost left hand corner cell. What are your options? 1..9 of course. Let's choose "1" as my first branch. What are the next branches? {"12", "13", "14", ..., "19"}. Let's pop off the front and look at it's next branches: "12" -> {"123", "124", ... "129"}. And so on. 

If we continued to do this, some branches won't have any other choices left. I call this a non-viable branch. Let's take this as an example:

```
-------------------
|1 2 3|4 5 6|7 8 9|
|4 5 6|1 2 3|_
...
-------------------
```

What can I put in the place of '_'? Nothing, we've exhausted all the choices. Therefore the procedure to determine the next_branch('123456789456123') should yield []. 

Now at some point, the length of our branching sequence will be 81 characters long. Ta-da! That's a solution. So that's the idea we need a pull sequences on and off a list, adding viable branches back on if there are any and discarding any non-viable branches or completed boards and storing them somewhere else. Adding and removing elements often is best handled using a double ended queue from the `collections` module. 

## Code building blocks
Let’s start with the basics. This is a board:

```python
    board = [' ' for _ in range(81)]
```

And we can get a sequence string notation `seq` from a `board` by the following function:

```python
    seq = ''.join(board)
```

We may need this because list are not hashable, but strings are. So we couldn't use a `board` as a key or members of a set, so maybe it's good to be able to from a `board` to a `seq`. What about the reverse? 

```python
def to_branch(seq):
    branch = []
    blanks = []
    len_seq = len(seq)
    for i in range(81):
        if i < len_seq:
            branch[i] = seq[i]
            if seq[i]==' ':
                blanks.append(seq[i])
        else:
            branch.append(' ')
            blanks.append(i)
```

## What's left?
So you're at a blank spot. And let's say the board has been filled out partially. What numbers can still go in that cell without violating any row, column, or block constraint? What values are "unpicked"?

```python
def unpicked(branch, c):
    c = int(c)
    p = []
    if branch[c]!=' ': return p
    for i, k in enumerate(branch):
        if k==' ' or i==c: continue
        if i//9==c//9:
            p.append(k)
        if i%9==c%9:
            p.append(k)
        if (i//9//3)==(c//9//3) and (i%9//3)==(c%9//3):
            p.append(k)
    return [str(k) for k in range(1, 10) if str(k) not in p]
```

I'll leave it up the reader to prove that this works. 
            
## Branching 
So you we have a branch and we know where its blanks are. Let's take the first blank and now we know how to figure out what is unpicked, we need to create viable branches (if any) or detect a completed board. 

```python
def next_seq(branch_blanks):
    res = {
        'board': None
        ,'branches': deque() # (branch: list[str], blanks: list[int], num_s: int)
    }
    branch, blanks, num_s = branch_blanks
    if num_s==1:
        left = unpicked(branch, blanks[0]) # look at the first blank
        if left: 
            branch[blanks[0]] = left[0]
            res['board'] = to_seq(branch)
            return res
    else:
        new_s, z = blanks[1:],blanks[0]
        for k in unpicked(branch, z):
            new_branch = branch[:] # performant copy
            new_branch[z]=k # set 'number'
            res['branches'].append((new_branch, new_s, num_s-1))
        return res
```

## Solve!
So now we just need to pull all the pieces together and find a (at least one) solution given a starting point (encoded in a `branches` deque).

```python
def solve(branches, out=1):
    solutions = []
    while branches:
        nxt = next_seq(branches.pop())
        if nxt['board']:
            solutions.append(nxt['board'])
        else:
            branches.extend(nxt['branches'])
        if len(solutions)>=out:
            return solutions
    return solutions
```

## Solver logic
Running this code will create a randomly filled in Sudoku board.

```python
one_to_nine = list('123456789')
shuffle(one_to_nine)
boards = []
branch = to_branch(''.join(one_to_nine))
branches = deque()
branches.append(branch)
solved = solve(branches)            
print_board(solved[0])
```

## Puzzle maker
Below is the code that will make a puzzle based on the following pseudo-code: start with a completed board. Replace a random number in the grid with a blank and try to solve it. If there is only one solution, choose another random cell to mask. Keep doing this until you stumble on a mask that leads to more than one solution, in which case the state of the board before then last change is a good enough puzzle. 

```python
puzzle = list(solved[0]) 
blanks = [i for i in range(81)]
shuffle(blanks)
for i, z in enumerate(blanks):
    k = puzzle[z]
    puzzle[z] = ' '
    # Check for single solution
    branch = to_branch(''.join(puzzle))
    branches = deque()
    branches.append(branch)
    solutions = solve(branches, out=2)
    # If so, remove one more and check
    if len(solutions)==1: continue
    # If not, then put the square back and you're done
    else:
        puzzle[z] = k
        break
        
print_board(puzzle)
```

## Pretty printer
This will take a `branch` and print it out nicely for debugging.

```python
def print_board(branch):
    print('-'*18)
    for i in range(min(len(branch), 81)):
        sep = ' ' if (i+1)%3 else '|'
        print(branch[i], end=sep)
        if (i+1)%9==0: print()
        if (i+1)%27==0: print('-----+-----+------')
    print()
```
