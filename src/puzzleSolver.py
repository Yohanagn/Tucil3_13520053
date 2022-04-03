import copy

class StateSpaceTree:
    def __init__(self, root, parent = None, depth=0, move=""):
        self.root = root
        self.parent = parent
        self.depth = depth
        self.move = move

class Queue:
    def __init__(self, priority):
        self.queue = []
        self.function = priority
    
    def isEmpty(self):
        return len(self.queue) == 0

    def firstElmt(self):
        return self.queue[0]

    def push(self, item):
        idx = 0
        found = False

        while(not found and idx < len(self.queue)):
            if(self.function(item, self.queue[idx])):
                found = True
            else:
                idx+=1
        
        self.queue.insert(idx, item)

    def pop(self):
        self.queue.pop(0)

class Puzzle:
    def __init__(self, dir):
        self.board = []
        self.size = 0

        f = open(dir, "r")
        for line in f:
            self.board.append(list(map(lambda x : int(x), line.split())))
        self.size = len(self.board)

    def emptyCell(self):
        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if(value==self.size**2):
                    return (i,j)
    def boardFlat(self):
        return [val for arr in self.board for val in arr]
        
    def move(self, a, b):
        (c, d) = self.emptyCell()
        if(c+a>=0 and c+a<self.size and d+b>=0 and d+b<self.size):
            moved_puzzle = copy.deepcopy(self)
            moved_puzzle.board[c][d], moved_puzzle.board[c+a][d+b] = moved_puzzle.board[c+a][d+b], moved_puzzle.board[c][d]
            return moved_puzzle
        else:
            return None

    def isSolveable(self):
        (c, d) = self.emptyCell()
        temp = self.boardFlat()
        x = (c+d) % 2
        total = 0
        for i in range(0,self.size**2):
            for j in range(i+1,self.size**2):
                if(temp[i]>temp[j]):
                    total+=1

        print("Jumlah inversi yang terjadi", total)
        print("Parity:", x)
        print("Alpha:", total + x, "(even)" if (total+x) % 2 == 0 else "(odd)")
    
        return (total + x) % 2 == 0

    def boardOutput(self):
        for row in self.board:
            for value in row:
                print('%4s' % (value if value!=self.size**2 else "#"), end="")
            print()

    