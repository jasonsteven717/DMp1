import pandas as pd
import re

def ibm(path = 'data/output.data'):
    trans = {}
    with open('IBM.data', 'r') as read:
        lines = read.readlines()
        temp_tid = 0
        for line in lines:
            line = re.split(r"\W+", line)
            tid, items = str(line[2]), str(line[3])
            if temp_tid != tid:
                temp_tid = tid
                trans[temp_tid] = {items}
            else:
                trans[temp_tid].add(items)

    return trans



def output(trans, filename, support = 0):
    items = []
    for tran in trans: items.extend(trans[tran])
    items = list(set(items))

    f = open('weka.csv', "w+")

    first = True
    for i in items:
        if first: first = False
        else: f.write(",")
        f.write(i)
    f.write("\n")

    for tran in trans:
        first = True
        #for s in range(support[i]):
        for item in items:
            if first: first =  False
            else: f.write(",")
            if item in trans[tran]: f.write("y")
            else: f.write(" ")

        f.write("\n")


if __name__ == '__main__':


    # for ibm
    trans = ibm()
    output(trans, 'weka.csv')