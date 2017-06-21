# Class Frequency analysis
# Created at: Feburary 27, 2017
# File input format: class1;class2;label

import fileinput

fileInfo = {}
files = []
nodes = []
analysis = {}

def search(fileClasses, node):
    if node not in fileClasses:
        return False
    return True

for line in fileinput.input():
    tokens = line.rstrip('\n').split(';')
    if "dashed" not in tokens[2]:
        fn = fileinput.filename()
        # get a list of files
        if fn not in files:
            files.append(fn)
        if fn not in fileInfo:
            fileInfo[fn] = []
        if tokens[0] not in fileInfo[fn]:
            fileInfo[fn].append(tokens[0])
        if tokens[1] not in fileInfo[fn]:
            fileInfo[fn].append(tokens[1])
        if tokens[0] not in nodes:
            nodes.append(tokens[0])
        if tokens[1] not in nodes:
            nodes.append(tokens[1])

for node in nodes:
    freq = 0
    for fn in files:
        if search(fileInfo[fn], node):
            freq = freq + 1
    analysis[node] = freq

#output frequency analysis 
for k,v in sorted(analysis.iteritems(), key=lambda (k,v):(v,k), reverse=True):
    print k,v


            



