import cv2
from matplotlib import pyplot as plt
import numpy as np

# Load the new image
new_image_path = '/Users/meha/Downloads/66467659-rocky-beach-with-sand-and-pebbles.jpg'
new_image = cv2.imread(new_image_path)

if new_image is None:
	print(f"Failed to load image at {new_image_path}")
else:
	# Convert the image to HSV color space
	hsv_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2HSV)

	# Define range of sand color in HSV
	lower_sand = np.array([10, 100, 20])
	upper_sand = np.array([25, 255, 255])

	# Threshold the HSV image to get only sand colors
	sand_mask = cv2.inRange(hsv_image, lower_sand, upper_sand)

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(new_image, new_image, mask=sand_mask)

	# Invert the mask to get the non-sand parts
	non_sand_mask = cv2.bitwise_not(sand_mask)
	non_sand = cv2.bitwise_and(new_image, new_image, mask=non_sand_mask)

	# Convert the new image to RGB (from BGR)
	non_sand_rgb = cv2.cvtColor(non_sand, cv2.COLOR_BGR2RGB)

	# Plotting the original image and the image without sand
	fig, axs = plt.subplots(1, 2, figsize=(15, 15))

	# Display the images
	axs[0].imshow(new_image)
	axs[0].set_title('Original Image')
	axs[0].axis('off')

	axs[1].imshow(non_sand_rgb)
	axs[1].set_title('Image without Sand')
	axs[1].axis('off')

	plt.show()
