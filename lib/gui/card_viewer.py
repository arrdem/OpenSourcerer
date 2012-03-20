#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tkinter

class card_viewer(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent or self
        self.resizable(width=True, height=True)
        self.parent.geometry('+%d+%d' % (320,320))

        self.img_frame = tkinter.LabelFrame()
        self.img_frame.grid(column=0,row=0,rowspan=1000, sticky='NW')

        self.data_frame = tkinter.LabelFrame(width=400, height=330)
        self.data_frame.grid(column=1,row=0,rowspan=1000,sticky = 'NSW')

        #self.button = Tkinter.Button(self, text=u"[ Done ]", command=self.destroy)
        #self.button.grid(column = 0, sticky='S')

        self.data = {}
        self.data_labels = []

    def set_img(self, f):
        self.raw_card = open(f, 'rb')
        self.card = tkinter.PhotoImage(self.raw_card)
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
        self.title("Card Viewer: "+d["Card Name:"])

    def set(self, card):
        self.set_img(card["Img File:"])
        self.set_data(card)

if __name__ == "__main__":
    app = card_viewer(None)
    app.set_img("./img/5634.jpeg")
    app.set(eval("""{'Mana Cost:': [0, 0, 0, 0, 1, 1, 2], 'Card Name:': 'Disciple of Grace', 'Community Votes:': 520, 'P/T:': [1, 2], 'Rarity:': 'Common', 'Card Text:': 'Protection from blackCycling 2 (2, Discard this card: Draw a card. ) ', 'Meta Rating:': 2015.0, 'Multiverse ID:Community Rating:': 'Sets  Legality', 'Community Rating:': 3.875, 'TAGS': ['Cycling', 'Protection'], 'Loyalty:': 'Sets  Legality', 'Types:': ['Creature', 'Human', 'Cleric'], 'Multiverse ID:': 5634, 'Hand/Life:': [0, 0], 'Img File:': u'./img/5634.jpeg', 'Img MD5Sum:': 'c198675a21668dedfdbd44bb9e7d0110', 'Flavor Text:': 'Beauty is beyond law.', 'Artist:': 'Robh Ruppel', 'Expansion:': "Urza's Saga (Common) "}"""))
    app.mainloop()
    exit(0)
