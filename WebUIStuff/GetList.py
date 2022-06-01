# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def default():
    return render_template('WebSearchTweet.html')

@app.route('/', methods=['POST'])
def getLuceneList():
    query = request.form['QueryToBeSearched']

    resultsList = the_lucene_function_with_the_list(query) #place holder for the lucene back end stuff 
    return render_template('Results.html', outputs=resultsList)

