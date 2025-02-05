import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
import json
import random


# from keras.models import load model
from tensorflow.keras.models import load_model
model = load_model('/home/dell/Desktop/Chatbot/chatbot_model.keras')
intents = json.loads(open('/home/dell/Desktop/Chatbot/intents.json', encoding="utf8").read())
words = pickle.load(open('/home/dell/Desktop/Chatbot/words.pkl','rb'))
classes = pickle.load(open('/home/dell/Desktop/Chatbot/classes.pkl','rb'))

# Flask Code
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def health_Check():
    return jsonify({"message": "Server is running successfully on local!"})


def decrypt(msg):
    # input format: how+are+you
    # output format: how are you
    # replacing + with spaces
    
    str = msg
    new_Str = str.replace('+',' ')
    return new_Str

def clean_Up(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bag_Of_Words(sentence, words, show_Details=True):
    # Tokenizing the sentence
    sentence = clean_Up(sentence)
    # Bag of words: matrix of N words
    bag = [0]*len(words)
    
    for s in sentence:
        for i,w in enumerate(words):
            if(w==s):
                bag[i]=1
                if show_Details:
                    print('Found in bag: %s' %w)
    return (np.array(bag))
  
  
def predict_Class(sentence, model):
    a = bag_Of_Words(sentence, words, show_Details=False)
    ans = model.predict(np.array([a]))[0]
    ERROR_THRESHOLD = 0.25
    res = [[i,r] for i,r in enumerate(ans) if r>ERROR_THRESHOLD]
    res.sort(key=lambda x:x[1], reverse=True)
    result_List = []
    
    for r in res:
        result_List.append({'intent':classes[r[0]], 'probablity': str(r[1])})
        
    return result_List

def getResponse(ints, intents_json):
   tag = ints[0]['intent']
   list_Of_Intents = intents_json['intents']
   
   for i in list_Of_Intents:
       if(i['tag']==tag):
           result = random.choice(i['responses'])
           break
     
   return result
   
 
def chatbot_Response(msg):
    ints = predict_Class(msg, model)
    try:
       response = getResponse(ints, intents)
    except:
        print('An exception occured!')
        response = 'I cannot answer this query, this is out of my limitation.'
    
    return response



@app.route("/query/<sentence>")
def query_Chatbot(sentence):
    message = decrypt(sentence)
    response = chatbot_Response(message)
    
    json_Obj = jsonify({"top": {"res":response}})
    return json_Obj

if __name__ == "__main__":
    # Only run the app locally (on localhost)
    app.run()