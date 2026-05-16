from image_processor import ImageProcessor
import cv2


processor = ImageProcessor()

image = processor.load_image(
    "sample.jpg"
)

modified = processor.generate_differences(
    image
)

cv2.imshow(
    "Original Image",
    image
)

cv2.imshow(
    "Modified Image",
    modified
)

cv2.waitKey(0)
cv2.destroyAllWindows()