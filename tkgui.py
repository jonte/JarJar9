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
#from matchdialog import MatchDialog
from BoardFrame import BoardFrame
from RackFrame import RackFrame
from ControlsFrame import ControlsFrame

class GUI:
    root = Tk()
    root.wm_title("JarJar9")
    placedPieces = []
    activeGame = None

    def __init__(self):
        self.drawControls()
        self.drawRackFrame()
        self.drawBoardFrame()
        self.login()

    def drawBoardFrame(self):
        self.boardFrame = BoardFrame(self)
        self.boardFrame.grid(row=0,column=0, columnspan=2)

    def drawRackFrame(self):
        self.rackFrame = RackFrame(self)
        self.rackFrame.grid(row=1,column=1, sticky=E)

    def login(self):
        self.jjb9 = JJB9()
        self.h = self.jjb9.h
        saltedPassword = self.h.getSaltedPassword()
        self.jjb9.login(self.h.getUsername(), saltedPassword)
        self.chooseGame()

    def setGameID(self, gid):
        self.activeGame = gid

    def chooseGame(self):
#        md = MatchDialog()
#        selectedItem = None
#        md.displayGames([('Maria', '<3', '1', lambda: self.setGameID(1)),\
#                     ('Ivar','hej','2', lambda: self.setGameID(2))])
#        md.root.wait_window(md.root)
        self.h.prettyPrintGames(self.jjb9.getGames())
        game = raw_input("Pick game with ID: ")
        self.setGameID(game)
        print "Item", self.activeGame

    def syncAction(self):
        game    = json.loads(self.jjb9.getGame(self.activeGame))
        self.boardFrame.drawBoard()
        board   = game['content']['game']['tiles']
        self.h.printBoard(self.jjb9.staticTiles)

        for w in board:
            self.boardFrame.setLetter(w[0],w[1],w[2])
        self.rackFrame.clearRack()
        try:
            rack = game['content']['game']['players'][0]['rack']
        except KeyError:
            rack = game['content']['game']['players'][1]['rack']
        print "Your rack is: %s" % (' '.join(rack))
        self.rackFrame.drawRack([(x, '1') for x in rack])

    def drawControls(self):
        cf = ControlsFrame(self)
        cf.grid(row=1, column=0, sticky=W)
        cf.drawControls()

    def playPieces(self):
        response = self.jjb9.playPieces(self.activeGame, self.placedPieces)
        js = json.loads(response)
        if js['status'] == 'success':
            print "Successfully played"
        self.syncAction()
        print response

    def placePiece(self, widget):
        selectedPiece = self.rackFrame.selectedPiece
        if selectedPiece != None:
            widget.draw(selectedPiece[0], selectedPiece[1], 'lightpink')
            gridInfo = selectedPiece[2].grid_info()
            self.placedPieces.append((int(widget.grid_info()['column']),
                                      int(widget.grid_info()['row']),
                                      selectedPiece[0],
                                      False))
            selectedPiece[2].destroy()
            self.rackFrame.selectedPiece = None

    def lookupTileStyle(self, x,y):
        return self.jjb9.staticTiles[y][x]

gui = GUI()
mainloop()
