import vertex
import runNetworks
import numpy.random as random 

modelRunning = "sampled"

def newSample():
  joint = {};
  rand1 = random.rand();
  if rand1 < 0.3:
    joint["a"] = 1;
  else:
    joint["a"] = 0;
  rand2 = random.rand();
  if joint["a"] == 1 and rand2 < 0.7:
    joint["b"] = 1;
  elif joint["a"] == 1:
    joint["b"] = 0;
  if joint["a"] == 0 and rand2 < 0.4:
    joint["b"] = 1;
  else:
    joint["b"] = 0;
  rand3 = random.rand();
  if joint["b"] == 1 and rand3 < 0.2:
    joint["c"] = 1;
  elif joint["b"] == 1:
    joint["c"] = 0;
  if joint["b"] == 0 and rand3 < 0.6:
    joint["c"] = 1;
  else:
    joint["c"] = 0;
  rand4 = random.rand();
  if joint["c"] == 1 and rand4 < 0.5:
    joint["d"] = 1;
  elif joint["c"] == 1:
    joint["d"] = 0;
  if joint["c"] == 0 and rand4 < 0.75:
    joint["d"] = 1;
  else:
    joint["d"] = 0;
  rand5 = random.rand();
  if joint["d"] == 1 and rand5 < 0.8:
    joint["e"] = 1;
  elif joint["d"] == 1:
    joint["e"] = 0;
  if joint["d"] == 0 and rand5 < 0.6:
    joint["e"] = 1;
  else:
    joint["e"] = 0;
  return joint;

def runAveragedNetwork(topologicalOrdering):
  averagedNet = averagedBayesianNetwork.AveragedBayesianNetwork(topologicalOrdering=topologicalOrdering);
  dataSamples = [];
  for samp in range(10):
    sampledDataPoint = newSample();
    dataSamples.append(sampledDataPoint);
  averagedNet.addModel(dataSamples);
    #if (len(dataSamples) % 100 == 0):
      #averagedNet.addModel(dataSamples[len(dataSamples) - 100 :]);
  finalEdges = averagedNet.getLearnedEdges();
  for e in finalEdges:
    print("child is " + e.endVertex.name);
    print("parent is " + e.startVertex.name);
  print(finalEdges);

if __name__ == "__main__":
  binaryVals = [0, 1];
  a = vertex.Vertex(parents = [], possibleParents = [], vals=binaryVals, name="a");
  b = vertex.Vertex(parents = [], possibleParents = [a], vals=binaryVals, name="b");
  c = vertex.Vertex(parents = [], possibleParents = [a,b], vals=binaryVals, name="c");
  d = vertex.Vertex(parents = [], possibleParents = [a,b,c], vals=binaryVals, name="d");
  e = vertex.Vertex(parents = [], possibleParents = [a,b,c,d], vals=binaryVals, name="e");
  topologicalOrdering = [a,b,c,d,e];
  if (modelRunning == "averaged"):
    runNetworks.runAveragedNetwork(topologicalOrdering, newSample);
  elif (modelRunning == "incremental"):
    runNetworks.runIncrementalNetwork(topologicalOrdering, newSample);
  elif (modelRunning == "sampled"):
    runNetworks.runSampledNetwork(topologicalOrdering, newSample);
