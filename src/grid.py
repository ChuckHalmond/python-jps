from node import Node

class Grid():
    '''
    The Grid serves as an encapsulation of the layout of the nodes.
    The matrix contains the walkable status of each node (True if the node is walkable, False otherwise).
    '''
    def __init__(self, width, height, matrix):
        self.matrix = matrix
        self.width = width
        self.height = height
        self.nodes = []

    def buildNodes(self):

        if (len(self.matrix) != self.height):
            raise Exception("height attribute must match with the matrix")

        if (len(self.matrix[0]) != self.width):
            raise Exception("width attribute must match with the matrix")

        for i in range(self.height):
            self.nodes.append([])
            for j in range(self.width):
                self.nodes[i].append(Node(j, i, self.matrix[i][j]))

        return self.nodes

    def getNodeAt(self, x, y):
        '''
            Returns the node at the specified position in the grid.
        '''
        return self.nodes[y][x]

    def isInside(self, x, y):
        '''
        Determines whether the position is inside the grid.
        '''
        return (x >= 0 and x < self.width) and (y >= 0 and y < self.height)

    def isWalkableAt(self, x, y):
        '''
            Returns wether the node at the specified position is Walkable or not.
        '''
        return self.isInside(x, y) and self.nodes[y][x].walkable


    def setWalkableAt(self, x, y, walkable):
        '''
        Sets the walkable property of the node at the given position.
        '''
        self.nodes[y][x].walkable = walkable

    def getNeighbors(self, node):
        '''
        Get the neighbors of the given node.
        '''
        x = node.x
        y = node.y
        nodes = self.nodes
        neighbors = []
        
        # ↑
        if (self.isWalkableAt(x, y - 1)):
            neighbors.append(nodes[y - 1][x])
        
        # →
        if (self.isWalkableAt(x + 1, y)):
            neighbors.append(nodes[y][x + 1])
        
        # ↓
        if (self.isWalkableAt(x, y + 1)):
            neighbors.append(nodes[y + 1][x])

        # ←
        if (self.isWalkableAt(x - 1, y)):
            neighbors.append(nodes[y][x - 1])

        # ↖
        if (self.isWalkableAt(x - 1, y - 1)):
            neighbors.append(nodes[y - 1][x - 1])

        # ↗
        if (self.isWalkableAt(x + 1, y - 1)):
            neighbors.append(nodes[y - 1][x + 1])

        # ↘
        if (self.isWalkableAt(x + 1, y + 1)):
            neighbors.append(nodes[y + 1][x + 1])

        # ↙
        if (self.isWalkableAt(x - 1, y + 1)):
            neighbors.append(nodes[y + 1][x - 1])
    
        return neighbors
