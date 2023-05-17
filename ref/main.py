import openai

from flask import Flask,jsonify,request

openai.api_key="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"
model_engine = "text-davinci-003"

import wikipedia
from keybert import KeyBERT
from googlesearch import search
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize
import numpy as np
import networkx as nx
import re
import wikipediaapi
import pywhatkit as pwt
from newsapi.newsapi_client import NewsApiClient

def DallE(question):
    return openai.Image.create(
    prompt=question,
        n=2,
        size="256x256")

def read_article(text):        
  sentences =[]        
  sentences = sent_tokenize(text)    
  for sentence in sentences:        
    sentence.replace("[^a-zA-Z0-9]"," ")     
  return sentences

def sentence_similarity(sent1,sent2,stopwords=None):    
    if stopwords is None:        
        stopwords = []        
    sent1 = [w.lower() for w in sent1]    
    sent2 = [w.lower() for w in sent2]
        
    all_words = list(set(sent1 + sent2))    
    vector1 = [0] * len(all_words)    
    vector2 = [0] * len(all_words)        
  #build the vector for the first sentence    
    for w in sent1:        
        if not w in stopwords:
            vector1[all_words.index(w)]+=1                                                             
  #build the vector for the second sentence    
    for w in sent2:        
        if not w in stopwords:            
            vector2[all_words.index(w)]+=1 
               
    return 1-cosine_distance(vector1,vector2)

def build_similarity_matrix(sentences,stop_words):
  #create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences),len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1!=idx2:
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1],sentences[idx2],stop_words)
    return similarity_matrix   

def generate_summary(text,top_n):
    nltk.download('stopwords')    
    nltk.download('punkt')
    stop_words = stopwords.words('english')    
    summarize_text = []
  # Step1: read text and tokenize    
    sentences = read_article(text)
  # Step2: generate similarity matrix            
    sentence_similarity_matrix = build_similarity_matrix(sentences,stop_words)
  # Step3: Rank sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
  # Step4: sort the rank and place top sentences
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True)
  
  # Step5: get the top n number of sentences based on rank
    for i in range(top_n):
        summarize_text.append(ranked_sentences[i][1])
  # Step6 : output the summarized version
    return " ".join(summarize_text),len(sentences)

kw_model = KeyBERT()
def chatGPT(prompt):   
    completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )
    response = completion.choices[0].text
    return response
    
def get_Answer(question):
    keywords=kw_model.extract_keywords(question, keyphrase_ngram_range=(1, 3), stop_words=None)
    full_res=chatGPT(keywords[0][0])
    res={"answer":generate_summary(full_res,5)}
    return res
    
    


# In[25]:


app=Flask(__name__)


# In[26]:


@app.route('/image')
def image():
    data=request.get_json()
    question=data['question']
    res= DallE(question)
    return jsonify(res)


# In[27]:


@app.route('/question')
def askQuestion():
    data=request.get_json()
    question=data['question']
    return jsonify({"result": get_Answer(question)})


# In[28]:


url = "https://shazam-song-recognizer.p.rapidapi.com/search_track"

querystring = {"query":"rampampam","limit":"10","start_from":"0","lang":"-"}

headers = {
	"X-RapidAPI-Key": "f20e97be1fmshc11d133ed41fef0p1e2197jsna0d87df59c19",
	"X-RapidAPI-Host": "shazam-song-recognizer.p.rapidapi.com"
}

response = request.request("POST", url, headers=headers, params=querystring)

print(response.text)

@app.route('/music')
def music():
    data=request.get_json()
    question=data['question']
    url = "https://shazam-song-recognizer.p.rapidapi.com/search_track"

    querystring = {"query":question,"limit":"10","start_from":"0","lang":"-"}

    headers = {
        "X-RapidAPI-Key": "f20e97be1fmshc11d133ed41fef0p1e2197jsna0d87df59c19",
        "X-RapidAPI-Host": "shazam-song-recognizer.p.rapidapi.com"
    }

    response = request.request("GET", url, headers=headers, params=querystring)
    return jsonify(response)


# In[19]:


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




