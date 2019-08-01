# sudoku_boards
Create solved boards first, then make puzzles.

## Introduction
I ran across this problem while checking out /r/learnpython on Reddit. /u/TeamTuck wrote some code that created "completed" sudoku boards (all cells in a sudoku board filled in with a number with uniqueness across rows, columns, and "blocks"). I thought I'd take a crack at solving it. I've tried many approaches and they all went nowhere...until recently. I had the clarity need to think about the problem in The Right Way (c). For closure, here's me telling you my thought process.

## Mistakes were made
I made a lot of mistakes. I think the failure I was having was that I though that you could do things sequentially, using a cell by cell walk, with the idea that if you find that you've taken the wrong path, just back up and choose a better one. That becomes a problem if you haven't been recording things right. I kept creating solutions where backtracking wasn't done correctly. I essentially destroyed the necessry information that I could recover from it.  

## Don't do that
So I tried to think outside the box and I have something that you could easily adapt to get what you are looking for. I think your problem generally stated is: I'd like to randomly generate a "solved" or completed sudoku board, all 81 squares fill in with valid numbers in which the constraints of unique numbers in columns, rows, and blocks are preserved. Presumably the next step is to then obscure some numbers and now you have a "puzzle maker". That's for another time.

My approach was to just create all possible boards. Rather than finding one, let's find them all! It might not be that big of a set especially since one of my insights was to recognize that we should always fill in the top row with numbers 1...9 in order. Why? Well, if we started there and found all possible solutions from that, then all we take each completed board and make a global substitute of the numbers with other numbers. We've just cut the number of boards we need to store by a factor of 9!, that is 9 factorial. 

## Algorithm
Ok so let's assume that you're ok with starting with the first row filled in with 1...9. Now we need to start "branching". Branching is the process of taking a partially filled in board and determining if we can fill in one more square. If we can, well that's a new branching we need to consider. After we fill in one more square, what can we do next? And on and on until we've filled in all the squares or a branch terminates because there are no other numbers that can be put in the next cell (this is called a "nonviable" branch). I have a "boards" array in my code that I continually add to when I find a solution. 

So to review: start somewhere (first branch), fill in one more square (new branch), repeatedly evaluate all branches until all the squares are filled in or you can go any further. So this process is growing and shrinking the branches list and when the list is empty, you're done. 

## Code building blocks
That's the idea, but let's be more specific. Lets say you start by filling in the first upper left hand cell with a "1". What are your next possible branches? 

For the purposes of not being too verbose (and this is how I solved the problem), let's define a notation I call sequences: a join of all filled in squares. So rather than representing the board as a 2x2 table, let's just list the numbers left to right top to bottom.

Given that definition, the with a start point of "1", we could have the following branches: "12", "13", "14", and so one. Since I said we are starting at "123456789", then our next branches are 

    1234567894
    1234567895
    1234567896
    1234567897
    1234567898
    1234567899

Given that the first block contains 1,2, and 3, we can't choose for the next branches any that end in 1,2,3.

So to be a little more specific the algorithm is such: define a list of all branches. Pop off the branches list one branch and determine what new, viable branches can come from that one branch (if any). If the next branch leads to a completed board, record that result and don't push anything back on to the branches list, else, push the next branch onto the branches list. Rinse, lather, repeat until we have no more entries in the branches list. That's it. You could call this a "depth" first search of all possible branches depending on how you set up your code.

## What is a board?
Ok, some more things to consider. So the first thing to note is that the way the math works out, it's "easier" to store the board as a list of 81 numbers, instead of a list of lists. It's easier if the board is one-dimensional. The initial state of the board could be defined as:

```python
    board = [0 for _ in range(81)]
```

I am going to use the sequence notation I described earlier. So we need a way of going back and forth between a sequence (which I abbreviate as seq) and a board. The starting point is with `seq = '123456789'`. We can push that to a board by the following code:

```python
    for i, k in enumerate(seq):
        board[i] = int(k)
```

And we can get a `seq` for a `board` by the following function:

```python
    def to_seq(cell):
        return ''.join([map(str, board[:cell]))
```

Seeing that we are interested in building new sequences from old sequences, let's expand the function to accept a second arguement `k`, which is the next number I was to push on the sequence:

```python
    def to_seq(cell, k):
        return ''.join([map(str, board[:cell]+[k])) # alternative: ''.join([str(s) for s in board[:cell]+[k]])
```

