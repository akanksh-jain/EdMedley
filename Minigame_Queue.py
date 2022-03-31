import queue

class Minigame_Queue:

    def __init__(self, queueMaxSize):
        self.queue = queue.LifoQueue(queueMaxSize);

    def addToMinigameQueue(self, minigame):
        if(self.queue.full()):
            return False;

        self.queue.put(minigame);
        return True;

    def getFromMinigameQueue(self):
        if(not self.queue.empty()):
            return self.queue.get();
        print("Failed to load minigame");
        return None;

    def isFull(self):
        return self.queue.full();

    def isEmpty(self):
        return self.queue.empty();
