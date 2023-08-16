from src.TerrainNavigator import Navigator

referenceAltitude = 1

datapath = "../data/"

pixel_delta_width = 20
pixel_delta_height = 30

referenceMap = "resized_direct_ref_3.png"

defaultDescentImages = ["resized_local_1.png"]  # , "scene2.jpg", "scene3.jpg"]

navigator = Navigator(referenceAltitude, referenceMap, datapath)
for descentimage in defaultDescentImages:
	navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
	print("-----------------------------------------------------")

