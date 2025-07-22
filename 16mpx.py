import os
import shutil
import random
import yaml

# CONFIGURATION
SRC_DIR = "sticky_dataset/stickytraps"
DST_DIR = "sticky_dataset/16mpx"
DST_IMG_TRAIN = os.path.join(DST_DIR, "images/train")
DST_IMG_VAL   = os.path.join(DST_DIR, "images/val")
DST_LABEL_TRAIN = os.path.join(DST_DIR, "labels/train")
DST_LABEL_VAL   = os.path.join(DST_DIR, "labels/val")
YAML_PATH = os.path.join(DST_DIR, "dataset.yaml")
CLASSES = ["Macrolophus", "Nesidiocoris", "Whitefly"]  # adapte se mudar as classes
SPLIT_RATIO = 0.8  # 80% train

# Ensure output folders exist
os.makedirs(DST_IMG_TRAIN, exist_ok=True)
os.makedirs(DST_IMG_VAL, exist_ok=True)
os.makedirs(DST_LABEL_TRAIN, exist_ok=True)
os.makedirs(DST_LABEL_VAL, exist_ok=True)

# Get all jpgs from SRC_DIR
all_imgs = [f for f in os.listdir(SRC_DIR) if f.lower().endswith(".jpg")]
random.shuffle(all_imgs)

n_train = int(len(all_imgs) * SPLIT_RATIO)
train_imgs = all_imgs[:n_train]
val_imgs = all_imgs[n_train:]

for img_set, img_list, dst_img_dir, dst_label_dir in [
    ('train', train_imgs, DST_IMG_TRAIN, DST_LABEL_TRAIN),
    ('val', val_imgs, DST_IMG_VAL, DST_LABEL_VAL),
]:
    for img_file in img_list:
        src_img_path = os.path.join(SRC_DIR, img_file)
        label_file = os.path.splitext(img_file)[0] + ".txt"
        src_label_path = os.path.join(SRC_DIR, label_file)

        # Copy image
        shutil.copy2(src_img_path, os.path.join(dst_img_dir, img_file))

        # Copy label if exists
        if os.path.exists(src_label_path):
            shutil.copy2(src_label_path, os.path.join(dst_label_dir, label_file))
        else:
            print(f"[WARN] No label for {img_file}")

    print(f"{img_set}: {len(img_list)} images/labels")

# Create dataset.yaml
yaml_dict = {
    "train": os.path.abspath(DST_IMG_TRAIN),
    "val": os.path.abspath(DST_IMG_VAL),
    "nc": len(CLASSES),
    "names": CLASSES
}

with open(YAML_PATH, "w") as f:
    yaml.dump(yaml_dict, f, sort_keys=False)

print(f"\n✅ Dataset split, organized and YAML file '{YAML_PATH}' created for YOLO training!")
