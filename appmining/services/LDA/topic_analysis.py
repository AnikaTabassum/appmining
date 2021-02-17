import pandas as pd
import os
# os.chdir('')
# Read data into papers
papers = pd.read_csv('../sample_data.csv')
# Print head
print(papers.head())

from html.parser import HTMLParser
import re
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  

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

# for col in df:
#     print(df[col].unique())
# withCat= papers.drop(columns=['SN','app_id', 'title'], axis=1).sample(65)
papers = papers.drop(columns=['SN','app_id', 'title'], axis=1).sample(65)
# print(papers.head())

# i=0
# for col in papers.columns:
# 	print(col,i)
# 	testParser.feed(col)
# 	i+=1
allData=[]
print("Df ", papers)
for col in papers: 
	print("col ",col)
	i=0
	if col=="description":
		for vl in papers[col]:
			testParser = Parse()
			print("val",i,vl) 
			testParser.feed(vl)
			allData.append(testParser.get_value())

			i+=1
papers.insert(2, "parsed", allData, True)
# withCat.insert(2, "parsed", allData, True)
# print(papers)
# print("mainLines",len(mainLines))

# i=0
# for row in papers.iterrows(): 
# 	try:
# 		val=papers['description'][i]
		
# 		pass
# 	except KeyError:
# 		print("KeyError")
# 	print("val",i,papers['description'][i]) 
# 	i+=1
# papers.insert(1,"parsed ",)

allWithoutTags=[]

import string

i=0
for vl in papers["parsed"]:
	# testParser = Parse()
	withoutTags=[]
	for data in vl:
		# print("valnnnnnnnnn",i,data, len(data)) 
		result = re.sub(r"http\S+", "", data)
		result = re.sub(r"www\S+", "", result)
		result = re.sub(r"\\t+", "", result)
		# result = result.replace("\xe2\x80\xa2", "")
		result = re.sub(r'(\\x(.){2})', '',result)

		# print("result ", result)
		if result!="":
			withoutTags.append(result)


		i+=1
	allWithoutTags.append(withoutTags)


# print("allWithoutTags", allWithoutTags)
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

allFilteredSentence=[]
for lists in allWithoutTags:
	filtered_sentence=[]
	for line in lists: 
		word_tokens = word_tokenize(line)  
		for w in word_tokens: 
			if w.isdecimal():
				pass
			else:
				if w not in stop_words:
					if w not in punctuations:
						filtered_sentence.append(ps.stem(w)) 
	allFilteredSentence.append(filtered_sentence)
			
############ lines without stop words ----- REMOVING STOP WORDS
# print("senserd ", allFilteredSentence)################ lines without stop words --------REMOVING STOP WORDS


# Import the wordcloud library
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# for sentence in allFilteredSentence:
# 	long_str=""
# 	for words in sentence:
# 		long_str=long_str+" "+words
		# print("sentence",long_str)
papers.insert(3, "filtered", allFilteredSentence, True)
# withCat.insert(3, "filtered", allFilteredSentence, True)


'''
for sentence in allFilteredSentence:
	long_str=""
	for words in sentence:
		# long_string=",".join(words)
		# words=ps.stem(words)
		long_str=long_str+" "+words
		# print("words ", words)
		# Create a WordCloud object
	wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
	# Generate a word cloud
	# print("wordcloud ", wordcloud)
	wordcloud.generate(long_str)
	# Visualize the word cloud
	wordcloud.to_image()
	wordcloud.to_file("cloud.png")

	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	# print("long ", long_str)
	# plt.show()
	long_str=""
# print("filtered ", papers)
'''

import gensim
from gensim.utils import simple_preprocess

# def sent_to_words(sentences):
#     for sentence in sentences:
#         # deacc=True removes punctuations
#         yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
# def remove_stopwords(texts):
#     return [[word for word in simple_preprocess(str(doc)) 
#              if word not in stop_words] for doc in texts]
data = papers.filtered.values.tolist()
print("datadata")
# data_words = list(sent_to_words(data))
# # remove stop words
# data_words = remove_stopwords(data_words)
# print(data_words[:1][0][:30])

# import gensim.corpora as corpora
# # Create Dictionary
# id2word = corpora.Dictionary(data)
# # Create Corpus
# texts = data
# # Term Document Frequency
# corpus = [id2word.doc2bow(text) for text in texts]
# # View
# print("what",corpus[:1][0][:30])

