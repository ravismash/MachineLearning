from flask import Flask, render_template, request, url_for
import urllib
from urllib.parse import quote 
from lxml import html
import requests
import string
import time
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters;

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('plagiarizer-submit.html')

@app.route('/IsItPlagiarized/', methods=['POST'])
def IsItPlagiarized():
        text_to_filter=request.form['text_to_check']
        if (text_to_filter.lstrip().rstrip() == ''):
                return render_template('plagiarizer-submit.html')
        punkt_param = PunktParameters()
        sentence_splitter = PunktSentenceTokenizer(punkt_param)
        sentences = sentence_splitter.tokenize(text_to_filter)
        probability_of_plagiarism = 0
        for a_sentence in sentences:
                # add a timer so we don't upset bing! 
                time.sleep(0.3)
                content = filter(lambda x: x in string.printable, a_sentence)
                the_term = urllib.parse.quote('+' + '"' + str(content) + '"')
                page = requests.get('https://www.google.com/search?q='+the_term)
                if ((not "No results found for" in page.text) and (not "No hay resultados para" in page.text) and (not "are no results for" in page.text)):
                    probability_of_plagiarism += 1;
        is_it_plagiarized = str((probability_of_plagiarism / len(sentences)) * 100) + '%'
        return render_template('plagiarizer-results.html', text_to_filter=text_to_filter, is_it_plagiarized=is_it_plagiarized)


if __name__ == "__main__":
    app.run(debug=True)
