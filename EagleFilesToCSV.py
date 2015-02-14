'''
Created on Oct 10, 2014

@author: Max A. Ruiz
'''

import re
from Tkinter import *
import tkFileDialog

def parseBOMValue(str1):
    flg = 0
    try:
        a = str1.index(',')
        b = str1.replace(', ','/')
        flg = 1
    except ValueError:
        pass
    c = re.findall(r' [a-zA-Z]+ [a-zA-Z]+', str1)
    d = re.findall(r'[a-zA-Z]+: [\w\W]+', str1)
    if c != None:
        if flg == 1:
            for sub in c:
                sub1 = sub.strip()
                sub2 = sub1.replace(' ', '-')
                e = b.replace(sub1, sub2)
                flg = 2
        else:
            for sub in c:
                sub1 = sub.strip()
                sub2 = sub1.replace(' ', '-')
                e = str1.replace(sub1, sub2)
                flg = 2
    if d != None:
        if flg == 2:
            for sub in d:
                sub1 = sub.strip()
                sub2 = sub1.replace(' ', '-')
                f = e.replace(sub, sub2)
                flg = 3
        elif flg == 1:
            for sub in d:
                sub1 = sub.strip()
                sub2 = sub1.replace(' ', '-')
                f = b.replace(sub, sub2)
                flg = 3
        else:
            for sub in d:
                sub1 = sub.strip()
                sub2 = sub1.replace(' ', '-')
                f = str1.replace(sub, sub2)
                flg = 3
    if flg == 0:
        return str1
    elif flg == 1:
        return b
    elif flg == 2:
        return e
    elif flg == 3:
        return f


def strToCSV(str1):
    arr1 = str1.split()
    if len(arr1) < 6:
        arr1.insert(2,'N/A')
    str2 = ''
    for j in range(len(arr1)):
        if j != len(arr1)-1:
            str2 = str2 + arr1[j] + ','
        else:
            str2 = str2 + arr1[j] + '\n'
    return str2

