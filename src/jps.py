import heapq
import math
import utils
import heuristics

from grid import Grid
from node import Node

class JPS():
    '''
    Path finder using the Jump Point Search algorithm.
    '''

    # List of the open nodes, structured as a heap queue.
    # The node at the top is the one the closest to the end node.
    openList: list()

    # Grid containing the layout of the nodes and their walkable status.
    grid: Grid

    # Initialises the open list and the grid.
    def __init__(self, grid):
        self.grid = grid
        self.openList = []
        self.heuristic = heuristics.manhattan

    # Initialises the open list with the start node.
    # While the open list is not empty, takes the first node of the heap
    # (closest node top the end node) and if it is not the end node,
    # looks for its successors in identifySuccessors().
    def findPath(self, startX, startY, endX, endY):

        self.startNode = self.grid.getNodeAt(startX, startY)
        self.endNode = self.grid.getNodeAt(endX, endY)

        # self.openList[i].f - self.openList[i + 1].f

        # set the `g` and `f` value of the start node to be 0
        self.startNode.g = 0
        self.startNode.f = 0

        # push the start node into the open list
        heapq.heappush(self.openList, (self.startNode.g - self.startNode.f, self.startNode))
        self.startNode.opened = True

        # while the open list is not empty
        while (len(self.openList) > 0):
            # pop the position of node which has the minimum `f` value.
            node = heapq.heappop(self.openList)[1]
            node.closed = True

            if (node == self.endNode):
                return utils.expandPath(utils.backtrace(self.endNode))

            self.identifySuccessors(node)

        # fail to find the path
        return []

    # For each neighbor of the node, looks for jump points with jump()
    # and add them to the open list.
    def identifySuccessors(self, node):
        '''
        Identify successors for the given node. Runs a jump point search in the
        direction of each available neighbor, adding any points found to the open
        list.
        '''
        endX = self.endNode.x
        endY = self.endNode.y
        x = node.x
        y = node.y

        neighbors = self.findNeighbors(node)

        for i in range(len(neighbors)):

            neighbor = neighbors[i]

            jumpPoint = self.jump(neighbor[0], neighbor[1], x, y)

            if (jumpPoint):

                jx = jumpPoint[0]
                jy = jumpPoint[1]

                jumpNode = self.grid.getNodeAt(jx, jy)

                if (jumpNode.closed):
                    continue

                # include distance, as parent may not be immediately adjacent:
                d = heuristics.octile(abs(jx - x), abs(jy - y))
                
                ng = node.g + d # next `g` value

                if (not jumpNode.opened or ng < jumpNode.g):

                    jumpNode.g = ng
                    jumpNode.h = jumpNode.h or self.heuristic(abs(jx - endX), abs(jy - endY))
                    jumpNode.f = jumpNode.g + jumpNode.h
                    jumpNode.parent = node

                    if (not jumpNode.opened):
                        heapq.heappush(self.openList, (jumpNode.g - jumpNode.f, jumpNode))
                        jumpNode.opened = True
                    else:
                        for i in range(len(self.openList)):
                            if (self.openList[i][1] == jumpNode):
                                self.openList[i] = (jumpNode.g - jumpNode.f, jumpNode)

    # Jumps recursively until a jump point is found.
    def jump(self, x, y, px, py):
        '''
        Search recursively in the direction (parent -> child), stopping only when a
        jump point is found.
        Returns the x, y coordinate of the jump point found, or None if not found
        '''

        dx = x - px
        dy = y - py

        if (not self.grid.isWalkableAt(x, y)):
            return None

        if (self.grid.getNodeAt(x, y) == self.endNode):
            return [x, y]

        # check for forced neighbors
        # along the diagonal
        if (dx != 0 and dy != 0):
            if ((self.grid.isWalkableAt(x - dx, y + dy) and not self.grid.isWalkableAt(x - dx, y)) or
                (self.grid.isWalkableAt(x + dx, y - dy) and not self.grid.isWalkableAt(x, y - dy))):
                return [x, y]
            # when moving diagonally, must check for vertical/horizontal jump points
            if (self.jump(x + dx, y, x, y) or self.jump(x, y + dy, x, y)):
                return [x, y]
        # horizontally/vertically
        else:
            if (dx != 0): # moving along x
                if ((self.grid.isWalkableAt(x + dx, y + 1) and not self.grid.isWalkableAt(x, y + 1)) or
                (self.grid.isWalkableAt(x + dx, y - 1) and not self.grid.isWalkableAt(x, y - 1))):
                    return [x, y]
            else:
                if ((self.grid.isWalkableAt(x + 1, y + dy) and not self.grid.isWalkableAt(x + 1, y)) or
                (self.grid.isWalkableAt(x - 1, y + dy) and not self.grid.isWalkableAt(x - 1, y))):
                    return [x, y]

        return self.jump(x + dx, y + dy, x, y)

    # Finds all the walkable neighbors of the given node.
    def findNeighbors(self, node):
        '''
        Find the neighbors for the given node. If the node has a parent,
        prune the neighbors based on the jump point search algorithm, otherwise
        returns all available neighbors.
        '''
        parent = node.parent
        x = node.x
        y = node.y
        neighbors = []

        # directed pruning: can ignore most neighbors, unless forced.
        if (parent):

            px = parent.x
            py = parent.y

            # get the normalized direction of travel
            dx = int((x - px) / max(abs(x - px), 1))
            dy = int((y - py) / max(abs(y - py), 1))

            # search diagonally
            if (dx != 0 and dy != 0):
                if (self.grid.isWalkableAt(x, y + dy)):
                    neighbors.append([x, y + dy])

                if (self.grid.isWalkableAt(x + dx, y)):
                    neighbors.append([x + dx, y])

                if (self.grid.isWalkableAt(x + dx, y + dy)):
                    neighbors.append([x + dx, y + dy])

                if (not self.grid.isWalkableAt(x - dx, y)):
                    neighbors.append([x - dx, y + dy])

                if (not self.grid.isWalkableAt(x, y - dy)):
                    neighbors.append([x + dx, y - dy])

            # search horizontally/vertically
            else:
                if (dx == 0):
                    if (self.grid.isWalkableAt(x, y + dy)):
                        neighbors.append([x, y + dy])

                    if (not self.grid.isWalkableAt(x + 1, y)):
                        neighbors.append([x + 1, y + dy])

                    if (not self.grid.isWalkableAt(x - 1, y)):
                        neighbors.append([x - 1, y + dy])
                else:
                    if (self.grid.isWalkableAt(x + dx, y)):
                        neighbors.append([x + dx, y])

                    if (not self.grid.isWalkableAt(x, y + 1)):
                        neighbors.append([x + dx, y + 1])

                    if (not self.grid.isWalkableAt(x, y - 1)):
                        neighbors.append([x + dx, y - 1])

        # return all neighbors
        else:
            neighborNodes = self.grid.getNeighbors(node)
            for i in range(len(neighborNodes)):
                neighborNode = neighborNodes[i]
                neighbors.append([neighborNode.x, neighborNode.y])

        return neighbors
