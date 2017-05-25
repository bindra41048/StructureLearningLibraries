import BayesianNetwork; 
import edge;
class AveragedBayesianNetwork:

  def __init__(self, topologicalOrdering):
    self.topologicalOrdering = topologicalOrdering;
    self.edgeCounts = {};
    self.numModelsConsidered = 0;
    for childIndex in range(len(topologicalOrdering)):
      for parentIndex in range(childIndex):
        self.edgeCounts[edge.Edge(topologicalOrdering[parentIndex], topologicalOrdering[childIndex])] = 0;
  
  def incrementEdgeCount(self, startVertex, endVertex):
    for e in self.edgeCounts.keys():
      if e.startVertex.name == startVertex.name and e.endVertex.name == endVertex.name:
        self.edgeCounts[e] += 1;

  def addModel(self, data):
    oldVertices = self.topologicalOrdering;
    self.numModelsConsidered += 1;
    newModel = BayesianNetwork.BayesianNetwork(self.topologicalOrdering);
    self.learnEdgesByK3(data, newModel);
    for vert in self.topologicalOrdering:
      vert.parents = [];
    for edge in newModel.edges:
      self.incrementEdgeCount(edge.startVertex, edge.endVertex);
    learnedEdges = self.getLearnedEdges();
    for e in learnedEdges:
      e.endVertex.parents.append(e.startVertex);
    for v in self.topologicalOrdering:
      print("vertex " + v.name + " has parents ");
      for p in v.parents:
        print("p.name");

 
  def getLearnedEdges(self): 
    learnedEdges = [];
    print(self.numModelsConsidered);
    for edge in self.edgeCounts:
      numModelsWithEdge = self.edgeCounts[edge];
      if (numModelsWithEdge >= 0.3 * self.numModelsConsidered):
        learnedEdges.append(edge);
    return learnedEdges;

  def updateCPTNewModel(self, data):
    for vertex in self.topologicalOrdering:
      vertex.setupCPTs(data);

  def edgePresent(self, potentialEdge, model):
    for e in model.getEdges():
      if (e.startVertex.name == potentialEdge.startVertex.name and e.endVertex.name == potentialEdge.endVertex.name): 
        return True;
    return False;

  def learnEdgesByK3(self, data, newModel): 
    for index in range(1, len(self.topologicalOrdering)):
      while (True): 
        currVertex = self.topologicalOrdering[index];
        self.updateCPTNewModel(data);
        currScore = newModel.scoreModel(data);
        maxScoreIncreasingAddition = None;
        currMaxScore = currScore;
        for parentIndex in range(index):
          potentialParent = self.topologicalOrdering[parentIndex];
          potentialEdgeAddition = edge.Edge(potentialParent, currVertex);
          if (not self.edgePresent(potentialEdgeAddition, newModel)): 
            newModel.addEdge(potentialParent, currVertex);
            self.updateCPTNewModel(data);
            modelScore = newModel.scoreModel(data);
            if (modelScore > currMaxScore):
              currMaxScore = modelScore;
              maxScoreIncreasingAddition = potentialParent;
            newModel.removeEdge(potentialParent, currVertex);
        if (maxScoreIncreasingAddition == None):
          break;
        newModel.addEdge(maxScoreIncreasingAddition, currVertex);
        #maxScoreIncreasingAddition = None;
