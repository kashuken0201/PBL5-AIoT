import glob
from sklearn.model_selection import train_test_split
import os

current_id = 0
label_ids = {}
x_dataset = []
y_dataset_labels = []

DATA_DIR = 'Recognization/data/FaceMask/'
TRAIN_DIR = 'Recognization/src/train/train.txt'
VALID_DIR = 'Recognization/src/train/valid.txt'

image_dir = DATA_DIR

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            x_dataset.append(path)
            y_dataset_labels.append(id_)

x_train, x_val, y_train, y_val = train_test_split(x_dataset, y_dataset_labels, test_size=0.25, random_state=42)

file_train = open(TRAIN_DIR, "w")
file_val = open(VALID_DIR, "w")
for i in range(len(x_train)):
    file_train.write(x_train[i])
    if i != len(x_train) - 1:
        file_train.write("\n")
for i in range(len(x_val)):
    file_val.write(x_val[i] + "\n")
    if i != len(x_val) - 1:
        file_val.write("\n")
file_train.close()
file_val.close()