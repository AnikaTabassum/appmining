import nltk
# nltk.download("punkt")
# from nltk.corpus import stopwords
# print(stopwords.words('english'))

from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
f = open("sample.txt", "r")
# print(f.read())
lines=f.readlines()
example_sent = """This is a sample sentence, 
                  showing off the stop words filtration."""
  
stop_words = set(stopwords.words('english'))  
  
word_tokens = word_tokenize(lines[0])  
  
filtered_sentence = [w for w in word_tokens if not w in stop_words]  
  
filtered_sentence = []  
  
for w in word_tokens:  
    if w not in stop_words:  
        filtered_sentence.append(w)  
  
print(word_tokens)  
print("sen",filtered_sentence)  