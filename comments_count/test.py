#!/usr/bin/python
import sys, time
sys.setrecursionlimit(10000)
#sys.setrecursionlimit(3000)
class Node:
    def __init__(self, pid, parent_id):
        self.pid = pid
        self.parent_id = parent_id
        self.parent = None
        self.children = []
        self.total = 0
        self.chilled = False

    def getTotal(self):
        if self.total == 0:
            total = 1
            for child in self.children:
                total += child.getTotal()
            self.total = total
        return self.total
    
    def getChillen(self):
        if self.chilled:
            return self.chilled
        else:
            l = len(self.children)
            if l > 0:
                for c in self.children:
                    l += c.getChillen()
            self.chilled = l
            return self.chilled

class Tree:
    def __init__(self):
        self.rootNode = None
        self.nodes = dict()

    def BuildTree(self):
        parent = None
        vals = self.nodes.values()
        keys = self.nodes.keys()
        l = len(keys)
        count = 0
        start = time.time()
        for node in vals:
            count += 1
            #if count % 1000 == 0: 
            #    print count
            #    print time.time() - start
            
            #if node.parent_id in keys:
            try:
                node.parent = self.nodes[node.parent_id]
                node.parent.children.append(node)
            except:
                pass

    def printTotal(self):
        total = 0
        for node in self.nodes.values():
            if node.getTotal() > total:
                total = node.getTotal()
        print "Biggest total: "+str(total)
   
    def printChillen(self):
        total = 0
        for node in self.nodes.values():
            if node.getChillen() > total:
                total = node.getChillen()
        print "Biggest child: "+str(total)

    def printChildren(self):
        total = 0
        for node in self.nodes.values():
            l = len(node.children)
            if l > total:
                total = l
        
        print "Biggest children: "+str(total)

nodes = dict()
f = open("comments.txt",'r')
for line in f:
    row = line.split(',',1)
    #print row
    nodes[int(row[0])] = Node(int(row[0]),int(row[1]))
    #tree.nodes[row[0]] = Node(row[0],row[1])
    #print str(row[0])+','+str(row[1])
f.close()
tree = Tree()
tree.nodes = nodes

print "Building"
tree.BuildTree()
print "Childering"
tree.printChildren()
tree.printChillen()
#print "Totalling"
#tree.printTotal()
