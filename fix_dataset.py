import os
import cv2

"""
This script processes all .jpg images in a given dataset directory.
It checks if each image is in portrait mode (height > width).
If so, it rotates the image 90 degrees counterclockwise to convert it to landscape mode.
Images already in landscape mode are left unchanged.
A summary of how many images were rotated is printed at the end.

Useful for standardizing your dataset for computer vision or deep learning tasks!
"""

# Path to the dataset folder
dataset_dir = "sticky_dataset/stickytraps"

# Counter for rotated images
rotated_count = 0

# Loop through all .jpg files in the folder
for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(".jpg"):
        image_path = os.path.join(dataset_dir, filename)

        # Load image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"[❌] Failed to load image: {filename}")
            continue

        # Get image dimensions: height (h), width (w)
        h, w = image.shape[:2]

        if h > w:
            # Portrait mode detected – rotate to landscape
            rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(image_path, rotated)  # Overwrite the original file
            rotated_count += 1
            print(f"[🔁] Rotated to landscape: {filename}")
        else:
            print(f"[✅] Already in landscape: {filename}")

print(f"\n✅ Finished: {rotated_count} images were rotated to landscape.")
