class MoveNode:

    def __init__(self, move, children, parent):
        self.move = move
        self.children = children
        self.parent = parent
        self.advantage_points = None
        self.depth = 1

    def __str__(self):
        stringRep = "Move : " + str(self.move) + \
                    " Point advantage : " + str(self.advantage_points) + \
                    " Checkmate : " + str(self.move.checkmate)
        stringRep += "\n"

        for child in self.children:
            stringRep += " " * self.get_depth() * 4
            stringRep += str(child)

        return stringRep

    def __gt__(self, other):
        if self.move.checkmate and not other.move.checkmate:
            return True
        if not self.move.checkmate and other.move.checkmate:
            return False
        if self.move.checkmate and other.move.checkmate:
            return False
        return self.advantage_points > other.advantage_points

    def __lt__(self, other):
        if self.move.checkmate and not other.move.checkmate:
            return False
        if not self.move.checkmate and other.move.checkmate:
            return True
        if self.move.stalemate and other.move.stalemate:
            return False
        return self.advantage_points < other.advantage_points

    def __eq__(self, other):
        if self.move.checkmate and other.move.checkmate:
            return True
        return self.advantage_points == other.advantage_points

    def getHighestNode(self):
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
            else:
                return highestNode

    def get_depth(self):
        depth = 1
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
                depth += 1
            else:
                return depth
