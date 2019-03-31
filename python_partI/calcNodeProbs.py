'''
 CA2 - Part1 -> calculate p(n = 0), p(n = 1), p(0 -> 1) using input.txt file and part1.v
 Negar Mirgati - Nooshin Taghavi
'''
import re

def calcSwitching() :
    nodeDict = {}
    alphaDict = {}
    addPrimaryInputsToDict(nodeDict)
    inputFile = open('part1.v', 'r').read().split(';')
    test = []
    for x in inputFile :
        lineParts = x.split(' ')
        if 'module' not in lineParts and 'input' not in lineParts and 'output' not in lineParts and '\nendmodule' not in lineParts and 'wire' not in lineParts:
            #if 'wire' not in lineParts :
                #createMapOfNodes(nodeDict, x)
            #else :
            parts = x.split(' ')
            calcProbsForNode(nodeDict, alphaDict, parts)
    
    printResultsInOutputFile(nodeDict, alphaDict)
                


# add wires as nodes to probability dict
def createMapOfNodes(nodeDict, x) :
    lineParts = x.replace('\n', '').replace('wire', '').replace(' ', '').split(',')
    for node in lineParts :
        nodeDict[node] = 0

# add primary inputs to probability dict
def addPrimaryInputsToDict(nodeDict) :
    counter = 0
    inputFile = open('probabilities.txt', 'r')
    for line in inputFile :
        if(counter <= 7):
            nodeDict['A[' + str(counter) + ']'] = float(line)
        else :
            nodeDict['B[' + str(counter - 8) + ']'] = float(line)
        counter += 1

    inputFile.close()

# calculate output node probabilities and alpha based on gate type and calculated probabilities 
def calcProbsForNode(nodeDict, alphaDict, parts) :
    gate = parts[2]
    if(gate == 'INV_X1') :
        (inputNode, outputNode) = getInputAndOutputsOne(parts)
        nodeDict[outputNode] = calcInv1Prob(nodeDict[inputNode])
        alphaDict[outputNode] = calcAlpha(nodeDict[outputNode])

    elif(gate == 'NAND2_X1' or gate == 'XOR2_X1' or gate == 'NOR2_X1' or gate == 'OR2_X1' or gate == 'AND2_X1' or gate == 'XNOR2_X1'):
        (inputNode1, inputNode2, outputNode) = getInputAndOutputsTwo(parts)
        nodeDict[outputNode] = calcTwoInputProb(gate, nodeDict[inputNode1], nodeDict[inputNode2])
        alphaDict[outputNode] = calcAlpha(nodeDict[outputNode])

    elif(gate == 'NAND3_X1' or gate == 'NOR3_X1' or  gate == 'OR3_X1' or gate == 'AND3_X1') :
        (inputNode1, inputNode2, inputNode3, outputNode) = getInputAndOutputsThree(parts)
        nodeDict[outputNode] = calcThreeInputProb(gate, nodeDict[inputNode1], nodeDict[inputNode2], nodeDict[inputNode3])
        alphaDict[outputNode] = calcAlpha(nodeDict[outputNode])

    elif(gate == 'NAND4_X1') :
        (inputNode1, inputNode2, inputNode3, inputNode4, outputNode) = getInputAndOutputsFour(parts)
        nodeDict[outputNode] = calcNand4Prob(nodeDict[inputNode1], nodeDict[inputNode2], nodeDict[inputNode3], nodeDict[inputNode4])
        alphaDict[outputNode] = calcAlpha(nodeDict[outputNode])

    else :
        print("Error Occured")

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

# parse three input gate input and outputs
def getInputAndOutputsThree(parts):
    s_inp1 = parts[5]
    s_inp2 = parts[6]
    s_inp3 = parts[7]
    s_out = parts[8]
    inputNode1 =  (s_inp1[s_inp1.find("(")+1:s_inp1.find(")")])
    inputNode2 =  (s_inp2[s_inp2.find("(")+1:s_inp2.find(")")])
    inputNode3 =  (s_inp3[s_inp3.find("(")+1:s_inp3.find(")")])
    outputNode = (s_out[s_out.find("(")+1:s_out.find(")")])
    return (inputNode1, inputNode2, inputNode3, outputNode)

# parse four input gate input and outputs
def getInputAndOutputsFour(parts):
    s_inp1 = parts[5]
    s_inp2 = parts[6]
    s_inp3 = parts[7]
    s_inp4 = parts[8]
    s_out = parts[9]
    inputNode1 =  (s_inp1[s_inp1.find("(")+1:s_inp1.find(")")])
    inputNode2 =  (s_inp2[s_inp2.find("(")+1:s_inp2.find(")")])
    inputNode3 =  (s_inp3[s_inp3.find("(")+1:s_inp3.find(")")])
    inputNode4 =  (s_inp4[s_inp4.find("(")+1:s_inp4.find(")")])
    outputNode = (s_out[s_out.find("(")+1:s_out.find(")")])
    return (inputNode1, inputNode2, inputNode3, inputNode4, outputNode)

# print calculated results in results.txt file
def printResultsInOutputFile(nodeDict, alphaDict):
    outfile = open('results.txt', 'w')
    for key in nodeDict.keys():
        line = (key + ' : ') + 'p(n = 1) : ' + str(nodeDict[key]) + ', p(n = 0) :' +  str(1 - nodeDict[key])
        if(alphaDict.has_key(key)):
            line += ', alpha : ' + str(alphaDict[key])
        
        print >> outfile, line

    

def calcInv1Prob(A):
    return (1 - A)

# calculate P(n = 1) for all 2-input gates used in part1.v
def calcTwoInputProb(gate, A, B) :
    if(gate == 'NAND2_X1'):
         return (1 - A*B)
    elif(gate == 'XOR2_X1'): 
        return ((A * (1-B)) + (B * (1 - A)))
    elif(gate == 'NOR2_X1'):
        return((1 - A)* (1 - B))
    elif(gate == 'OR2_X1'):
        return (1 - (1 - A) * (1 - B))
    elif(gate == 'AND2_X1'):
        return A * B
    else :
        return ( (A * B) + ((1 - A) * (1 - B)) )

# calculate P(n = 1) for all 3-input gates used in part1.v
def calcThreeInputProb(gate, A, B, C):
    if(gate == 'NAND3_X1'):
        return (1 - A * B * C)
    elif(gate == 'NOR3_X1'):
        return (1 - A) * (1 - B) * (1 - C)
    elif(gate == 'OR3_X1'):
        return (1 - (1 - A) * (1 - B) * (1 - C))
    else :
        return A * B * C

# calculate P(n = 1) for all 4-input gates used in part1.v
def calcNand4Prob(A, B, C, D):
    return (1 - (A * B * C * D))

# calculate P(0 -> 1)
def calcAlpha(p) :
    return p * (1 - p)

def main() :
    calcSwitching()

if __name__== "__main__":
      main()

