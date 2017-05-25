import math
import edge
class BayesianNetwork:

  def __init__(self, topologicalOrdering): 
    self.topologicalOrdering = topologicalOrdering; 
    self.edges = [];
  
  def getEdges(self):
    return self.edges; 
  
  def addEdge(self, parentVert, vert):
    vert.addParent(parentVert);
    self.edges.append(edge.Edge(parentVert, vert));

  def removeEdge(self, parentVert, vert):
    vert.removeParent(parentVert);
    edgeToRemove = None;
    for edge in self.edges:
      if edge.startVertex == parentVert and edge.endVertex == vert:
        edgeToRemove = edge;  
    self.edges.remove(edgeToRemove);

  def scoreModel(self, data):
    modelScore = 0;
    for vertex in self.topologicalOrdering:
      modelScore += self.vertexContributionToModelScore(vertex, data);
    return modelScore;

  def vertexContributionToModelScore(self, vertex, data):
    vertexComplexity = vertex.numFreeParameters() * 0.5 * math.log(len(data));
    vertexInfo = 0;
    for dataPoint in data:
      parentJointAssignment = '';
      for parent in vertex.parents:
        parentJointAssignment += str(dataPoint[parent.name]);
      vertexInfo += math.log(vertex.currCPTTable[parentJointAssignment][dataPoint[vertex.name]]);
    return vertexInfo - vertexComplexity;
