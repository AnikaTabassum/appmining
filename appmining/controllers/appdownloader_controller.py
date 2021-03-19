# """
# Routes and views for the flask application.
# """
from datetime import datetime
from flask import render_template, redirect, request, jsonify, session
import json
import pickle
from appmining import app
from appmining.services import *
from google_play_scraper import app as apk
# import parser
global application, download_link, appName, topicNo
import os
@app.route('/')
@app.route('/apps')
def appsearch():
	print("try")
	# appdownloader().whoamI()
	return render_template('appsearch/index.html')
def downloadDesc(appid):
	result = apk(
		# 'com.nianticlabs.pokemongo',
		'com.tinybuildgames.helloneighbor',
		lang='en', # defaults to 'en'
		country='us' # defaults to 'us'
	)
	desc=[result["description"]][0]
	print(desc)
	
	parseVal(desc)

@app.route('/api/search', methods=['POST', 'PUT'])
def searchapp():
	global application, download_link, appName
	app_name = request.json
	result=appdownloader().search(app_name)
	download_link=result[0]
	application=result[1]
	img_src=result[2]
	print("img_src", img_src)
	n= download_link.count("/")
	print("n",n)
	appid=download_link.rsplit('/', 1)[-1]
	appName=download_link.rsplit('/', 1)[-1]
	print("jddon", result)
	downloadDesc(appid)
	return jsonify({'app_name':result[1], 'img_src': result[2]})

@app.route('/api/download', methods=['POST', 'PUT'])
def downaloadapp():
	global application, download_link
	# app_name = request.json
	result=appdownloader().download_apk(download_link)
	print("downaloadapp", result)
	calculateScore()
	return jsonify({"downloaded":result})

@app.route('/api/detect', methods=['POST', 'PUT'])
def detecgapp():
	global application, download_link
	# app_name = request.json
	result=appdownloader().download_apk(download_link)
	print("downaloadapp", result)
	return jsonify(result)


import pandas as pd
import os
# os.chdir('')
# Read data into papers
# papers = pd.read_csv('all_merged.csv')
# # Print head
# print(papers.head())

from html.parser import HTMLParser
import re
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  
from langdetect import detect
class Parse(HTMLParser):
	def __init__(self):
	#Since Python 3, we need to call the __init__() function 
	#of the parent class
		super().__init__()
		self.reset()
		self.mainLines=[]
 
	#Defining what the methods should output when called by HTMLParser.
	def handle_starttag(self, tag, attrs):
		# print("Start tag: ", tag)
		for a in attrs:
			# print("Attributes of the tag: ", a)
			popop=""
 
	def handle_data(self, data):
		
		self.mainLines.append(data)
		# papers['description_parsed'].map(data)	
		# print("Here's the data: ", data)
 
	def handle_endtag(self, tag):
		strEnd= "This is end tag"

	def get_value(self):
		return self.mainLines
def parseVal(vl):
	if detect(vl)=="en":
		# dtect_lan.append(detect(vl))
		testParser = Parse()
		print("val",vl) 
		testParser.feed(vl)
		parsed=testParser.get_value()
		print("parsed",parsed)

		removeLinks(parsed[0])


def removeLinks(data):
	result = re.sub(r"http\S+", "", data)
	result = re.sub(r"www\S+", "", result)
	result = re.sub(r"\\t+", "", result)
	# result = result.replace("\xe2\x80\xa2", "")
	result = re.sub(r'(\\x(.){2})', '',result)
	print("result",result)
	stopWordAndStemming(result)

def stopWordAndStemming(line):
	filtered_sentence=[]
	stop_words = set(stopwords.words('english')) 
	stop_words.add("the")
	stop_words.add("get")
	stop_words.add("free")
	stop_words.add("app")
	stop_words.add("you")
	stop_words.add("use")
	stop_words.add("features")
	stop_words.add("make")
	stop_words.add("like")
	stop_words.add("new")
	stop_words.add("--")
	stop_words.add("b")
	stop_words.add("\"")
	stop_words.add("\'s")
	stop_words.add("''")
	stop_words.add("b\'")

	from nltk.stem import PorterStemmer 
	from nltk.tokenize import word_tokenize 

	ps = PorterStemmer() 
	# define punctuation
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

	 
	word_tokens = word_tokenize(line)  
	for w in word_tokens: 
		if w.isdecimal():
			pass
		else:
			if w not in stop_words:
				if w not in punctuations:
					print(ps.stem(w))
					filtered_sentence.append(ps.stem(w)) 
	topicFind(filtered_sentence)
# allFilteredSentence.append(filtered_sentence)

def topicFind(filtered_sentence):
	global topicNo
	with open("lda_model.pk","rb") as fpck:
		lda = pickle.load(fpck)

	with open("dicts.pkl","rb") as d:
		dicts = pickle.load(d)
	stri=""
	for d in filtered_sentence:
		stri=stri+" "+d
	bow = dicts.doc2bow(stri.split())
	t = lda.get_document_topics(bow)
	print("t", t)
	t=sorted(t, key = lambda x: float(x[1]), reverse = True)
	i=4
	prev_len=len(t)
	for i in range(4,len(t)):
		# t.remove((t[i][0],t[i][1]))
		
		ind=t[4][0]
		# print("i ",i, ind)
		t.pop(4)
		# t.pop(t.index((t[i][0],t[i][1])))
		t.append(tuple([ind, 0]))
	t=sorted(t, key = lambda x: float(x[0]), reverse = False)
	topics=[]
	for i in range(0,12):
		topics.append(t[i][1])
	print(topics)
	with open("kmeans.pk","rb") as k:
		km = pickle.load(k)
				
	print(km.predict([topics]))
	pred=km.predict([topics])
	topicNo=pred[0]
	print("topicNo", topicNo)

def calculateScore():
	global appName
	os.system("apktool" + " d " + appName+".apk")
	root = appName
	# import os 
	dir_path = os.path.dirname(os.path.realpath(__file__))

	print("dir_path", dir_path)
	cwd = os.getcwd()
	print("cwd", cwd)
	parser().parseFile(root)
	print(countapi().countIDFscore(cwd+"\\outputFile.txt",topicNo))