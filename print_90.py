import cv2
import xml.etree.ElementTree as ET
import os

# Base filename (without extension) for the image and XML annotation
img_name = "1170"

# Directory where the input images and XML annotation files are located
img_dir = "sticky_dataset/stickytraps"

# Directory where the annotated preview image will be saved
output_dir = "images"

# Create the output directory if it does not already exist
os.makedirs(output_dir, exist_ok=True)

# Full file paths for the input image, annotation, and output image
image_path = os.path.join(img_dir, f"{img_name}.jpg")
xml_path = os.path.join(img_dir, f"{img_name}.xml")
output_path = os.path.join(output_dir, f"{img_name}_rotated_annotated.jpg")

# Load the image using OpenCV
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

# Rotate the image 90 degrees counter-clockwise (to demonstrate annotation mismatch)
image_rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
h, w = image_rotated.shape[:2]
print(f"[INFO] Rotated image size: {w}x{h}")

# Parse the XML annotation file (Pascal VOC format)
tree = ET.parse(xml_path)
root = tree.getroot()

# Draw bounding boxes from the original annotation (assuming landscape orientation)
for obj in root.findall('object'):
    name = obj.find('name').text  # Class label for the object (e.g., insect type)
    bbox = obj.find('bndbox')
    xmin = int(float(bbox.find('xmin').text))
    ymin = int(float(bbox.find('ymin').text))
    xmax = int(float(bbox.find('xmax').text))
    ymax = int(float(bbox.find('ymax').text))

    # These boxes will appear in the wrong place due to the rotation (for demonstration)
    cv2.rectangle(image_rotated, (xmin, ymin), (xmax, ymax), (0, 0, 255), 5)
    cv2.putText(image_rotated, name, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

# Save the rotated and annotated image to the output directory
cv2.imwrite(output_path, image_rotated)
print(f"[INFO] Preview saved to: {output_path}")
