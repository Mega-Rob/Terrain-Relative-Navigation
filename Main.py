from src.TerrainNavigator import Navigator

referenceAltitude = 2000 #2000

datapath = "../data/"
referenceMap = "resized_inverted_image.png"
referenceCatalogue = "finalReferenceCraterData"

# defaultDescentImages = ["Scene1.ppm", "Scene2.ppm", "Scene3.ppm", "Scene4.ppm"]
# defaultDescentImages = ["resized_inverted_image.png", "inverted_test_image.png"]
defaultDescentImages = ["inverted_test_image.png"]

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
for descentimage in defaultDescentImages:
	navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
