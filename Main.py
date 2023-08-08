from src.TerrainNavigator import Navigator
import timeit
import numpy as np
import cv2


# full_start = timeit.default_timer()


def plot_point_on_image(x, y, image):
	cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # Draws a red circle at (x, y)
	cv2.imshow('Image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def image_correction(pixel_delta_width, pixel_delta_height):
	# Load the new image
	image_path_2 = ('/Users/meha/PycharmProjects/Terrain-Relative-Navigation/data/TRN/referenceMap_large.png')
	img_2 = cv2.imread(image_path_2)
	gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

	img_h, img_w, img_c = img_2.shape

	x1, y1 = 0, 0
	x2, y2 = img_w, 0
	x3, y3 = 0, img_h
	x4, y4 = img_w, img_h

	pts_dst = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype='float32')

	# ------------------------------------------------ #
	# for i in range(0, 160):
	# pixel_delta_width = 30
	# pixel_delta_height = 20

	x1, y1 = pixel_delta_width, pixel_delta_height
	x2, y2 = img_w - pixel_delta_width, pixel_delta_height
	x3, y3 = pixel_delta_width, img_h - pixel_delta_height
	x4, y4 = img_w - pixel_delta_height, img_h - pixel_delta_height

	# plot_point_on_image(x1, y1, img_2)
	# plot_point_on_image(x2, y2, img_2)
	# plot_point_on_image(x3, y4, img_2)
	# plot_point_on_image(x4, y4, img_2)
	# Define coordinates of four corners in the destination image
	pts_src = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype='float32')

	# Compute the perspective transform matrix
	M = cv2.getPerspectiveTransform(pts_src, pts_dst)

	img_2_copy = img_2.copy()
	# Apply the perspective transformation
	img_transformed = cv2.warpPerspective(img_2_copy, M, (img_w, img_h))
	# cv2.imshow('Transformed Image', img_transformed)
	# cv2.waitKey()
	cv2.imwrite('/Users/meha/PycharmProjects/Terrain-Relative-Navigation/data/TRN/corrected_referenceMap_large.png',
	            img_transformed)
	print(" ----  IMAGE SAVED ---- ")
	cv2.destroyAllWindows()


## ----------------------------------------------------------------------

referenceAltitude = 1

datapath = "../data/"

pixel_delta_width = 20
pixel_delta_height = 30
# image_correction(pixel_delta_width, pixel_delta_height)

referenceMap = "resized_direct_ref_3.png"
referenceCatalogue = "finalReferenceCraterData"

defaultDescentImages = ["resized_local_1.png"]  # , "scene2.jpg", "scene3.jpg"]

navigator = Navigator(referenceAltitude, referenceMap, referenceCatalogue, datapath)
for descentimage in defaultDescentImages:
	navigator.locateDescentImageInReferenceImage(datapath + "TRN/" + descentimage)
	print("-----------------------------------------------------")
# input(" press enter ")
