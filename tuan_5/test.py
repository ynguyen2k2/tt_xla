import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Load the image using any suitable method (e.g., PIL, OpenCV, scikit-image)
image = plt.imread("D:\\Desktop\\tt_xla\\git\\tt_xla\\tuan_5\\image\\image.jpg")

# Perform any necessary preprocessing on the image if required

# Convert the image to grayscale if needed
grayscale_image = np.mean(image, axis=2)

# Threshold the image to obtain a binary representation
threshold = 0.5
binary_image = np.where(grayscale_image > threshold, 1, 0)

# Label connected regions in the binary image
labeled_array, num_labels = ndimage.label(binary_image)

# Find the bounding boxes of the connected regions
slices = ndimage.find_objects(labeled_array)

# Create a figure and axis
fig, ax = plt.subplots()

# Display the image
ax.imshow(image)

# Draw bounding boxes on the image
for label_slice in slices:
    bboxx = label_slice[0]
    bboxy = label_slice[1]
    print(label_slice[0],label_slice[1])

    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                         linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)


# Show the image with bounding boxes
plt.show()