import heapq
import itertools

# Create a priority queue
class PQ:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = -1
        self.counter = itertools.count()
        self.size = 0
        self.numAdded = 0

    # update the queue and priorities
    def update(self,game,priority=0):
        hash = game.hash()
        self.numAdded += 1
        if hash in self.entry_finder:
            self.remove_game(game)
        count = next(self.counter)
        entry = [priority,count,game]
        self.entry_finder[hash] = entry
        heapq.heappush(self.pq,entry)
        self.size += 1

    # remove some particular move
    def remove_game(self,task):
        entry = self.entry_finder.pop(task.hash())
        entry[-1] = self.REMOVED
        self.size -= 1
    
    # pop an object out of the queue
    def pop(self):
        while len(self.pq) > 0:
            priority,count,task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task.hash()]
                self.size -= 1
                return task
        return KeyError("Pop from an empty priority queue",str(self.size),str(self.pq))

    # check if a queue is empty
    def isEmpty(self):
        return self.size == 0
