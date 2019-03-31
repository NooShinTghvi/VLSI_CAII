'''
 CA2 - Part2 -> calculate 5 best inputs w.r.t gate leakages
 Negar Mirgati - Nooshin Taghavi
'''
import itertools

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
        print('to be calculated first')
        return None


def calcTotalLeakage(nodeDict, sortedLines) :
    leakageVal = 0
    for x in sortedLines :
            lineParts = x.split(' ')
            parts = x.split(' ')
            val = calcProbsForNode(nodeDict, parts)
            leakageVal += val

    return leakageVal
                


# add wires as nodes to probability dict
def createMapOfNodes(nodeDict, x) :
    lineParts = x.replace('\n', '').replace('wire', '').replace(' ', '').split(',')
    for node in lineParts :
        nodeDict[node] = 0

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
def calcProbsForNode(nodeDict, parts) :
    gate = parts[2]
    if(gate == 'INV_X1') :
        (inputNode, outputNode) = getInputAndOutputsOne(parts)
        nodeDict[outputNode] = ~(nodeDict[inputNode])
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
        print('to be calculated first')
        return None

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

def nand2(A, B) :
    return (~(A & B))

def nor2(A, B): 
    return (~(A | B))


# print calculated results in results.txt file
def printResultsInOutputFile(nodeDict, alphaDict):
    outfile = open('results.txt', 'w')
    for key in nodeDict.keys():
        line = (key + ' : ') + 'p(n = 1) : ' + str(nodeDict[key]) + ', p(n = 0) :' +  str(1 - nodeDict[key])
        if(alphaDict.has_key(key)):
            line += ', alpha : ' + str(alphaDict[key])
        
        print >> outfile, line


# return leakage based on gate type and its inputs
def calcLeakageTwo(gate, A, B) :
    if(gate == 'NAND2_X1'):
        if(A == 0 and B == 0):
            return 11
        elif ((A == 0 and B == 1) or (A == 1 and B == 0)):
            return 38
        else:
            return 58
    else:
        if(A == 0 and B == 0):
            return 47
        elif ((A == 0 and B == 1) or (A == 1 and B == 0)):
            return 30
        else :
            return 25

def calcLeakageOne(A):
    if(A == 0):
        return 19
    else : 
        return 18
        

def main() :
    leakageValues = []
    counter = 0
    sortedLines = getSortedLines()
    for x in (["".join(seq) for seq in itertools.product("01", repeat=16)]) :
        nodeDict = {}
        addPrimaryInputsToDict(nodeDict, x)
        leakageValues.append(calcTotalLeakage(nodeDict, sortedLines))
        print(counter)
        counter += 1
    
    sortedList = sorted(leakageValues)
    for i in range(0, 6):
        print (sortedList[i])
    print (sortedList(len(sortedList) - 1))


if __name__== "__main__":
      main()

