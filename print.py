import cv2
import xml.etree.ElementTree as ET
import os

# Nome base do arquivo (sem extensão)
img_name = "1000"
img_dir = "sticky_dataset/stickytraps"
xml_dir = "sticky_dataset/stickytraps"
output_dir = "images"

# Garante que a pasta de saída existe
os.makedirs(output_dir, exist_ok=True)

image_path = os.path.join(img_dir, f"{img_name}.jpg")
xml_path = os.path.join(xml_dir, f"{img_name}.xml")
output_path = os.path.join(output_dir, f"{img_name}_preview.jpg")

# Carrega imagem
image = cv2.imread(image_path)
if image is None:
    print(f"Erro ao abrir imagem: {image_path}")
    exit(1)
h, w = image.shape[:2]
print(f"[INFO] Resolução: {w}x{h}")

# Lê XML
tree = ET.parse(xml_path)
root = tree.getroot()

for obj in root.findall('object'):
    name = obj.find('name').text
    bbox = obj.find('bndbox')
    xmin = int(float(bbox.find('xmin').text))
    ymin = int(float(bbox.find('ymin').text))
    xmax = int(float(bbox.find('xmax').text))
    ymax = int(float(bbox.find('ymax').text))

    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0,0,255), 4)
    cv2.putText(image, name, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)

# Salva preview na pasta images
cv2.imwrite(output_path, image)
print(f"[INFO] Preview salvo: {output_path}")
