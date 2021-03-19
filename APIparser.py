__author__ = 'Matt Clarke-Lauer'
__email__ = 'matt@clarkelauer.com'
__credits__ = ['Matt Clarke-Lauer']
__date__ = 6 / 30 / 13

__version__ = '0.1'
__status__ = 'Development'

import sys
import traceback
import log
import util
import pdb
import subprocess

def __init__():
    print("afjkjkds")
def parseSmaliFiles(content):
    """
    Parse smali code into python directory
    """
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
                            f = open("let_test.txt", "a")
                            method["Android API"].append(methodLine)
                            f.write(methodLine+"\n")
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
                    methodLine = content.readline().lstrip()
                method['Code'].append(methodLine)
                smali_class['Methods'].append(method)
            else:
                pass
            line = content.readline()
    except:
        print (line)
        tb = traceback.format_exc()
        print (tb)
        sys.exit(1)
    return smali_class


import os
import fnmatch 
from os.path import isfile
def parseDir(path):
    # set up class and results dictionary
    log.info("Performing recursive search for smali files")
    classes = {}
    sharedobj_strings = {}
    filename=[]
    pattern='*.smali'
    print("alld",os.listdir(path))
    allfile=os.listdir(path)
    filesList=[]
    folderList=[]
    smaliList=[]
    from fnmatch import fnmatch

    root = 'D:\\8th_semester\\my_8th_semester\\SPL3\\YouTube_v16.05.37_apkpure.com'
    pattern = "*.smali"

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                smaliList.append(os.path.join(path, name))
                print (os.path.join(path, name))
    for files in allfile:
        if isfile(files):

            filesList.append(files)
            allfile.remove(files)
        else:
            files=os.path.join(path,files)
            folderList.append(files)
    print("psosp ", allfile)
    print("qwifjw ", folderList)

    # for files in os.walk(path):
    #     print("files", files)
    #     for basename in files:
    #         print("basename", basename)
    #         if fnmatch.fnmatch(basename, pattern):
    #             filename = os.path.join(root, basename)
    # print("filename ", filename)

    for smali in smaliList:
        
        print("vbnjm", smali)
        log.info("Parsing " + smali)
        f = open(smali, 'r')
        smali_class = parseSmaliFiles(f)
        classes[smali_class['ClassName']] = smali_class

    for sharedobj in util.find_files(path, '*.so'):
        log.info("Processing: " + sharedobj)
        f = open(sharedobj, 'r')
        smali_class = parseSmaliFiles(f)
        sharedobj_strings[sharedobj] =  util.unique_strings_from_file(sharedobj)


    log.info("Parsing Complete")
    return { 'classes' : classes,
             'sharedobjs' : sharedobj_strings }

if __name__ == '__main__':
    # D:\8th_semester\my_8th_semester\SPL3\YouTube_v16.05.37_apkpure.com\smali\android\arch\lifecycle
    path="D:\\8th_semester\\my_8th_semester\\SPL3\\YouTube_v16.05.37_apkpure.com\\smali\\android\\arch\\lifecycle"
    parseDir(path)