import os
import sys
import subprocess
from shutil import copyfile

walk_dir = "D:\\8th_semester\\my_8th_semester\\SPL3\\all_apks\\trivia"
# os.system("apktool" + " d " + "D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\AnyDesk Remote Control_v6.1.8_apkpure.com.apk")
#-------------------------------------decompile----------------------------

i = 0

# apktool = "/usr/local/bin/apktool.jar"

for root, subdirs, files in os.walk(walk_dir):
	list_file_path = os.path.join(root, 'my-directory-list.txt') 
	 
	with open(list_file_path, 'wb') as list_file:
		for file in files:
			if file.endswith(".apk"):
				i=i+1
				filenn=os.path.join(root,file)
				nbc=file.replace(" ","_")
				outs=os.path.join(root,"output")
				newname=os.path.join(outs,nbc)
				copyfile(filenn,newname)
				print (str(i)+"-"+filenn) 
				os.system("apktool" + " d " + newname)
				# os.system("apktool" + " d " + "D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\AnyDesk Remote Control_v6.1.8_apkpure.com")