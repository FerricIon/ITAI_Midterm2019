import json as js
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import math
import random

with open('../data/rate.json','r',encoding='UTF-8') as file:
    filmdata = js.load(file)
def invalid(x):
    if x['releaseYear'] == None:
        return False
    if x['runtime'] == None:
        return False
    if x['rate_average'] == 0:
        return False
    if x['budge'] == 0 or x['revenue'] == 0:
        return False
    return True

def read_input(data):
    data = list(filter(invalid, data))
    random.shuffle(data)
    rate_list=[]
    for x in data:
        rate_list.append(x['rate_average'] * 100)
    rate=np.asarray(rate_list,dtype="float")
    rate=np.reshape(rate,(-1,1))
    print(min(rate), max(rate))
    information_list=[]
    for x in data:
        temp=[]
        temp.append(x['budge']/100000)
        temp.append(x['revenue']/100000)
        temp.append(x['runtime'])
        temp.append(x['releaseYear'])
        cnt=0
        for y in x['genre']:
            temp.append(y)
            cnt+=1
            if cnt>=5:
                break
        while cnt<5:
            temp.append(0)
            cnt+=1
        cnt=0
        for y in x['cast']:
            temp.append(y)
            cnt+=1
            if cnt>=5:
                break
        while cnt<5:
            temp.append(0)
            cnt+=1
        cnt=0
        for y in x['crew']:
            temp.append(y)
            cnt+=1
            if(cnt>=5):
                break
        while cnt<5:
            temp.append(0)
            cnt+=1
        cnt=0
        for y in x['production_companies']:
            temp.append(y)
            cnt+=1
            if(cnt>=5):
                break
        while cnt<5:
            temp.append(0)
            cnt+=1
        information_list.append(temp)
    information=np.asarray(information_list,dtype="float")
    return information,rate

info,score = read_input(filmdata)

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

model.compile(optimizer=tf.train.RMSPropOptimizer(0.005), loss=tf.keras.losses.mean_squared_error, metrics=['accuracy'])

# model.fit(info[:-100], score[:-100], epochs=200, batch_size=32)
model.load_weights('./weight')

model.evaluate(info[-100:], score[-100:], batch_size=64)

result=model.predict(info)
print(max(result), min(result))

model.save_weights('./weight')

# x=tf.placeholder("float",shape=[None,24])
# _y=tf.placeholder("float",shape=[None,1])

# def add_layer(inputs, in_size, out_size, activation_function=None):
#     Weights = tf.Variable(tf.random_normal([in_size, out_size]))
#     biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
#     Wx_plus_b = tf.matmul(inputs, Weights) + biases
#     if activation_function is None:
#         outputs = Wx_plus_b
#     else:
#         outputs = activation_function(Wx_plus_b)
#     return outputs

# l1=add_layer(x,24,24,tf.nn.relu)
# l2=add_layer(l1,24,24,tf.nn.relu)
# prediction=add_layer(l2,24,1,None)


# loss = tf.reduce_mean(tf.reduce_sum(tf.square(_y-prediction), reduction_indices=[1]))
# train_step=tf.train.GradientDescentOptimizer(0.1).minimize(loss)
# with tf.Session() as sess:
#     init=tf.initialize_all_variables()
#     sess.run(init)
#     for i in range(1000):
#         sess.run(train_step,feed_dict={x:info,_y:score})
#         if i%50==0:
#             print(sess.run(loss,feed_dict={x:info,_y:score}))
            
