import math;

class sample:
  
  def __init__(self, jointAssignments, randomNumber):
    self.jointAssignments = jointAssignments;
    self.randomNumber = randomNumber;

class Vertex:
  
  SAMPLE_NUMBER = 50;
  
  def __init__(self, parents, possibleParents, vals, name):
    self.name = name;
    self.parents = parents;
    self.possibleParents = possibleParents;
    self.vals = vals;
    self.currJointDataPoints = 0;
    self.currCPTTable = {};
    '''
    self.jointCounts = {};
    self.parentCounts = {};
    self.samples = {};
    for (val in self.vals):
      self.samples[val] = [];
    self.marginalCounts = {};
    for (val in self.vals):
      self.marginalCounts[val] = 0;
    self.currFrontierDataPoints = 0;
    self.frontierModels = {};
    for (vertex in self.possibleParents):
      if (not vertex in self.parents):
        self.frontierModels[vertex.name] = {}; 
  '''
 
  ''' 
  def updateFrontierModels(self):
    self.currFrontierDataPoints = 0;
    updatedFrontierModels = {};
    for (vertex in self.possibleParents):
      if (not vertex in self.parents):
        updatedFrontierModels[vertex.name] = {};
    self.frontierModels = updatedFrontierModels;

   def updateJointCounts(self, data):
    for (dataPoint in data):
      self.currJointDataPoints += 1;
      jointAssignment = {};
      parentAssignment = {};
      jointAssignment[self.name] = dataPoint[self.name];
      for (parent in self.parents):
        jointAssignments[parent.name] = dataPoint[parent.name];
        parentAssignment[parent.name] = dataPoint[parent.name];
      if (jointAssignment in self.jointCounts):
        self.jointCounts[jointAssignment] += 1;
      else:
        self.jointCounts[jointAssignment] = 1;
      if (parentAssignment in self.parentCounts):
        self.parentCounts[parentAssignment] += 1;
      else:
        self.parentCounts[parentAssignment] = 1;

  def updateFrontierCounts(self, data):
    self.currFrontierDataPoints += len(data);
    for (vertexCand in self.frontierModels):
      for (datapoint in data):
        jointAssignment = {};
        jointAssignment[self.name] = dataPoint[self.name];
        for (parent in self.parents):
          jointAssignment[parent.name] = dataPoint[parent.name];
        jointAssignment[vertexCand] = dataPoint[vertexCand];
      if (jointAssignment in self.frontierModels[vertexCand]):
        self.frontierModels[vertexCand][jointAssignment] += 1;
      else:
        self.frontierModels[vertexCand][jointAssignment] = 1;

  def addSample(self, dataPoint):
    newSample = sample(dataPoint, random.random());
    vertexVal = dataPoint[self.name];
    if len(self.samples[vertexVal]):
      self.samples[vertexVal].append(newSample);
    else:
      minVal = 1.0;
      minSample = None;
      for (samp in self.samples[vertexVal]):
        if (samp.randomNumber < minVal):
          minVal = samp.randomNumber;
          minSample = samp;
      if (newSample.randomNumber > minVal):
        self.samples[vertexVal].append(newSample);
        self.samples[vertexVal].remove(minSample);

  def addMarginalCount(self, dataPoint);
    dataPointVal = dataPoint[self.name];
    self.marginalCounts[dataPointVal] += 1;

  def marginalizeParent(self, parentVertex):
    newParentCounts = {};
    newJointCounts = {};
    for (entry in self.jointCounts):
      currCount = self.jointCounts[entry];
      entryCopy = entry; 
      entryCopy.pop(parentVertex.name, None);
      if (entryCopy in newJointCounts.keys()):
        newJointCounts[entryCopy] += currCount;
      else:
        newJointCounts[entryCopy] = currCount;
  '''
  def numFreeParameters(self):
    numFreeParameters = 1;
    for vert in self.parents:
      numFreeParameters *= len(vert.vals); 
    numFreeParameters *= (len(self.vals) - 1);
    return numFreeParameters;       
  '''
  def updateJointCounts(self, data):
    for (dataPoint in data):
      self.currJointDataPoints += 1; 
      jointAssignment = {};
      parentAssignment = {};
      jointAssignment[self.name] = dataPoint[self.name];
      for (parent in self.parents):
        jointAssignments[parent.name] = dataPoint[parent.name];
        parentAssignment[parent.name] = dataPoint[parent.name];
      if (jointAssignment in self.jointCounts):
        self.jointCounts[jointAssignment] += 1;
      else:
        self.jointCounts[jointAssignment] = 1;
      if (parentAssignment in self.parentCounts):
        self.parentCounts[parentAssignment] += 1;
      else:
        self.parentCounts[parentAssignment] = 1;

  def updateFrontierCounts(self, data):
    self.currFrontierDataPoints += len(data);
    for (frontier in self.frontierModels):
      for (datapoint in data):
 

  def mutualInfoWithParents(self, dataPoint):
    mutualInfoScore = 0;
    for (
    for (jointAssignment in self.jointCounts.keys()):
      jointCount = self.jointCounts[jointAssignment];
      parentAssignment = jointAssignment;
      parentAssignment.pop(self.name, None);
      parentCount = self.parentCounts[parentAssignment];
      mutualInfoScore +=  jointCount * math.log(float(jointCount) / float(parentCount));
    return mutualInfoScore;

  '''
  def contributionToModelScore(self, data):
    vertexComplexity = self.numFreeParameters() * 0.5 * math.log(len(data));
    vertexInfo = 0; 
    for dataPoint in data:
      parentJointAssignment = '';
      for parent in self.parents:
        parentJointAssignment += str(dataPoint[parent.name]);
      vertexInfo += math.log(self.currCPTTable[parentJointAssignment][dataPoint[self.name]]);
    return vertexInfo - vertexComplexity;

  def setupCPTs(self, data):
    self.reinitializeCounts();
    self.updateCountsFromData(data);
    self.marginalizeDataCounts();

  def reinitializeCounts(self):
    self.currCPTTable = {};

  def updateCountsFromData(self, data):
    for dataPoint in data:
      jointParentAssignment = '';
      for parent in self.parents:
        jointParentAssignment += str(dataPoint[parent.name]);
      if (jointParentAssignment not in self.currCPTTable.keys()):
        self.currCPTTable[jointParentAssignment] = {};
        for val in self.vals:
          self.currCPTTable[jointParentAssignment][val] = 0;
      vertexVal = dataPoint[self.name];
      self.currCPTTable[jointParentAssignment][vertexVal] += 1;

  def marginalizeDataCounts(self):
    for entry in self.currCPTTable:
      totalCounts = 0;
      for val in self.vals:
        totalCounts += self.currCPTTable[entry][val];
      for val in self.vals:
        self.currCPTTable[entry][val] = float(self.currCPTTable[entry][val]) / float(totalCounts);

  def addParent(self, newParent):
    self.parents.append(newParent);

  def removeParent(self, oldParent):
    self.parents.remove(oldParent);   
