#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <stdio.h>
using namespace std;

class Node {
    public:
    int id;
    int parent_id;
    Node *parent;
    std::vector<Node*> children;
    int total;

    Node(int, int);
    ~Node();
    int getTotal();
};

Node::Node (int iid, int iparent_id){
    id = iid;
    parent_id = iparent_id;
    parent = NULL;
    total = 0;
}

Node::~Node(){
}

int Node::getTotal(){
    if (total == 0){
        total = 1;
        std::vector<Node*>::iterator it;
        for (it=children.begin(); it < children.end(); it++){
            total += (*it)->getTotal();
        }
    }
    return total;
}

typedef std::map<int, Node*> Dict;
typedef Dict::const_iterator It;

class Tree{
    public:
        Node *root;
        Dict nodes;

    Tree();
    Tree(Dict);
    ~Tree();
    void BuildTree();
    void printTotals();
    void printCount();
};

Tree::Tree(){
    root = NULL;
    
}

Tree::Tree(Dict d){
    root = NULL;
    nodes = d;
}

Tree::~Tree(){

}

void Tree::printCount(){
    int total = 0;
    int id = 0;
    for(It it(nodes.begin()); it != nodes.end(); ++it){
        if (it->second->getTotal() > total){
            total = it->second->getTotal();
            id = it->second->id;
        }
    }
    printf("Biggest total number of replies(%d): %d\n", id, total);
}

void Tree::BuildTree(){
    for (It it(nodes.begin()); it != nodes.end(); ++it){
        Node *parent;
        //cout << it->second->parent_id << endl;
        if (nodes.count(it->second->parent_id)>0){
            parent = nodes.find(it->second->parent_id)->second;
            it->second->parent = parent;
            parent->children.push_back(it->second);
        }
    }
}

void Tree::printTotals(){
    int ts = 0;
    int id = 0;
    for (It it(nodes.begin()); it != nodes.end(); ++it){
        int s = it->second->children.size();
        if (s > ts){
            ts = s;
            id = it->second->id;
        }
    }
    printf("Most single level replies(%id): %d\n", id, ts);
}

int main(){
    ifstream coms;
    string line;

    int id,pid,sep;
    Dict nodes;

    coms.open("comments.txt");
    while(getline(coms,line)){
        sscanf(line.c_str(), "%d,%d", &id, &pid);
        nodes[id] = new Node(id, pid);
    }
    coms.close();
    
    Tree tree;
    tree.nodes = nodes;
    tree.BuildTree();
    tree.printTotals();
    tree.printCount();
    
    return 0;
}
