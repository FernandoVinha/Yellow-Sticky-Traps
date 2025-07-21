import os
import cv2
import xml.etree.ElementTree as ET
import random
import yaml

# Main configuration
DATASET_DIR = "sticky_dataset"
SRC_IMG_DIR = os.path.join(DATASET_DIR, "stickytraps")
SRC_XML_DIR = os.path.join(DATASET_DIR, "stickytraps")
# Abbreviation mapping as found in your XML files
ABBR_TO_CLASS = {
    "WF": "Whitefly",
    "TH": "Thysanoptera",
    "MA": "Macrolophus",
    "NE": "Nesidiocoris"
}
CLASSES = ["Macrolophus", "Nesidiocoris", "Whitefly", "Thysanoptera"]
SPLIT_RATIO = 0.8  # 80% train, 20% val

# Target resolutions: (folder_name, target_area_in_pixels)
TARGETS = [
    ("16mpx", None),        # Original, no resizing
    ("5mpx", 5_000_000),    # ~5 megapixels
    ("2mpx", 2_000_000),    # ~2 megapixels
]

def area_resize(image, target_area):
    """Resize image to the target area (pixels), only if larger. Keep original if smaller."""
    h, w = image.shape[:2]
    area = h * w
    if target_area is None or area <= target_area:
        return image.copy()
    scale = (target_area / area) ** 0.5
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

# Collect all original images
img_files = [f for f in os.listdir(SRC_IMG_DIR) if f.lower().endswith(".jpg")]
img_files.sort()
random.shuffle(img_files)
n_train = int(len(img_files) * SPLIT_RATIO)
train_imgs = img_files[:n_train]
val_imgs = img_files[n_train:]
splits = [("train", train_imgs), ("val", val_imgs)]

for set_name, area in TARGETS:
    print(f"\n=== Processing set: {set_name} ===")
    # Paths for the YAML config
    yaml_path = os.path.join(DATASET_DIR, set_name, "dataset.yaml")
    rel_img_dir = f"{set_name}/images"
    abs_set_dir = os.path.join(DATASET_DIR, set_name)

    # Prepare split dirs for images and labels
    for split, split_imgs in splits:
        img_out_dir = os.path.join(DATASET_DIR, set_name, "images", split)
        label_out_dir = os.path.join(DATASET_DIR, set_name, "labels", split)
        os.makedirs(img_out_dir, exist_ok=True)
        os.makedirs(label_out_dir, exist_ok=True)

        for img_name in split_imgs:
            src_img_path = os.path.join(SRC_IMG_DIR, img_name)
            xml_path = os.path.join(SRC_XML_DIR, img_name.replace(".jpg", ".xml"))
            out_img_path = os.path.join(img_out_dir, img_name)
            out_txt_path = os.path.join(label_out_dir, img_name.replace(".jpg", ".txt"))

            # Load the original image
            img = cv2.imread(src_img_path)
            if img is None:
                print(f"[WARN] Image not found: {src_img_path}")
                continue

            # Resize if necessary
            img_out = area_resize(img, area)
            cv2.imwrite(out_img_path, img_out)
            img_h, img_w = img_out.shape[:2]

            # Check if XML exists
            if not os.path.exists(xml_path):
                print(f"[WARN] XML not found for: {img_name}")
                continue

            # Parse XML to get original bboxes
            tree = ET.parse(xml_path)
            root = tree.getroot()
            size_tag = root.find("size")
            orig_w = int(size_tag.find("width").text)
            orig_h = int(size_tag.find("height").text)
            scale_x = img_w / orig_w
            scale_y = img_h / orig_h

            yolo_lines = []
            for obj in root.findall("object"):
                abbr = obj.find("name").text
                if abbr not in ABBR_TO_CLASS:
                    print(f"[WARN] Unknown class abbreviation '{abbr}' in {xml_path}")
                    continue
                cls = ABBR_TO_CLASS[abbr]
                cls_id = CLASSES.index(cls)
                bndbox = obj.find("bndbox")
                xmin = float(bndbox.find("xmin").text)
                ymin = float(bndbox.find("ymin").text)
                xmax = float(bndbox.find("xmax").text)
                ymax = float(bndbox.find("ymax").text)

                # Scale bboxes for new dimensions
                xmin_s = xmin * scale_x
                xmax_s = xmax * scale_x
                ymin_s = ymin * scale_y
                ymax_s = ymax * scale_y

                # YOLO format: cx, cy, w, h (normalized)
                cx = ((xmin_s + xmax_s) / 2) / img_w
                cy = ((ymin_s + ymax_s) / 2) / img_h
                bw = (xmax_s - xmin_s) / img_w
                bh = (ymax_s - ymin_s) / img_h

                yolo_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

            # Write YOLO annotation file
            with open(out_txt_path, "w") as f:
                f.write("\n".join(yolo_lines))
            print(f"[{set_name}][{split.upper()}] {img_name}: {len(yolo_lines)} objects")

    # After images and labels, create the dataset.yaml for this set
    yaml_dict = {
        "train": os.path.abspath(os.path.join(abs_set_dir, "images/train")),
        "val": os.path.abspath(os.path.join(abs_set_dir, "images/val")),
        "nc": len(CLASSES),
        "names": CLASSES
    }
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_dict, f, sort_keys=False)
    print(f"[YAML] Created {yaml_path}")

print("\n✅ Resizing, splitting, YOLO conversion, and YAML creation complete!")
