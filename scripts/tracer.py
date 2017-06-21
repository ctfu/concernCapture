# Created at: July 05, 2016     Last modified: April 11, 2017
# Provided with a source class, trace through all its calling classes
# imported file format: class1;class2;label
import fileinput
import math

adjList = {}
visited = {}
#parent dict to store the parent node of visited node
parent = {}
#edges dict to count the frequency of edges
edges = {}
target = 'CarSalesSystem'
#mark the cutting point
markers = []

for line in fileinput.input():
  tokens = line.rstrip('\n').split(';')
  if "dashed" not in tokens[2]:
    #get all the edges
    edge = tokens[0] + "->" + tokens[1]
    if edge in edges:
      edges[edge] += 1
    else:
      edges[edge] = 1
    #get all the unique nodes
    if tokens[0] not in visited:
      visited[tokens[0]] = False
    if tokens[1] not in visited:
      visited[tokens[1]] = False
    #build the adjacency list
    if tokens[0] in adjList:
      #strip the rear quotation mark before adding
      tokens[2] = tokens[2].strip('"')
      adjList[tokens[0]].append((tokens[1], tokens[2]))
    else:
      #strip the rear quotation mark before adding
      tokens[2] = tokens[2].strip('"')
      adjList[tokens[0]] = [(tokens[1], tokens[2])]
    if tokens[1] not in adjList:
      adjList[tokens[1]] = []

# Modified DFS algorithm to search through the classes connecting to the searching target
def dfs_visite(adjList, visited, source):
  visited[source] = True
  for w in adjList[source]:
    edge = source + "->" + w[0]
    if (not visited[w[0]]):
      parent[w[0]] = source
      #add the edge frequency and add back the quatation mark before print
      print source, "->", w[0], "[", w[1], str(edges[edge]) + '"', "penwidth=", math.log(edges[edge]+1), "]"
      if(w[0] in markers):
        return
      dfs_visite(adjList, visited, w[0])
    else:
      if(w[0] != source and parent.get(w[0]) != None and parent[w[0]] != source):
        parent[w[0]] = source
        #add the edge frequency and add back the quatation mark before print
        print source, "->", w[0], "[", w[1], str(edges[edge]) + '"', "penwidth=", math.log(edges[edge]+1), "]"


#generating dot file
print "digraph grpah {"
print "overlap=false"

dfs_visite(adjList, visited, target)

#print markers[0], "[style=\"filled\", fillcolor=\"red\"]"

print "}"
