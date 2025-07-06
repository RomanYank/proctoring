import os
import yaml
from processing import preprocess_dataset, convert_to_yolo
from ultralytics import YOLO
import torch

CSV_PATH = "data.csv"
CLASS_DESC_PATH = "descriptions.csv"
IMAGES_PATH = "data/images/train"
LABELS_PATH = "data/labels/train"
DATA_YAML_PATH = "./config.yaml"
TARGET_CLASSES = ["Person", "Cell phone", "Book", "Mobile phone"]

def main():
    df, label_encoder, scaler = preprocess_dataset(csv_path=CSV_PATH, class_desc_path=CLASS_DESC_PATH, target_classes=TARGET_CLASSES, max_images_per_class=100)
    convert_to_yolo(df, images_dir=IMAGES_PATH, labels_dir=LABELS_PATH, label_encoder=label_encoder)
    names = label_encoder.classes_.tolist()
    data_config = {"train": IMAGES_PATH, "val": IMAGES_PATH, "nc": len(names), "names": names}

    os.makedirs(os.path.dirname(DATA_YAML_PATH), exist_ok=True)
    with open(DATA_YAML_PATH, "w") as f:
        yaml.dump(data_config, f)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Используем устройство: {device}")

    model = YOLO("yolov11n.pt")
    model.train(data=DATA_YAML_PATH, epochs=50, device=device)
    model.save("best.pt")

if __name__ == '__main__':
    main()