# from pprint import pprint
# # number of topics
# num_topics = 10
# # Build LDA model
# lda_model = gensim.models.LdaMulticore(corpus=corpus,
#                                        id2word=id2word,
#                                        num_topics=num_topics)
# # Print the Keyword in the 10 topics
# pprint(lda_model.print_topics())
# doc_lda = lda_model[corpus]
from sklearn.feature_extraction.text import CountVectorizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from datetime import datetime

from gensim.models.wrappers import LdaMallet

def get_most_freq_words(str, n=None):
	vect = CountVectorizer().fit(str)
	bag_of_words = vect.transform(str)
	sum_words = bag_of_words.sum(axis=0) 
	freq = [(word, sum_words[0, idx]) for word, idx in vect.vocabulary_.items()]
	freq =sorted(freq, key = lambda x: x[1], reverse=True)
	return freq[:n]
  
print(get_most_freq_words([ word for tweet in papers.filtered for word in tweet],30))


#################################################################################################################################\

tweets_dictionary = Dictionary(papers.filtered)
print("tweets_dictionary ", tweets_dictionary[124])
# build the corpus i.e. vectors with the filtered words
tweets_corpus = [tweets_dictionary.doc2bow(tweet) for tweet in papers.filtered]
# print("tweets_corpus ",tweets_corpus)
# compute coherence
tweets_coherence = []
for nb_topics in range(1,4):
	lda = LdaModel(tweets_corpus, num_topics = nb_topics, id2word = tweets_dictionary, passes=10, alpha=4)
	cohm = CoherenceModel(model=lda, corpus=tweets_corpus, dictionary=tweets_dictionary, coherence='u_mass')
	coh = cohm.get_coherence()
	tweets_coherence.append(coh)

# visualize coherence
plt.figure(figsize=(10,5))
plt.plot(range(1,4),tweets_coherence)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence Score");
plt.show()

import matplotlib.gridspec as gridspec
import math
k = 6
tweets_lda = LdaModel(tweets_corpus, num_topics = k, id2word = tweets_dictionary, passes=10,alpha=4)
print("tweets_coherence ", tweets_coherence)


# print("lda -----------",[tweets_lda.get_document_topics(item) for item in tweets_corpus])
# for item in tweets_corpus:
# 	print(len(tweets_corpus), "dpapa", tweets_lda.get_document_topics(item))
# print("get document topics ", tweets_lda.get_document_topics(tweets_corpus[6]))
# print("tweets_lda ", len(tweets_dictionary))



def plot_top_words(lda=tweets_lda, nb_topics=k, nb_words=10):
	top_words = [[word for word,_ in lda.show_topic(topic_id, topn=10)] for topic_id in range(lda.num_topics)]
	for topic_id in range(lda.num_topics):
		ll=lda.get_topic_terms(topic_id,topn=10)
		print("ll",ll,"topic_id", topic_id)
		for val in ll:
			print("opo ", tweets_dictionary[val[0]],"probability:" ,val[1])
		# print("id:",ll[0], tweets_dictionary[ll[0]], "probability:",ll[1])
		# print("get_topic_terms",lda.get_topic_terms(topic_id,topn=10))
	top_betas = [[beta for _,beta in lda.show_topic(topic_id, topn=10)] for topic_id in range(lda.num_topics)]
	# for top in top_words:
	# 	print("top ",len(top))
	# 	for word in top:
	# 		print("word",word)



	gs  = gridspec.GridSpec(round(math.sqrt(k))+1,round(math.sqrt(k))+1)
	gs.update(wspace=0.5, hspace=0.5)
	plt.figure(figsize=(20,15))
	for i in range(nb_topics):
		ax = plt.subplot(gs[i])
		plt.barh(range(nb_words), top_betas[i][:nb_words], align='center',color='blue', ecolor='black')
		ax.invert_yaxis()
		ax.set_yticks(range(nb_words))
		ax.set_yticklabels(top_words[i][:nb_words])
		plt.title("Topic "+str(i))
		plt.show()
		
  
plot_top_words()
f = open("file_with_topic_probab.txt", "w")
# # f.write("Now the file has more content!")
for data in papers.filtered:
	content=[]
	
	for lines in data:
		content.append(lines)
	f.write(str(content)+"\n"+str(tweets_lda.print_topics()))
	f.write("\n")
	# print(ln,tweets_lda.print_topics())
