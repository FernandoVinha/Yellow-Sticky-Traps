import os
import cv2

# Diretórios
src_base = "sticky_dataset/16mpx/images"
dst_base = "sticky_dataset/5mpx/images"
splits = ["train", "val"]

# Tamanho alvo: 5MP
target_pixels = 5_000_000

for split in splits:
    src_dir = os.path.join(src_base, split)
    dst_dir = os.path.join(dst_base, split)
    os.makedirs(dst_dir, exist_ok=True)

    for fname in os.listdir(src_dir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        img_path = os.path.join(src_dir, fname)
        out_path = os.path.join(dst_dir, fname)

        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {img_path}")
            continue
        h, w = img.shape[:2]
        cur_pixels = w * h
        scale = (target_pixels / cur_pixels) ** 0.5

        new_w = int(w * scale)
        new_h = int(h * scale)

        # Redimensiona
        img_resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        cv2.imwrite(out_path, img_resized)
        print(f"{img_path} -> {out_path} ({w}x{h} -> {new_w}x{new_h})")

print("Imagens convertidas para ~5MP (mantendo proporção).")

# DICA: labels .txt não precisam ser alterados, pois são normalizados!
# Depois, copie a estrutura de labels/ para sticky_dataset/5mpx/labels/ (os mesmos arquivos .txt).
