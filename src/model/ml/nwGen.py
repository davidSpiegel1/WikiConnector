# Next Word Predictor Generator

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


x = 0
y = 0
def readFile():
    with open('book.txt','r',encoding='utf-8') as file:
        text = file.read()
    return text

def tokenize(text):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([text])
    #total_words = len(tokenizer.word_index)+1
    return tokenizer
# Attempting to form n-grams from the sequences
def gatherInputSequences(tokenizer,text):
    input_sequences = []
    for line in text.split('\n'):
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1,len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    #max_sequence_len = max([len(seq) for seq in input_sequences])

    return input_sequences

def makeModel(input_sequences,total_words):

    max_sequence_len=0
    #maxi = -1
    #print("The input sequences: ",input_sequences)
    for seq in input_sequences:
        print("The seq",seq)
        print("The len of seq:",len(seq))
        if len(seq) >= max_sequence_len:
            max_sequence_len = len(seq)
    #print("What maxi is:",maxi)
    #print("The max sequence: ",max_sequence_len)
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    x = input_sequences[:,:-1]
    y = input_sequences[:,-1]
    y = np.array(tf.keras.utils.to_categorical(y, num_classes=total_words))
    model = Sequential()
    model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
    model.add(LSTM(150))
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.fit(x,y,epochs=1,verbose=1)
    return model

def compileModel(model,X,y):
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.fit(X,y,epochs=100,verbose=1)
text = readFile()
print(text)
tokenizer = tokenize(text)
total_word = len(tokenizer.word_index)+1
print("Total words:",total_word)
print("tokenizer: ",tokenizer)
input_sequences = gatherInputSequences(tokenizer,text)
print(input_sequences)
model = makeModel(input_sequences,total_word)
print(model.summary())
print("What x is: ",x)
#compileModel(model,x,y)



