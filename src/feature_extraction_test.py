import cv2
import numpy as np

# Load the image
img = cv2.imread('/Users/meha/PycharmProjects/Terrain-Relative-Navigation/data/TRN/Image2.jpeg')

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Use thresholding to create binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# For each contour, find the minimum enclosing circle
for cnt in contours:
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)

    # If the radius meets a certain criteria (e.g. larger than 10), draw the circle
    if radius > 100:
        cv2.circle(img, center, radius, (0, 255, 0), 2)

# Display the image with detected objects
cv2.imshow('Object Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
