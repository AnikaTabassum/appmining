# # root = "D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\analyzed\\topic_1\\scan_my_tesla_UI_demo_v2.0.8_apkpure.com"
############## ekhane senstive_api
import os
import fnmatch 
from os.path import isfile
import math
1
root = "D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_11\\apiCalls" 
# pattern = "*.txt"
classes = {}
smaliList=[]
apkFiles=[]
for path, subdirs, files in os.walk(root, topdown=True):
	# print("path ", path,files)
	print("subdirs ", subdirs)
	
	break
for val in files:
	apkFiles.append(path+"\\"+val)
	print("vaaaa ", path+"\\"+val)
	# for name in files:
	# 	# if fnmatch(name, pattern):
	# 	smaliList.append(os.path.join(path, name))
		# print (os.path.join(path, name))
flag1=0
flag2=0
flag3=0
flag4=0
def countVal(match):
	global flag1, flag2, flag3, flag4
	print(flag1, flag2, flag3, flag4)
	cnt=0
	for apks in apkFiles:
	
		print("loop3", apks)
		try:
			ff=open(apks, 'r',  errors="ignore")
			# print("file ", files)
			lines= ff.readlines()
			for line in lines:
				# print("line ",line,"match", match)
				# print("loop4")
				if match in line:
					cnt+=1
					flag4=1
					print("match",match, cnt)
					break
			# if flag4==1:
			# 	# print("flag4", flag4)
			# 	# flag3=1
			# 	break

		except Exception as e:
			print(e)
		# if flag4==1:
		# 	# flag2=1
		# 	break
	flag4=0		
		
	print("cnt",cnt)
	return cnt

# countVal("stop")

f = open(r"D:\\8th_semester\\my_8th_semester\\SPL3\\axplorer-master\\axplorer-master\\permissions\\api-25\\senstive_api.txt", 'r', encoding="utf8")
lines=f.readlines()
print(lines)
N=len(apkFiles)
print("N ",N)
weightCount={}
x=0
for line in lines:
	print("line ", line)
	lisstt= line.split(".")
	for vl in lisstt:
		if '(' in vl:
			# print(vl)
			# print(vl.index('('))
			print("ppo",vl[:vl.index('(')])
			methodName= vl[:vl.index('(')]
			dfa=countVal(methodName)
			with open('myfile-07_03_2021_topic_11.txt', 'a') as f:
				print(methodName,dfa, file=f)
			# if dfa !=0:
			# 	# weightCount[methodName]=math.log(N/dfa)
			# 	with open('myfile-06_03_2021_topic0.txt', 'a') as f:
			# 		print(line,methodName,dfa, file=f)
	# x+=1
			# print(line.split("."))
# f2= open(r"D:\\8th_semester\\my_8th_semester\\SPL3\axplorer-master\\axplorer-master\\permissions\\api-25\\sdk-map-25.txt", 'r')

# print(weightCount)
# for er in weightCount:
# 	print(er)
# with open('myfile-04.txt', 'w') as f:
# 	print(weightCount, file=f)