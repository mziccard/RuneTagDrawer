'''
Created on 19/ago/2011

@author: Marco
'''
import Configuration
import DigitalModel

class ModelsCache(object):
    '''
    Class used to read models names
    from file-system and keep them in cache 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.models = []
        
        in_file = open("ModelNames", "r")
        nameString = in_file.read()
        modelNames = nameString.split()
        for modelName in modelNames:
            in_file = open(Configuration.MODEL_DIR()+modelName+".model", "r")
            tagNames = []
            tagPositions = []
            tagSizes = []
            tagDefaultSizes = []
            for line in in_file:
                rune = line.split()
                tagNames.append(rune[0])
                tagPositions.append((float(rune[1]), float(rune[2])))
                tagSizes.append(float(rune[3]))
                tagDefaultSizes.append(float(rune[4]))
        
            model = DigitalModel.DigitalModel(modelName, tagNames, tagPositions, tagSizes, tagDefaultSizes)
            self.models.append(model)
            in_file.close()
        
    def AddModel(self, modelName, tagNames, tagPositions, tagSizes, tagDefaultSizes):
        model = DigitalModel.DigitalModel(modelName, tagNames, tagPositions, tagSizes, tagDefaultSizes)
        self.models.append(model)
        
    def GetModel(self, modelName):
        for model in self.models:
            if model.name == modelName:
                return model
       
        
