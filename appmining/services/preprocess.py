from html.parser import HTMLParser
import re
from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  
f = open("sample.txt", "r")
# print(f.read())
lines=f.readlines()
mainLines=[]########lines without links---------------------- REMOVING LINKS
class Parse(HTMLParser):
	def __init__(self):
	#Since Python 3, we need to call the __init__() function 
	#of the parent class
		super().__init__()
		self.reset()
 
	#Defining what the methods should output when called by HTMLParser.
	def handle_starttag(self, tag, attrs):
		print("Start tag: ", tag)
		for a in attrs:
			print("Attributes of the tag: ", a)
 
	def handle_data(self, data):
		mainLines.append(data)
		print("Here's the data: ", data)
 
	def handle_endtag(self, tag):
		print("End tag: ", tag)
 
 
testParser = Parse()
stri="b'From the makers of award-winning Castle Cats, Dungeon Dogs is an idle RPG that allows you to battle, build, collect and craft all from the comfort of your mobile device.<br/><br/>Join our rebels Lyra, Ken and Poppy on their adventures in Lupinia to take down the evil cat king, who is suppressing the canine population and treating them as second-class citizens.<br/><br/>"
testParser.feed(lines[0])
print(len(mainLines))
# filtered_sentence = [w for w in word_tokens if not w in stop_words] 
stop_words = set(stopwords.words('english')) 
filtered_sentence = [] 
withoutTags=[]##############lines without tags  ------ REMOVING TAGS
for lineNo in mainLines:
	result = re.sub(r"http\S+", "", lineNo)
	# result = re.sub(r"www\S+", "", lineNo)
	result = re.sub(r"\\t+", "", result)
	# result= re.sub(r'[^\w]', ' ', result)
	withoutTags.append(result)
	print(result)
	
for line in withoutTags: 
	word_tokens = word_tokenize(line)  
	for w in word_tokens: 
		if w not in stop_words:  
			filtered_sentence.append(w) 
print("sen ", filtered_sentence)################ lines without stop words --------REMOVING STOP WORDS