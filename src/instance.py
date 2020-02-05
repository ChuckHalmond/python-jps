import csv

from node import Node
from colors import Colors

class Instance():
    def __init__(self, matrix, matrixWidth, matrixHeight, startX, startY, endX, endY):
        self.matrix = matrix
        self.matrixWidth = matrixWidth
        self.matrixHeight = matrixHeight
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

class InstanceUtilities():

    @staticmethod
    def readCSVInstance(url):
        matrix = []

        with open(url) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=';')

            startX = None
            startY = None
            endX = None
            endY = None

            colCount = 0
            rowCount = 0

            rowIdx = 0
            colIdx = 0

            for row in csvReader:
                matrix.append([])

                colIdx = 0
                for col in row:

                    if col == 'X':
                        matrix[rowIdx].append(False)
                        print('X', end='')

                    else:
                        if col == 'D':
                            startX = colIdx
                            startY = rowIdx
                            print('D', end='')
                            
                        elif col == 'A':
                            endX = colIdx
                            endY = rowIdx
                            print('A', end='')

                        else:
                            print(' ', end='')

                        matrix[rowIdx].append(True)

                    colIdx = colIdx + 1
                
                if (colCount > 0 and colIdx != colCount):
                    raise Exception("The instance must have a constant columns count.")
                else:
                    colCount = colIdx
                
                rowIdx = rowIdx + 1
                print()
            rowCount = rowIdx
        
        if (startX == None):
            raise Exception("The instance must have a start node.")
        
        if (endX == None):
            raise Exception("The instance must have a end node.")
        
        return Instance(matrix, colCount, rowCount, startX, startY, endX, endY)

    @staticmethod
    def displayInstanceWithPath(instance, path):

        for y in range(instance.matrixHeight):
            for x in range(instance.matrixWidth):

                if (instance.matrix[y][x]):
                    
                    if (x == instance.startX and y == instance.startY):
                        Colors.queryPrintColor(Colors.GREEN)
                        print('D', end='')
                    elif (x == instance.endX and y == instance.endY):
                        Colors.queryPrintColor(Colors.RED)
                        print('A', end='')
                    else:
                        inPath = False
                        for node in path:
                            if (node[0] == x and node[1] == y):
                                if (path.count(node) > 1):
                                    Colors.queryPrintColor(Colors.CYAN)
                                    print('@', end='')
                                    while (path.count(node) > 0):
                                        path.remove(node)
                                else:
                                    Colors.queryPrintColor(Colors.YELLOW)
                                    print('o', end='')
                                inPath = True

                        if (not inPath):
                            print(' ', end='')
                else:
                    Colors.queryPrintColor(Colors.BLACK)
                    print('X', end='')
            print()
