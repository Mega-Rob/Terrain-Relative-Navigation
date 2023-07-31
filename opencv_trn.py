import cv2
import numpy as np

local_image = cv2.imread('local_image.png')

reference_image = cv2.imread('reference_image.png')

# reference_image_calibrated = reference_image.copy()
pts_src_perspective = np.array([[50, 0], [600, 0], [0, 480], [640, 480]], dtype='float32')
pts_dst_perspective = np.array([[0, 0], [511, 0], [0, 511], [511, 511]], dtype='float32')
M_perspective = cv2.getPerspectiveTransform(pts_src_perspective, pts_dst_perspective)
reference_image_calibrated = cv2.warpPerspective(reference_image, M_perspective, (512, 512))

