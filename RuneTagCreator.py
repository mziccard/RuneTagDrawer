'''
Created on 16/ago/2011

@author: Marco
'''
from reportlab.graphics import renderPM
from reportlab.lib.colors import black
from reportlab.lib.units import cm 
from math import sqrt
import wx
import Configuration

class RuneTagCreator(object):
    '''
    classdocs
    '''
    BASEDIR = "runeTags/"
    BASEDIR_WIN = "runeTags\\"
    FILE_FORMAT = "bmp"
    CONFIG_FILE = "RuneTagNames"
    
    @staticmethod
    def addRuneTag(tagDefinition):

        lines = tagDefinition.split("\n")
        if len(lines) is 0:
            raise Exception("ERROR 1: formato non riconosciuto")
        
        title = lines.pop(0)
        if len(lines) is 0:
            raise Exception("ERROR 3: formato non riconosciuto")
        
        name = lines.pop(0)
        name = name[0:-1]
        if name == "":
            raise Exception("ERROR 4: nome mancante")
        if len(lines) is 0:
            raise Exception("ERROR 5: formato non riconosciuto")
        
        in_file = open("RuneTagNames", "r")
        nameString = in_file.read()
        names = nameString.split("\n")
        

        for oldName in names:
            component = oldName.split("_")
            if component[0] == name:
                raise NameError("ERROR: "+oldName+" already present")
        
        size = float(lines.pop(0))
        if len(lines) is 0:
            raise Exception("ERROR 6: formato non riconosciuto")
        
        print "SIZE:"
        print size
        c2 = renderPM.PMCanvas((size/10*2+1)*cm, (size/10*2+1)*cm)
        c2.setFillColor(black)
        
        world_measure = lines.pop(0)
        if len(lines) is 0:
            raise Exception("ERROR 7: formato non riconosciuto")
        
        num_slots = float(lines.pop(0))
        if len(lines) is 0:
            raise Exception("ERROR 8: formato non riconosciuto")
        
        for i in [0,1,2,3]:
            print lines.pop(0)
            if len(lines) is 0:
                raise Exception("ERROR 9: formato non riconosciuto")
        print len(lines)
        ellipsesString = ""
        for line in lines:
            ellipsesString+=line+"\n"
            ellipse = line.split(" ")
            if len(ellipse) == 10:
                xCenter = -1*float(ellipse[3])
                yCenter = -1*float(ellipse[6])
                radius = 0.5*sqrt((float(ellipse[3])*2)*(float(ellipse[3])*2)+(float(ellipse[6])*2)*(float(ellipse[6])*2)-4*float(ellipse[9]))
                c2.circle(xCenter/10*cm+5.5*cm, yCenter/10*cm+5.5*cm, radius/10*cm)
                c2.fillstrokepath(1, 1)

        filename = RuneTagCreator.BASEDIR
        filename+=name
        filename+="."+RuneTagCreator.FILE_FORMAT
        c2.saveToFile(filename, RuneTagCreator.FILE_FORMAT)

        image = wx.Image(filename)
        scaledImage = image.Scale(100,100,wx.IMAGE_QUALITY_HIGH)
        filename = RuneTagCreator.BASEDIR
        filename+=name
        filename+="-small"
        filename+="."+RuneTagCreator.FILE_FORMAT
        scaledImage.SaveFile(filename, wx.BITMAP_TYPE_BMP)
        
        out_file = open(RuneTagCreator.CONFIG_FILE,"a")
        out_file.write(name+"_"+str((size/10*2+1)*(1/Configuration.REAL_RATIO))+"\n")
        out_file.close()
        
        out_file = open(RuneTagCreator.BASEDIR+name+".txt", "w")
        out_file.write(ellipsesString)
        out_file.close()
        
        return (name, (size/10*2+1)*(1/Configuration.REAL_RATIO))