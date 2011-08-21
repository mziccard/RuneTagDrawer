import wx
import DrawableFrame
import RuneTagList
import RuneTagInfo
from RuneTagCreator import RuneTagCreator
from PdfStructure import PdfStructure
import ModelNameDialog

class RuneTagDrawer(wx.Frame):
    
    drawableFrame = None
    runeTagList = None
    
    def __init__(self):
        
        wx.Frame.__init__(self, None)
        self.SetTitle("Rune tag drawer")
        
        self.sizer = wx.BoxSizer()
        panel = wx.Panel(self, -1)
        panel.SetSize((800,630))
        panel.SetMinSize((800,630))
        self.SetMinSize((800,630))
        self.SetMaxSize((800,630))
        self.Fit()
        
        self.drawableFrame = DrawableFrame.DrawableFrame(panel, 424, 600)                       
        self.runeTagInfo = RuneTagInfo.RuneTagInfo(panel)
        self.runeTagList = RuneTagList.RuneTagList(panel, self.GetClientSize().GetHeight(), self.drawableFrame, self.runeTagInfo)
        
        self.child_windows = []
        self.child_windows.append(self.runeTagList)
        self.child_windows.append(self.drawableFrame)
        self.child_windows.append(self.runeTagInfo)
        
        self.sizer.Add(self.runeTagList)
        self.sizer.Add(self.drawableFrame)
        self.sizer.Add(self.runeTagInfo)
        

        panel.SetSizer(self.sizer)
        
        self.Centre();
        
        menuFile = wx.Menu()
        menuFile.Append(wx.ID_OPEN, "Load Tag", "Loads a new Rune Tag")
        menuFile.Append(wx.ID_SAVE, "Export PDF", "Export drawable section in PDF")
        menuFile.AppendSeparator()
        menuFile.Append(wx.ID_EXIT, "Exit", "Terminate the program")
        
        self.menuModel = wx.Menu()
        self.menuModel.Append(wx.ID_ADD, "Save as Model", "Saves current configuration as a model")
        self.CreateMenuModel()
        
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "File")
        menuBar.Append(self.menuModel, "Model")

        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, wx.ID_SAVE, self.OnExport)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, wx.ID_ADD, self.OnSaveModel)
                                    
    def CreateMenuModel(self):
        items = self.menuModel.GetMenuItems()
        for item in items:
            if item.GetId() != wx.ID_ADD:
                self.menuModel.RemoveItem(item)

        self.menuModel.AppendSeparator()
        names = PdfStructure.GetModelNames()
        for name in names:
            itemMenu = wx.Menu()
            itemMenu.Append(0, "Generate "+name, "Generate model "+name)
            itemMenu.Append(1, "Delete "+name, "Delete model "+name)
            self.menuModel.AppendMenu(-1, name+" Options", itemMenu)
            self.Bind(wx.EVT_MENU, lambda evt, s=name:self.OnGenerateDeleteModel(evt,s))
        wx.EVT_MENU(self, wx.ID_ADD, self.OnSaveModel)
            
    def OnGenerateDeleteModel(self, evt, name):
        if evt.GetId() == 0:
            self.drawableFrame.Clear()
            model = PdfStructure.GetModel(name)
            i = 0
            for tagName in model.tagNames:
                self.drawableFrame.DrawRuneTag(tagName, model.tagPositions[i], model.tagSizes[i], model.tagDefaultSizes[i], self.runeTagInfo)
                i+=1
        elif evt.GetId() == 1:
            PdfStructure.DeleteModel(name)
            self.CreateMenuModel()       
            
    def OnSaveModel(self, event):
        dlg = ModelNameDialog.ModelNameDialog(self, -1, "Save as model")
        dlg.ShowModal()
        dlg.Destroy()
        self.CreateMenuModel()       
        
    def OnExit(self, event):
        self.Destroy()
        
    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Seleziona un file di configurazione di un tag", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
                inputFile = open(dlg.GetPath(),"r")
                tagDefinition = inputFile.read()
                try:
                    (runeTagName, runeTagSize) = RuneTagCreator.addRuneTag(tagDefinition)
                    self.runeTagList.AddGraphicRuneTag(runeTagName, runeTagSize)
                except NameError as nameError:
                    dlg2 = wx.MessageDialog(self, "Nome duplicato\n\nDettagli:\n"+unicode(nameError), "ERRORE", wx.OK | wx.ICON_INFORMATION)
                    dlg2.ShowModal()
                    dlg2.Destroy()
                except Exception as error:
                    dlg2 = wx.MessageDialog(self, "Impossibile interpretare il file come un rune tag\n\nDettagli:\n"+unicode(error), "ERRORE", wx.OK | wx.ICON_INFORMATION)
                    dlg2.ShowModal()
                    dlg2.Destroy()
        dlg.Destroy()
    
    def OnExport(self, event):
        dlg = wx.FileDialog(self, "Esporta in formato PDF", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            PdfStructure.GeneratePDF(dlg.GetPath())
        dlg.Destroy()

       
app = wx.PySimpleApp()
f = RuneTagDrawer()
f.Show()
app.MainLoop()
