'''
Created on 16/ago/2011

@author: Marco
'''
from reportlab.pdfgen import canvas 
from reportlab.lib.units import cm 
from math import sqrt
import ModelsCache
import Configuration

class PdfStructure(object):
    '''
    classdocs
    '''

    __markerList = []
    __modelsCache = ModelsCache.ModelsCache()
    
    @staticmethod
    def AddMarker(digitalMarker):
        PdfStructure.__markerList.append(digitalMarker)
    
    @staticmethod
    def RemoveMarker(tagName):
        for tag in PdfStructure.__markerList:
            if tag.name == tagName:
                PdfStructure.__markerList.remove(tag)
    
    @staticmethod
    def GeneratePDF(fileName):
        c = canvas.Canvas(fileName);
        for digitalMarker in PdfStructure.__markerList:
            inputFile = open(Configuration.TAG_DIR()+digitalMarker.name+".txt","r")
            tagDefinition = inputFile.read()
            
            lines = tagDefinition.split("\n")
            
            (x,y) = digitalMarker.GetCenter();
            tX = (float(x)/424)*21
            tY = (float(y)/600)*29.7    
 
            for line in lines:
                ellipse = line.split(" ")
                if len(ellipse) == 10:
                    xCenter = -1*float(ellipse[3])
                    xCenter = (float(xCenter)/digitalMarker.defaultSize)*digitalMarker.size
                    
                    yCenter = -1*float(ellipse[6])
                    yCenter = (float(yCenter)/digitalMarker.defaultSize)*digitalMarker.size
                    
                    radius = ((0.5*sqrt((float(ellipse[3])*2)*(float(ellipse[3])*2)+(float(ellipse[6])*2)*(float(ellipse[6])*2)-4*float(ellipse[9])))/224)*digitalMarker.size
                    c.circle(xCenter/10*cm+tX*cm, yCenter/10*cm+tY*cm, radius/10*cm, fill=True)

        c.save()
        
    @staticmethod
    def SaveModel(modelName):
        out_file = open(Configuration.MODEL_DIR()+modelName+".model","a")
        if not modelName:
            raise Exception("ERROR: name is empty")
        if not PdfStructure.__markerList:
            raise Exception("ERROR: nothing to save as model")
        for model in PdfStructure.__modelsCache.models:
            if modelName == model.name:
                raise Exception("ERROR: duplicated name")
        
        model_names_file = open("ModelNames","a")
        model_names_file.write(modelName+"\n")
        model_names_file.close()
        
        runeNames = []
        runePositions = []
        runeSizes = []
        runeDefaultSizes = []
        
        for rune in PdfStructure.__markerList:
            runeNames.append(rune.name)
            runePositions.append((rune.x, rune.y))
            runeSizes.append(rune.size)
            runeDefaultSizes.append(rune.defaultSize)
            out_file.write(rune.name+" "+str(rune.x)+" "+str(rune.y)+" "+str(rune.size)+" "+str(rune.defaultSize)+"\n")
        out_file.close()
        
        PdfStructure.__modelsCache.AddModel(modelName, runeNames, runePositions, runeSizes, runeDefaultSizes)

    @staticmethod
    def GetModelNames():
        modelNames = []
        for model in PdfStructure.__modelsCache.models:
            modelNames.append(model.name)
        return modelNames
    
    @staticmethod
    def GetModel(modelName):
        return PdfStructure.__modelsCache.GetModel(modelName)
    
    @staticmethod
    def DeleteModel(name):
        model_names_file = open("ModelNames","r")
        modelNames = model_names_file.read()
        model_names_file.close()
        model_names_file = open("ModelNames","w")
        modelNames = modelNames.replace(name, "")
        model_names_file.write(modelNames)
        model_names_file.close()
        
        for model in PdfStructure.__modelsCache.models:
            if model.name == name:
                PdfStructure.__modelsCache.models.remove(model)
        
            