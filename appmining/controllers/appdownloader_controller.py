# """
# Routes and views for the flask application.
# """
from datetime import datetime
from flask import render_template, redirect, request, jsonify, session
import json
import pdfkit
import pickle
from appmining import app
from appmining.services import *
from google_play_scraper import app as apk
# import parser
global application, topicWords,malwareFlag , filesss, download_link, appName, topicNo, score, histogram, ratings, reviews, description
import os
from flask_wkhtmltopdf import Wkhtmltopdf

from pynput.keyboard import Key, Controller
@app.route('/')
@app.route('/apps')
def appsearch():
	print("try")
	# appdownloader().whoamI()
	return render_template('appsearch/index.html')

@app.route('/report')
def report():
	print("try report")
	# appdownloader().whoamI()
	return render_template('report/index.html')
def downloadDesc(appid):
	
	result = apk(
		# 'com.nianticlabs.pokemongo',
		appid,
		lang='en', # defaults to 'en'
		country='us' # defaults to 'us'
	)
	global score, histogram, ratings, reviews, appName, description
	desc=[result["description"]][0]
	description= desc
	print(desc)
	print("score",result['score'])
	print("histogram", result['histogram'])
	print("ratings", result['ratings'])
	print("reviews ", result['reviews'])
	score= result['score']
	histogram= result['histogram']
	ratings= result['ratings']
	reviews = result['reviews']
	parseVal(desc)

@app.route('/api/search', methods=['POST', 'PUT'])
def searchapp():
	global application, download_link, appName, score, histogram, ratings, reviews
	app_name = request.json
	result=appdownloader().search(app_name) 
	download_link=result[0]
	application=result[1]
	img_src=result[2]
	print("img_src", img_src)
	n= download_link.count("/")
	print("n",n, app_name)
	appid=download_link.rsplit('/', 1)[-1]
	appName=download_link.rsplit('/', 1)[-1]
	print("jddon", result, appid)
	downloadDesc(appid)
	return jsonify({'app_name':result[1], 'img_src': result[2], 'score':score, 'ratings':ratings, 'histogram':histogram})

@app.route('/api/download', methods=['POST', 'PUT'])
def downaloadapp():
	global application, download_link
	# app_name = request.json
	result=appdownloader().download_apk(download_link)
	print("downaloadapp", result)
	# calculateScore()
	return jsonify({"downloaded":result})

# @app.route('/api/detect', methods=['POST', 'PUT'])
# def detecgapp():
# 	global application, download_link
# 	# app_name = request.json
# 	result=appdownloader().download_apk(download_link)
# 	print("downaloadapp", result)
# 	return jsonify(result)
from twilio.rest import Client


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
		print("val-------------",vl) 
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
	with open("lda_model_3.pk","rb") as fpck:
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
	print("topics",topics)
	with open("kmeans_26_03_2021.pk","rb") as k:
		km = pickle.load(k)
				
	print(km.predict([topics]))
	pred=km.predict([topics])
	topicNo=pred[0]
	if topicNo==2:
		topicNo+=1
	print("topicNo", topicNo)
@app.route('/api/detect', methods=['POST', 'PUT'])
def calculateScore():
	global appName, topicNo, malwareFlag, filesss
	os.system("apktool " + appName+".apk"+" & ‘\r\n’")

	# keyboard = Controller()
	# # keyboard.press(Key.cmd)
	# # keyboard.release(Key.cmd)
	# os.system(keyboard.press('a'))
	# os.system(keyboard.release('a'))
	root = appName
	# import os 
	dir_path = os.path.dirname(os.path.realpath(__file__))

	print("dir_path", dir_path)
	cwd = os.getcwd()
	print("cwd", cwd)
	filesss=parser().parseFile(root)
	# print(countapi().countIDFscore(cwd+"\\outputFile.txt",topicNo))
	modelName="oc_svm_"+str(topicNo)+".pk"
	sc=countapi().countIDFscore(cwd+"\\"+filesss,topicNo)
	score=[sc]
	print("score ", sc)
	with open(modelName,"rb") as k:
		md = pickle.load(k)
				
	pred=md.predict([score])
	print("pred ", pred)
	malwareFlag="This App is suspected as Malware! "
	flag="malware"
	if pred[0]==1:
		malwareFlag="This App is safe to install "
		flag="normal"
	# else:
	# 	# the following line needs your Twilio Account SID and Auth Token
	# 	client = Client("AC3b57140eded5855ff98128f6d00024e2", "58d87802b41743db0c2ee55a1d7f8575")

	# 	# change the "from_" number to your Twilio number and the "to" number
	# 	# to the phone number you signed up for Twilio with, or upgrade your
	# 	# account to send SMS to any phone number
	# 	client.messages.create(to="+8801955073646", 
	# 						   from_="+13236738996", 
	# 						   body=malwareFlag)
	print("malwareFlag", malwareFlag)
	plot_fig().plot(topicNo, sc)
	return jsonify({"anomaly":malwareFlag,"flag":flag})
	# topicNo=pred[0]
	# print("topicNo", topicNo)

