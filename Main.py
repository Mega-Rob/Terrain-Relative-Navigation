from src.TerrainNavigator import Navigator
import timeit
import numpy as np
import cv2

# full_start = timeit.default_timer()

referenceAltitude = 2000

datapath = "../data/"

referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCraterData"

# defaultDescentImages = ["scene1_resized.jpg", "scene2_resized.jpg", "scene3_resized.jpg"]
defaultDescentImages = ["scene1.ppm"]  # , "scene2.jpg", "scene3.jpg"]

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
for descentimage in defaultDescentImages:
	navigator.locateDescentImageInReferenceImage(datapath + "TRN/Old/" + descentimage)
	print("-----------------------------------------------------")
	# input(" press enter ")

# full_end = timeit.default_timer()

# full_execution_time = full_end - full_start

# print(f"Program executed in: {full_execution_time} seconds")
