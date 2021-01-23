from langdetect import detect
import nltk
# nltk.download()
# print(detect("War doesn't show who's right, just who's left."))
f = open("sample.txt", "r")
# print(f.read())
lines=f.readlines()
tokens = nltk.word_tokenize(lines[0])
print(tokens)
# print(len(lines))
linesArr=lines[0].split(".")
print("lines ", linesArr)
all=[]
# print(detect(f.read()))
for row in linesArr:
    try:
        language = detect(row[0])
        # print("language ====1", row, language)
    except:
        language = "error"
        # print("This row throws and error:", row[0])
    # row.append(language)
   	# langs.append(language)
    # all.append(row)

print(detect("কারাদণ্ড; দণ্ডাদেশ; দণ্ডাজ্ঞা; দণ্ডনির্ধারণ; শাস্তিদান; মত"))
print(detect("policy"))