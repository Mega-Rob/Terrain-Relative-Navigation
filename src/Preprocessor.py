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
        allcombinationnormvectors[k] = []
        for (k2, point2) in centerpoints.items():
            if point[0] == point2[0] and point[1] == point2[1]:
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                allcombinationnormvectors[k].append(vect)
    return allcombinationnormvectors


def preprocessReferenceImage(refImageCraters):
    """
    Loads data from a given catalogue file and computes the combinations of unit vectors of each crater.
    :param catalogue: String indicating which file to load the data catalogue from.
    :param combinations: String to store the found combinations in.
    :return: None
    """
    referenceCatalogueCenterpoints = extractCenterpoints(refImageCraters)
    centerpoints = {}
    for k, v in referenceCatalogueCenterpoints.items():
        centerpoints[k] = v
    allPossibleCombinations = allCombinationNormVectors(centerpoints)
    return allPossibleCombinations
    # viewer.saveData(datapath, allPossibleCombinations, combinations)


def extractCenterpoints(craters):
    centerpoints = {}
    list(map(lambda item: centerpoints.update({item[0]: item[1].centerpoint}), craters.items()))
    return centerpoints
