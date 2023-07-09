from src.TerrainNavigator import Navigator

referenceAltitude = 2500 #2000

datapath = "../data/"
referenceMap = "ReferenceMap.ppm"
referenceCatalogue = "finalReferenceCraterData"

# defaultDescentImages = ["Scene1.ppm", "Scene2.ppm", "Scene3.ppm", "Scene4.ppm"]
defaultDescentImages = ["Scene1.ppm"]

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
for descentimage in defaultDescentImages:
	navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
