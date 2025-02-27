import numpy as np

import math
import random
from PIL import ImageDraw

import src.shownp as viewer

"""
Started on this code but could not get it to work.
"""


def rotateAroundOrigin(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def retrieveSemiMinorAxis(fartestpoints, middlepoint, draw):
    rightpoint = 0
    # viewer.drawpoint(draw, middlepoint, 6)
    if (fartestpoints[0][0] > fartestpoints[1][0]):
        rightpoint = viewer.reverseCoordinates(fartestpoints[0])
    else:
        rightpoint = viewer.reverseCoordinates(fartestpoints[1])
    # rotatedpoint = rotateAroundOrigin(middlepoint, rightpoint, 0.3)
    # viewer.drawpoint(draw, middlepoint, 6)
    viewer.drawpoint(draw, viewer.reverseCoordinates(fartestpoints[0]), 6)
    # viewer.drawpoint(draw, (rotatedpoint[0], rotatedpoint[1]), 6)


def drawFoundCraters(sortedclusters, imagematrix, im):
    # draw = ImageDraw.Draw(im)
    mat = []
    edgeclusters = {}
    for (k, v) in sortedclusters.items():
        # v = sortedclusters[1]
        edgecluster = viewer.findEdges(v, imagematrix)  # Retrieves map of edgepoints in each cluster.
        edgeclusters[k] = edgecluster
        # map(lambda x: viewer.drawpoint(draw, (x[1], x[0]), 6), edgecluster)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster)  # Search for fartestpoint in cluster for diameter determination.
        # viewer.drawpoint(draw, (fartestpoints[0][1],fartestpoints[0][0]), 6)
        # viewer.drawpoint(draw, fartestpoints[0], 6)
        semiMajorAxis = 1 * distance
        a = semiMajorAxis / 2
        x, y = viewer.calculateMiddlePoint(semiMajorAxis, fartestpoints)

        bbox = (x - a, y - a, x + a, y + a)
        im = viewer.draw_ellipse(im, bbox, width=2)  # Thick bounds
        im = draw_thick_point(im, [x, y])
    # map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), edgeclusters.items())
    # viewer.plotClusters(mat)
    # im.save("output.png")
    im.show()


def draw_thick_point(im, xy):
    i = int(xy[0])
    j = int(xy[1])
    draw = ImageDraw.Draw(im)
    for x in range(i-2, i+1):
        for y in range(j-2, j+1):
            draw.point([x, y], fill='#31ff00')
    return im
