# Functions
def to_seq(c, k):
    return ''.join(map(str, board[:c]+[k]))
    
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
    
    
def unpicked(seq):
    board = [0 for _ in range(81)]
    for i, k in enumerate(seq):
        board[i] = int(k)
    p = []
    c = len(seq)
    for i in range(c):
        k = board[i]
        if not k: continue
        if i//9==c//9:
            p.append(k)
        if i%9==c%9:
            p.append(k)
        if (i//9//3)==(c//9//3) and (i%9//3)==(c%9//3):
            p.append(k)
    return [k for k in range(1, 10) if k not in p] 
                    
def print_board(branch):
    print('-'*18)
    for i in range(min(len(branch), 81)):
        sep = ' ' if (i+1)%3 else '|'
        print(branch[i], end=sep)
        if (i+1)%9==0: print()
        if (i+1)%27==0: print('-----+-----+------')
    print()
    
# Main part
picks = {}
boards = []
branches = next_seq('123456789') # pick seed here
total = 0
ticks = 1
total = len(branches)
while branches:
    # Helpful printout
    if ticks%100_000==0:
        print(f'boards: {len(boards)}',end=', ')
        print(f'branches: {len(branches)} ({min(map(len, branches))})',end=' ')
        print(f'({max(map(len,branches))})',end=', ')
        print(f'total: {total}')
    new_br = next_seq(branches.pop())
    total += len(new_br)
    branches.extend(new_br)
    ticks+=1
    # if boards: break
print(f'Final: {len(boards)}')
print_boards(boards[-1])