class EagleFilesToCSV(Frame):

    file_opt = options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['title'] = 'This is a title'

    wfile_opt = woptions = {}
    woptions['defaultextension'] = '.csv'
    woptions['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
    woptions['initialdir'] = 'C:\\'
    woptions['initialfile'] = 'myfile.csv'
    woptions['title'] = 'This is a title'

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('EAGLE Files to CSV')
        self.pack()

        self.initGUI()
        self.fillMenuButtons()
        master.config(menu=self.menubar)

    def toCSV(self, file, csvFile, mode=0):
        if mode == 0:
            j = ''
            for line in file:
                words = line.split()
                words.append('\n')
                l = len(words)
                for i in range(l):
                    if i < l and words[i] != '\n':
                        j = j + str(words[i]) + ','
                    else:
                        j = j + str(words[i])

            file.close()
            csvFile.write(j)
            csvFile.close()
        elif mode == 1:
            j = ''
            k = []
            p = []
            while len(k) == 0 and len(p) == 0:
                t0 = file.readline()
                k = re.findall(r'(Part[\s]+Value)',t0)
                p = re.findall(r'(Qty Value[\s]+Device)',t0)


            if len(k) > len(p): # Part type BOM file
                for line in file:
                    words = line.split()
                    l = len(words)
                    m = ''
                    words1 = []
                    for i in range(l):
                        pinhd = re.findall(r'(PINHD-[\w]+)', words[i])
                        if len(pinhd) > 0:
                            pin = True
                            break
                        else:
                            pin = False
                    if pin:
                        words1.append(words[0])
                        words1.append('N/A')
                        for i in range(1,l):
                            words1.append(words[i])
                        words1[len(words1)-2] = words1[len(words1)-2] + words1[len(words1)-1]
                        words1.pop()
                        words.append('\n')
                        words = words1

                    if len(words) > 5:

                        for n in range(4,l):
                            m = m + words[n] + ' '
                        for n in range(4,l):
                            del words[4]

                        if m.count(',') > 0:
                            m1 = re.findall(r'(\w+),', m)
                            m2 = re.findall(r',[\s]+([\w\s]+)', m)
                            m = m1[0] + ' ' + m2[0]

                        words.append(m)

                    words.append('\n')
                    l = len(words)

                    for i in range(l):
                        if words[i] != '\n':
                            j = j + str(words[i]) + ','
                        else:
                            j = j + str(words[i])

                file.close()
                csvFile.write(j)
                csvFile.close()

            elif len(p) > len(k): # Value type BOM File
                csvStr = 'Qty,Value,Device,Package,Parts,Description\n'
                # csvStr will be finished product to write to .csv file
                rows = []
                for line in file:
                    rows.append(line)
                for i in range(len(rows)):
                    str1 = str(rows[i])
                    str2 = parseBOMValue(str1)
                    str3 = strToCSV(str2)
                    csvStr = csvStr + str3
                file.close()
                csvFile.write(csvStr)
                csvFile.close()
            else:
                pass
        else:
            pass


    def getPartList(self):
        pFileTxt = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        if pFileTxt != None:
            self.parseFileName(str(pFileTxt))
            pFileCsv = tkFileDialog.asksaveasfile(mode='w', **self.wfile_opt)

            if pFileCsv != None:
                self.parseFileName(str(pFileCsv), fType='csv', mode=1)
                self.toCSV(pFileTxt, pFileCsv)


    def getPinList(self):
        pnFileTxt = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        if pnFileTxt != None:
            self.parseFileName(str(pnFileTxt))
            pnFileCsv = tkFileDialog.asksaveasfile(mode='w', **self.wfile_opt)
            if pnFileCsv != None:
                self.parseFileName(str(pnFileCsv), fType='csv', mode=1)
                self.toCSV(pnFileTxt, pnFileCsv)


    def getNetList(self):
        nFileTxt = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        if nFileTxt != None:
            self.parseFileName(str(nFileTxt))
            nFileCsv = tkFileDialog.asksaveasfile(mode='w', **self.wfile_opt)
            if nFileCsv != None:
                self.parseFileName(str(nFileCsv), fType='csv', mode=1)
                self.toCSV(nFileTxt, nFileCsv)

    def getBOMList(self):
        bFileTxt = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        if bFileTxt != None:
            self.parseFileName(str(bFileTxt))
            bFileCsv = tkFileDialog.asksaveasfile(mode='w', **self.wfile_opt)
            if bFileCsv != None:
                self.parseFileName(str(bFileCsv), fType='csv', mode=1)
                self.toCSV(bFileTxt, bFileCsv, mode=1)

    def initGUI(self):

        bF = Frame(self)
        bF.pack()

        partFrame = LabelFrame(bF, text='Part List')
        partFrame.pack(side='left')
        b1 = Button(partFrame, text='Select Part File', command = self.getPartList)
        b1.pack(side='left')

        pinFrame = LabelFrame(bF, text='Pin List')
        pinFrame.pack(side='left')
        b2 = Button(pinFrame, text='Select Pin File', command = self.getPinList)
        b2.pack(side='left')

        netFrame = LabelFrame(bF, text='Net List')
        netFrame.pack(side='left')
        b3 = Button(netFrame, text='Select Net File', command=self.getNetList)
        b3.pack(side='left')

        bomFrame = LabelFrame(bF, text='BOM List')
        bomFrame.pack(side='left')
        b4 = Button(bomFrame, text='Select BOM File', command=self.getBOMList)
        b4.pack(side='left')

        self.logFrame = LabelFrame(self, text='Log')
        self.logFrame.pack()
        self.logVar = StringVar()
        self.log = Label(self.logFrame, textvariable=self.logVar, width=50)
        self.log.pack(side='bottom', anchor='s')

    def parseFileName(self, string, fType='txt', mode=0):
        wordArray = re.findall(r'(\w)', string)
        sz = len(wordArray)
        if sz > 100:
            sz = sz/2 + (sz/2-50)
            self.log.pack_forget()
            self.log = Label(self.logFrame, textvariable=self.logVar, width=int(sz))
            self.log.pack(side='bottom', anchor='s')
        try:
            fName = re.findall(r'/([\w]+\.{0})'.format(fType), string)[0]
            fLoc = re.findall(r'\'([\w\W]+)/', string)[0]
            if mode == 0:
                self.logThis = 'Loaded: ' + fName + '\nFrom: ' + fLoc
            elif mode == 1:
                self.logThis = 'Saved: ' + fName + '\nTo: ' + fLoc
            else:
                self.logThis = 'Mode error'
        except:
            self.logThis = 'Failed to load/save file'

        self.logVar.set(self.logThis)

    def newInstance(self):
        EagleFilesToCSV(master=Toplevel())

    # This method is used to generate the file menu. The file menu is applied
    # to the Tk() root frame, not the self.mainFrame that everything else belongs to.
    # This is because it was meant to be this way.
    def fillMenuButtons(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New Window", command=self.newInstance)

        self.menubar.add_cascade(label="File", menu=filemenu)



if __name__ == "__main__":
    root = Tk()
    app = EagleFilesToCSV(master=root)
    app.mainloop()
