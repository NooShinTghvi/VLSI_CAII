'''
 CA2 - Part2 -> calculate 5 best inputs w.r.t gate leakages
 Negar Mirgati - Nooshin Taghavi
'''
import itertools
import operator

def getSortedLines() :
    sortedLines = []
    visitedNodes = {}
    addPrimaryInputsToDict(visitedNodes, '0000000000000000')
    inputFile = open('part2.v', 'r').read().split(';')
    while(inputFile):
        for x in inputFile :
            lineParts = x.split(' ')
            if 'module' not in lineParts and 'input' not in lineParts and 'output' not in lineParts and '\nendmodule' not in lineParts and 'wire' not in lineParts:
                parts = x.split(' ')
                val = canBeCalculated(visitedNodes, parts)
                if(val != None) :
                    sortedLines.append(x)
                    inputFile.remove(x)
            else:
                inputFile.remove(x)
    return sortedLines

def canBeCalculated(nodeDict, parts) :
    gate = parts[2]
    if(gate == 'INV_X1') :
        (inputNode, outputNode) = getInputAndOutputsOne(parts)
        if((nodeDict.has_key(inputNode))) : 
            nodeDict[outputNode] = ~(nodeDict[inputNode])
            return 1
        else :
            return None

    elif(gate == 'NAND2_X1'):
        (inputNode1, inputNode2, outputNode) = getInputAndOutputsTwo(parts)
        if((nodeDict.has_key(inputNode1) and nodeDict.has_key(inputNode2))) : 
            nodeDict[outputNode] = nand2(nodeDict[inputNode1], nodeDict[inputNode2])
            return 1
        else :
            return None

    elif(gate == 'NOR2_X1') :
        (inputNode1, inputNode2, outputNode) = getInputAndOutputsTwo(parts)
        if((nodeDict.has_key(inputNode1) and nodeDict.has_key(inputNode2))) : 
            nodeDict[outputNode] = nor2(nodeDict[inputNode1], nodeDict[inputNode2])
            return 1
        else :
            return None
    else :
        print('ERR occured')
        return None


def calcTotalLeakage(nodeDict, sortedLines) :
    leakageVal = 0
    for x in sortedLines :
            lineParts = x.split(' ')
            parts = x.split(' ')
            val = getLeakageOfGate(nodeDict, parts)
            leakageVal += val
    return leakageVal
                
# add primary inputs to probability dict
def addPrimaryInputsToDict(nodeDict, input) :
    counter = 0
    for val in input :
        if(counter <= 7):
            nodeDict['A[' + str(counter) + ']'] = int(val)
        else :
            nodeDict['B[' + str(counter - 8) + ']'] = int(val)
        counter += 1

# calculate output node values and leakage based on gate inputs
def getLeakageOfGate(nodeDict, parts) :
    gate = parts[2]
    if(gate == 'INV_X1') :
        (inputNode, outputNode) = getInputAndOutputsOne(parts)
        nodeDict[outputNode] = inverter1(nodeDict[inputNode])
        return (calcLeakageOne(nodeDict[inputNode]))


    elif(gate == 'NAND2_X1'):
        (inputNode1, inputNode2, outputNode) = getInputAndOutputsTwo(parts)
        nodeDict[outputNode] = nand2(nodeDict[inputNode1], nodeDict[inputNode2])
        return (calcLeakageTwo(gate, nodeDict[inputNode1], nodeDict[inputNode2]))


    elif(gate == 'NOR2_X1') :
        (inputNode1, inputNode2, outputNode) = getInputAndOutputsTwo(parts)
        nodeDict[outputNode] = nor2(nodeDict[inputNode1], nodeDict[inputNode2])
        return (calcLeakageTwo(gate, nodeDict[inputNode1], nodeDict[inputNode2]))

    else :
        print("ERR OCCURED!!!!!!!")

# parse one input gate input and outputs
def getInputAndOutputsOne(parts):
    s_inp = parts[5]
    s_out = parts[6]
    inputNode =  (s_inp[s_inp.find("(")+1:s_inp.find(")")])
    outputNode = (s_out[s_out.find("(")+1:s_out.find(")")])
    return(inputNode, outputNode)

# parse two input gate input and outputs
def getInputAndOutputsTwo(parts):
    s_inp1 = parts[5]
    s_inp2 = parts[6]
    s_out = parts[7]
    inputNode1 =  (s_inp1[s_inp1.find("(")+1:s_inp1.find(")")])
    inputNode2 =  (s_inp2[s_inp2.find("(")+1:s_inp2.find(")")])
    outputNode = (s_out[s_out.find("(")+1:s_out.find(")")])
    return(inputNode1, inputNode2, outputNode)

def inverter1(A) :
    if(A == 1) :
        return 0
    elif(A == 0):
        return 1
    else :
        print("ERRRRRRRRRRR")

def nand2(A, B) :
    if(A is None or B is None):
        return None
    if(A == 1 and B == 1):
        res = 0
    else :
        res = 1  
    return res
   
def nor2(A, B): 
    if(A is None or B is None):
        return None
    if(A == 0 and B == 0) :
        res = 1
    else : 
        res = 0 
    return res


# print calculated results in results.txt file
def printResults(leakageValues, inputs):
    outfile = open('results.txt', 'w')
    sorted_x = sorted(leakageValues.items(), key=operator.itemgetter(1))
    for i in range(0, 6):
        index = sorted_x[i][0]
        line = 'input : ' + inputs[index] + ' leakge = ' + str(sorted_x[i][1])
        print(line)
        print >> outfile, line
    #print(sorted_x[len(sorted_x)-1])


# return leakage based on gate type and its inputs for two input gates
def calcLeakageTwo(gate, A, B) :
    if(gate == 'NAND2_X1'):
        if(A == 0 and B == 0):
            return 11
        elif ((A == 0 and B == 1) or (A == 1 and B == 0)):
            return 38
        elif(A == 1 and B == 1):
            return 58
        else :
            print("ERR OCCURED")

    elif(gate == 'NOR2_X1'):
        if(A == 0 and B == 0):
            return 47
        elif ((A == 0 and B == 1) or (A == 1 and B == 0)):
            return 30
        elif(A == 1 and B == 1) :
            return 25
    else :
        print("ERR OCCURED")

# return leakage based on gate type and its inputs for one input gates
def calcLeakageOne(A):
    if(A == 0):
        return 19
    elif (A == 1)  : 
        return 18
    else :
        print("ERR OCCURED")
        
def main() :
    leakageValues = {}
    inputs = []
    counter = 0
    sortedLines = getSortedLines()
    for x in (["".join(seq) for seq in itertools.product("01", repeat=16)]) :
        nodeDict = {}
        addPrimaryInputsToDict(nodeDict, x)
        leakageValues[counter] = calcTotalLeakage(nodeDict, sortedLines)
        inputs.append(x)
        print(counter)
        counter += 1
    
    printResults(leakageValues, inputs)
  
if __name__== "__main__":
      main()