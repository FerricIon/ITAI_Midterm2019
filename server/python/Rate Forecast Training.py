import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import json
from progressbar import *
import random


ids = {}
for d in ['cast', 'crew', 'genre', 'company']:
	with open('../data/' + d + 'ID.csv', 'r', encoding='utf-8') as stream:
		ids[d] = dict(map(lambda x: (int(x[1]), x[0]), enumerate(stream.read().split(','))))
def obtainTrainingData (data):
	ret = { 'num': [], 'genre': [], 'cast': [], 'crew': [], 'company': [], 'label': [] }
	progress = ProgressBar()
	for x in progress(data):
		ret['num'].append([x['budget'] / 1e5, x['revenue'] / 1e5, x['runtime'], x['releaseYear']])
		for d in ['genre', 'cast', 'crew', 'company']:
			x[d] = list(map(lambda u: ids[d][u], np.unique(x[d])))
			ret[d].append([1 if i in x[d] else 0 for i in range(len(ids[d]))])
		ret['label'].append([x['rateAverage']])
	for d in ret:
		ret[d] = np.asarray(ret[d])
	return ret

# Model
inputNums = tf.keras.Input(shape=(4, ), name='Nums_Input')
inputGenres = tf.keras.Input(shape=(len(ids['genre']), ), name='Genre_Input')
inputCast = tf.keras.Input(shape=(len(ids['cast']), ), name='Cast_Input')
inputCrew = tf.keras.Input(shape=(len(ids['crew']), ), name='Crew_Input')
inputProductionCompanies = tf.keras.Input(shape=(len(ids['company']), ), name='Company_Input')

hiddenGenres = layers.Dense(64, activation='softmax', name='Genre_Hidden')(inputGenres)
outputGenres = layers.Dense(15, name='Genre_Output')(hiddenGenres)
hiddenCast = layers.Dense(500, activation='softmax', name='Cast_Hidden')(inputCast)
hiddenCast = layers.Dropout(rate=0.3, name='Cast_Dropout')(hiddenCast)
outputCast = layers.Dense(15, name='Cast_Output')(hiddenCast)
hiddenCrew = layers.Dense(500, activation='softmax', name='Crew_Hidden')(inputCrew)
hiddenCrew = layers.Dropout(rate=0.3, name='Crew_Dropout')(hiddenCrew)
outputCrew = layers.Dense(15, name='Crew_Output')(hiddenCrew)
hiddenProductionCompanies = layers.Dense(500, activation='softmax', name='Company_Hidden')(inputProductionCompanies)
hiddenProductionCompanies = layers.Dropout(rate=0.3, name='Company_Dropout')(hiddenProductionCompanies)
outputProductionCompanies = layers.Dense(15, name='Company_Output')(hiddenProductionCompanies)

mergedLayer = layers.concatenate([inputNums, outputGenres, outputCast, outputCrew, outputProductionCompanies], name='Merged_Input')

hidden = layers.Dense(128, kernel_regularizer=tf.keras.regularizers.l1(0.01), name='Hidden1')(mergedLayer)
# hidden = layers.Dropout(rate=0.1)(hidden)
hidden = layers.Dense(64, kernel_regularizer=tf.keras.regularizers.l1(0.01), name='Hidden2')(hidden)
# hidden = layers.Dropout(rate=0.2)(hidden)
hidden = layers.Dense(20, kernel_regularizer=tf.keras.regularizers.l1(0.01), name='Hidden3')(hidden)
output = layers.Dense(1, name='Output')(hidden)

model = tf.keras.Model([inputNums, inputGenres, inputCast, inputCrew, inputProductionCompanies], output)
model.compile(
	optimizer=tf.keras.optimizers.RMSprop(0.0005),
	loss=tf.keras.losses.mean_squared_error
)

# Data
with open('../data/rate2.json', 'r', encoding='utf-8') as data:
	data = json.load(data)
	random.shuffle(data)
	print('Start loading data.')
	trainingData = obtainTrainingData(data)
	print('Done.')

# model = tf.keras.models.load_model('./nnmodel')
model.fit(
	[trainingData['num'], trainingData['genre'], trainingData['cast'], trainingData['crew'], trainingData['company']],
	trainingData['label'],
	epochs=500,
	batch_size=32,
	validation_split=0.1,
	callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)]
)

model.save('./nmodel')
