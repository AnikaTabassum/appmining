
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import os
from appmining import app

import os
import fnmatch 
from os.path import isfile
class parser(object):

	def __init__(self, *args, **kwargs):
		print("afjkjkds")
	def parseSmaliFiles(self,content, fileNames, filename):
		"""
		Parse smali code into python directory
		"""
		print("nope------")
		smali_class = {}
		smaliClassName = content.readline()
		smali_class['ClassName'] = smaliClassName.split(' ')[-1][:-1]
		smali_class['Keywords'] = smaliClassName.split(' ')[1:-1]
		smali_class['Metrics'] = {'Reflections':0,'Methods':0,'Invocations':0}
		smali_class['Methods'] = []
		smali_class['Fields'] = []
		smali_class['Loader'] = []
		#smali_class['Dependecies'] = []
		#smali_class['Annotations'] = []
		line = content.readline()
		try:
			while line:
				if line.startswith('.super'):
					smali_class['SuperClass'] = line.split(' ')[1][:-1]
				elif line.startswith('.annotated'):
					# TODO: Handle Annotations
					# this may take more research into different types of annotations
					pass
				elif line.startswith('.source'):
					smali_class['SourceFile'] = line.split(' ')[1][1:-2]
				elif line.startswith('.implements'):
					smali_class['Implements'] = line.split(' ')[1][:-1]
				elif line.startswith('.field'):
					field = {}
					field['KeyWords'] = line.split('=')[0].split(' ')[1:-1]
					field['Name'] = line.split('=')[0].rstrip().split(' ')[-1].split(':')[0]
					field['Type'] = line.split('=')[0].rstrip().split(' ')[-1].split(':')[1][:-1]
					smali_class['Fields'].append(field)
				elif line.startswith('.method'):
					smali_class['Metrics']['Methods']+= 1
					method = {}
					method['MethodName'] = line.split(' ')[-1][:-1]
					method['Keywords'] = line.split(' ')[1:-1]
					method['Returns'] = line.split(')')[-1]
					method['Parameters'] = line.split('(')[-1].split(')')[0]
					method['Invokes'] = []
					method['LibCalls'] = []
					method['Android API'] = []
					method['ConstStrings'] = []
					method['Dependencies'] = []
					method['Code'] = []
					method['Code'].append(line)
					methodLine = content.readline().lstrip()
					while not methodLine.startswith('.end method'):
						if "ClassLoader" in methodLine:
							smali_class["Loader"].append(methodLine)
						invokes = {}
						if not methodLine == "\n":
							method['Code'] += ''.join(methodLine)
						if methodLine.startswith('invoke'):
							invokes['Type'] = methodLine.split(' ')[0]
							invokes['Class'] = \
								methodLine.split('}')[1][1:].split('-')[0]
							method['Dependencies']\
								.append(methodLine.split('}')[1][1:]
									.split('-')[0])
							invokes['Function'] = \
								methodLine.split('}')[1].split('>')[1]
							if (('Landroid' in methodLine)):
								# print("fileNames", fileNames)
								f = open(filename, "a",errors="ignore")
								method["Android API"].append(methodLine)
								try:
									f.write(methodLine+"\n")
								except Exception as e:
									pass
								
								# print("API ", methodLine)
							if (('Ljava' in invokes['Class']) or
									('Landroid' in invokes['Class']) or
									('Ljavax' in invokes['Class'])):
								method['LibCalls'].append(invokes)
							else:
								method['Invokes'].append(invokes)

							smali_class['Metrics']['Invocations']+= 1
							if("reflect" in invokes['Function']):
								smali_class['Metrics']['Reflections']+= 1
						elif methodLine.startswith('const-string'):
							method['ConstStrings'].append(methodLine.split('"')[1])
						try:
							methodLine = content.readline().lstrip()
						except Exception as e:
							methodLine=""
							print(e)
						
					method['Code'].append(methodLine)
					smali_class['Methods'].append(method)
					# print("method ", method)------- eta lagbe i guess
				else:
					pass
				line = content.readline()
		except:
			print (line)
			tb = traceback.format_exc()
			print (tb)
			sys.exit(1)
		return smali_class

	def parseFile(self,path):
		print("called parseFile", path)
		import time
		timestr = time.strftime("%Y%m%d-%H%M%S")
		print (timestr)
		filename="output"+timestr+".txt"
		classes = {}
		smaliList=[]
		pattern='*.smali'
		for path, subdirs, files in os.walk(path):
			for name in files:
				print("name ", name)
				if fnmatch.fnmatch(name, pattern):
					smaliList.append(os.path.join(path, name))

		for smali in smaliList:
			print("vbnjm", smali, len(smaliList))
			# log.info("Parsing " + smali)
			filen=smali
			# f = open(smali, 'r')
			# smali_class = self.parseSmaliFiles(f, path, filename)
			# classes[smali_class['ClassName']] = smali_class
			try:
				f = open(smali, 'r')
				smali_class = self.parseSmaliFiles(f, filen, filename)
				classes[smali_class['ClassName']] = smali_class
			except Exception as e:
				pass

		return filename


	def parseDir(self,path):
		# set up class and results dictionary
		# log.info("Performing recursive search for smali files")
		classes = {}
		sharedobj_strings = {}
		filename=[]
		pattern='*.smali'
		print("alld",os.listdir(path))
		allfile=os.listdir(path)
		filesList=[]
		folderList=[]
		smaliList=[]
		# from fnmatch import fnmatch
		# import os
		# import fnmatch 
		# from os.path import isfile
		# import math
		p=0
		apkFiles=[]
		root = "D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_11" 
		for path, subdirs, files in os.walk(root, topdown=True):
			
			print(subdirs)
			break
		for val in subdirs:
			filen=path+"\\"+val
			apkFiles.append(path+"\\"+val)
			print("hjd",path+"\\"+val)
		# root = 'D:\\8th_semester\\my_8th_semester\\SPL3\\apks_mid\\analyzed\\topic_5'
		# root = "D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_0\\0_Room_Planner_Home_Interior_Floorplan_Design_3D_v1016_apkpure.com"
		
		for i in range(len(apkFiles)-1,len(apkFiles)): 
			filen=apkFiles[i]   
			pattern = "*.smali"
			import fnmatch
			for path, subdirs, files in os.walk(filen):
				for name in files:
					# print("name ", name)
					if fnmatch.fnmatch(name, pattern):
						smaliList.append(os.path.join(path, name))
						# print (os.path.join(path, name))
					# print("here")
			for files in allfile:
				if isfile(files):

					filesList.append(files)
					allfile.remove(files)
				else:
					files=os.path.join(path,files)
					folderList.append(files)
			
			for smali in smaliList:
				
				print("vbnjm", smali)
				log.info("Parsing " + smali)
				try:
					f = open(smali, 'r')
					smali_class = parseSmaliFiles(f, filen)
					classes[smali_class['ClassName']] = smali_class
				except Exception as e:
					pass
			

		# for sharedobj in util.find_files(path, '*.so'):
		#     log.info("Processing: " + sharedobj)
		#     f = open(sharedobj, 'r')
		#     smali_class = parseSmaliFiles(f)
		#     sharedobj_strings[sharedobj] =  util.unique_strings_from_file(sharedobj)


		log.info("Parsing Complete")
		return { 'classes' : classes,
				 'sharedobjs' : sharedobj_strings }

	# if __name__ == '__main__':
	#     # D:\8th_semester\my_8th_semester\SPL3\YouTube_v16.05.37_apkpure.com\smali\android\arch\lifecycle
	#     path="D:\\8th_semester\\my_8th_semester\\SPL3\\YouTube_v16.05.37_apkpure.com\\smali\\android\\arch\\lifecycle"
	#     parseDir(path)