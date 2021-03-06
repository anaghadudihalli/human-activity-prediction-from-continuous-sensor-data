# -*- coding: utf-8 -*-
from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf
import pandas as pd
from sklearn import preprocessing
import io
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
import keras
from keras.callbacks import TensorBoard
from tensorflow.keras import regularizers
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn import metrics
import glob
import os
from keras.models import load_model
from keras.utils.vis_utils import plot_model

#df2 = pd.read_csv('/content/drive/Shared drives/Dataset/csh101.ann.features.csv')
path = r'/content/drive/Shared drives/Dataset/train/'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f) for f in all_files)
df2 = pd.concat(df_from_each_file, ignore_index=True)

#df2 = pd.read_csv('/content/drive/Shared drives/Dataset/csh101.ann.features.csv')
path = r'/content/drive/Shared drives/Dataset/test/'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f) for f in all_files)
df2_test = pd.concat(df_from_each_file, ignore_index=True)

df2.shape

df2_test.shape

df2.info()

df2['activity'].value_counts()

df2[df2['activity']=='r1.Sleep']

df2['lastSensorDayOfWeek'].unique()

label_encoder = preprocessing.LabelEncoder()
df2['activity']

corr = df2.corr()
fig, ax = plt.subplots(figsize=(15,15))
ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);

df2.nunique()
df2[df2['numDistinctSensors']==1].head()
# Check for null values in the dataset
df2.isnull().sum()
df2.isna().sum()

#Check for any duplicate values
df2.duplicated()

#Dropping the correlated and irrelevant attributes
#lastSensorEventSeconds,lastSensorID,lastMotionLocation,numDistinctSensors
df2=df2.drop(columns=['lastSensorEventSeconds','lastSensorID','lastMotionLocation','numDistinctSensors'])

#lastSensorEventSeconds,lastSensorID,lastMotionLocation,numDistinctSensors
df2_test=df2_test.drop(columns=['lastSensorEventSeconds','lastSensorID','lastMotionLocation','numDistinctSensors'])

#Dropping rows with irrelevant values
df2=df2[df2['activity']!='r1.Sleep']
df2=df2[df2['activity']!='r2.Personal_Hygiene']
df2=df2[df2['activity']!= 'r1.Cook_Breakfast']
df2=df2[df2['activity']!= 'r2.Eat_Breakfast']
df2=df2[df2['activity']!= 'r2.Dress']

#Dropping rows with irrelevant values
df2_test=df2_test[df2_test['activity']!='r1.Sleep']
df2_test=df2_test[df2_test['activity']!='r2.Personal_Hygiene']
df2_test=df2_test[df2_test['activity']!= 'r1.Cook_Breakfast']
df2_test=df2_test[df2_test['activity']!= 'r2.Eat_Breakfast']
df2_test=df2_test[df2_test['activity']!= 'r2.Dress']

#Separating the label from the data
Y = df2['activity']
np.unique(Y)
Y = label_encoder.fit_transform(Y)
Y = Y.reshape(Y.shape[0],1)
np.unique(Y)

df2.shape
X = df2[df2.columns[:-1]]
X.shape

#Scaling the data
transformer = RobustScaler().fit(X)
X = transformer.transform(X)
X
###validation split
X, valX, Y, valY = train_test_split(X, Y, test_size=0.2, random_state = 0)
X.shape

model = keras.Sequential([
    keras.layers.Dense(1000, activation='relu',input_dim=32),
    keras.layers.Dense(800, activation='relu'),
    keras.layers.Dense(640, activation='relu'),
    keras.layers.Dense(580, activation='relu'),
    keras.layers.Dense(330, activation='relu'),
    keras.layers.Dense(250, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(42, activation='softmax')

])


model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

with tf.device('/device:GPU:0'):
  history=model.fit(X, Y, epochs=40, validation_data=(valX,valY),batch_size=1024)
  #,callbacks=[es,tensorboard_callback]





################################## Graph for Train and Validation #############################################
print("Train vs Validation Performance measure")
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.plot(hist['epoch'], hist['acc'],
         label='Train Accuracy')
plt.plot(hist['epoch'], hist['val_acc'],
         label = 'Val Accuracy')
plt.plot(hist['epoch'], hist['loss'],
         label='Train Loss')
plt.plot(hist['epoch'], hist['val_loss'],
         label = 'Val Loss')
plt.legend()

pred=model.predict_classes(valX,verbose=0)
tl=valY
acc=metrics.accuracy_score(tl,pred)
print(acc)
precision=metrics.precision_score(tl,pred,average='weighted')
print(precision)
recall=metrics.recall_score(tl,pred,average='weighted')
print(recall)
f1=f1_score(tl,pred,average='weighted')
print(f1)

model.save('/content/drive/Shared drives/Dataset/MLNeuralNetwork.h5')

log_reg = keras.Sequential([
      keras.layers.Dense(42, activation='softmax')
])
log_reg.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history=log_reg.fit(X, Y, epochs=40, validation_data=(valX,valY),batch_size=1024)

################################## Graph #############################################
print("Logistic Regression")
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
plt.figure()
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.plot(hist['epoch'], hist['acc'],
         label='Train Accuracy')
plt.plot(hist['epoch'], hist['val_acc'],
         label = 'Val Accuracy')
plt.plot(hist['epoch'], hist['loss'],
         label='Train Loss')
plt.plot(hist['epoch'], hist['val_loss'],
         label = 'Val Loss')
plt.legend()

#Logistic Regression
pred=log_reg.predict_classes(valX,verbose=0)
tl=valY
acc=metrics.accuracy_score(tl,pred)
print(acc)
precision=metrics.precision_score(tl,pred,average='micro')
print(precision)
recall=metrics.recall_score(tl,pred,average='micro')
print(recall)
f1=f1_score(tl,pred,average='weighted')
print(f1)

model.save('/content/drive/Shared drives/Dataset/ML_Logistic.h5')

#----------------------Testing the model with Test data--------------------------------------------------

#Separating the label from the data
Y_test = df2_test['activity']
np.unique(Y)
Y_test = label_encoder.fit_transform(Y_test)
Y_test = Y_test.reshape(Y_test.shape[0],1)
np.unique(Y_test)

df2_test.shape
X_test = df2_test[df2_test.columns[:-1]]
X_test.shape

X_test = transformer.transform(X_test)

model_final=tf.keras.models.load_model('/content/drive/Shared drives/Dataset/MLNeuralNetwork.h5')
score = model_final.evaluate(X, Y, batch_size=1024)

tf.keras.utils.plot_model(model,to_file='/content/drive/Shared drives/Dataset/model.png',show_shapes=True)
