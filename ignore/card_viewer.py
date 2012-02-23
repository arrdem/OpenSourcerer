#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter
import Image, ImageTk

class card_viewer(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent or self
        self.resizable(width=True, height=True)
        self.parent.geometry('+%d+%d' % (320,320))

        self.img_frame = Tkinter.LabelFrame()
        self.img_frame.grid(column=0,row=0,rowspan=1000, sticky='NW')

        self.data_frame = Tkinter.LabelFrame(width=400, height=330)
        self.data_frame.grid(column=1,row=0,rowspan=1000,sticky = 'NSW')

        #self.button = Tkinter.Button(self, text=u"[ Done ]", command=self.destroy)
        #self.button.grid(column = 0, sticky='S')

        self.data = {}
        self.data_labels = []

    def set_img(self, f):
        self.raw_card = Image.open(f)
        self.card = ImageTk.PhotoImage(self.raw_card)
        self.label_image = Tkinter.Label(self.img_frame, image=self.card)
        self.label_image.place(x=0,y=0,width=self.raw_card.size[0],height=self.raw_card.size[1])
        self.label_image.grid(column=0,row=0,rowspan=1000)

    def set_data(self, d):
        self.data_labels = []
        self.data = d

        i=0
        for foo in self.data:
            self.data_labels.append(Tkinter.Label(self.data_frame, text=(str(foo)+" "+str(self.data[foo])), wraplength=450))
            self.data_labels[-1].grid(column=1,row=i, sticky='W')
            i+=1

        self.update()
        self.title("Card Viewer: "+d[u"Card Name:"])

    def set(self, card):
        self.set_img(card[u"Img File:"])
        self.set_data(card)

if __name__ == "__main__":
    app = card_viewer(None)
    app.set_img("./img/5634.jpeg")
    app.set(eval("""{u'Mana Cost:': [0, 0, 0, 0, 1, 1, 2], u'Card Name:': 'Disciple of Grace', u'Community Votes:': 520, u'P/T:': [1, 2], u'Rarity:': 'Common', u'Card Text:': 'Protection from blackCycling 2 (2, Discard this card: Draw a card. ) ', u'Meta Rating:': 2015.0, u'Multiverse ID:Community Rating:': 'Sets  Legality', u'Community Rating:': 3.875, 'TAGS': ['Cycling', 'Protection'], u'Loyalty:': 'Sets  Legality', u'Types:': ['Creature', 'Human', 'Cleric'], u'Multiverse ID:': 5634, u'Hand/Life:': [0, 0], u'Img File:': u'./img/5634.jpeg', u'Img MD5Sum:': 'c198675a21668dedfdbd44bb9e7d0110', u'Flavor Text:': 'Beauty is beyond law.', u'Artist:': 'Robh Ruppel', u'Expansion:': "Urza's Saga (Common) "}"""))
    app.mainloop()
    exit(0)
