import json
import tensorflow as tf
from tensorflow.keras import layers

model = tf.keras.Sequential()
model.add(layers.Dropout(0.2))
model.add(layers.Dense(32, input_dim=24, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(64, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(24, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(12, kernel_regularizer=tf.keras.regularizers.l1(0.01)))
model.add(layers.Dense(1, kernel_regularizer=tf.keras.regularizers.l1(0.01)))

model.load_weights('./weight')

pMax = 1387.0581
pMin = 107.87997

user_data = json.loads(input())
print(model.predict(user_data)[0])