f.close()
# print(content)
# content=['b', '1', '500', '1', '1', '1', '2019.11', '2019.04', '1', '2.', '3', 'IT', '4', '5', '6.', '7.', '8', 'nc', '3', '9', '2019', '2018', '2017', '2016', '2015', '2014', 'sn', 'helpdesk', 'jobkorea.co.kr', 'mobil', 'jobkorea.co.kr', '1588-9350', '1.', '2.', '3.', 'jobkorea', 'app', 'readi', 'next', 'career', 'move', 'from', 'search', 'appli', 'find', 'job', 'jobkorea', 'korea\\', "'s", '1', 'job', 'search', 'applic', '1', 'fast', 'precis', '``', 'smart', 'search', "''", 'search', 'result', 'keyword', 'locat', '2', 'appli', 'submit', 'jobkorea', 'resum', 'mobil', 'devic', '3', 'access', 'member', 'exclus', 'servic', '4', 'receiv', 'instant', 'job', 'alert', 'notif', '5', 'inform', 'cover', 'letter', 'exampl', 'interview', 'review', 'salari', '6', 'job', 'post', 'avail', 'employ', 'recruit', '1588-9350']
# # content=" pratilipi read write get involv pratilipi india 's largest digit platform connect reader writer 12 indian languag read 25 lakh+ stori book poem articl magazin novel essay etc 2,50,000 writer connect world 2.3 crores+ reader 2.5 lakh+ writer download today start read write origin stori languag read anywher anytim On way offic break bednev without bookuilt book lover pratilipi put million stori novel poem audio book english number indian languag fingertip pratilipi perfect blend classic old new-ag literatur old wise writer inspir write wherea writer feel young restless write share stori reach million reader have stori tell self-publish pratilipi join largest commun writer creat draft add imag publish right pratilipi provid hassl advanc writer panel act write littl less scari whole lot comfort connect never alon they say take villag rais child At pratilipi say take commun writer We stori tell the dialogue-stimul commun pratilipi bring writer reader singl destin platform ye curat collect stori read download stori android phone read anywher anytim without worri carri book pay singl paisa ... ye awesom featur 1 read go anytim anywher 2 download read offlin 3 add stori wish list dont miss anyth 4 share stori friend build commun 5 continu read left seamless experi 6 get personalis recommend read everyday 7 rate review stori read commun better 8 author profil read stori favourit author 9 publish stori earn recognit commun 22 million reader 10 read write 12 differ languag explor best content never pratilipi stori current avail follow languag 1 hindi stori 2 tamil stori 3 marathi stori 4 gujarati stori 5 kannada stori 6 telugu stori 7 bengali stori 8 malayalam stori 9 english stori 10 punjabi stori 11 odia stori 12 urdu stori categori 1 short stori 2 love stori 3 romanc stori 4 scienc fiction stori 5 action adventur stori 6 travel stori 7 ghost stori 8 mysteri stori 9 women health children stori 10 suspens thriller stori 11 motiv stori 12 social stori 13 best stori 14 kid stori 15 popular stori 16 classic fiction 17 comic 18 poem 19 audio stori how start pratilipi download pratilipi read popular genr save favourit librari self-publish pratilipi join largest commun writer thi complet free payment detail requir join pratilipi make world better place one read time"
# bow_vector = tweets_dictionary.doc2bow(content)
# print("bow_vector", bow_vector)
# q= tweets_lda[bow_vector]

# from operator import itemgetter 
# res = max(q, key = itemgetter(1))[0] 
# res1 = max(q, key = itemgetter(1))[1] 
# print("REs : ",res, "res1:",res1)
# if (res  == 1 ):
# 	print("This .txt file is related to Politics/Government, Accuracy:",res1)
# # elif (res == 2) :
#         print("This .txt file is related to sports, Accuracy:",res1)
# elif res==3:
#         print("This .txt file is related to Computer, Accuracy:",res1)

# f=open("output.txt","a")
# for tweet in papers.filtered:
# 	for d in tweet:
# 		bow = tweets_dictionary.doc2bow(d.split())
# 		t = tweets_lda.get_document_topics(bow)
# 		# print("t ",t)
# 		f.write(d+" "+str(t)+"\n")

# f.close()


