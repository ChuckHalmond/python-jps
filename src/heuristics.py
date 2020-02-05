import math

SQRT2 = math.sqrt(2)

'''
Manhattan distance.
'''
def manhattan(dx, dy):
      return dx + dy

'''
Euclidean distance.
'''
def euclidean(dx, dy):
    return math.sqrt(dx * dx + dy * dy)

'''
Octile distance.
'''
def octile(dx, dy):
      F = SQRT2 - 1
      return F * dx + dy if (dx < dy) else F * dy + dx

'''
Chebyshev distance.
'''
def chebyshev(dx, dy):
    return max(dx, dy)