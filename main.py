import logging
import os
import sys

logging.basicConfig(
    filename="skip.log",
    filemode='w',
    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

logger = logging.getLogger("skip.log")
debugList = []

def read_file():
    fileInDirectory = os.listdir()
    flacInDirectory = []
    for file in fileInDirectory:
        if file[-5:] == ".flac":
            flacInDirectory.append(file)
    return flacInDirectory

def trackInfo(flacInDirectory):
    trackMetadata = []
    for file in flacInDirectory:
        skip = 0
        sampleRate = os.popen("metaflac --show-sample-rate \""+file+"\"").read()
        sampleRate = sampleRate.rstrip('\n')
        if sampleRate == "44100":
            skip = 286
        elif sampleRate == "48000":
            skip = 312
        elif sampleRate == "96000":
            skip = 624
        elif sampleRate == "192000":
            skip = 1248
        md5sum = os.popen("metaflac --show-md5sum \""+file+"\"").read()
        md5sum = md5sum.rstrip('\n')
        trackMetadata.append([file, sampleRate, skip, md5sum])
    return trackMetadata

def PCMsplice(trackMetadata):
    for track in trackMetadata:
        os.popen("flac -8 --skip="+str(track[2])+" -f \""+str(track[0])+"\"").read()
        os.popen("metaflac --set-tag=BP=1 \""+str(track[0])+"\"").read()
        if track[1] != 0:
            debugList.append("Sample rate: "+str(track[1])+"Hz, skipping "+str(track[2])+" samples"+"\n")
        else:
            debugList.append("Error: Skipping"+track[0])
    return
        

def verify(debugList):
    length = int(len(debugList)/3)
    newDebugList = []
    for i in range(length):
        firstMD5 = debugList[i].find("md5")
        firstMD5 = debugList[i][firstMD5+4:]
        secondMD5 = debugList[i+(2*length)].find("md5")
        secondMD5 = debugList[i+(2*length)][secondMD5+4:]
        if firstMD5 == secondMD5:
            newDebugList.append("Failed - "+debugList[i]+" updated md5-"+secondMD5)
        else:
            newDebugList.append("Success - "+debugList[i]+" updated md5-"+secondMD5)
        newDebugList.append(debugList[i+length])
    return newDebugList

def main(debugList):
    flacInDirectory = read_file()
    trackMetadata = trackInfo(flacInDirectory)
    for track in trackMetadata:
        debugList.append("Files before splice: "+" filename-"+str(track[0])+" sampleRate-"+str(track[1])+" skip-"+str(track[2])+" md5-"+str(track[3]))
    skipLog = PCMsplice(trackMetadata)
    trackMetadata = trackInfo(flacInDirectory)
    for track in trackMetadata:
        debugList.append("Files after splice: "+"filename-"+str(track[0])+" sampleRate-"+str(track[1])+" skip-"+str(track[2])+" md5-"+str(track[3]))
    debugList = verify(debugList)
    return debugList

debugList = main(debugList)

for item in debugList:
    logger.debug(item)
