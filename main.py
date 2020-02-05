import sys
import time

sys.path.append('src')

from src.jps import JPS
from src.grid import Grid
from src.instance import Instance, InstanceUtilities

from src.colors import Colors

def executeJPSOnCSVInstance(url):

    print('Reading the instance..')

    instance = InstanceUtilities.readCSVInstance(url)

    print('Done.')

    grid = Grid(instance.matrixWidth, instance.matrixHeight, instance.matrix)
    grid.buildNodes()

    print('Computing JPS..')

    startTime = time.time()

    jps = JPS(grid)
    path = jps.findPath(instance.startX, instance.startY, instance.endX, instance.endY)

    endTime = time.time() - startTime

    InstanceUtilities.displayInstanceWithPath(instance, path)

    Colors.queryPrintColor(Colors.GREY)

    print('Done. Result computed in ' + str(endTime) + ' ms.')

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        executeJPSOnCSVInstance(sys.argv[1])
    else:
        print('Please pass a valid instance CSV file as first argument.')