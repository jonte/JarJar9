from Tkinter import *
from Tile import Tile

class BoardFrame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.boardRefs = [[None for x in range(15)] for xx in range(15)]
    
    def drawBoard(self):
        for y in range(0,15):
            for x in range(0,15):
                style = self.parent.lookupTileStyle(x,y)
                if style == 0:
                   letter = ''
                   points = ''
                   color  = "lightgray"
                elif style == 1:
                   letter = 'DL'
                   points = ''
                   color  = "green"
                elif style == 2:
                   letter = 'TL'
                   points = ''
                   color  = "blue"
                elif style == 3:
                   letter = 'DW'
                   points = ''
                   color  = "orange"
                elif style == 4:
                   letter = 'TW'
                   points = ''
                   color  = "red"

                w = Tile(   self, 
                            letter=letter,
                            points = points,
                            callback = lambda x: self.parent.placePiece(x.widget.master),
                            color = color)
                self.boardRefs[x][y] = w
                w.grid(row=y, column=x)

    def setLetter(self, x, y, letter):
        points = self.parent.h.getLetterPoints(letter)
        self.boardRefs[x][y].draw(letter,points)
        self.boardRefs[x][y].lock()
