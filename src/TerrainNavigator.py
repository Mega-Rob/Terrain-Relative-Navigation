import random
from PIL import Image

import numpy as np
from PIL import ImageDraw

import src.Preprocessor as preprocessor
import src.CraterDetector as craterDetector


class Navigator:
    def __init__(self, referenceAltitude, referenceMap, datapath):
        """
        Initializes an instance of Navigator object which preprocesses the referenceMap automatically.
        By creating a Navigator object once, it makes it possible to detect consecutive images without
        preprocessing it.
        :param referenceAltitude: The altitude at which the reference image is given
        :param referenceMap: The name of the reference map.
        """
        self.datapath = datapath
        self.referenceAltitude = referenceAltitude
        self.referenceMap = referenceMap
        self.descent_im = None

    def oneCombinationUnitVector(self, point, centerpoints):
        """
        Takes one point in a given list of points and calculates all the unit vectors to the other centerpoints
        in the list.
        This method is only to be accessed by methods in this module and not intended to be accessed arbitrarily.
        :param point: point from where all the other relative positions should be calculated
        :param centerpoints: list of all the centerpoints that needs to be processed.
        :return: unit vectors every other centerpoint of craters in the image.
        """
        unitvectors = []
        for (k2, point2) in centerpoints.items():
            if (point[0] == point2[0] and point[1] == point2[1]):
                continue
            else:
                vect = (point2 - point) / np.linalg.norm(point2 - point)
                unitvectors.append(vect)
        return unitvectors

    def drawDescentImageOnReferenceImage(self, upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint, middlepoint, foundreferencecraters, referenceCenterPoints):
        """
        Draws the specified coordinates of the landers location on to the reference map.
        This method is only to be accessed by methods in this module and not intended to be accessed arbitrarily.
        :param upperleftpoint: upperleft point in the reference image
        :param upperrightpoint: upperright point in the reference image
        :param lowerleftpoint: lowerleft point in the reference image
        :param lowerrightpoint: lower right point in reference
        :param middlepoint: Exact location of the lander on the reference image.
        :return: Null
        """
        refimage = Image.open(self.datapath + "TRN/" + self.referenceMap)
        # font = ImageFont.truetype("sans-serif.ttf", 14)
        draw = ImageDraw.Draw(refimage)
        draw.line((upperleftpoint[0], upperleftpoint[1], upperrightpoint[0], upperrightpoint[1]), fill='#31ff00', width=2)
        draw.line((upperleftpoint[0], upperleftpoint[1], lowerleftpoint[0], lowerleftpoint[1]), fill='#31ff00', width=2)
        draw.line((lowerleftpoint[0], lowerleftpoint[1], lowerrightpoint[0], lowerrightpoint[1]), fill='#31ff00', width=2)
        draw.line((lowerrightpoint[0], lowerrightpoint[1], upperrightpoint[0], upperrightpoint[1]), fill='#31ff00', width=2)
        draw.line((middlepoint[0], middlepoint[1]-1, middlepoint[0], middlepoint[1]+1), fill='#31ff00', width=12)
        draw.line((middlepoint[0]-1, middlepoint[1], middlepoint[0]+1, middlepoint[1]), fill='#31ff00', width=12)
        for crater in foundreferencecraters:
            draw.line((crater[1], crater[0] - 3, crater[1], crater[0] + 3), fill='#0800ff',
                      width=15)
            draw.line((crater[1] - 3, crater[0], crater[1] + 3, crater[0]), fill='#0800ff',
                      width=15)
        for ref_crater in referenceCenterPoints.values():
            draw.line((ref_crater[1], ref_crater[0] - 1, ref_crater[1], ref_crater[0] + 1), fill='#ff0000',
                      width=12)
            draw.line((ref_crater[1] - 1, ref_crater[0], ref_crater[1] + 1, ref_crater[0]), fill='#ff0000',
                      width=12)

        refimage.show()

    def executePatternRecognition(self, allPossibleCombinations, referenceCraters, descentImageCraters):
        """
        This part actually executes the pattern recognition on the reference map.
        This method is only to be accessed by methods in this module and not intended to be accessed arbitrarily.
        :param allPossibleCombinations: Dictionary of all craters containing the relative distances to every other crater on the image
        :param referenceCraters: centerpoint are the catalogued centerpoints of all the craters in the reference map
        :param descentImageCraters: list of all the crater centerpoints and diameters in the descent image.
        :return: The approximate location of the lander on top of the referenceMap.
        """
        referenceCenterPoints = preprocessor.extractCenterpoints(referenceCraters)
        descentImageCenterPoints = preprocessor.extractCenterpoints(descentImageCraters)
        verificationcraters = random.sample(list(descentImageCraters.items()), 3)

        print("Reference centre points")
        print(referenceCenterPoints)
        print("\n")
        print("Descent image centre points")
        print(descentImageCenterPoints)
        print("\n")
        print("verification craters")
        print(verificationcraters)
        print("\n")

        foundreferencecraters = []
        scale = 0
        # add counter to account for number of craters exploited
        crater_counter = 0
        for descentkey, crater in verificationcraters:
            smallSet = self.oneCombinationUnitVector(crater.centerpoint, descentImageCenterPoints)
            for (referencekey, values) in allPossibleCombinations.items():
                if (self.isSubsetOf(smallSet, values, 0.2)):
                    foundreferencecraters.append(referenceCenterPoints[referencekey])
                    scale = scale + descentImageCraters[descentkey].diameter/referenceCraters[referencekey].diameter
                    crater_counter += 1
                    break

        if crater_counter == 0:
            print("NO IDENTIFICATION")
            return None
        s = 1.75
        print("scale : ", s)
        print("\n")
        print("found reference craters")
        print(foundreferencecraters)
        lowerleftpoint, lowerrightpoint,  upperleftpoint, upperrightpoint = self.findViewingRectangle(
            foundreferencecraters, s, verificationcraters)
        middlepoint = (upperleftpoint + lowerleftpoint + upperrightpoint + lowerrightpoint) / 4
        print("centre point : ", middlepoint)
        self.drawDescentImageOnReferenceImage(upperleftpoint, upperrightpoint, lowerleftpoint, lowerrightpoint,
                                                  middlepoint, foundreferencecraters, referenceCenterPoints)
        return middlepoint

    def findViewingRectangle(self, foundreferencecraters, s, verificationcraters):
        """
        Method for finding the drawing rectangle.
        :param foundreferencecraters:
        :param s:
        :param verificationcraters:
        :return:
        """
        upperleftpoint = np.array([0, 0])
        lowerrightpoint = np.array([0, 0])
        upperrightpoint = np.array([0, 0])
        lowerleftpoint = np.array([0, 0])
        nbr_found_ref_craters = len(foundreferencecraters)
        x_img = self.descent_im.size[0]
        y_img = self.descent_im.size[1]
        for i in range(nbr_found_ref_craters):
            verificationcrater = verificationcraters[i][1].centerpoint
            referencecrater = foundreferencecraters[i]
            r = np.array([referencecrater[0], referencecrater[1]])
            v = np.array([verificationcrater[0], verificationcrater[1]])

            upperleftpoint = upperleftpoint + (r - (v / s))
            lowerrightpoint = lowerrightpoint + [r[0] + (x_img - v[0]) / s, r[1] + (y_img - v[1]) / s]
            upperrightpoint = upperrightpoint + [r[0] + (x_img - v[0]) / s, r[1] - v[1] / s]
            lowerleftpoint = lowerleftpoint + [r[0] - v[0] / s, r[1] + (y_img - v[1]) / s]
        upperrightpoint = upperrightpoint/nbr_found_ref_craters
        lowerrightpoint = lowerrightpoint/nbr_found_ref_craters
        upperleftpoint = upperleftpoint/nbr_found_ref_craters
        lowerleftpoint = lowerleftpoint/nbr_found_ref_craters
        return lowerleftpoint, lowerrightpoint, upperleftpoint, upperrightpoint

    def isSubsetOf(self, smallSet, values, threshold):
        """
        Evaluates whether a smaller set of unit vectors is a subset of a larger set. It does this by allowing a certain error,
        as the unit vectors in a reference image may not be exactly the same as in the detected image.
        This method is only to be accessed by methods in this module and not intended to be accessed arbitrarily.
        :param smallSet: Set containing unit vectors of a certain crater in the descent image.
        :param values: Set containing unit vectors of a certain crater in the reference image.
        :param threshold: Error factor that can be tolerated. If the error is higher than this, the vectors are not the same.
        :return: If the smaller set is identified to be a subset of the larger set, it returns true, else it returns false.
        """
        matchesfound = 0
        for vector in smallSet:
            vectorequal = False
            for refvector in values:
                if (self.isAlmostEquals(vector, refvector, threshold)):
                    vectorequal = True
                    matchesfound += 1
                    break
            if not(vectorequal):
                break
        if (matchesfound == len(smallSet)):
            return True
        else:
            return False

    def isAlmostEquals(self, vector, refvector, threshold):
        """
        Compares 2 different unit vector to verify whether they have almost the same direction. This is done by including
        a small error factor which allows for flexibility.
        This method is only to be accessed by methods in this module and not intended to be accessed arbitrarily.
        :param vector: First vector to be compared.
        :param refvector: Second vector with which the first vector is compared to check for equality.
        :param threshold: Error factor that can be tolerated. If the error is higher than this, the vectors are not the same.
        :return: If the smaller set is identified to be a subset of the larger set, it returns true, else it returns false.
        """
        if (((vector[0] - threshold < refvector[0]) and (vector[0] + threshold > refvector[0])) and
                ((vector[1] - threshold < refvector[1]) and (vector[1] + threshold > refvector[1]))
            ): return True
        else: return False

    def locateDescentImageInReferenceImage(self, imagename):
        """
        This method uses the preprocessed referencemap to locate the descent image. It provides the coordinates
        and altitude on the image produced.
        :param imagename: the descent image which needs to be located in the reference map.
        :return: None
        """

        # Reference Image
        print("reference image")
        im_ref = Image.open(self.datapath + "TRN/" + self.referenceMap)
        refImageCraters = craterDetector.extractCraters(im_ref)
        print(refImageCraters)
        allPossibleCombinations = preprocessor.preprocessReferenceImage(refImageCraters)
        print("descent image")

        # Local image
        im = Image.open(imagename)
        self.descent_im = im
        descentImageCraters = craterDetector.extractCraters(im)
        print("descent image craters")
        print("------------------")
        self.executePatternRecognition(allPossibleCombinations, refImageCraters, descentImageCraters)
