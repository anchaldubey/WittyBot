#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:20:09 2025

@author: dell
"""

# Imports and Downloads
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import json
import pickle

import numpy as np
from keras.optimizers import SGD
import random

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
# Initializing lists
words = []
classes = []
documents = []
ignore_Words = ['?','!','@','$']

# Using our json file
data_File = open('intents.json').read()
intents = json.loads(data_File)

# Populating the lists
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Take each word and tokenize it
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        
        # Adding documents
        documents.append((w,intent['tag']))
        
        # Adding classes to our class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_Words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# Used for debugging
#print(len(documents),"Documents:",documents)
#print(len(classes),"Classes:",classes)
#print(len(words),"Words:",words)

pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))   

# Initializing the training data
training = []
output_Empty = [0]*len(classes)

for doc in documents:
    # Initializing the bag of words
    bags = []
    # List of tokenized words for the pattern
    pattern_Words = doc[0]
    pattern_Words = [lemmatizer.lemmatize(word.lower()) for word in pattern_Words]
    
    for w in words:
        if w in pattern_Words:
            bags.append(1)
        else:
            bags.append(0)
    # Output is '0' for each tag and '1' for current tag
    # Output_Row is for tags actually and bags is for words
    output_Row = list(output_Empty)
    output_Row[classes.index(doc[1])] = 1
    
    # training is appended with both bags and output_Row i.e. words and tags
    # training now contains pair of these
    training.append([bags,output_Row])
    
random.shuffle(training)
training = np.array(training, dtype = object) # training will be required to be converted to numpy array

train_x = list(training[:,0])
train_y = list(training[:,1])

# To check
print('Training data created!')
#print('train_x: ',train_x)
#print('train_y: ',train_y)

# Creating the model
# 3 layers: 1st layer 128 neurons, 2nd layer 64 neurons and
# 3rd layer contains number of neurons equal to number of intents to predict output intent with softmax

model = Sequential()
# Layer-1
model.add(Dense(128, input_shape = (len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
# Layer-2
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
# Layer-3
model.add(Dense(len(train_y[0]), activation = 'softmax')) # We don't use dropout in last layer

# Compiling model
# Stochastic gradient descent with nesterov accelerated gradient gives good results here
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.keras')

print('Model created!')