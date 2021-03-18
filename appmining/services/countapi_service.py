# # root = "D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\analyzed\\topic_1\\scan_my_tesla_UI_demo_v2.0.8_apkpure.com"
import os
import fnmatch 
from os.path import isfile
import math
1
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import os
from appmining import app

import os
import fnmatch 
from os.path import isfile
# root = "D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\analyzed\\topic_0" 
# pattern = "*.txt"
# classes = {}
# smaliList=[]
# for path, subdirs, files in os.walk(root):
# 	# print("path ", path,files)
# 	for name in files:
# 		# if fnmatch(name, pattern):
# 		smaliList.append(os.path.join(path, name))
		# print (os.path.join(path, name))
class countapi(object):
	def __init__(self, *args, **kwargs):
		print("countapi")

	def countIDFscore(self, filename, topicNo):
		print("filename", filename)
		root = "D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_"+str(topicNo)+"\\apiCalls" 
		for path, subdirs, files in os.walk(root, topdown=True):
			
			print(files)
			
		N=len(files)
		f = open(filename, "r",errors="ignore")
		totalVal=int(0)
		lines=f.readlines()
		for line in lines:
			topicCountFile="D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\myfile-07_03_2021_topic_"+str(topicNo)+".txt"
			# print("topicCountFile", topicCountFile)
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
					
		# writer.writerow([i,file,totalVal])
		# i+=1
		return totalVal