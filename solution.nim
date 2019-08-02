import strutils
import strformat
import math
import intsets
import sequtils
import times, os

var board: array[81, int]

proc print_seq(branch: seq[int]): string = 
    let dash = '-'
    var divr = "-----+-----+-----|\n|"
    var endr = "\n|"
    result = dash.repeat(19) & '\n' & '|'
    var sep = ""
    for i in 0..<branch.len:
        sep = if (i+1)%%3==0: "|" else: " "
        result.add($branch[i] & sep)
        if (i+1)%%9==0: result.add(endr)
        if (i+1)%%27==0: result.add(divr) 

proc next_branches(branch: seq[int]): seq[seq[int]] =
    var s = initIntSet() 
    for k in [1,2,3,4,5,6,7,8,9]:
        s.incl(k)
    let br_len = branch.len
    for i in 0 .. <br_len:
        if (i div 9)==(br_len div 9):
            s.excl(branch[i])
        if (i %% 9)==(br_len %% 9):
            s.excl(branch[i])
        if (i %% 9 div 3)==(br_len %% 9 div 3):
            if (i div 9 div 3)==(br_len div 9 div 3):
                s.excl(branch[i])
    for k in s.items():
        result.add(concat(branch, @[k]))

var br = newSeq[int](81)

echo("ID column numbers (i %% 9)")
for i in 0 .. <81:
    br[i] = i %% 9
echo(print_seq(br))

echo("ID row numbers (i div 9)")
for i in 0 .. <81:
    br[i] = i div 9
echo(print_seq(br))

echo("ID block numbers (row-wise: div 9 div 3)")
for i in 0 .. <81:
    br[i] = 3*(i div 9 div 3) + (i %% 9 div 3)
echo(print_seq(br))

var seed = @[1,2,3,4,5,6,7,8,9]
var branches: seq[seq[int]]
var boards: seq[seq[int]]
branches.add(seed)

let time = cpuTime()
while branches.len>0:
    for nxt in next_branches(branches.pop()).items():
        if nxt.len==81:
            boards.add(nxt)
        else:
            branches.add(nxt)
    if boards.len > 100000: # 1,000 solutions ~ 1.17 sec
        break
echo "Time taken: ", cpuTime()-time
