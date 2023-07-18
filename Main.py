from src.TerrainNavigator import Navigator
import timeit

full_start = timeit.default_timer()

referenceAltitude = 1

datapath = "../data/"
# referenceMap = "resized_inverted_image.png"
referenceMap = "random_circles_no_intersect.png"
referenceCatalogue = "finalReferenceCraterData"

# defaultDescentImages = ["Scene1.ppm", "Scene2.ppm", "Scene3.ppm", "Scene4.ppm"]
# defaultDescentImages = ["resized_inverted_image.png", "inverted_test_image.png"]
# defaultDescentImages = ["inverted_test_image.png"]
defaultDescentImages = ["cropped_image.png"]

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
for descentimage in defaultDescentImages:
	for i in range(1):
		navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
		print("-----------------------------------------------------")
		# input(" press enter ")

full_end = timeit.default_timer()

full_execution_time = full_end - full_start

print(f"Program executed in: {full_execution_time} seconds")