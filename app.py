from __future__ import division
import feedparser
from flask import Flask,session, render_template, flash, request,Markup,redirect,url_for,escape,jsonify
import pymysql
from hashlib import md5
import json
import urllib
import pyttsx3

import re
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

db = pymysql.connect("localhost", "root", "", "rssfeed")
dbCrimeMap = pymysql.connect("localhost","root","","crimemap")

app= Flask(__name__)
#api = Api(app)
app.secret_key = 'my unobvious secret key'


class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        #print(content)
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        #print(content.split("\r\n\r\n"))
        return content.split("\r\n\r\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in range(n)] for x in range(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        #summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)



@app.route('/',methods=['GET','POST'])
def index():
    title=''
    text=""""""
    summary=''
    originalLength = 0
    summaryLength = 0
    summaryRatio = 0
    #engine = pyttsx3.init()
    #voices = engine.getProperty('voices')
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        
        st = SummaryTool()
        sentences_dic = st.get_senteces_ranks(text)
        summary = st.get_summary(title, text, sentences_dic)
        originalLength = len(title)+len(text)
        summaryLength = len(summary)
        summaryRatio = (100 - (100 * (len(summary) / (len(title) + len(text)))))
        #print("Text:"+text)
        #print(summary)
    # engine.setProperty('rate', 150)
    # engine.setProperty('voice', voices[1].id)
    # engine.say(summary)
    # engine.runAndWait()
    return render_template('hello.html',title=title,text=text,summary=summary,originalLength=originalLength,summaryLength=summaryLength,summaryRatio=summaryRatio)

@app.route('/speech',methods=['GET','POST'])
def speech():
    summary=''
    title=''
    text=''
    originalLength=''
    summaryLength=''
    summaryRatio=''
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if request.method == 'POST':
        summary =  request.form.get('summary2')
        title =  request.form.get('title') 
        text =  request.form.get('text') 
        originalLength =  request.form.get('originalLength') 
        summaryLength =  request.form.get('summaryLength')
        summaryRatio =  request.form.get('summaryRatio')   
        #print(title)

    engine.setProperty('rate', 150)
    engine.setProperty('voice', voices[1].id)
    engine.say(summary)
    engine.runAndWait()
    

    return render_template('hello.html',title=title,text=text,summary=summary,originalLength=originalLength,summaryLength=summaryLength,summaryRatio=summaryRatio)


if __name__ == "__main__":
    app.run()