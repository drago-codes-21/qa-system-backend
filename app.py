from flask import Flask, jsonify , request
from keywordExtraction import getKeywords
from extractiveSummary import extractiveSummerize
from api_1 import chatGPT
from flask_cors import CORS
from image import DallE
import wikipediaapi
import wikipedia

app = Flask(__name__)
CORS(app)
wiki_wiki = wikipediaapi.Wikipedia('en')

@app.route('/')
def main() :
    return "<p>hii</p>"

@app.route('/question/', methods = ['POST'])
def getQuestion() :
    data=request.get_json()
    question=data['question']
    keywords =  getKeywords(question)
    domains=[]
    if(len(keywords.split()) < 3):
        domains=wikipedia.search(keywords)
    answer = chatGPT(keywords)
    return jsonify({ "result" : extractiveSummerize(answer, 2),"domain": domains}) 

@app.route('/question/details/', methods = ['POST'])
def getQuestionDetails() :
    data=request.get_json()
    question=data['question']
    keywords =  getKeywords(question)
    answer = chatGPT(keywords)
    return jsonify({ "result" : extractiveSummerize(answer, 4)})   

@app.route('/image/', methods =['POST'])
def image():
    data=request.get_json()
    question=data['question']
    res= DallE(question)
    return jsonify({"result" : res})

@app.route('/music/')
def music():
    data=request.get_json()
    question=data['question']
    url = "https://shazam-song-recognizer.p.rapidapi.com/search"

    querystring = {"query":question,"limit":"10","start_from":"0","lang":"-"}

    headers = {
        "X-RapidAPI-Key": "8850818c60msh02f2c2c75fe3ffcp1c6fafjsnc80b69e7bb17",
        "X-RapidAPI-Host": "shazam-song-recognizer.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return jsonify(response)

if __name__ == '__main__' :
    app.run(debug=True)
     

# question = request.query
    