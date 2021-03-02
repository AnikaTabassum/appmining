import pandas as pd
import os
# os.chdir('')
# Read data into papers
papers = pd.read_csv('all_merged.csv')
# Print head
print(papers.head())

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

# for col in df:
#     print(df[col].unique())
# withCat= papers.drop(columns=['SN','app_id', 'title'], axis=1).sample(65)
papers = papers.drop(columns=['app_id', 'app_name'], axis=1)
# print(papers.head())

# i=0
# for col in papers.columns:
# 	print(col,i)
# 	testParser.feed(col)
# 	i+=1
allData=[]
mainData=[]
# print("Df ", papers)
for col in papers: 
	print("col ",col)
	i=1
	if col=="description":
		for vl in papers[col]:
			try:
				if detect(vl)=="en":
					# dtect_lan.append(detect(vl))
					testParser = Parse()
					print("val",i,vl) 
					testParser.feed(vl)
					mainData.append(vl)
					allData.append(testParser.get_value())
				else:
					papers.drop(papers.index[[i-1]], inplace=True)
			except Exception as e:
				papers.drop(papers.index[[i-1]], inplace=True)
				print("This row throws and error:", i)
			

			i+=1
# updated = papers 
# updated = updated.drop(columns=['description', 'category'], axis=1)
# print("Df---2 ", updated)
# updated.insert(1,"description ",mainData, True)
# updated.insert(2, "parsed", allData, True)
papers.insert(2, "parsed", allData, True)


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
	lda = LdaModel(tweets_corpus, num_topics = nb_topics, id2word = tweets_dictionary, passes=10, alpha=5)
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
k = 12
tweets_lda = LdaModel(tweets_corpus, num_topics = k, id2word = tweets_dictionary, passes=10,alpha=5)
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
f = open("file_with_topic_probab_01_03_2021.txt", "w", encoding="utf-8")
# # f.write("Now the file has more content!")
for data in papers.filtered:
	content=[]
	
	for lines in data:
		content.append(lines)
	f.write(str(content)+"\n"+str(tweets_lda.print_topics()))
	f.write("\n")
	# print(ln,tweets_lda.print_topics())
f.close()


import csv
with open('output_file_with_topics_01_03_2021.csv', 'w', newline='', encoding="utf-8") as file:
	writer = csv.writer(file)
	writer.writerow(["document_name","cat" ,"topic_0", "topic_1", "topic_2", "topic_3", "topic_4", "topic_5","topic_6", "topic_7", "topic_8", "topic_9", "topic_10", "topic_11"])
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
					
				
				t=sorted(t, key = lambda x: float(x[0]), reverse = False)
				print("after last",t , len(t), p)
				writer.writerow([stri, mycat, t[0][1], t[1][1], t[2][1], t[3][1], t[4][1], t[5][1],t[6][1], t[7][1], t[8][1], t[9][1], t[10][1], t[11][1]])
				p+=1
