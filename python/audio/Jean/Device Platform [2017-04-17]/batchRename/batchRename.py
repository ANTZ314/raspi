import os

recdir = "G:/recordings"
pyrecDir = "C:/Users/Adrian/Documents/python-audio/test"

os.chdir(recdir)
#print (os.getcwd())

for files in os.listdir(recdir):
    #print files
    #print (os.path.splitext(files))
    fileName, fileExt = os.path.splitext(files)
    #print fileName
    #print fileExt
    #print (fileName.split("-"))
    #print (fileName.split("_"))
    fileHead, fileWant = fileName.split("_")
    #print fileHead
    #print fileWant
    #print ("{}{}".format(fileWant, fileExt))
    fileWant = fileWant.replace("-", "_")
    print ("{}{}".format(fileWant, fileExt))
    newName = ("{}{}".format(fileWant, fileExt))
    os.rename(files, newName)















#if fileName.endswith(sharedVariables.globalVariables["waveExt"]):
 #   fullFilePath = os.path.join(dirs, fileName).replace("\\", "/")