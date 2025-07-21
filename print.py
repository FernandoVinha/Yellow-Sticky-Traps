import cv2
import xml.etree.ElementTree as ET
import os

# Base filename (without extension)
img_name = "1000"

# Input directories for images and XML files
img_dir = "sticky_dataset/stickytraps"
xml_dir = "sticky_dataset/stickytraps"

# Output directory for the annotated preview images
output_dir = "images"

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Build full paths for input image, XML annotation, and output preview image
image_path = os.path.join(img_dir, f"{img_name}.jpg")
xml_path = os.path.join(xml_dir, f"{img_name}.xml")
output_path = os.path.join(output_dir, f"{img_name}_preview.jpg")

# Load the image using OpenCV
image = cv2.imread(image_path)
if image is None:
    print(f"[ERROR] Failed to open image: {image_path}")
    exit(1)
h, w = image.shape[:2]
print(f"[INFO] Image resolution: {w}x{h}")

# Parse the XML annotation file (Pascal VOC format)
tree = ET.parse(xml_path)
root = tree.getroot()

# Iterate through all annotated objects in the XML file
for obj in root.findall('object'):
    name = obj.find('name').text  # Class label for the object (e.g., insect type)
    bbox = obj.find('bndbox')
    # Extract bounding box coordinates and convert to integers
    xmin = int(float(bbox.find('xmin').text))
    ymin = int(float(bbox.find('ymin').text))
    xmax = int(float(bbox.find('xmax').text))
    ymax = int(float(bbox.find('ymax').text))

    # Draw a rectangle for the bounding box (in red)
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 4)
    # Put the class name above the bounding box (in green)
    cv2.putText(image, name, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

# Save the annotated image to the output directory
cv2.imwrite(output_path, image)
print(f"[INFO] Preview saved to: {output_path}")
