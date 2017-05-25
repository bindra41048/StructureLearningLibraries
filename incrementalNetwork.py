import BayesianNetwork
import math
class FrontierModel:
 
  def __init__(self, vertex, currParentSet, parentInQuestion, add):
    self.vertex = vertex;
    self.parentInQuestion = parentInQuestion;
    self.currParentSet = currParentSet;
    self.counts = {}; 
    self.currCPTs = {};
    self.add = add;
         
  def addDataToCounts(self, data):
    for dataPoint in data:
      parentJoint = '';
      for parent in self.vertex.parents:
        if (self.add or not parent == self.parentInQuestion):
          parentJoint += str(dataPoint[parent.name]);
      if self.add and not self.parentInQuestion == None:
        parentJoint += str(dataPoint[self.parentInQuestion.name]);
      if not parentJoint in self.counts.keys():
        self.counts[parentJoint] = {};
        for val in self.vertex.vals:
          self.counts[parentJoint][str(val)] = 0;
      self.counts[parentJoint][str(dataPoint[self.vertex.name])] += 1;
    #for joint in self.counts.keys():
      #for val in self.vertex.vals:
        #print("For vertex " + str(self.vertex.name) + "the joint " + str(joint) + " and val " + str(val) + "count is " + str(self.counts[joint][(str)val]));

  def normalizeCounts(self):
    for parentJoint in self.counts:
      totalCount = 0;
      for val in self.vertex.vals:
        totalCount += self.counts[parentJoint][str(val)];
      self.currCPTs[parentJoint] = {};
      for val in self.vertex.vals:
        self.currCPTs[parentJoint][str(val)] = float(self.counts[parentJoint][str(val)]) / float(totalCount);

class IncrementalNetwork:

  def __init__(self, topologicalOrdering):
    self.topologicalOrdering = topologicalOrdering;
    self.frontierModels = {};
    self.jointDataPoints = {};
    self.currentModels = {};
    for vertex in topologicalOrdering:
      self.frontierModels[vertex.name] = [];
      self.initializeNewFrontierModels(vertex);
      self.jointDataPoints[vertex.name] = [];
      self.currentModels[vertex.name] = FrontierModel(vertex, vertex.parents, None, True);
    

  def modelComplexity(self, model, vert):
    numFreeParameters = 1;
    for vert in model.currParentSet:
      if (model.add or not vert.name == model.parentInQuestion.name): 
        numFreeParameters *= len(vert.vals);
    numFreeParameters *= (len(model.vertex.vals) - 1);
    if (model.add and model.parentInQuestion != None):
      numFreeParameters *= len(model.parentInQuestion.vals);
    return 0.5 * math.log(len(self.jointDataPoints[model.vertex.name])) * numFreeParameters;

  def getDiffMutualInfo(self, originalModel, frontierModel, vert):
    originalMutualInfo = 0;
    frontierMutualInfo = 0;
    for dataPoint in self.jointDataPoints[vert.name]:
      jointOriginal = '';
      for parent in vert.parents:
        jointOriginal += str(dataPoint[parent.name]);
      originalMutualInfo += math.log(originalModel.currCPTs[jointOriginal][str(dataPoint[vert.name])]);
      jointFrontier = '';
      for parent in vert.parents:
        if(frontierModel.add or parent != frontierModel.parentInQuestion):
          jointFrontier += str(dataPoint[parent.name]);
      if (frontierModel.add): 
        jointFrontier += str(dataPoint[frontierModel.parentInQuestion.name]);
      frontierMutualInfo += math.log(frontierModel.currCPTs[jointFrontier][str(dataPoint[vert.name])]);
    return (frontierMutualInfo - self.modelComplexity(frontierModel, vert)) - (originalMutualInfo- self.modelComplexity(originalModel, vert));

  def addDataToModels(self, data):
    for vertex in self.topologicalOrdering:
      self.currentModels[vertex.name].addDataToCounts(data);
      self.currentModels[vertex.name].normalizeCounts();
      for frontierModel in self.frontierModels[vertex.name]:
        frontierModel.addDataToCounts(data);
        frontierModel.normalizeCounts();
      for dataPoint in data:
        self.jointDataPoints[vertex.name].append(dataPoint);   

  def selectIdealFrontierModel(self):
    maxImprovement = 0;
    idealFrontierModel = None;
    for vert in self.topologicalOrdering:
      for model in self.frontierModels[vert.name]:
        score = self.getDiffMutualInfo(self.currentModels[vert.name], model, vert);
        if score > maxImprovement:
          maxImprovement = score;
          idealFrontierModel = model;
    return idealFrontierModel;

  def updateFrontier(self, idealFrontierModel):
    vertForIdealFrontModel = idealFrontierModel.vertex;
    self.jointDataPoints[vertForIdealFrontModel.name] = [];
    parentInQuestion = idealFrontierModel.parentInQuestion;
    if (idealFrontierModel.add):
      #need to update frontier models to allow an add none option
      vertForIdealFrontModel.parents.append(parentInQuestion);
    else:
      vertForIdealFrontModel.parents.remove(parentInQuestion);
    self.currentModels[vertForIdealFrontModel.name] = FrontierModel(vertForIdealFrontModel, vertForIdealFrontModel.parents, None, True);
    self.frontierModels[vertForIdealFrontModel.name] = [];
    self.initializeNewFrontierModels(vertForIdealFrontModel);
      
  def updateModel(self, data):
    self.addDataToModels(data);
    idealFrontierModel = self.selectIdealFrontierModel();
    #keep current model
    if idealFrontierModel == None:
      return;
    self.updateFrontier(idealFrontierModel);

  def initializeNewFrontierModels(self, vertex):
    for vert in vertex.possibleParents:
      if vert in vertex.parents:
        self.frontierModels[vertex.name].append(FrontierModel(vertex, vertex.parents, vert, False));
      else:
        self.frontierModels[vertex.name].append(FrontierModel(vertex, vertex.parents, vert, True));
