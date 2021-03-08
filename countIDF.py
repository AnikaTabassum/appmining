### ekhane sensitive api
import os
import math
fileList=[]
root = "D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_11\\apiCalls" 
for path, subdirs, files in os.walk(root, topdown=True):
	
	print(files)
N=len(files)
for file in files:
	fileList.append(path+"\\"+file)
import csv
i=1
with open('topic_11_IDF.csv', 'w', newline='') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(["Serial", "Name", "Scores"])
	for file in fileList:
		f = open(file, "r",errors="ignore")
		totalVal=int(0)
		lines=f.readlines()
		for line in lines:
			topicCountFile="D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\myfile-07_03_2021_topic_11.txt"
			ff = open(topicCountFile, "r")
			allAPi= ff.readlines()
			for apiline in allAPi:
				ii=apiline.split(" ")
				# print("allAPi", ii[0])
				if ii[0] in line:
					try:
						val= math.log(N/int(ii[1]))
					
						print(line,val)
						totalVal+=val
					except Exception as e:
						print(e)
					
		writer.writerow([i,file,totalVal])
		i+=1
