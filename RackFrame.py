from Tkinter import *
from Tile import Tile

class RackFrame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.selectedPiece = None
        self.rack = []

    def drawRack(self, rack):
        for widget in self.rack:
            widget.destroy()
        self.rack = []
        for i in range(7):
            try:
                w = Tile(   self, 
                            letter = rack[i][0],
                            points = rack[i][1],
                            callback = lambda x: self.rackPieceSelect(x.widget.master),
                            color='lightblue')
                w.grid(row = 0, column = i)
                self.rack.append(w)
            except IndexError:
                pass # There aren't enough tiles

    def clearRack(self):
        for x in self.rack:
            x.destroy()
           
    def rackPieceSelect(self, piece):
        piece.highlight()
        self.selectedPiece = (piece.letter, piece.points, piece)
