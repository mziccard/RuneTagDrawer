'''
Created on 18/ago/2011

@author: Marco
'''
from wx import *
import Configuration

class RuneTagInfo(Window):
    '''
    This class displays some info about displayed rune tags.
    Info are dinamically updated as soon as a rune tag is focused
    '''

    def __init__(self, parent):
        Window.__init__(self, parent, -1)
        panel = Panel(self, -1, style=wx.SUNKEN_BORDER)
        panel.SetPosition((5,5))
        panel.SetSize((220,595))
        
        title = "Tag Name"
        position = "- Rune position"
        size = "- Rune size"
        
        italic = wx.Font(10, wx.NORMAL, wx.ITALIC, wx.NORMAL)
        bold = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        self.title = wx.StaticText(panel, -1, title, (10,15), style=wx.ALIGN_CENTRE)
        self.title.SetFont(bold)
        
        wx.StaticText(panel, -1, position, (10,45), style=wx.ALIGN_CENTRE)
        self.position = wx.StaticText(panel, -1, "", (45,65), style=wx.ALIGN_LEFT)
        self.position.SetFont(italic)

        wx.StaticText(panel, -1, size, (10,145), style=wx.ALIGN_CENTRE)
        self.size = wx.StaticText(panel, -1, "", (45,165), style=wx.ALIGN_LEFT)
        self.size.SetFont(italic)        

    def updateTitle(self, title):
        self.title.SetLabel(title)
    
    def updatePosition(self, x, y):
        xCm=round(x*Configuration.REAL_RATIO,4)
        yCm=round(y*Configuration.REAL_RATIO,4)
        stringPosition = "cm:\n"+str(xCm)+", "+str(yCm)+"\npixel:\n"+str(round(x,0))+", "+str(round(y,0));
        self.position.SetLabel(stringPosition)
        
    def updateRadius(self, radius):
        radiusCm=round(radius*Configuration.REAL_RATIO,4)
        stringSize = "cm:\n"+str(radiusCm)+"\npixel:\n"+str(round(radius,0))
        self.size.SetLabel(stringSize)