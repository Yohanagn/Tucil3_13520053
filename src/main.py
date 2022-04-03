import time
import argparse
from puzzleSolver import Puzzle
from puzzleSolver import Queue
from puzzleSolver import StateSpaceTree

def tiles(puzzle):
    total = 0
    board = puzzle.boardFlat()
    
    for i in range(1, puzzle.size**2+1):
        if(board[i-1] != i):
            total+=1
    return total

def distance(puzzle):
    total = 0
    board = puzzle.boardFlat()

    for index in range(0, puzzle.size**2):
        currentElmt = board[index]
        if(currentElmt!=puzzle.size**2):
            cur_r, cur_c = (currentElmt-1) // puzzle.size, (currentElmt-1) % puzzle.size
            index_r, index_c = index // puzzle.size, index % puzzle.size

            total += abs(index_r - cur_r) + abs(index_c - cur_c)
    return total

def isSorted(puzzle):
    board = puzzle.boardFlat()
    
    for i in range(1, (puzzle.size**2)+1):
        if(board[i-1] != i):
            return False

    return True

def solution(solved):
    sol = []

    state = solved.parent
    prev = solved

    while(state != None):
       sol.insert(0,prev) 
       prev = state
       state = state.parent    
    return sol

argument_parser = argparse.ArgumentParser(prog='python main.py')
argument_parser.add_argument('filename', metavar='filename', type=str, help='Filename dari puzzle')
argument_parser.add_argument('-sh', '--shorthand', action='store_true', help='Menampilkan solusi')
argument_parser.add_argument('-md', '--manhattandist', action='store_true', help='Mengkalkulasi jarak')
argument = argument_parser.parse_args()

root = StateSpaceTree( Puzzle("../test/" + argument.filename) )
root.root.boardOutput()
print()

if(not root.root.isSolveable()):
    print("Puzzle is unsolveable.")
    exit()

print("Puzzle is solveable.")
print()

count = 1
cost = tiles
if(argument.manhattandist):
    cost = distance

pq = Queue(lambda x,y : x.depth + cost(x.root) <= y.depth + cost(y.root))
pq.push(root)
solution_state = None
movesItem = [(-1,0), (0,-1), (1,0), (0,1)]
moves = ["Up", "Left", "Down", "Right"]

start = time.process_time_ns()

while(not pq.isEmpty()):
    current = pq.firstElmt()
    pq.pop()
    if(isSorted(current.root)):
        solution_state = current
        break
    for i, (dr, dc) in enumerate(movesItem):
        if(moves[(i+2)%4] != current.move):
            total = StateSpaceTree(current.root.move(dr, dc), parent=current, depth=current.depth+1, move=moves[i])
            if(total != None and total.root != None):
                count += 1
                pq.push( total )

solution_array = solution(solution_state)
end = time.process_time_ns()

if(not argument.shorthand):
    for index, state in enumerate(solution_array):
        print("Step", str(index+1) + ":", state.move)
        state.root.boardOutput()
        print()

print("Jumlah pergeseran yang terjadi:", len(solution_array))
solutionSH = ""
for i in range(len(solution_array)):
    solutionSH += solution_array[i].move[0] + " "
solutionSH += "Solved"
print(solutionSH)

print(count,"nodes generated")

timeTaken = end - start
print(timeTaken / 1000000, "ms taken")