import averagedBayesianNetwork
import incrementalNetwork
import sampledNetwork
import BayesianNetwork
import vertex

def getCopy(v):
  return vertex.Vertex(parents = [], possibleParents = [], vals=binaryVals, name="a");

def printNetworkScore(topologicalOrdering, data, outFile):
  totalScore = 0;
  for v in topologicalOrdering:
    v.setupCPTs(data);
    print(v.contributionToModelScore(data));
    totalScore += v.contributionToModelScore(data); 
  outFile.write(str(totalScore) + "\n");
  
def runSampledNetwork(topologicalOrdering, newSample):
  outfile = open('sampleWrite.txt', 'w');
  sampledNet = sampledNetwork.SampledNetwork(topologicalOrdering);
  dataSamples = [];
  for samp in range(101):
    sampledPoint = newSample();
    dataSamples.append(sampledPoint);
  for partial in range(101): 
    if (partial % 5 == 0 and partial > 0):
      sampledNet.processNewData(dataSamples[partial - 5 : partial]);
      printNetworkScore(sampledNet.topologicalOrdering, dataSamples, outfile);

def runAveragedNetwork(topologicalOrdering, newSample):
  outfile = open('averagedWrite.txt', 'w');
  averagedNet = averagedBayesianNetwork.AveragedBayesianNetwork(topologicalOrdering=topologicalOrdering);
  dataSamples = [];
  for samp in range(101):
    sampledDataPoint = newSample();
    dataSamples.append(sampledDataPoint);
  for partial in range(101):
    if (partial % 5 == 0 and partial > 0):
      averagedNet.addModel(dataSamples[partial-5:partial]);
      printNetworkScore(averagedNet.topologicalOrdering, dataSamples, outfile);
  averagedNet.getLearnedEdges();

def runIncrementalNetwork(topologicalOrdering, newSample):  
  outfile = open('incrementalWrite.txt', 'w');
  incrementalNet = incrementalNetwork.IncrementalNetwork(topologicalOrdering = topologicalOrdering);
  dataSamples = [];
  for samp in range(101):
    dataSamples.append(newSample());
  for partial in range(101):
    if (partial % 5 == 0 and partial > 0):
      incrementalNet.updateModel(dataSamples[partial - 5 : partial]);
      printNetworkScore(incrementalNet.topologicalOrdering, dataSamples, outfile);
