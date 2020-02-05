import math

def backtrace(node):
    '''
    Backtrace according to the parent records and return the path.
    (including both start and end nodes)
    '''

    path = [[node.x, node.y]]

    while (node.parent):
        node = node.parent
        path.append([node.x, node.y])

    path.reverse()

    return path

def biBacktrace(nodeA, nodeB):
    '''
    Backtrace from start and end node, and return the path.
    (including both start and end nodes)
    '''

    pathA = backtrace(nodeA)
    pathB = backtrace(nodeB)

    pathB.reverse()

    return pathA.extend(pathB)

def pathLength(path):
    '''
    Compute the length of the path.
    '''

    for i in range(path.length):
        a = path[i - 1]
        b = path[i]
        dx = a[0] - b[0]
        dy = a[1] - b[1]

        sum += math.sqrt(dx * dx + dy * dy)

    return sum


def interpolate(x0, y0, x1, y1):
    '''
    Given the start and end coordinates, return all the coordinates lying
    on the line formed by these coordinates, based on Bresenham's algorithm.
    '''

    line = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while (True):
        line.append([x0, y0])

        if (x0 == x1 and y0 == y1):
            break

        e2 = 2 * err

        if (e2 > -dy):
            err = err - dy
            x0 = x0 + sx

        if (e2 < dx):
            err = err + dx
            y0 = y0 + sy

    return line

def expandPath(path):
    '''
    Given a compressed path, return a new path that has all the segments
    in it interpolated.
    '''

    expanded = []
    pathLen = len(path)

    if (pathLen < 2):
        return expanded

    for i in range(pathLen - 1):
        coord0 = path[i]
        coord1 = path[i + 1]

        interpolated = interpolate(coord0[0], coord0[1], coord1[0], coord1[1])
        interpolatedLen = len(interpolated)

        for j in range(interpolatedLen):
            expanded.append(interpolated[j])

        expanded.append(path[pathLen - 1])

    return expanded

def smoothenPath(grid, path):
    '''
    Smoothen the give path.
    The original path will not be modified; a new path will be returned.
    '''

    pathLen = len(path)

    x0 = path[0][0] # path start x
    y0 = path[0][1] # path start y
    x1 = path[pathLen - 1][0] # path end x
    y1 = path[pathLen - 1][1] # path end y

    sx = x0 # current start coordinate
    sy = y0 # current start coordinate

    newPath = [[sx, sy]]

    for i in range(len):
        coord = path[i]
        ex = coord[0] # current end coordinate
        ey = coord[1] # current end coordinate

        line = interpolate(sx, sy, ex, ey)

        blocked = False
        for j in range(len(line)):
            testCoord = line[j]

            if (not grid.isWalkableAt(testCoord[0], testCoord[1])):
                blocked = True
                break

        if (blocked):
            lastValidCoord = path[i - 1]
            newPath.append(lastValidCoord)
            sx = lastValidCoord[0]
            sy = lastValidCoord[1]

    newPath.append([x1, y1])

    return newPath

def compressPath(path):
    '''
    Compress a path, remove redundant nodes without altering the shape
    The original path is not modified
    '''

    # nothing to compress
    if (len(path) < 3):
        return path

    compressed = []

    sx = path[0][0] # start x
    sy = path[0][1] # start y
    px = path[1][0] # second point x
    py = path[1][1] # second point y
    dx = px - sx # direction between the two points
    dy = py - sy # direction between the two points

    # normalize the direction
    sq = math.sqrt(dx * dx + dy * dy)
    dx /= sq
    dy /= sq

    # start the new path
    compressed.append([sx,sy])

    for i in range(len(path)):

        # store the last point
        lx = px
        ly = py

        # store the last direction
        ldx = dx
        ldy = dy

        # next point
        px = path[i][0]
        py = path[i][1]

        # next direction
        dx = px - lx
        dy = py - ly

        # normalize
        sq = math.sqrt(dx * dx + dy * dy)
        dx /= sq
        dy /= sq

        # if the direction has changed, store the point
        if (dx != ldx or dy != ldy):
            compressed.append([lx,ly])

    # store the last point
    compressed.append([px,py])

    return compressed