@app.route('/api/description', methods=['POST', 'PUT'])
def reportload():	
	global score, histogram, ratings, reviews, appName, description, topicWords
	print(appName, score, description)
	topicWords=[]
	if topicNo==0:
		topicWords=['control','account','mobil','TV','remot','transact','bank','servic','payment']
	elif topicNo==1:
		topicWords=['workout','home','fat','weight','exercis','fit','lose','burn','app','women']
	elif topicNo==2:
		topicWords=['game','play','friend','mode','pool','carrom','player','board']
	elif topicNo==3:
		topicWords=['game','music','play','fun','learn','color','song','piano','kid']
	elif topicNo==4:
		topicWords=['english','bangla','translat','languag','word','voic','text','medicin','dictionari','speak']
	elif topicNo==5:
		topicWords=['run','player','game','world','custom','use','purchas','play','talk']
	elif topicNo==6:
		topicWords=['game','play','quiz','brain','puzzl','hous','fun','level','test']
	elif topicNo==7:
		topicWords=['video','call','chat','messag','messeng','play','friend','game','cricket']
	elif topicNo==8:
		topicWords=['rent','friend','peopl','share','order','locat','job','advertis','video']
	elif topicNo==9:
		topicWords=['game','kid','learn','cook','babi','educ','cake','fun','shop','cream']
	elif topicNo==10:
		topicWords=['girl','home','chat','recip','height','design','wall','room','increas','meet']
	elif topicNo==11:
		topicWords=['color','order','food','deliveri','secur','pizza','connect','restaur','use']
	# appName="test"
	# score="4.89"
	# description="ytdrecdrvfbnuhimojuyhgtrfdsgfvnhjkl\
	# uybgkjlnhjgfvdtvhyuijkmnbjvhgfvtyuijk"
	return jsonify({'app_name':appName, 'score':score, 'description': description, 'topicWords': topicWords}) 

@app.route('/api/downloadaspdf', methods=['POST', 'PUT'])	
def downloadaspdf():

	global filesss, topicWords,appName, score, description, topicNo
	# topicNo=6
	global score, histogram, ratings, reviews, appName, description, topicWords
	# print(appName, score, description)
	topicWords=[]
	if topicNo==0:
		topicWords=['control','account','mobil','TV','remot','transact','bank','servic','payment']
	elif topicNo==1:
		topicWords=['workout','home','fat','weight','exercis','fit','lose','burn','app','women']
	elif topicNo==2:
		topicWords=['game','play','friend','mode','pool','carrom','player','board']
	elif topicNo==3:
		topicWords=['game','music','play','fun','learn','color','song','piano','kid']
	elif topicNo==4:
		topicWords=['english','bangla','translat','languag','word','voic','text','medicin','dictionari','speak']
	elif topicNo==5:
		topicWords=['run','player','game','world','custom','use','purchas','play','talk']
	elif topicNo==6:
		topicWords=['game','play','quiz','brain','puzzl','hous','fun','level','test']
	elif topicNo==7:
		topicWords=['video','call','chat','messag','messeng','play','friend','game','cricket']
	elif topicNo==8:
		topicWords=['rent','friend','peopl','share','order','locat','job','advertis','video']
	elif topicNo==9:
		topicWords=['game','kid','learn','cook','babi','educ','cake','fun','shop','cream']
	elif topicNo==10:
		topicWords=['girl','home','chat','recip','height','design','wall','room','increas','meet']
	elif topicNo==11:
		topicWords=['color','order','food','deliveri','secur','pizza','connect','restaur','use']

	# appName="test"
	# score="4.89"
	# description="ytdrecdrvfbnuhimojuyhgtrfdsgfvnhjkl\
	# uybgkjlnhjgfvdtvhyuijkmnbjvhgfvtyuijk"
	# filesss="Sfkjnszijtr"
	# topicWords=['english','bangla','translat','languag','word','voic','text','medicin','dictionari','speak']
	

	fil= filesss+".pdf"
	print("fil ", fil, topicWords)
	tw=topicWords[0]
	for i  in range(1,len(topicWords)):
		tw= tw+","+ topicWords[i]
	from fpdf import FPDF
  
	  
	# save FPDF() class into a 
	# variable pdf
	pdf = FPDF()
	  
	# Add a page
	pdf.add_page()
	  
	# set style and size of font 
	# that you want in the pdf
	pdf.set_font("Arial", size = 10)
	  
	# create a cell
	pdf.cell(200, 10, txt = "App Report", 
			 ln = 1, align = 'C')
	pdf.cell(200, 10, txt = "App id : "+ appName ,
			 ln = 2, align = 'C')
	pdf.cell(200, 10, txt = "rating : "+ str(score),
			 ln = 3, align = 'C')
	# pdf.cell(200, 10, txt = "App Description : "+ str(description),
	# 		 ln = 4, align = 'C')
	# add another cell
	pdf.cell(200, 10, txt = "Most significant words of this topic are: "+tw,
			 ln = 5, align = 'C')
	pdf.image('appmining/static/images/my_plot.png', x=50 , w=100, h=80)
	sss="The orange app is the new app. The blue app is the other app of the same topic"
	# pdf.cell(200, 10, txt = sss,
	#          ln = 11, align = 'C')
	# save the pdf with name .pdf
	infile = open("appmining/static/images/output.txt", "r", encoding="UTF-8")
	
	ss=[]
	# insert the texts in pdf
	for x in infile:
		im=x.find(">")
		sdd=x[im+1:]
		lm=sdd.find("(")
		sdd=sdd[:lm]
		print("sdd ", sdd)
		ss.append(sdd)
	pp=ss[0]
	for i  in range(1,len(ss)):
		pp= pp+","+ ss[i]
	pdf.cell(200, 10, txt ="Sensitive API calls made by this app are: "+ pp, ln = 1, align = 'C')
	pdf.output("appmining/static/images/"+fil) 


	# wkhtmltopdf = Wkhtmltopdf(app)
	# path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
	# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
	# pdfkit.from_url("http://127.0.0.1:5000/report", fil, configuration=config)
	# pdfkit.from_string(render_template('report/index.html'))
	print("pungi")
	return jsonify({'fil':fil})