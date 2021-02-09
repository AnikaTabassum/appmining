import pandas as pd
import os
# os.chdir('')
# Read data into papers
papers = pd.read_csv('../sample_data.csv')
# Print head
print(papers.head())

# for col in papers.columns: 
#     print(col) 

papers = papers.drop(columns=['SN','app_id', 'title', 'category'], axis=1).sample(100)
print(papers.head())
# for col in papers.columns: 
#     print(col) 

#Remove punctuation/lower casing

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
 
	#Defining what the methods should output when called by HTMLParser.
	def handle_starttag(self, tag, attrs):
		# print("Start tag: ", tag)
		for a in attrs:
			print("Attributes of the tag: ", a)
 
	def handle_data(self, data):
		# mainLines.append(data)
		papers['description_parsed'].map(data)	
		# print("Here's the data: ", data)
 
	def handle_endtag(self, tag):
		strEnd= "This is end tag"

# testParser = Parse()
# testParser.feed(lines[0])

papers['description_parsed'] = \
testParser = Parse()
papers['description'].map(testParser.feed("papers['description']"))
# Convert the titles to lowercase
# papers['description_parsed'] = \
# papers['description_parsed'].map(lambda x: x.lower())
# Print out the first rows of papers
print("parsed ",papers['description_parsed'].head())

# Load the regular expression library
import re
# Remove punctuation
papers['description_processed'] = \
papers['description'].map(lambda x: re.sub('[,\.!?]', '', x))
# Convert the titles to lowercase
papers['description_processed'] = \
papers['description_processed'].map(lambda x: x.lower())
# Print out the first rows of papers
print("wghat",papers['description_processed'].head())

for col in papers.columns: 
    print(col)

# Exploratory Analysis

# Import the wordcloud library
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# Join the different processed titles together.
long_string = ','.join(list(papers['description_processed'].values))

stri="b'From makers award-winning Castle Cats , Dungeon Dogs idle RPG allows battle , build , collect craft comfort mobile device . Join rebels Lyra , Ken Poppy adventures Lupinia take evil cat king , suppressing canine population treating second-class citizens . Dungeon Dogs perfect pick play game tried trusted gameplay mechanics beautiful artwork capture hearts gamers young old . Set rebels battle foes whilst busy collect loot later join fight oppression real time , choice ! Features : IDLE AND ACTION GAMEPLAY SYSTEM Set heroes battle busy collect rewards return upgrade heroes Dungeon Dogs\xe2\x80\x99 crafting system collect new , epic doggos , individual skillset characteristics . Alternatively , join battles whenever want help heroes ! COLLECTING AND CUSTOMISATION With 45 different dog heroes collect launch plenty options choose . Set heroes battle evolve unlock new skills , characteristics outfits make hero original . You also collect 100 different items guild leader customise liking . FRESH AND ORIGINAL NARRATIVE Dungeon Dogs\xe2\x80\x99 standalone narrative fits perfectly Castle Cats Universe pawsome , pun filled storyline engage captivate newcomers , well veterans PocApp\xe2\x80\x99s Idle RPG games . LIKE THE CHARACTERS , THE GAME WILL KEEP EVOLVING Packed 85+ quests launch , Dungeon Dogs stop ! Dungeon Dogs ever-evolving game regular event updates added game , creating longevity . Whether spring , summer , fall , holiday even special celebrity event , want keep coming back . Extra heroes also added regular intervals special guest heroes making appearance help expand collection . FULL COMMUNITY SUPPORT We always listening , want include much possible . Dungeon Dogs related competitions , fan art features fully supported PocApp Studios social media channels Discord server . You never know , idea may even make game ! How cool ? Get paws ready download ! It\xe2\x80\x99s pawsome ! For information , please visit : FOLLOW US ON SOCIAL MEDIA : Facebook : Twitter : Instagram : Discord : We love feedback please feel free write us contact [ ] pocappstudios.com _______ Oh wait ! Last least , boring stuff ... Privacy Policy : Terms Of Service EULA : "
# Create a WordCloud object
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
# Generate a word cloud
# print("wordcloud ", wordcloud)
wordcloud.generate(stri)
# Visualize the word cloud
wordcloud.to_image()
wordcloud.to_file("cloud.png")

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

#Prepare data for LDA Analysis

# import gensim
# from gensim.utils import simple_preprocess
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# stop_words = stopwords.words('english')
# stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
# def sent_to_words(sentences):
#     for sentence in sentences:
#         # deacc=True removes punctuations
#         yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
# def remove_stopwords(texts):
#     return [[word for word in simple_preprocess(str(doc)) 
#              if word not in stop_words] for doc in texts]
# data = papers.paper_text_processed.values.tolist()
# data_words = list(sent_to_words(data))
# # remove stop words
# data_words = remove_stopwords(data_words)
# print(data_words[:1][0][:30])