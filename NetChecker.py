'''
Created on Feb 13, 2015

@author: Max Ruiz
'''

from Tkinter import *
from FileCommands import HandleFile
from HelpCommands import *


class NetChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.initGui()


    def initGui(self):
        self.initNetCheckFrame()
        self.initEagleFileNameLB()
        self.initLog()
        self.initTraceList()
        self.initPartsList()
        self.initPadPinSheetList()
        self.fillMenuButtons()
        self.master.config(menu=self.menubar)
        self.master.title('ICE - Net list eXAMiner')
        self.pack()
        self.traceList.bind('<<ListboxSelect>>', self.updatePartsList)
        self.partsList.bind('<<ListboxSelect>>', self.updatePadPinSheet)

    def openUsrFile(self):
        self.HF = HandleFile()
        self.log = self.HF.openUsrFile()
        self.usrFileName = self.HF.getFName()
        self.nets = self.HF.getNets()
        self.netList = self.HF.getNetlist()
        self.initiallUpdate()

    def saveFileToXML(self):
        self.HF.saveFileToXML()

    def newInstance(self):
        NetChecker(master=Toplevel())

    def initiallUpdate(self):
        self.updateEagleFileNameLB()
        self.updateTraceList()
        self.updateLog()

    def initNetCheckFrame(self):
        self.mainFrame = LabelFrame(self, text='Net list eXAMiner')
        self.mainFrame.pack()

    def initEagleFileNameLB(self):
        eagleLblFrm = LabelFrame(self.mainFrame, text='EAGLE Net list file')
        self.eagFLB = Listbox(eagleLblFrm, height=1, width=15)
        self.eagFLB.pack(side='left')
        self.eagFLB.insert(0, 'No File')
        eagleLblFrm.pack(anchor=W)

    # This function will update the file name list box to let the user see which file
    # they are viewing. The list box is visible at the top left side of the window.
    def updateEagleFileNameLB(self):
        try:
            self.eagFLB.delete(0, self.eagFLB.size())
            self.eagFLB.insert(0, self.usrFileName)
        except:
            self.eagFLB.insert(0, self.usrFileName)

    # Log will display user activity as well as display user errors
    def initLog(self):
        logFrame = LabelFrame(self.mainFrame, text='Log')
        self.logLst = Listbox(logFrame, height=7, width=151)
        self.logLst.pack()
        logFrame.pack(side='bottom', anchor=W)

    # This command takes the string variable "self.log" and loads it into the log list box
    def updateLog(self):
        try:
            self.logLst.delete(0)
        except:
            pass
        self.logLst.insert(0, self.log)

    def initTraceList(self):
        trcLstFrm = LabelFrame(self.mainFrame, text='Traces')
        self.traceList = Listbox(trcLstFrm, width=40, height=21)
        traceScrlBr = Scrollbar(trcLstFrm, orient=VERTICAL, command=self.traceList.yview )
        self.traceList["yscrollcommand"] = traceScrlBr.set
        traceScrlBr.pack(side='left', fill=Y)
        self.traceList.pack(fill='both', expand=True,side='left')
        trcLstFrm.pack(side='left')

    # The trace list box updates only once after the user has selected which file they want
    # to view.
    def updateTraceList(self):
        for i in range(len(self.nets)):
            self.traceList.insert(i, str(self.nets[i]))

    # This list box will display all parts attached to a specific trace
    # when a user clicks on the corresponding trace
    def initPartsList(self):
        prtLstFrm = LabelFrame(self.mainFrame, text='Parts')

        # This trace label will show the name of the trace under inspection
        # while the user is looking at the parts list
        self.trcLabel = StringVar()
        self.trcLabel.set('-')
        self.trcLblForPrtLst = Label(prtLstFrm, textvariable=self.trcLabel, width=15)
        self.trcLblForPrtLst.pack(side='top', anchor=W)

        self.partsList = Listbox(prtLstFrm, width=40, height=20)
        partsScrlBr = Scrollbar(prtLstFrm, orient=VERTICAL, command=self.partsList.yview )
        self.partsList["yscrollcommand"] = partsScrlBr.set
        partsScrlBr.pack(side='left', fill=Y)
        self.partsList.pack(side='left')
        prtLstFrm.pack(side='left')

    # This function is used to iterate through the parts belonging to a
    # specific trace that the user has selected from the trace list box
    # and loads them into the parts list box.
    def updatePartsList(self, event):
        # Delete any parts currently in the parts list box
        self.partsList.delete(0, self.partsList.size())

        # get selected trace name from trace list box selection
        self.curTrcTxt = self.traceList.get(self.traceList.curselection()[0])
        self.trcLabel.set(self.curTrcTxt)

        partLists = []
        self.parts = []
        for nets in self.nets:
            if self.curTrcTxt == nets:
                partLists = self.netList[nets] # load in part lists into another list

        for parts in partLists:
            self.parts.append(parts[0]) # take first element of each part list (Name of Part)

        for i in range(len(self.parts)):
            # self.partsList is a list box being filled with the names of parts from partLists
            # notice the different placement of "s"'s in the var name
            self.partsList.insert(i, str(self.parts[i]))

        self.curTrcTxt = self.traceList.get(self.traceList.curselection()[0])
        self.log = str(self.curTrcTxt)
        self.updateLog()

    # Three list boxes are generated here because they are all tied together
    # The list boxes will display the Pad, Pins, and Sheets respectively
    # for each part a user selects from the parts list box
    def initPadPinSheetList(self):
        pdLstFrm = LabelFrame(self.mainFrame, text='Pad')
        pnLstFrm = LabelFrame(self.mainFrame, text='Pin')
        sheetLstFrm = LabelFrame(self.mainFrame, text='Sheet')

        self.padLst = Listbox(pdLstFrm, height=21, width=20)
        self.padLst.pack(side='top')

        self.pinLst = Listbox(pnLstFrm, height=21, width=20)
        self.pinLst.pack(side='top')

        self.sheetLst = Listbox(sheetLstFrm, height=21, width=20)
        self.sheetLst.pack(side='top')

        pdLstFrm.pack(side='left')
        pnLstFrm.pack(side='left')
        sheetLstFrm.pack(side='left')

    # The Pad, Pin and Sheet list boxes need to be updated each time a new part has been
    # selected from the parts list box. This function will fill each respective list box
    # with its respective information.
    def updatePadPinSheet(self, event):
        if self.padLst.size() > 0:
            self.padLst.delete(0, self.padLst.size())
        if self.pinLst.size() > 0:
            self.pinLst.delete(0, self.pinLst.size())
        if self.sheetLst.size() > 0:
            self.sheetLst.delete(0, self.sheetLst.size())

        self.curPrtTxt = self.partsList.get(self.partsList.curselection()[0])

        self.log = self.curTrcTxt + ' -> ' + str(self.curPrtTxt)
        self.updateLog()

        for x in self.netList[self.curTrcTxt]:
            if x[0] == self.curPrtTxt:
                self.padLst.insert(1, x[1])
                self.pinLst.insert(1, x[2])
                self.sheetLst.insert(1, x[3])

    # This method is used to generate the file menu. The file menu is applied
    # to the Tk() root frame, not the self.mainFrame that everything else belongs to.
    # This is because it was meant to be this way.
    def fillMenuButtons(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New Window", command=self.newInstance)
        filemenu.add_command(label="Open File", command=self.openUsrFile)
        filemenu.add_command(label="Save to XML", command=self.saveFileToXML)

        self.menubar.add_cascade(label="File", menu=filemenu)

        '''
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=None)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=None)
        editmenu.add_command(label="Copy", command=None)
        editmenu.add_command(label="Paste", command=None)
        editmenu.add_command(label="Delete", command=None)
        editmenu.add_command(label="Select All", command=None)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        '''

        helpmenu = Menu(self.menubar, tearoff=0)
        HC = HelpCommands()
        helpmenu.add_command(label="Help Index", command= lambda: HC.help())
        helpmenu.add_command(label="About...", command= lambda: HC.about())
        self.menubar.add_cascade(label="Help", menu=helpmenu)





if __name__ == '__main__':
    root = Tk()
    app = NetChecker(master=root)
    app.mainloop()
