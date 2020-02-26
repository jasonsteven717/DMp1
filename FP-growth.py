# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:24:09 2019

@author: TsungYuan
"""
import numpy as np 
import pandas as pd
import csv
import time

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      
        self.children = {} 
    def inc(self, numOccur):
        self.count += numOccur
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)
            
def load_data(file):
    data_set = []
    i = 0
    with open(file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if i == 0: 
                i+=1 
                continue
            data_set.append(row)
    return data_set

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def createTree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  
        if headerTable[k] < minSup: 
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None 
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet: 
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable 

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count) 
    else:   
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):   
    while (nodeToTest.nodeLink != None):    
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
    
def ascendTree(leafNode, prefixPath): 
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
        
def findPrefixPath(basePat, treeNode): 
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    sorted_headerTable = sorted(headerTable.items(), key=lambda p: p[1][0])  
    bigL = [v[0] for v in sorted_headerTable] 
    for basePat in bigL:
        newFreqSet = preFix.copy()  
        newFreqSet.add(basePat)     
        freqItemList.append(newFreqSet) 
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  
        myCondTree, myHead = createTree(condPattBases, minSup) 
        if myHead != None:
            #myCondTree.disp()
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList) 

if __name__ == "__main__":
    start = time.clock()
    minSup = 1000
    data_set = load_data('adult.csv')
    initSet = createInitSet(data_set)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    end = time.clock()
    freqItems = [] 
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems) 
    #print(freqItems) 
    print(len(findPrefixPath('>50K', myHeaderTab['>50K'][1])),"rules : ")
    print(findPrefixPath('>50K', myHeaderTab['>50K'][1]))
    print("time cost : ",end-start)
