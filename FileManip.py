'''
Created on Feb 11, 2015

@author: Max Ruiz
'''

import tkFileDialog as tf

class FileManip():
    def __init__(self, root):
        self.root = root
        self.fileOptions()

    def fileOptions(self):
        self.fopt = file_opt = {}
        file_opt['defaultextension'] = '.csv'
        file_opt['filetypes'] = [('Comma Separated Values', '.csv'), ('Excel', '.xlsx'), ('All Files', '.*')]
        file_opt['initialdir'] = 'C:\\'
        file_opt['parent'] = self.root
        file_opt['multiple'] = False
        file_opt['title'] = 'File'

    def openFile(self):
        return tf.askopenfile(mode = 'r', **self.fopt)

    def openFilename(self):
        return tf.askopenfilename(**self.fopt)

    def saveFile(self):
        return tf.asksaveasfile(mode = 'w', **self.fopt)

    def saveFilename(self):
        return tf.asksaveasfilename(**self.fopt)

    def getDirectory(self):
        return tf.askdirectory(**self.fopt)

    def extendFileOptions(self, xopts={}):
        for opt in xopts:
            try:
                self.fopt[opt] = xopts[opt]
            except:
                # poor/bad option
                pass

''' # For Testing
import Tkinter
if __name__=='__main__':
    root = Tkinter.Tk()
    fm = FileManip(root)
    fm.openFile()
    print(fm.openFilename)
    yopts = {}
    yopts['multiple'] = True
    fm.extendFileOptions(xopts=yopts)
    root.mainloop()
'''
