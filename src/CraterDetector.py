import numpy as np
import timeit
import scipy.cluster.hierarchy as hcluster
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from scipy import ndimage #, random

import src.shownp as viewer
import src.EllipseFitter as ellipsefitter
from src.Crater import ClusterCrater
from src.Crater import Crater

primaryFilterTreshold = 170
secondaryFilterThreshold = 240


def applyPrimaryIlluminationFilter(im):
    """
    Uses predefined threshold to filter out pixels with lower gray-scale value

    [1] All gray-scale values lower than a threshold are set to 0
    [2] All gray-scale values higher than a threshold are set to 255 (max)

    :param im: The image file that needs to be filtered.
    :return: array (list) = list of all the pixels set to 0. imagematrix (ndarray) = matrix of the image with values either 0 of 255.
    """
    global primaryFilterTreshold
    array = []
    # print("im size : ", im.size)
    imagematrix = viewer.RGBToGray(np.asarray(im)) # convert color to grayscale
    # imagematrix = np.asarray(im)
    imagematrix_copy = np.copy(imagematrix)
    # print("im matrix size : ", imagematrix_copy.shape)
    for i in range(0, imagematrix_copy.shape[0] - 1):
        for j in range(0, imagematrix_copy.shape[1] - 1):

            if imagematrix_copy[i, j] >= primaryFilterTreshold:  # CHANGED SIGN
                imagematrix_copy[i, j] = 0
                array.append([i, j])
            else:
                imagematrix_copy[i, j] = 255
    # Uncomment this next line of code to view the intermediate result of the filter.
    # viewer.showGray(imagematrix_copy)
    return array, imagematrix_copy


def retrieveCraterClusters(array):
    """
    Uses hierarchical clustering to cluster pixels on an image that have values 0
    assigned to them.
    :param array: list of all the points that have value 0 assigned to them.
    :return: hashmap of all the clusters sorted by index.
    """
    mat = np.array(array)
    # print("mat size : ", mat.size)
    thresh = 10  # 5.5
    start_time = timeit.default_timer()
    clusters = hcluster.fclusterdata(mat, thresh, criterion="distance")
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"clustering executed in: {execution_time} seconds")
    sortedclusters = {}
    # print("nbr clusters : ", len(clusters))
    for i in range(0, len(clusters) - 1):
        if clusters[i] in sortedclusters.keys():
            sortedclusters[clusters[i]].append(mat[i])
        else:
            sortedclusters[clusters[i]] = [mat[i]]
    sortedclusters = {k: v for k, v in sortedclusters.items() if len(v) > 60}

    ## Uncomment this section to plot the clusters.
    mat = []
    # map(lambda (k, v): map(lambda l: mat.append([l[0], l[1]]), v), sortedclusters.items())
    list(map(lambda item: list(map(lambda l: mat.append([l[0], l[1]]), item[1])), sortedclusters.items()))
    # viewer.plotClusters(mat)
    ###
    return reIndexCenterPoints(sortedclusters)

def reIndexCenterPoints(centerpoints):
    """
    Helper method to rearrange missing cluster points in the given hashmap.
    This method is only to be accessed by methods in this module and not intented to be accesed arbitrarily.
    :param centerpoints: All the centerpoints of the craters in an image that needs sorting.
    :return: sorted cluster points.
    """
    counter = 1
    sortedcenterpoints = {}
    for (k, v) in centerpoints.items():
        sortedcenterpoints[counter] = v
        counter += 1
    return sortedcenterpoints

def retrieveAllClusterCenterPoints(sortedclusters, imagematrix):
    """
    Processes the clusters and returns list of all the centerpoints of the craters found in an image.
    :param sortedclusters: Clusters found on the image
    :param imagematrix: original image in matrix form
    :return: return all the centerpoints and initial diameters of the
    """
    # draw = ImageDraw.Draw(im)
    craters = {}
    edges = {}
    for (k, v) in sortedclusters.items():
        edgecluster = viewer.findEdges(v, imagematrix)
        # map(lambda x: edges[x.key]=x.value, edgecluster)
        # map(lambda x: viewer.drawpoint(draw, (x[1], x[0]), 6), edgecluster)
        distance, fartestpoints = viewer.searchForFartestPoint(edgecluster) #Search for fartestpoint in cluster for diameter determination.
        diameter = 1 * distance
        y, x = viewer.calculateMiddlePoint(diameter, fartestpoints)  # CHANGED X, Y to Y, X
        centerpoint = np.array([x, y])
        craters[k] = Crater(k, centerpoint, diameter)
    return craters


def extractCraters(im):
    """
    This method is only to be accessed by methods in this module and not intented to be accessed arbitrarily.
    :param im: image that needs to be processed and retrieve respective diameters.
    :return: centerpoint and the diameters of all the craters in the given image.
    """
    # print("applyPrimaryIlluminationFilter")
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    # print("retrieveCraterClusters")
    sortedclusters = retrieveCraterClusters(array)
    # print("retrieveAllClusterCenterPoints")
    craters = retrieveAllClusterCenterPoints(sortedclusters, imagematrix)
    # print("drawFoundCraters")
    # ellipsefitter.drawFoundCraters(sortedclusters, imagematrix, im)
    # print("extractCraters Finished")
    return craters

def extractCratersWithImage(im):
    """
    This method is only to be accessed by methods in this module and not intented to be accessed arbitrarily.
    :param im: image that needs to be processed and retrieve respective diameters.
    :return: centerpoint and the diameters of all the craters in the given image.
    """
    array, imagematrix = applyPrimaryIlluminationFilter(im)
    sortedclusters = retrieveCraterClusters(array)
    ellipsefitter.drawFoundCraters(sortedclusters, imagematrix, im)
