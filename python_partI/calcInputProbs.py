from __future__ import division
def calcProbabilities() :
    counts = [0] * 16
    inputFile = open("../input.txt","r") 
    outputFile = open("probabilities.txt","w") 
    for line in inputFile:
        for j in range(0, len(line)):
            if(line[j] != '\n' and line[j] == '1'):
                counts[j] +=1
    
    newList = [ (x / 50000) for x in counts]
    for elem in newList :
         print >> outputFile, elem

    outputFile.close()
    inputFile.close()
    
                

calcProbabilities()