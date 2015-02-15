'''
Created on 19/ago/2011

@author: Marco
'''
import wx

class TagSizeDialog(wx.Dialog):
    '''
    Dialog that allows user to specify manually center position and size
    of a rune tag 
    '''


    def __init__(self, parent, id , title, resizableRuneTag, x, y, radius):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, id, title, size=(250, 250))
        self.resizableRuneTag = resizableRuneTag
        
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'Rune radius (cm)', (5, 5), (240, 70))
        self.radius = wx.TextCtrl(panel, -1, '', (10, 30), (230, 30))
        self.radius.SetValue(str(radius))
        
        wx.StaticBox(panel, -1, 'Rune center position (cm)', (5, 80), (240, 100))
        self.labelX = wx.StaticText(panel, -1, "X:", (10, 110))
        self.x = wx.TextCtrl(panel, -1, '', (40, 110), (195, 30))
        self.x.SetValue(str(x))
        self.labelY = wx.StaticText(panel, -1, "Y:", (10, 145))
        self.y = wx.TextCtrl(panel, -1, '', (40, 145), (195, 30))
        self.y.SetValue(str(y))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, -1, 'Ok', size=(70, 30))
        okButton.Bind(wx.EVT_BUTTON, self.SaveSize)
        
        closeButton = wx.Button(self, -1, 'Annulla', size=(70, 30))
        closeButton.Bind(wx.EVT_BUTTON, self.Close)
        hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        
    def SaveSize(self, evt):
        xString = self.x.GetValue()
        yString = self.y.GetValue()
        radiusString = self.radius.GetValue()
        
        x = 0
        y = 0
        radius = 0
        
        error = ""
        if (xString == "") or (yString == "") or (radiusString == ""):
            error = "Some value missing"
        else:
            try:
                x = float(xString)
                y = float(yString)
                radius = float (self.radius.GetValue())
            except Exception as exception:
                error = str(exception)
                
            if error == "":
                if (x < 0 and y < 0) or (x>21 and y>29.7):
                    error = "Position invalid:\n x should be 0<x<21\n y should be 0<y<29.7"
                if radius<0 or radius > 21:
                    error = "Radius invalid:\n radius should be >0 and <21"
        
        if error != "":
            dlg2 = wx.MessageDialog(self.Parent, "Impossibile cambiare posizione\n\nDettagli:\n"+error, "ERRORE", wx.OK | wx.ICON_INFORMATION)
            dlg2.ShowModal()
            dlg2.Destroy()
        else:
            self.resizableRuneTag.UpdateSize(x, y, radius)
            self.Destroy()
        
    def Close(self, evt):
        self.Destroy()
