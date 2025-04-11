import cv2
import numpy as np

# Create a test image
img = np.zeros((480, 640, 3), dtype=np.uint8)

# Draw some shapes
cv2.rectangle(img, (100, 100), (540, 380), (0, 255, 0), -1)
cv2.circle(img, (320, 240), 100, (0, 0, 255), -1)
cv2.putText(img, "Test Image", (220, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Save the image
cv2.imwrite('test.jpg', img)
print("Test image created: test.jpg")
