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
from MatchDialog    import MatchDialog
from BoardFrame     import BoardFrame
from RackFrame      import RackFrame
from ControlsFrame  import ControlsFrame
from PlayersFrame   import PlayersFrame

class GUI:
    root = Tk()
    root.wm_title("JarJar9")
    placedPieces = []
    activeGame = None
    tickLength = 5000

    def __init__(self):
        self.drawControls()
        self.drawRackFrame()
        self.drawBoardFrame()
        self.drawPlayersFrame()
        self.login()
        self.root.withdraw()

    def drawBoardFrame(self):
        self.boardFrame = BoardFrame(self)
        self.boardFrame.grid(row=0,column=0, columnspan=2)

    def drawRackFrame(self):
        self.rackFrame = RackFrame(self)
        self.rackFrame.grid(row=1,column=1, sticky=E)

    def drawPlayersFrame(self):
        self.playersFrame = PlayersFrame(self.root)
        self.playersFrame.grid(row=2, column = 0, columnspan=3, sticky = W+E)
        self.playersFrame.columnconfigure(0, weight=1)

    def login(self):
        self.jjb9 = JJB9()
        self.h = self.jjb9.h
        saltedPassword = self.h.getSaltedPassword()
        self.jjb9.login(self.h.getUsername(), saltedPassword)
        self.chooseGame()

    """
    Sets gameID, shows main game window and initiates a sync
    """
    def startGameWithID(self, gid):
        self.setGameID(gid)
        self.root.update()
        self.root.deiconify()
        #self.updateLoop()
        self.syncAction()

    """
    Triggers a fetch loop, updating the game from the server.
    TODO: This isn't a valid approach.. The board can't be updated when the player
            is making a move etc, that would make the board clear.
    """
    def updateLoop(self):
        print "Updating.."
        self.syncAction()
        self.root.after(self.tickLength, self.updateLoop)

    def setGameID(self, gid):
        self.activeGame = gid

    def setPlayerScores(self, playersJson):
        for playerNum in range(len(playersJson)):
            self.playersFrame.setPlayerText(
                        int(playerNum), 
                        playersJson[playerNum]['username'],
                        playersJson[playerNum]['score'])

    def chooseGame(self):
        md = MatchDialog()
        selectedItem = None
        games = []
        for game in self.jjb9.getGames():
            games.append((game['players'][0]['username'],
                          game['last_move']['main_word'],
                          game['id'],
                          lambda: self.startGameWithID(game['id'])))
        md.displayGames(games)

    def syncAction(self):
        game    = json.loads(self.jjb9.getGame(self.activeGame))
        self.boardFrame.drawBoard()
        board   = game['content']['game']['tiles']
        self.h.printBoard(self.jjb9.staticTiles)

        for w in board:
            self.boardFrame.setLetter(w[0],w[1],w[2])
        self.rackFrame.clearRack()
        self.setPlayerScores(game['content']['game']['players'])
        try:
            rack = game['content']['game']['players'][0]['rack']
        except KeyError:
            rack = game['content']['game']['players'][1]['rack']
        print "Your rack is: %s" % (' '.join(rack))
        self.rackFrame.drawRack([(x, self.h.getLetterPoints(x)) for x in rack])

    def drawControls(self):
        cf = ControlsFrame(self.root)
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
