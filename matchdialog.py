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

class MatchItem(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent)
        self.parent = parent
        nickLabel       = Label(self, text=options['nickname'])
        lastWordLabel   = Label(self, text=options['lastword'])
        gameIDLabel     = Label(self, text=options['gameid'])
        playButton      = Button(self, text="Play!",\
                    command=lambda: self.playCallback(options['callback']))
        nickLabel.grid(row=0, column=0)
        lastWordLabel.grid(row=1, column=0)
        gameIDLabel.grid(row=2, column=0)
        playButton.grid(row=0,column=1,rowspan=3, sticky=W+E+N+S)

    def playCallback(self, cb):
        self.parent.destroy()
        cb()

class MatchDialog:
    root = Tk()
    root.wm_title("JarJar9: Select match")

    # Games is a list of tuples ("opponent", "lastWord", "gameID", 
    #                               playbuttoncallback)
    def displayGames(self, games):
        i = 0
        for (nick, lw, gid, cb) in games:
            match = MatchItem(self.root, nickname=nick, lastword=lw, 
                              gameid=gid, callback=cb)
            match.grid(row=i, column=0)
            i += 1

if __name__ == "__main__":
    md = MatchDialog()
    md.displayGames([('Maria', '<3', '1', lambda: 1+1),\
                     ('Ivar','hej','2', lambda: 1+1)])
    mainloop()
