#Codigo en C

class Traduccion:
    def __init__(self):
        self.header = \
'#include <iostream>    \n \
 #include <vector>      \n \
using namespace std;    \n \
struct edge;          \n \
struct node{          \n  \
int data;               \n  \
vector<edge> vec_edges;  \n  \
};                  \n \
struct edge{     \n \
vector<node> vec_nodes; \n \
};                  \n' 
