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
