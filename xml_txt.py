import os
import cv2
import xml.etree.ElementTree as ET

# Class and abbreviation map
ABBR_TO_CLASS = {
    "WF": "Whitefly",
    "MR": "Macrolophus",
    "NC": "Nesidiocoris",
    "TR": "Thysanoptera"  # Opcional, pode pular esses se quiser
}
CLASSES = ["Macrolophus", "Nesidiocoris", "Whitefly", "Thysanoptera"]

def voc_xml_to_yolo_txt(img_path, xml_path, txt_path=None, verbose=True):
    if txt_path is None:
        txt_path = os.path.splitext(img_path)[0] + ".txt"
    img = cv2.imread(img_path)
    if img is None:
        if verbose:
            print(f"[WARN] Image not found: {img_path}")
        return False
    img_h, img_w = img.shape[:2]
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        if verbose:
            print(f"[WARN] Failed to parse XML: {xml_path}: {e}")
        return False

    yolo_lines = []
    for obj in root.findall("object"):
        abbr = obj.find("name").text
        if abbr not in ABBR_TO_CLASS:
            if verbose:
                print(f"[SKIP] Unknown class '{abbr}' in {xml_path}")
            continue
        cls = ABBR_TO_CLASS[abbr]
        cls_id = CLASSES.index(cls)
        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)
        xmin = max(0, min(xmin, img_w-1))
        xmax = max(0, min(xmax, img_w-1))
        ymin = max(0, min(ymin, img_h-1))
        ymax = max(0, min(ymax, img_h-1))
        cx = ((xmin + xmax) / 2) / img_w
        cy = ((ymin + ymax) / 2) / img_h
        bw = (xmax - xmin) / img_w
        bh = (ymax - ymin) / img_h
        if not (0 <= cx <= 1 and 0 <= cy <= 1 and 0 <= bw <= 1 and 0 <= bh <= 1):
            if verbose:
                print(f"[SKIP] Out-of-bounds bbox in {xml_path}: {cx}, {cy}, {bw}, {bh}")
            continue
        yolo_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

    if yolo_lines:
        with open(txt_path, "w") as f:
            f.write("\n".join(yolo_lines))
        if verbose:
            print(f"[OK] {txt_path} ({len(yolo_lines)} objects)")
        return True
    else:
        if verbose:
            print(f"[EMPTY] No valid objects in {xml_path}")
        return False

# --------- Loop to process the whole folder --------------

DATASET_DIR = "sticky_dataset/stickytraps"
files = os.listdir(DATASET_DIR)
images = [f for f in files if f.lower().endswith(".jpg")]

count_success = 0
count_empty = 0
count_failed = 0

for img_file in images:
    img_path = os.path.join(DATASET_DIR, img_file)
    xml_path = os.path.splitext(img_path)[0] + ".xml"
    if os.path.exists(xml_path):
        result = voc_xml_to_yolo_txt(img_path, xml_path)
        if result:
            count_success += 1
        else:
            count_empty += 1
    else:
        print(f"[WARN] No XML found for image: {img_path}")
        count_failed += 1

print(f"\nDone! Converted {count_success} files. {count_empty} had no valid objects. {count_failed} images had no XML.")

