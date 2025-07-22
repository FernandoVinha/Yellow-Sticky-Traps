import os
import cv2

dataset_base = "sticky_dataset/5mpx"
output_base = "sticky_dataset/120px"
splits = ["train", "val"]
crop_size = 120

for split in splits:
    img_dir = os.path.join(dataset_base, "images", split)
    label_dir = os.path.join(dataset_base, "labels", split)
    out_img_dir = os.path.join(output_base, split, "images")
    out_label_dir = os.path.join(output_base, split, "labels")
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_label_dir, exist_ok=True)

    img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"\n[{split}] Encontradas {len(img_files)} imagens em {img_dir}")

    for img_file in img_files:
        name = os.path.splitext(img_file)[0]
        img_path = os.path.join(img_dir, img_file)
        label_path = os.path.join(label_dir, name + ".txt")

        if not os.path.exists(label_path):
            print(f"Label não encontrado para: {img_file}")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"Erro ao ler imagem: {img_path}")
            continue
        h, w = img.shape[:2]

        with open(label_path) as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) < 5:
                print(f"Linha inválida em {label_path}: {line}")
                continue
            class_id, x_center, y_center, bbox_w, bbox_h = map(float, parts)
            xc = x_center * w
            yc = y_center * h
            bw = bbox_w * w
            bh = bbox_h * h

            x1 = int(round(xc - crop_size/2))
            y1 = int(round(yc - crop_size/2))
            x1 = max(0, min(w - crop_size, x1))
            y1 = max(0, min(h - crop_size, y1))
            x2 = x1 + crop_size
            y2 = y1 + crop_size

            crop = img[y1:y2, x1:x2]
            if crop.shape[0] != crop_size or crop.shape[1] != crop_size:
                print(f"Crop fora do tamanho em {img_file} bbox {idx}")
                continue

            xc_crop = xc - x1
            yc_crop = yc - y1
            bw_crop = bw
            bh_crop = bh
            xc_norm = xc_crop / crop_size
            yc_norm = yc_crop / crop_size
            bw_norm = bw_crop / crop_size
            bh_norm = bh_crop / crop_size

            xc_norm = max(0, min(1, xc_norm))
            yc_norm = max(0, min(1, yc_norm))
            bw_norm = max(0, min(1, bw_norm))
            bh_norm = max(0, min(1, bh_norm))

            crop_filename = f"{name}_bb{idx}_class{int(class_id)}.jpg"
            crop_img_path = os.path.join(out_img_dir, crop_filename)
            cv2.imwrite(crop_img_path, crop)

            crop_label_path = os.path.join(out_label_dir, crop_filename.replace('.jpg', '.txt'))
            with open(crop_label_path, "w") as ftxt:
                ftxt.write(f"{int(class_id)} {xc_norm:.6f} {yc_norm:.6f} {bw_norm:.6f} {bh_norm:.6f}\n")

            print(f"Salvo: {crop_img_path} + {crop_label_path}")

print("Crops e labels YOLO de 120x120 px gerados.")
