'''
Created on 29/lug/2011

@author: Marco
'''
import wx
import ConfigReader
import Configuration

class GraphicRuneTag(wx.Window):
    '''
    This class displays a list of saved rune tags wich users
    are allowed to draw
    '''
    
    RuneTagName = None
    
    def __init__(self, parent, drawer, info, runeTagName, size):        
        
        self.RuneTagName = runeTagName
        self.OriginalPixelSize = size     
        wx.Window.__init__(self, parent)
        self.drawer = drawer  
        self.info = info      
        self.SetSize((100,100))

        bmp = wx.Bitmap(Configuration.TAG_DIR()+runeTagName+"-small.bmp")

        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, bmp, (0, 0))
        self.bitmap.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        
        wx.StaticText(self, -1, runeTagName, (0,80), style=wx.ALIGN_CENTRE)

        
    def OnDoubleClick(self, event):
        self.drawer.DrawRuneTag(self.RuneTagName, (50,50), self.OriginalPixelSize, self.OriginalPixelSize, self.info)

class RuneTagList(wx.Window):
    
    _ConfigReader = ConfigReader.ConfigReader()
    
    def __init__(self, parent, height, drawer, info):
        
        wx.Window.__init__(self, parent)
        self.SetSize((150, height-30))
        
        self.drawer = drawer
        self.info = info

        self.scrolling_window = wx.ScrolledWindow( self )
        self.scrolling_window.SetScrollRate(5,5)
        self.scrolling_window.EnableScrolling(True,True)
        self.sizer_container = wx.BoxSizer( wx.HORIZONTAL )
        self.sizer = wx.BoxSizer( wx.VERTICAL )

        self.sizer_container.Add(self.sizer,1,wx.CENTER,wx.EXPAND)
        self.child_windows = []
        index = 0
        for runeTagName in self._ConfigReader.RuneTagNames:
            if runeTagName != "":
                size = self._ConfigReader.RuneTagSize[index]
                self.AddGraphicRuneTag(runeTagName, size)

        self.scrolling_window.SetSizer(self.sizer_container)
        self.scrolling_window.SetSize(self.GetClientSize())
        
    def AddGraphicRuneTag(self, runeTagName, size):
        runeTag = GraphicRuneTag(self.scrolling_window, self.drawer, self.info, runeTagName, size)
        self.sizer.Add(runeTag, 0, wx.CENTER|wx.ALL, 5)
        self.child_windows.append(runeTag)
        self.sizer.Layout()
        self.sizer_container.Layout()
        self.Layout()
        self.scrolling_window.Layout()  
        self.scrolling_window.Update()
        self.scrolling_window.FitInside()      

        