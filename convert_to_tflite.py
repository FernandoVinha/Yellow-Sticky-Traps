import tensorflow as tf
import numpy as np
import os
from PIL import Image

# Caminho para o modelo exportado
saved_model_dir = "120px/weights/best_saved_model"

# Caminho para algumas imagens de exemplo para calibração
sample_images_dir = "sticky_dataset/120px/train/images"  # Altere se necessário

# Tamanho de entrada (128x128 para seu modelo)
IMG_SIZE = 128

# Gera um dataset representativo para calibrar o modelo
def representative_dataset_gen():
    image_files = [os.path.join(sample_images_dir, f) for f in os.listdir(sample_images_dir) if f.endswith(".jpg")]
    for img_path in image_files[:100]:
        img = Image.open(img_path).resize((IMG_SIZE, IMG_SIZE))
        img = np.array(img)

        if img.ndim == 2:  # grayscale
            img = np.stack([img] * 3, axis=-1)
        elif img.shape[2] == 4:  # RGBA
            img = img[:, :, :3]

        img = img.astype(np.float32) / 255.0  # ⚠️ conversão correta!
        img = np.expand_dims(img, axis=0)    # shape: (1, 128, 128, 3)
        yield [img]

# Cria o conversor
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# ⚠️ Quantização total exige representative_dataset
converter.representative_dataset = representative_dataset_gen

# Tipos para ESP32 (quantização total)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Converte
tflite_model = converter.convert()

# Salva
output_path = "120px/weights/best_quantized.tflite"
with open(output_path, "wb") as f:
    f.write(tflite_model)

print(f"✅ Modelo TFLite quantizado salvo em {output_path}")
