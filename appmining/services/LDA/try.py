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
papers = papers.drop(columns=['SN','app_id', 'title', 'category'], axis=1).sample(100)
# print(papers.head())

# i=0
# for col in papers.columns:
# 	print(col,i)
# 	testParser.feed(col)
# 	i+=1
allData=[]
# print("Df ", papers)
for col in papers: 
	i=0
	for vl in papers[col]:
		testParser = Parse()
		# print("val",i,vl) 
		testParser.feed(vl)
		allData.append(testParser.get_value())

		i+=1
papers.insert(1, "parsed", allData, True)
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

			if w not in stop_words:
				if w not in punctuations:
					filtered_sentence.append(ps.stem(w)) 
	allFilteredSentence.append(filtered_sentence)
			
############ lines without stop words ----- REMOVING STOP WORDS
# print("senserd ", allFilteredSentence[0])################ lines without stop words --------REMOVING STOP WORDS


# Import the wordcloud library
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# for sentence in allFilteredSentence:
# 	long_str=""
# 	for words in sentence:
# 		long_str=long_str+" "+words
		# print("sentence",long_str)
papers.insert(2, "filtered", allFilteredSentence, True)




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

import gensim.corpora as corpora
# Create Dictionary
id2word = corpora.Dictionary(data)
# Create Corpus
texts = data
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]
# View
print("what",corpus[:1][0][:30])

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

def get_most_freq_words(str, n=None):
    vect = CountVectorizer().fit(str)
    bag_of_words = vect.transform(str)
    sum_words = bag_of_words.sum(axis=0) 
    freq = [(word, sum_words[0, idx]) for word, idx in vect.vocabulary_.items()]
    freq =sorted(freq, key = lambda x: x[1], reverse=True)
    return freq[:n]
  
print(get_most_freq_words([ word for tweet in papers.filtered for word in tweet],30))


#################################################################################################################################\
# build a dictionary where for each tweet, each word has its own id.
# We have 6882 tweets and 10893 words in the dictionary.
tweets_dictionary = Dictionary(papers.filtered)

# build the corpus i.e. vectors with the number of occurence of each word per tweet
tweets_corpus = [tweets_dictionary.doc2bow(tweet) for tweet in papers.filtered]

# compute coherence
tweets_coherence = []
for nb_topics in range(1,36):
    lda = LdaModel(tweets_corpus, num_topics = nb_topics, id2word = tweets_dictionary, passes=10)
    cohm = CoherenceModel(model=lda, corpus=tweets_corpus, dictionary=tweets_dictionary, coherence='u_mass')
    coh = cohm.get_coherence()
    tweets_coherence.append(coh)

# visualize coherence
plt.figure(figsize=(10,5))
plt.plot(range(1,36),tweets_coherence)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence Score");
plt.show()

import matplotlib.gridspec as gridspec
import math
k = 6
tweets_lda = LdaModel(tweets_corpus, num_topics = k, id2word = tweets_dictionary, passes=10)

def plot_top_words(lda=tweets_lda, nb_topics=k, nb_words=10):
    top_words = [[word for word,_ in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]
    top_betas = [[beta for _,beta in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]

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