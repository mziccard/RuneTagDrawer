'''
Created on 19/ago/2011

@author: Marco
'''
import wx
from PdfStructure import PdfStructure

class ModelNameDialog(wx.Dialog):
    '''
    Dialog that allows user to specify a name for a created model
    name cannot already exist and model cannot be empty
    '''


    def __init__(self, parent, id , title):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, id, title, size=(250, 120))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'Model name', (5, 5), (240, 70))
        self.name = wx.TextCtrl(panel, -1, '', (10, 30), (230, 30))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, -1, 'Ok', size=(70, 30))
        okButton.Bind(wx.EVT_BUTTON, self.SaveModel)
        
        closeButton = wx.Button(self, -1, 'Annulla', size=(70, 30))
        closeButton.Bind(wx.EVT_BUTTON, self.Close)
        hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        
    def SaveModel(self, evt):
        try:
            modelName = self.name.GetValue().replace(" ","-")
            PdfStructure.SaveModel(modelName)
            self.Destroy()
        except Exception as nameError:
            dlg2 = wx.MessageDialog(self.Parent, "Impossibile salvare modello\n\nDettagli:\n"+unicode(nameError), "ERRORE", wx.OK | wx.ICON_INFORMATION)
            dlg2.ShowModal()
            dlg2.Destroy()
        
    def Close(self, evt):
        self.Destroy()
        