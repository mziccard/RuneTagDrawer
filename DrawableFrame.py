import wx
import ResizableRuneTag
'''
Created on 23/lug/2011

@author: Marco
'''

class DrawableFrame(wx.Window):
    '''
    Allows user to put resizable rune tags in a A4 like white frame
    Configuration realized on that frame is then replicated proportionally at export time
    '''

    def __init__(self, parent, height, width):
        print "CALLED"
        wx.Window.__init__(self, parent)
        self.SetSize((height, width))
        self.SetMinSize((height, width))
        self.SetMaxSize((height, width))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.resizableRuneTags = []
        '''
        Constructor
        '''
                
    def DrawRuneTag(self, runeTagName, position, size, originalSize, info):
        self.resizableRuneTags.append(ResizableRuneTag.ResizableRuneTag(self, runeTagName, size, position, originalSize, info))
        
    def Clear(self):
        for resizableRuneTag in self.resizableRuneTags:
            resizableRuneTag.Destroy()
    
    def checkSpecificPosition(self, changedRuneTag):
    	for tag in self.resizableRuneTags:
    		if changedRuneTag != tag:
    			radius1 = (tag.GetSize().GetHeight())/2 - 5
    			radius2 = (changedRuneTag.GetSize().GetHeight())/2 - 5
    			deltax = (tag.GetPosition().x + radius1) - (changedRuneTag.GetPosition().x + radius2)
    			deltay = (tag.GetPosition().y + radius1) - (changedRuneTag.GetPosition().y + radius2)
    			distance = (deltax*deltax + deltay*deltay)**(0.5)
    			radiusSum = radius1 + radius2
    			if distance <= radiusSum:
    				print "In the output pdf file some slots of "+changedRuneTag.name+" RuneTag may laps over "+tag.name+"RuneTag"

    def checkPosition(self):
    	size = len(self.resizableRuneTags)
    	for i in range(0, size):
    		for j in range(i+1, size):
    			tag1 = self.resizableRuneTags[i]
    			tag2 = self.resizableRuneTags[j]
    			radius1 = (tag1.GetSize().GetHeight())/2 - 5
    			radius2 = (tag2.GetSize().GetHeight())/2 - 5
    			deltax = (tag1.GetPosition().x + radius1) - (tag2.GetPosition().x + radius2)
    			deltay = (tag1.GetPosition().y + radius1) - (tag2.GetPosition().y + radius2)
    			distance = (deltax**2 + deltay**2)**(0.5)
    			radiusSum = radius1 + radius2
    			if distance <= radiusSum:
    				print "In the output pdf file some slots of "+tag1.name+" RuneTag may laps over "+tag2.name+" RuneTag"
