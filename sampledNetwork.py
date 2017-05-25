import random;
import Queue;
import BayesianNetwork;

MAX_SAMPLES = 10;

class IdealUpdate:
  
  def __init__(self, addition, vertex, parentInQuestion):
    self.addition = addition;
    self.vertex = vertex;
    self.parentInQuestion = parentInQuestion;

class Sample:
  
  def __init__(self, joint):
    self.joint = joint;
    self.randNum = random.random();

class SampledNetwork:

  def __init__(self, topologicalOrdering):
    self.topologicalOrdering = topologicalOrdering;
    self.samples = {};
    for vert in self.topologicalOrdering:
      self.samples[vert.name] = {};
      for val in vert.vals:
        self.samples[vert.name][val] = Queue.PriorityQueue(maxsize = MAX_SAMPLES);
    self.underlyingModel = BayesianNetwork.BayesianNetwork(topologicalOrdering); 
        
  def processNewSample(self, sample):
    for vertex in self.topologicalOrdering:
      vertVal = sample.joint[vertex.name];
      if (self.samples[vertex.name][vertVal].full()):
        oldSampleRandNum, oldSampleJoint = self.samples[vertex.name][vertVal].get();
        if oldSampleRandNum > sample.randNum:
          self.samples[vertex.name][vertVal].put((oldSampleRandNum, oldSampleJoint));
        else:
          self.samples[vertex.name][vertVal].put((sample.randNum, sample.joint));
      else:
        self.samples[vertex.name][vertVal].put((sample.randNum, sample.joint));
  
  def getJointsFromPQueue(self, pQueue, pQueueCopy, joints):
    while (not pQueue.empty()):
      newDataPoint = pQueue.get();
      pQueueCopy.put(newDataPoint);
      randNum, joint = newDataPoint;
      joints.append(joint);
    print("The size of joints is " + str(len(joints)));

  def updateCountsFromSample(self, vertex, vertexCPTTable):
    for val in vertex.vals:
      jointSamples = [];
      copyPQueue = Queue.PriorityQueue(maxsize = MAX_SAMPLES);
      self.getJointsFromPQueue(self.samples[vertex.name][val], copyPQueue, jointSamples);
      self.samples[vertex.name][val] = copyPQueue;
      for joint in jointSamples:  
        jointParentAssignment = '';
        for parent in vertex.parents:
          jointParentAssignment += str(joint[parent.name]);
        if jointParentAssignment not in vertexCPTTable.keys():
          vertexCPTTable[jointParentAssignment] = {};
          for val in vertex.vals:
            vertexCPTTable[jointParentAssignment][val] = 0;
        vertexVal = joint[vertex.name];
        vertexCPTTable[jointParentAssignment][vertexVal] += 1;

  def marginalizeDataCounts(self, vertexCPTTable, vertex):
    for entry in vertexCPTTable:
      totalCounts = 0;
      for val in vertex.vals:
        totalCounts += vertexCPTTable[entry][val];
      for val in vertex.vals:
        vertexCPTTable[entry][val] = float(vertexCPTTable[entry][val]) / float(totalCounts);  
  
  def updateVertexCPTs(self, vertex):
    vertexCPTTable = {};
    self.updateCountsFromSample(vertex, vertexCPTTable);
    self.marginalizeDataCounts(vertexCPTTable, vertex);
    vertex.currCPTTable = vertexCPTTable;
  
  def getIdealUpdateModel(self):
    idealChange = None;
    largestIncrease = 0;
    for vertex in self.topologicalOrdering:
      self.updateVertexCPTs(vertex);
      vertexSamplePoints = [];
      for val in vertex.vals:
        copyPQueue = Queue.PriorityQueue(maxsize = MAX_SAMPLES);
        sampleJoints = [];
        self.getJointsFromPQueue(self.samples[vertex.name][val], copyPQueue, sampleJoints);
        self.samples[vertex.name][val] = copyPQueue;
        print("The sample joints is " + str(sampleJoints));
        for dataPoint in sampleJoints:
          vertexSamplePoints.append(dataPoint);
      currVertexScore = self.underlyingModel.vertexContributionToModelScore(vertex, vertexSamplePoints);
      for parent in vertex.possibleParents:
        addition = True;
        if (parent in vertex.parents):
          self.underlyingModel.removeEdge(parent, vertex);
          addition = False;
        else:
          self.underlyingModel.addEdge(parent, vertex);
        self.updateVertexCPTs(vertex);
        newScore = self.underlyingModel.vertexContributionToModelScore(vertex, vertexSamplePoints);
        if (newScore - currVertexScore) > largestIncrease:
          largestIncrease = newScore - currVertexScore;
          idealChange = IdealUpdate(addition, vertex, parent);
        #backtrack
        if (not addition):
          self.underlyingModel.addEdge(parent, vertex);
        else:
          self.underlyingModel.removeEdge(parent, vertex);
    return idealChange;

  def processNewData(self, data):
    for dataPoint in data:
      print(dataPoint);
      samp = Sample(dataPoint);
      self.processNewSample(samp);
    idealUpdateModel = self.getIdealUpdateModel()
    if (idealUpdateModel == None):
      return;
    if (idealUpdateModel.addition == True):
      self.underlyingModel.addEdge(idealUpdateModel.parentInQuestion, idealUpdateModel.vertex);
    else:
      self.underlyingModel.removeEdge(idealUpdateModel.parentInQuestion, idealUpdateModel.vertex);
