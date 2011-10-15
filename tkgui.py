#!/usr/bin/env python
#    This file is part of JarJar9.
#
#    JarJar9 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    JarJar9 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with JarJar9.  If not, see <http://www.gnu.org/licenses/>.

from Tkinter import *
from JarJar9 import JJB9
from JarJar9 import Helpers
import json
from Tile import Tile

class GUI:
    root = Tk()
    root.wm_title("JarJar9")
    boardRefs = [[None for x in range(15)] for xx in range(15)]
    rack = []
    selectedPiece = None
    placedPieces = []
    activeGame = None

    def __init__(self):
        self.drawControls()
        self.login()

    def login(self):
        self.jjb9 = JJB9()
        self.h = self.jjb9.h
        saltedPassword = self.h.getSaltedPassword()
        self.jjb9.login(self.h.getUsername(), saltedPassword)
        self.chooseGame()

    def chooseGame(self):
        self.h.prettyPrintGames(self.jjb9.getGames())
        game = raw_input("Pick game with ID: ")
        self.activeGame = game

    def syncAction(self):
        game    = json.loads(self.jjb9.getGame(self.activeGame))
        self.drawBoard()
        board   = game['content']['game']['tiles']
        self.h.printBoard(self.jjb9.staticTiles)

        for w in board:
            self.setLetter(w[0],w[1],w[2])
        self.clearRack()
        try:
            rack = game['content']['game']['players'][0]['rack']
        except KeyError:
            rack = game['content']['game']['players'][1]['rack']
        print "Your rack is: %s" % (' '.join(rack))
        self.drawRack([(x, '1') for x in rack])

    # Controls are on the 15:th row, 0-14 are board cells
    def drawControls(self):
        syncBtn = Button(self.root, text="Sync",\
                         command=lambda: self.syncAction())
        playBtn = Button(self.root, text="Play!",\
                        command=lambda: self.playPieces())

        syncBtn.grid(row=15, column=0, columnspan=3)
        playBtn.grid(row=15, column=3, columnspan=3)

    def playPieces(self):
        response = self.jjb9.playPieces(self.activeGame, self.placedPieces)
        js = json.loads(response)
        if js['status'] == 'success':
            print "Successfully played"
        self.syncAction()
        print response


    def drawRack(self, rack):
        for widget in self.rack:
            widget.destroy()
        self.rack = []
        for i in range(7):
            try:
                w = Tile(self.root, letter = rack[i][0],
                                    points = rack[i][1],
                                    callback = lambda x: self.rackPieceSelect(x.widget.master),
                                    color='lightblue')
                w.grid(row = 15, column = 8+i)
                self.rack.append(w)
            except IndexError:
                pass # There aren't enough tiles

    def clearRack(self):
        for x in self.rack:
            x.destroy()
           
    def rackPieceSelect(self, piece):
        piece.highlight()
        self.selectedPiece = (piece.letter, piece.points, piece)

    def placePiece(self, widget):
        if self.selectedPiece != None:
            widget.draw(self.selectedPiece[0], self.selectedPiece[1], 'lightpink')
            gridInfo = self.selectedPiece[2].grid_info()
            self.placedPieces.append((int(widget.grid_info()['column']),
                                      int(widget.grid_info()['row']),
                                      self.selectedPiece[0],
                                      False))
            self.selectedPiece[2].destroy()
            self.selectedPiece = None

    def drawBoard(self):
        for y in range(0,15):
            for x in range(0,15):
                style = self.lookupTileStyle(x,y)
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

                w = Tile(  self.root, 
                            letter=letter,
                            points = points,
                            callback = lambda x: self.placePiece(x.widget.master),
                            color = color)
                self.boardRefs[x][y] = w
                w.grid(row=y, column=x)

    def lookupTileStyle(self, x,y):
        return self.jjb9.staticTiles[y][x]

    def setLetter(self, x, y, letter):
        points = self.h.getLetterPoints(letter)
        self.boardRefs[x][y].draw(letter,points)
        self.boardRefs[x][y].lock()

gui = GUI()
mainloop()
