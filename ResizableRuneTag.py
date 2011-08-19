'''
Created on 30/lug/2011

@author: Marco
'''
import wx
from DigitalRuneTag import DigitalRuneTag
from PdfStructure import PdfStructure
import Configuration

class ResizableRuneTag(wx.Window):
    
    mode = None
    selected = True
    
    def __init__(self, parent, tagName, size, position, originalSize, info):
        wx.Window.__init__(self, parent, -1, position)
        #self.SetBackgroundColour(wx.Colour(100, 100, 200))
        self.info = info
        self.digitalRuneTag = DigitalRuneTag(tagName, position[0]+5, position[1]+5, size, originalSize)
        PdfStructure.AddMarker(self.digitalRuneTag)
        self.SetSize((size+10,size+10))
        self.makeImage(tagName, size)
        self.makeButton(size)
        self.SetWindowStyleFlag(wx.BORDER_SUNKEN)
        self.SetCursor(wx.StockCursor(wx.CURSOR_RIGHT_ARROW))
       
    def OnStartMove(self, evt):
        self.position = evt.GetPosition()
        self.SetBackgroundColour(wx.BLACK)
        self.SetFocus()
        self.Enable()
       
    def OnStopMove(self, evt):
        self.SetBackgroundColour(None)
        
    def makeButton(self, size):
        self.button = wx.Window(self, -1)
        self.button.SetPosition((size+5,size+5))
        self.button.SetOwnBackgroundColour(wx.Colour(50, 50, 100))
        self.button.SetCursor(wx.StockCursor(wx.CURSOR_SIZENWSE))
        self.button.SetSize(wx.Size(5, 5)) 
        self.button.Bind(wx.EVT_LEFT_DOWN, self.OnStartResize)
        self.button.Bind(wx.EVT_LEFT_UP, self.OnEndResize)
        #self.button.Bind(wx.EVT_MOTION, self.OnMotion)
        self.button.Bind(wx.EVT_MOTION, self.OnMotion)
        
    def makeImage(self, tagName, size):
        self.image = wx.Image(Configuration.TAG_DIR()+tagName+".bmp")
        scaledImage = self.image.Scale(size,size)
        bmp = scaledImage.ConvertToBitmap()
        scaledImage.Destroy()
        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, bmp, (5,5), (size,size))
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnStartMove)
        self.bitmap.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.bitmap.Bind(wx.EVT_LEFT_UP, self.OnStopMove)
        self.bitmap.Bind(wx.EVT_MOTION, self.OnMotionMove)
        
    def UpdateInfo(self):
        self.info.updateTitle(self.digitalRuneTag.name)
        self.info.updatePosition(self.digitalRuneTag.x, self.digitalRuneTag.y)
        self.info.updateSize(self.digitalRuneTag.size, self.digitalRuneTag.size)
        
    def OnStartResize(self, evt):
        self.oldSize = self.GetSize()
        self.oldPosition = wx.GetMousePosition()
        self.mode = "resize"
        if not self.button.HasCapture():
            self.button.CaptureMouse()
        evt.Skip() 
    
    def OnEndResize(self,evt):
        self.mode = None
        self.button.ReleaseMouse()
        evt.Skip()  
        
    def OnRightDown(self, evt):
            popup = wx.Menu()
            item = wx.MenuItem(popup, wx.NewId(), 'Elimina')
            popup.AppendItem(item)
            popup.Bind(wx.EVT_MENU, self.DeleteMarker, id=item.GetId())
            self.PopupMenu(popup, evt.GetPosition())
        
    def DeleteMarker(self, evt):
        PdfStructure.RemoveMarker(self.digitalRuneTag.name)
        self.Parent.resizableRuneTags.remove(self)
        self.Hide()
    
    def OnMotionMove(self, evt):
        if evt.Dragging():
            if self.mode != "resize":
                currentoffset = evt.GetPosition()
                distance = currentoffset - self.position
                currentPosition = self.GetPosition()
                self.SetPosition((currentPosition.x+distance.x, currentPosition.y+distance.y))
                self.digitalRuneTag.x = currentPosition.x+distance.x+5
                self.digitalRuneTag.y = currentPosition.y+distance.y+5
        self.UpdateInfo()
                                         
    def OnMotion(self, evt):
                # I'm not sure which of these to call
                # self.SetSize(wx.Size(distance.x, distance.y))
        if evt.Dragging():
            if self.mode is "resize":
                distance = wx.GetMousePosition() - self.oldPosition
                (oldX, oldY) = self.oldSize
                distance.x+=oldX
                distance.y = distance.x
                self.digitalRuneTag.size = distance.x-10

                scaledImage = self.image.Scale(distance.x-10, distance.y-10,wx.IMAGE_QUALITY_NORMAL)
                bmp = scaledImage.ConvertToBitmap()
                scaledImage.Destroy()

                self.bitmap.Destroy()
                self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, bmp, (5,5), (distance.x-10, distance.y-10))
                self.button.SetPosition((distance.x-5, distance.y-5))
                self.SetSize((distance.x,distance.y))
                self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnStartMove)
                self.bitmap.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
                self.bitmap.Bind(wx.EVT_LEFT_UP, self.OnStopMove)
                self.bitmap.Bind(wx.EVT_MOTION, self.OnMotionMove)
        self.UpdateInfo()
    
    def Destroy(self):
        PdfStructure.RemoveMarker(self.digitalRuneTag.name)
        wx.Window.Destroy(self)