I think you'll see how that will be useful later.

## What are my choices (what's left)?
Ok, so let's talk about evaluating the next possible squares to fill out. Given a partially filled board (or sequence, we can talk about them interchangeably since we can use code to go back and forth between the two), what are all the next possible boards? We need a way of knowing what choices we have left, what numbers are "unpicked" given the row, column, block constraints. What about those constraints? Here we need to talk about how we can navigate the board.

Given a board, what are all the numbers that share the same row as a given cell. So for instance, if I show you to following partial board: 

```
1 2 3 4 5 6 7 8 9
9 8 7 3 2 1 6 5 4
6 5 4 9 8 7 3 2 1
8 9 6 7 4 5 2 1 3
4 7 2 1 6 3 8 9 5
5 3 1 2 .
```

What numbers have been already seen in the same row as the "."? You can look at it and say "5,3,1,2" easily. But let's do that in code. Notice the dot is in position 49 (0-based indexing). We should get that answer if we do the following snippet:

```python
    c = 49
    p = [] # p = picked
    for i in range(c):
        if i//9==c//9:
            if k: p.append(k) 
    # p = [5,3,2,1]
```

For columns we use the operator `%`. So we could combine the two:

```python

    c = 49
    p = [] # p = picked
    for i in range(c):
        if i//9==c//9:
            if k: p.append(k)
        if i%9==c%9:
            if k: p.append(k)
    # p = [5,3,1,2,5,2,8,4,6]
```

For "blocks" you have to think about this a little more and it depends on how you want to associate blocks with numbers. I chose to number the blocks for left to right, top to bottom like so

```
0 0 0 1 1 1 2 2 2
0 0 0 1 1 1 2 2 2
0 0 0 1 1 1 2 2 2
3 3 3 4 4 4 5 5 5
3 3 3 4 4 4 5 5 5
3 3 3 4 4 4 5 5 5
6 6 6 7 7 7 8 8 8
6 6 6 7 7 7 8 8 8
6 6 6 7 7 7 8 8 8
```
or
```
0 1 2
3 4 5
6 7 8
```
You could have done it "column-wise" like this:
```
0 3 6
1 4 7
2 5 8
```
The question is how do you associate each cell with a block? Here's the answer, I'll let you ponder this (because we are labeling blocks "row-wise):

```python

    c = 49
    p = [] # p = picked
    for i in range(c):
        if i//9==c//9:
            if k: p.append(k)
        if i%9==c%9:
            if k: p.append(k)
        if (i//9//3)==(c//9//3) and (i%9//3)==(c%9//3):
            p.append(k)
```

So that mens that we know what numbers are "unpicked" given a partially filled board or seq by:

```python
    def unpicked(seq):
        board = [0 for _ in range(81)]
        for i, k in enumerate(seq):
            board[i] = int(k)
        p = [] # p = picked
        c = len(seq)
        for i in range(81):
            k = board[i]
            if not k: continue
            if i//9==c//9:
                p.append(k)
            if i%9==c%9:
                p.append(k)
            if (i//9//3)==(c//9//3) and (i%9//3)==(c%9//3):
                p.append(k)
        return [k for k in range(1, 10) if k not in p]
```

## Next
Next let's think about how to create the "next sequence" or branch given an existing branch. Here's the code:

```python
    def next_seq(seq):
        next_br = []
        left = unpicked(seq)
        if left:
            for k in left:
                new_seq = seq+str(k)
                if len(new_seq)==81:
                    boards.append(new_seq)
                else:
                    next_br.append(new_seq)
        return next_br
```

I've failed to mention, but I do have a global variable `boards` which keeps a record of the all completed, valid Sudoku boards. Notice that with this code, non-viable branches die of natural causes and new, viable ones are created fo the next iteration.

## Branching
Here is the code that manages the `branches` list:

```python
    boards = []
    branches = next_seq('123456789') # pick your seed value (could be random choice)
    while branches:
        new_br = next_seq(branches.pop())
        branches.extend(new_br)
        # for early out uncomment: 
        # if boards: break
    print(f'Final: {len(boards)}')
```

## Board printing
To look at any sequence (or branch) partial or complete use this `print_board` method:

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

I've set the code to run with a seed of '123456789' and I am hoping that this can all fit into a database and the that the number won't be too astronomical, but I might be wrong on that. 

I'll leave it up to the reader to pick a random seen and to implement the early out (should happend really fast) to produce random board. 