# import csv
# with open('output_file_test.csv', 'w', newline='') as file:
# 	writer = csv.writer(file)
# 	writer.writerow(["document_name", "topic_0", "topic_1", "topic_2", "topic_3", "topic_4", "topic_5"])
# 	for tweet in papers.filtered:
# 		for d in tweet:
# 			if d.isdecimal():
# 				pass
# 			else:
# 				bow = tweets_dictionary.doc2bow(d.split())
# 				t = tweets_lda.get_document_topics(bow)
# 				# print("jane")
# 				# tempList=[]
# 				# for val in tempList:
# 				# 	tempList.append(val)
# 				writer.writerow([d, t[0][1],t[1][1],t[2][1],t[3][1],t[4][1],t[5][1]])
	# writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
	# writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
	# writer.writerow([3, "Guido van Rossum", "Python Programming"])

import csv
with open('output_file_with_topics.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["document_name","cat" ,"topic_0", "topic_1", "topic_2", "topic_3", "topic_4", "topic_5"])
	mycatList=[]
	for kk in papers:
		if kk=="category":
			for cats in papers[kk]:
				mycatList.append(cats)
				# print("cats", type(cats))
		if kk=="filtered":
			p=0
			for tweet in papers[kk]:
				mycat=mycatList[p]
				stri=""
				for d in tweet:
					stri=stri+" "+d

				bow = tweets_dictionary.doc2bow(stri.split())
				t = tweets_lda.get_document_topics(bow)
				print("before",t)
				t=sorted(t, key = lambda x: float(x[1]), reverse = True)
				print("after",t)
				# print("len ", len(t))
				i=4
				prev_len=len(t)
				for i in range(4,len(t)):
					# t.remove((t[i][0],t[i][1]))
					
					ind=t[4][0]
					# print("i ",i, ind)
					t.pop(4)
					# t.pop(t.index((t[i][0],t[i][1])))
					t.append(tuple([ind, 0]))
					# print("after change ",t)
					
				# for i in range(len(t),prev_len):
				# 	# t.extend((tuple([i,0])))
				# 	t.append(tuple([i, 0]))
				# 	# i+=1
					# t[i][1]=023
					# print("vals ",t[i][0],type(t[i][0]),t[i][1], t.index((t[i][0],t[i][1])))
				# print("jane",t)
				# tempList=[]
				# for val in tempList:
				# 	tempList.append(val)
				
				t=sorted(t, key = lambda x: float(x[0]), reverse = False)
				# print("after last",t)
				writer.writerow([stri, mycat, t[0][1], t[1][1], t[2][1], t[3][1], t[4][1], t[5][1]])
				p+=1

# for cal in withCat.category:
# 	print("with", cal)
# #############-----------------------------------------------------------------
# import csv
# with open('output_file_str_ll_cat.csv', 'w', newline='') as file:
# 	writer = csv.writer(file)
# 	writer.writerow(["document_name", "topic_0", "topic_1", "topic_2", "topic_3", "topic_4", "topic_5"])
# 	for alltweet in withCat:
# 		print("alltweet ", alltweet)
# 		tweet=alltweet.filtered
# 		stri=""
# 		for d in tweet:
# 			stri=stri+" "+d

# 		bow = tweets_dictionary.doc2bow(stri.split())
# 		t = tweets_lda.get_document_topics(bow)
# 		print("before",t)
# 		t=sorted(t, key = lambda x: float(x[1]), reverse = True)
# 		print("after",t)
# 		# print("len ", len(t))
# 		i=4
# 		prev_len=len(t)
# 		for i in range(4,len(t)):
# 			# t.remove((t[i][0],t[i][1]))
			
# 			ind=t[4][0]
# 			# print("i ",i, ind)
# 			t.pop(4)
# 			# t.pop(t.index((t[i][0],t[i][1])))
# 			t.append(tuple([ind, 0]))
# 			# print("after change ",t)
			
# 		# for i in range(len(t),prev_len):
# 		# 	# t.extend((tuple([i,0])))
# 		# 	t.append(tuple([i, 0]))
# 		# 	# i+=1
# 			# t[i][1]=023
# 			# print("vals ",t[i][0],type(t[i][0]),t[i][1], t.index((t[i][0],t[i][1])))
# 		# print("jane",t)
# 		# tempList=[]
# 		# for val in tempList:
# 		# 	tempList.append(val)
		
# 		t=sorted(t, key = lambda x: float(x[0]), reverse = False)
# 		# print("after last",t)
# 		writer.writerow([stri, t[0][1], t[1][1], t[2][1], t[3][1], t[4][1], t[5][1]])

