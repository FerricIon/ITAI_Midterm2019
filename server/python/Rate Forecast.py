import json
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = tf.keras.Sequential()
model.add(layers.Dropout(rate=0.2))
model.add(layers.Dense(32, input_dim=24, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(rate=0.3))
model.add(layers.Dense(64, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(rate=0.3))
model.add(layers.Dense(24, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(rate=0.1))
model.add(layers.Dense(12, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dense(1, kernel_regularizer=tf.keras.regularizers.l1(0.01)))

model.load_weights('./weight')

pMax = 1387.0581
pMin = 107.87997

user_data = np.asarray([json.loads(input())], dtype="float")
result = model.predict(user_data)[0][0]
result = (result - pMin) / (pMax - pMin) * 10
result = min(result, 10)
result = max(result, 0)
print(result)
