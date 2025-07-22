import os
import cv2
import numpy as np
import random
import shutil

base_dir = "sticky_dataset/120px"
splits = ["train", "val"]
angles = [90, 180, 270]

def adjust_brightness(img, max_dark=0.2):
    factor = 1.0 - random.uniform(0, max_dark)
    return np.clip(img * factor, 0, 255).astype(np.uint8)

def rotate_bbox_yolo(xc, yc, w, h, angle_deg):
    if angle_deg == 90:
        return yc, 1 - xc, h, w
    elif angle_deg == 180:
        return 1 - xc, 1 - yc, w, h
    elif angle_deg == 270:
        return 1 - yc, xc, h, w
    else:
        return xc, yc, w, h

for split in splits:
    input_img_dir = os.path.join(base_dir, split, "images")
    input_lbl_dir = os.path.join(base_dir, split, "labels")
    output_img_dir = os.path.join(base_dir, split, "images")
    output_lbl_dir = os.path.join(base_dir, split, "labels")
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_lbl_dir, exist_ok=True)

    for fname in os.listdir(input_img_dir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img_path = os.path.join(input_img_dir, fname)
        lbl_path = os.path.join(input_lbl_dir, fname.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt'))
        if not os.path.exists(lbl_path):
            print(f"⚠️ Label not found for {fname}, skipping.")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ Error reading image: {img_path}")
            continue
        h, w = img.shape[:2]
        base, ext = os.path.splitext(fname)

        # Copy original (comment out if you don't want to duplicate)
        shutil.copy(img_path, os.path.join(output_img_dir, f"{base}_orig{ext}"))
        shutil.copy(lbl_path, os.path.join(output_lbl_dir, f"{base}_orig.txt"))

        # Load labels
        with open(lbl_path) as f:
            lines = f.readlines()

        for angle in angles:
            # Rotate image
            if angle == 90:
                rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            elif angle == 180:
                rotated_img = cv2.rotate(img, cv2.ROTATE_180)
            elif angle == 270:
                rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                continue

            # Rotate bounding boxes
            rotated_labels = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls, xc, yc, bw, bh = parts
                xc, yc, bw, bh = map(float, (xc, yc, bw, bh))
                rxc, ryc, rbw, rbh = rotate_bbox_yolo(xc, yc, bw, bh, angle)
                rxc, ryc, rbw, rbh = [min(max(v, 0), 1) for v in (rxc, ryc, rbw, rbh)]
                rotated_labels.append(f"{cls} {rxc:.6f} {ryc:.6f} {rbw:.6f} {rbh:.6f}")

            # 50% chance to darken
            if random.random() < 0.5:
                out_img = adjust_brightness(rotated_img)
                suffix = f"{angle}_dark"
            else:
                out_img = rotated_img
                suffix = f"{angle}"

            out_img_name = f"{base}_rot{suffix}{ext}"
            out_lbl_name = f"{base}_rot{suffix}.txt"
            cv2.imwrite(os.path.join(output_img_dir, out_img_name), out_img)
            with open(os.path.join(output_lbl_dir, out_lbl_name), "w") as fout:
                fout.write("\n".join(rotated_labels) + "\n")

print("✅ Augmentation completed for train and val!")