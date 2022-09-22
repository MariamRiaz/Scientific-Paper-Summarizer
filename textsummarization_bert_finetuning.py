# -*- coding: utf-8 -*-
"""TextSummarization_BERT_FineTuning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cm0Y_ZpIN_omtotm04b1nFYCOMjwQxrB
"""

!pip install transformers

import numpy as np
import pandas as pd

import sklearn.model_selection as ms
import sklearn.preprocessing as p

import tensorflow as tf
import transformers as trfs

import tensorflow as tf
device = tf.test.gpu_device_name()
if device != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device))

!nvidia-smi

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data/newdataframe.csv', delimiter=',', encoding= "utf-8")

print(df.head(5))

labels = df['label2'].nunique()

# Max length of encoded string(including special tokens such as [CLS] and [SEP]):
MAX_SEQUENCE_LENGTH = 300

# BERT model with lowercase chars only:
PRETRAINED_MODEL_NAME = 'distilbert-base-uncased'

# Batch size for fitting:
BATCH_SIZE = 256

# Number of epochs:
EPOCHS=100

def create_model(max_sequence, model_name, num_labels):

    #This is the input (words from the dataset after encoding):
    input_ids = tf.keras.layers.Input(shape=(max_sequence,), dtype=tf.int32, name='input_ids')
    attention_mask = tf.keras.layers.Input((max_sequence,), dtype=tf.int32, name='attention_mask')
    token_type_ids = tf.keras.layers.Input((max_sequence,), dtype=tf.int32)
    bert_model = trfs.TFBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels, output_hidden_states=False)
    base_output = bert_model.bert([input_ids, attention_mask , token_type_ids])
    #for layer in bert_model.layers:
      #layer.trainable = False
    output = base_output[1]
    outputs = tf.keras.layers.Dense(num_labels, activation='softmax')(output)
    model = tf.keras.models.Model(inputs=[input_ids, attention_mask , token_type_ids], outputs=outputs)
    llist = []
    for k, v in bert_model._get_trainable_state().items():
        llist.append(k)
    print(len(llist))
    layer_list = llist[201:214]
    print(layer_list)
    for k,v in bert_model._get_trainable_state().items():
      if k in layer_list:
        k.trainable = True
      else:
        k.trainable = False
    return model

#Creating the model
model =create_model (MAX_SEQUENCE_LENGTH, PRETRAINED_MODEL_NAME, num_labels=labels)
#Learning rate for the trainable parameters
lr = 1e-5
#Model Optimizer
opt = tf.keras.optimizers.Adam(learning_rate = lr, epsilon=1e-08)
#Compiling the model
model.compile(optimizer=opt,loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False), metrics=['accuracy'])

model.summary()

def batch_encode(X, tokenizer):
    return tokenizer.batch_encode_plus(
    X,
    max_length=MAX_SEQUENCE_LENGTH, # set the length of the sequences
    add_special_tokens=True, # add [CLS] and [SEP] tokens
    return_attention_mask=True,
    return_token_type_ids=True, # not needed for this type of ML task
    pad_to_max_length=True,
    truncation = True, # add 0 pad tokens to the sequences less than max_length
    return_tensors='tf'
)

tokenizer = trfs.DistilBertTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)
X_total = batch_encode(df["sentences"].values, tokenizer)

X_train, X_val, y_train, y_val = ms.train_test_split(X_total.values(), df["label2"].values, test_size=0.3, random_state=42)

from sklearn.utils import class_weight
neg, pos = np.bincount(df['label2'])
total = neg + pos
print('Total: {}\n    Positive: {} ({:.2f}% of total)\n'.format(total, pos, 100 * pos / total))
weight_for_0 = (1 / neg) * (total / 2.0)
weight_for_1 = (1 / pos) * (total / 2.0)

cls_weight = {0: weight_for_0, 1: weight_for_1}

print('Weight for class 0: {:.2f}'.format(weight_for_0))
print('Weight for class 1: {:.2f}'.format(weight_for_1))

EPOCHS = 5
BATCH_SIZE = 256
NUM_STEPS = len(X_train["input_ids"])/ BATCH_SIZE

# Train the model
history = model.fit(
    x=X_train.values(),
    y=y_train,
    validation_data=(X_val.values(), y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    class_weight = {0: 0.53, 1: 5},
)

#tf.saved_model.save(model, "/content/drive/MyDrive/Colab Notebooks/model/sum3/summodel")
model.save("/content/drive/MyDrive/Colab Notebooks/model/sum4/summodel")
print("Saved model to disk")

import matplotlib.pyplot as plt
def visualize_results(history):
    # Plot the accuracy and loss curves
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1,6)
    plt.plot(epochs, acc, 'b', label='Training acc')
    plt.plot(epochs, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel("Number of epochs")
    plt.ylabel("Accuracy achieved after every epoch")
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel("Number of epochs")
    plt.ylabel("Loss after every epoch")
    plt.legend()
    plt.show()

visualize_results(history)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
print(acc)
print(val_acc)
print(loss)
print(val_loss)

new_model = tf.keras.models.load_model("/content/drive/MyDrive/Colab Notebooks/model/sum4/summodel")

# Check its architecture
new_model.summary()

df2 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data/A Binarized Neural Network Joint Model for Machine Translation.csv', delimiter=',', encoding= "utf-8")

X_test = df2["0"].values
X_test = batch_encode(X_test, tokenizer)
logits_score = model.predict(X_test.values())

#model.save('/content/drive/MyDrive/Colab Notebooks/model/sum2/summodel')
#from tensorflow import keras
#new_model = keras.models.load_model('/content/drive/MyDrive/Colab Notebooks/model/sum2/summodel')
logits_score = new_model.predict(X_test.values())
print(new_model)
#from tensorflow import keras
#new_model = keras.models.load_model('/content/drive/MyDrive/Colab Notebooks/model/sum2/summodel')
print(logits_score)
#from scipy.special import softmax
#for logit in logits_score.logits:
  #print(logit)
  #probabilities = softmax(logit, axis=0)
  #print(probabilities)

test = df2["0"].values
test2 = batch_encode(test, tokenizer)
score = new_model.predict(test2.values())

row_index=[]
for i in enumerate(score):
  if i[1][1] > 0.5:
    row_index.append(i[0])

for j in enumerate(test):
  #print(j)
  if j[0] in row_index:
    print(j[1])