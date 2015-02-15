'''
Created on 16/ago/2011

@author: Marco
'''

class DigitalRuneTag(object):
    
    __assignedId = 0
    
    def __init__(self, name, x, y, width, originalWidth):
        '''
        Constructor
        '''
        self.id = DigitalRuneTag.__assignedId
        DigitalRuneTag.__assignedId+1
        self.name = name
        self.x = x
        self.y = y
        self.size = width
        self.defaultSize=originalWidth
                
    def GetCenter(self):
        half = self.size/2
        return (self.x + half, 600 - (self.y + half))