import copy
import queue

# import the user defined modules
from board import *
from priority import PQ

# search class to search for the best move
class Search:
    def __init__(self,start):
        self.parentTrace = {}
        self.start = start
        self.gamePath = []
        self.movePath = []
        self.numMoves = 0
        self.end = None

    # creatre the path to be printed
    def unwindPath(self):
        if self.end:
            target = self.end
        else:
            target = constructTargetBoard(self.start.numRods,self.start.numDisks,self.start.targetRod)

        startHash = self.start.hash()
        nextHash = target.hash()

        self.gamePath = []
        self.movePath = []

        if not startHash == nextHash:
            while(True):
                self.gamePath.insert(0,constructBoard(nextHash,self.start.numRods,self.start.numDisks,self.start.targetRod))
                if startHash == nextHash:
                    break
                else:
                    moves = self.parentTrace[nextHash][1]
                    self.movePath.insert(0,moves)
                    nextHash = self.parentTrace[nextHash][0]
        
        self.numMoves = len(self.movePath)

    # print the path
    def printPath(self,verbose = False):
        if verbose:
            counter = 0
            for i in range(len(self.gamePath)):
                if counter == 0:
                    print("original")
                    print("Heuristic = " + str(self.gamePath[i].heuristic()) + " : Actual Dist = " + str(len(self.gamePath) - counter - 1))
                    self.gamePath[i].printBoard()
                else:
                    print("Move = " + str(counter) + " : " + str(self.movePath[counter - 1]))
                    print("Heuristic = " + str(self.gamePath[i].heuristic()) + " : Actual Dist = " + str(len(self.gamePath) - counter - 1))
                    self.gamePath[i].printBoard()
                print("----------------------------------------")
                counter += 1
        else:
            for i in range(len(self.movePath)):
                print("Move = " + str(i + 1) + " : " + str(self.movePath[i]))
    
# BFS Class
class bfsSearch(Search):
    def __init__(self,start,end=None):
        super().__init__(start)
        if end is None:
            self.end = constructTargetBoard(start.numRods,start.numDisks,start.targetRod)
        else:
            self.end = end
        self.endHash = self.end.hash()
        self.parentTrace = {}
        self.search()

    # create a tree and apply BFS using queue
    def search(self):
        self.parentTrace = {}
        q = queue.Queue()
        q.put((self.start,(0,0,0)))
        while (not q.empty()):
            game = q.get()[0]
            hash = game.hash()
            if game.isFinished():
                self.unwindPath()
                return
            successors = game.successor()
            successors[:] = filter(lambda x: x[0].hash() not in self.parentTrace,successors)
            for successor in successors:
                self.parentTrace[successor[0].hash()] = (hash,successor[1])
                q.put(successor)

# DFS Class
class dfsSearch(Search):
    def __init__(self,start,end=None):
        super().__init__(start)
        if end is None:
            self.end = constructTargetBoard(start.numRods,start.numDisks,start.targetRod)
        else:
            self.end = end
        self.endHash = self.end.hash()
        self.parentTrace = {}
        self.search()
    
    # create a tree and apply DFS using stack
    def search(self):
        self.parentTrace = {}
        stack = [(self.start,(0,0,0))]
        while (not len(stack) == 0):
            game = stack.pop()[0]
            hash = game.hash()
            if game.isFinished():
                self.unwindPath()
                return
            successors = game.successor()
            successors[:] = filter(lambda x: x[0].hash() not in self.parentTrace,successors)
            for successor in successors:
                self.parentTrace[successor[0].hash()] = (hash,successor[1])
                stack.append(successor)

# A* Search Class
class AstarSearch(Search):
    def __init__(self,start,debug=False):
        super().__init__(start)
        self.end = constructTargetBoard(start.numRods,start.numDisks,start.targetRod)
        self.endHash = self.end.hash()
        self.openSet = PQ()
        self.openSet.update(start)
        self.closedSet = {}
        self.gScore = {start.hash():0}
        self.parentTrace[start.hash()] = {}
        self.search()
    
    # create a tree and apply A* search using openset
    def search(self):
        while not self.openSet.isEmpty():
            current = self.openSet.pop()
            chash = current.hash()
            if current.isFinished():
                self.unwindPath()
                return
            successors = current.successor()
            self.closedSet[chash] = True
            for successor in successors:
                shash = successor[0].hash()
                if shash in self.closedSet:
                    continue
                temp_gScore = self.gScore[chash] + 1
                if shash not in self.gScore:
                    self.gScore[shash] = temp_gScore
                elif temp_gScore >= self.gScore[shash]:
                    continue
                else:
                    self.gScore[shash] = temp_gScore
                self.parentTrace[shash] = (chash,successor[1])
                self.openSet.update(successor[0],temp_gScore + successor[0].heuristic())

# AO* Search Class
class AOstarSearch(Search):
    def __init__(self,start):
        super().__init__(start)
        self.end = constructTargetBoard(start.numRods,start.numDisks,start.targetRod)
        self.endHash = self.end.hash()
        self.openSet = PQ()
        self.openSet.update(start)
        self.closedSet = {}
        self.gScore = {start.hash():0}
        self.parentTrace[start.hash()] = {}
        self.search()

    # create a tree and apply AO* search using openset
    def search(self):
        while not self.openSet.isEmpty():
            current = self.openSet.pop()
            chash = current.hash()
            if current.isFinished():
                self.unwindPath()
                return
            successors = current.successor()
            self.closedSet[chash] = True
            for successor in successors:
                shash = successor[0].hash()
                if shash in self.closedSet:
                    continue
                temp_gScore = self.gScore[chash] + 1
                if shash not in self.gScore:
                    self.gScore[shash] = temp_gScore
                elif temp_gScore >= self.gScore[shash]:
                    continue
                else:
                    self.gScore[shash] = temp_gScore
                self.parentTrace[shash] = (chash,successor[1])
                self.openSet.update(successor[0],temp_gScore)                

# main function
if __name__ == "__main__":
    rods = int(input("Please enter the number of rods: "))
    disks = int(input("Please enter the number of disks: "))
    targetRod = int(input("Please enter the target rod number: "))
    board = towerOfHanoi(rods,disks,targetRod-1)
    
    # run until user exits
    while(True):
        print("Menu...")
        print("0. exit")
        print("1. BFS algorithm")
        print("2. DFS algorithm")
        print("3. A* algorithm")
        print("4. AO* algorithm")
        
        # take choice from user
        ch = int(input("Enter your choice based on the menu above..."))
        
        # choice conditions
        if ch == 0:
            exit(0)
        elif ch == 1:
            bfsSearch(board).printPath(True)
        elif ch == 2:
            dfsSearch(board).printPath(True)
        elif ch == 3:
            AstarSearch(board).printPath(True)
        elif ch == 4:
            AOstarSearch(board).printPath(True)
        else:
            print("Please enter a correct choice value")
