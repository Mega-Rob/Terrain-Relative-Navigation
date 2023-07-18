import numpy as np


import src.shownp as viewer

def allCombinationNormVectors(centerpoints):
    """
    Brute force calculations of every existing combinations of unit vectors in the catalogue.
    This method is meant to be private and not be accessed by method outside this module.
    :param centerpoints: Positions of all craters in the reference image
    :return: hashmap containing all the crater ids as key and with value of list indicating the unit vectors.
    """
    allcombinationnormvectors = {}
    for (k, point) in centerpoints.items():
        # print(type(point), point)
        allcombinationnormvectors[k] = []
        for (k2, point2) in centerpoints.items():
            # print(type(point2), point2)
            if point[0] == point2[0] and point[1] == point2[1]:
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                allcombinationnormvectors[k].append(vect)
    # print("all combination norm vector completed")
    return allcombinationnormvectors


def preprocessReferenceImage(refImageCraters):
    # def preprocessReferenceImage(catalogue, combinations, datapath):
    """
    Loads data from a given catalogue file and computes the combinations of unit vectors of each crater.
    :param catalogue: String indicating which file to load the data catalogue from.
    :param combinations: String to store the found combinations in.
    :return: None
    """
    # referenceCatalogueCenterpoints = extractCenterpoints(viewer.loadData(datapath, catalogue))
    referenceCatalogueCenterpoints = extractCenterpoints(refImageCraters)
    centerpoints = {}
    for k, v in referenceCatalogueCenterpoints.items():
        centerpoints[k] = v
    allPossibleCombinations = allCombinationNormVectors(centerpoints)
    return allPossibleCombinations
    # viewer.saveData(datapath, allPossibleCombinations, combinations)


def extractCenterpoints(craters):
    centerpoints = {}
    # map(lambda (key, crater): centerpoints.update({key:crater.centerpoint}), craters.items())
    list(map(lambda item: centerpoints.update({item[0]: item[1].centerpoint}), craters.items()))
    return centerpoints


#### Neural Network#####
# testdat = [sum(map(lambda x: x[0],sortedclusters[1]))/len(sortedclusters[1]), sum(map(lambda x: x[1],sortedclusters[1]))/len(sortedclusters[1])]
# diameter = np.sqrt(len(sortedclusters[1])/3.14)*2
# print diameter
# print "centroidin is x={}, y={}".format(testdat[0], testdat[1])
#
# testdat.append(diameter)
# testdat.append(testdat[0]*testdat[0])
# testdat.append(testdat[1]*testdat[1])
# network = Network([5,6,4,2],  alpha=0.1, beta=0.1, Lambda=0.9)
# network.read_network(dir="neural_network_configuration")
# print network.feed(testdat)*57

### Attempt for median filter#####

# def dataarray(matrix):
#     array = []
#     for i in range(512):
#         for j in range(512):
#             array.append([i, j, matrix[i][j]])
#     return array
# med = ndimage.median_filter(imagematrix, 16)
# medianfilteredimage = imagematrix - med
# viewer.showGray(medianfilteredimage)
# print imagematrix[-1,0]
#
# def getNeighbours(matrix, i, j):
#     if i==0 & j==0:
#         return np.array([matrix[1,0], matrix[0,1]])
#
#     elif i==0 & j==0:
#         return np.array([matrix[1,0], matrix[0,1]])
