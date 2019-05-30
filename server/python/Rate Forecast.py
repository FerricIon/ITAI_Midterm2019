import tensorflow as tf
import numpy as np
import json
import os
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

ids = {}
for d in ['cast', 'crew', 'genre', 'company']:
	with open('../data/' + d + 'ID.csv', 'r', encoding='utf-8') as stream:
		ids[d] = dict(map(lambda x: (int(x[1]), x[0]), enumerate(stream.read().split(','))))
def pretreat(x):
  ret = [[[x['budget'] / 1e5, x['revenue'] / 1e5, x['runtime'], x['releaseYear']]]]
  for d in ['genre', 'cast', 'crew', 'company']:
    ret.append([[1 if i in list(map(lambda u: ids[d][u], filter(lambda u: u in ids[d], x[d]))) else 0 for i in range(len(ids[d]))]])
  return ret

model = tf.keras.models.load_model('./nmodel')
data = pretreat(json.loads(input()))
print(model.predict(data, steps=1))
