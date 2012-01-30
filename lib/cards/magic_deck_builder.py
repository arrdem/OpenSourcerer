#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mcardlib
if mcardlib._test() != 0:
    raise Exception("[!] MCARDLIB FAILED TO IMPORT. Somehow.")

import Tkinter
import tkMessageBox
from PIL import Image, ImageTk

_lib = mcardlib.load()

class main(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.resizable(width=True, height=True)
        self.grid_columnconfigure(0,weight=2)
        self.title(u'Magic Deck Builder')
        self.i = 15

    def initialize(self):
        self.grid()

        self.picture(15,column=5,row=0)

        self.deck = [Tkinter.Listbox(self)]

        for i in range(len(self.deck)):
            self.deck[i].grid(column=i,row=0,rowspan=3,sticky='NS')
        
        self.update()

    def picture(self, i, column=0,row=0,columnspan=3):
        self.raw_card = self.getImage(i)
        self.card = ImageTk.PhotoImage(self.raw_card)
        self.label_image = Tkinter.Label(self, image=self.card)
        self.label_image.place(x=0,y=0,width=self.raw_card.size[0],height=self.raw_card.size[1])
        self.label_image.grid(column=column,row=row,columnspan=columnspan)

    def getImage(self, i):
        return Image.open("./img/{0}.jpeg".format(i))

    def NextButton(self):
        self.i += 1
        self.picture(self.i)
        self.update()
        
    def Exit(self):
        exit(0)
        
if __name__ == "__main__":
    
    app = main(None)
    app.mainloop()
    exit(0)
