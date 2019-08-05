#  Imports Here
import os

# Package Imports Here
import audioProcessor.inputs as dbspinputs
import audioProcessor.processFunction as processfunction
import audioProcessor.allVariables as sharedVariables
import averageRMS as averageRMS

processfunction.processFile

dbspinputs.bufferSize
dbspinputs.chunkSizeMs

# Starts Loop for Write Buffer of Files
for dirs, subdirs, fileNames in os.walk(sharedVariables.globalVariables["recReadDirectory"]):
    for fileName in fileNames:
        if fileName.endswith(sharedVariables.globalVariables["waveExt"]):
            fullFilePath = os.path.join(dirs, fileName).replace("\\", "/")
            processfunction.processFile(fullFilePath, fileName, dbspinputs.chunkSizeMs, dbspinputs.bufferSize, averageRMS.recAverageRMS)

print("\nDone.")