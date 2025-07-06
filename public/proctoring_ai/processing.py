import os
import pandas as pd
import requests
import cv2
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import time

def load_data(path):
    return pd.read_csv(path)

def map_label_ids_to_names(df, class_descriptions_path):
    class_df = pd.read_csv(class_descriptions_path, header=None, names=["LabelName", "ClassName"])
    label_map = dict(zip(class_df["LabelName"], class_df["ClassName"]))
    df["LabelName"] = df["LabelName"].map(label_map).fillna("unknown")
    return df

def filter_target_classes(df, target_classes, max_images_per_class=400):
    filtered_df = pd.DataFrame()
    
    for cls in target_classes:
        class_df = df[df["LabelName"] == cls]
        top_image_ids = class_df["ImageID"].drop_duplicates().head(max_images_per_class)
        
        filtered_class_df = df[df["ImageID"].isin(top_image_ids)]
        filtered_df = pd.concat([filtered_df, filtered_class_df], ignore_index=True)

    return filtered_df.drop_duplicates()

def fill_missing_values(df):
    df.fillna({'XMin': 0, 'YMin': 0, 'XMax': 0, 'YMax': 0, 'LabelName': 'unknown'}, inplace=True)
    return df

def encode_classes(df):
    le = LabelEncoder()
    df['class_id'] = le.fit_transform(df['LabelName'])
    return df, le

def add_engineered_features(df):
    df['width'] = df['XMax'] - df['XMin']
    df['height'] = df['YMax'] - df['YMin']
    df['area'] = df['width'] * df['height']
    df['aspect_ratio'] = df['width'] / (df['height'] + 1e-6)
    return df

def normalize_features(df, feature_cols):
    scaler = MinMaxScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df, scaler

def preprocess_dataset(csv_path, class_desc_path, target_classes, max_images_per_class=100):
    df = load_data(csv_path)
    df = map_label_ids_to_names(df, class_desc_path)
    df = filter_target_classes(df, target_classes, max_images_per_class)
    df = fill_missing_values(df)
    df, label_encoder = encode_classes(df)
    df = add_engineered_features(df)
    
    features = ['XMin', 'YMin', 'XMax', 'YMax', 'width', 'height', 'area', 'aspect_ratio']
    df, scaler = normalize_features(df, features)

    return df, label_encoder, scaler

def download_missing_images(df, images_dir, dataset_type='train'):
    os.makedirs(images_dir, exist_ok=True)
    base_url = f"https://open-images-dataset.s3.amazonaws.com/{dataset_type}/"

    for image_id in df['ImageID'].unique():
        filename = f"{image_id}.jpg"
        image_path = os.path.join(images_dir, filename)

        if os.path.exists(image_path):
            print(f"Уже существует: {filename}")
            continue

        url = base_url + filename
        print(f"Скачиваю {filename} ...")
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Скачано: {filename}")


def convert_to_yolo(df, images_dir, labels_dir, label_encoder):
    os.makedirs(labels_dir, exist_ok=True)
    download_missing_images(df, images_dir)
    grouped = df.groupby("ImageID")

    for image_id, group in grouped:
        filename = image_id + ".jpg"
        image_path = os.path.join(images_dir, filename)
        label_path = os.path.join(labels_dir, image_id + ".txt")

        with open(label_path, "w") as f:
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            for _, row in group.iterrows():
                x_center = ((row["XMin"] + row["XMax"]) / 2)
                y_center = ((row["YMin"] + row["YMax"]) / 2)
                width = row["XMax"] - row["XMin"]
                height = row["YMax"] - row["YMin"]
                f.write(f"{row['class_id']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"YOLO аннотации сохранены в {labels_dir}")
