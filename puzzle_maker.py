from collections import defaultdict
from random import shuffle
from collections import deque
# Functions
def to_branch(seq):
    branch = []
    blanks = []
    len_seq = len(seq)
    for i in range(81):
        if i < len_seq:
            if seq[i]!=' ':
                branch.append(seq[i])
            else:
                branch.append(' ')
                blanks.append(i)
        else:
            branch.append(' ')
            blanks.append(i)
    return (branch, blanks, len(blanks))
                
def to_seq(branch):
    return ''.join(branch)

branches = []    
def next_seq(branch_blanks):
    # Find the first blank
    res = {
        'board': None
        ,'branches': deque() # (branch: list[str], blanks: list[int], num_s: int)
    }
    branch, blanks, num_s = branch_blanks
    if num_s==1:
        left = unpicked(branch, blanks[0])
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
                    
def print_board(branch):
    print('-'*18)
    for i in range(min(len(branch), 81)):
        sep = ' ' if (i+1)%3 else '|'
        print(branch[i], end=sep)
        if (i+1)%9==0: print()
        if (i+1)%27==0: print('-----+-----+------')
    print()
    
# Now do it
one_to_nine = list('123456789')
shuffle(one_to_nine)
boards = []
branch = to_branch(''.join(one_to_nine))
branches = deque()
branches.append(branch)
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
    
solved = solve(branches)            

# Now make a puzzle
# Remove one square at random
def puzzler(solution):
    puzzle = list(solution[:]) 
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
    blanks = sum([1 for c in puzzle if c==' '])
    return puzzle, blanks, z

counts = defaultdict(list)
with open('puzzles.txt', 'a') as f:
    for i in range(15000):
        puzzle, blanks, z = puzzler(solved[0])
        f.write(''.join(puzzle))
        f.write(f', {str(blanks)}, {str(z)}\n')
        print(i)   
