#include <iostream>    
  #include <vector>      
 using namespace std;    
 struct edge;          
 struct node{          
  int data;               
  vector<edge> vec_edges;  
  };                  
 struct edge{     
 vector<node> vec_nodes; 
 };                  
int a;
int b;
int c;
node N;
node M;
edge S;
void main()
{b=100005+3;
a=2;
M.data = 3;
c=10+5;
N.vec_edges.push_back(S);
S.vec_nodes.push_back(N);
M.vec_edges.push_back(S);
S.vec_nodes.push_back(M);
}