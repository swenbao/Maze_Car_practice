import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.tree import DecisionTreeRegressor
import glob
import json
import joblib
import os

features = np.array([])
labels = np.array([])

# data = {
#   "features": [scene_info["F_sensor"], scene_info["L_sensor"], scene_info["L_T_sensor"], scene_info["R_sensor"], scene_info["R_T_sensor"], scene_info["end_x"], scene_info["end_y"]],
#   "label": self.control_list
# }

# Load the dataset from ../data/2/map_1 ~ map_10/*.json
for i in range(1, 12):
    for file_path in glob.glob(f'./data/3/map_{i}/*.json'):
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                label = [data["label"][0], data["label"][1]]
                features = np.append(features, data['features'])
                labels = np.append(labels, label)

features = features.reshape(-1, 7)
labels = labels.reshape(-1, 2)

# print(features)

# print(len(features))
# print(len(labels))

# Create the model
model = MultiOutputRegressor(DecisionTreeRegressor())

# Train the model
print("Training the model...")
model.fit(features, labels)

# Save the model using joblib
print("Saving the model...")
model_dir = './models/'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)
joblib.dump(model, os.path.join(model_dir, 'model5.pkl'))

# how to predict
# model.predict([[1, 2, 3, 4, 5, 6, 7]]) # returns [[1, 2]]