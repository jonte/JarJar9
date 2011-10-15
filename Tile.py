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

class Tile(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=24, height=24)
        self.canvas.bind("<Button-1>", options['callback'])
        self.color  = None
        self.letter = None
        self.points = None
        if ('color' in options):
            color = options['color']
        else:
            color = 'white'
        self.draw(options['letter'], options['points'], color)

    def draw(self,letter, points, color = 'white'): 
        self.letter = letter
        self.points = points
        self.color = color
        w = self.canvas
        w.delete(ALL)
        w.create_rectangle(0,0,24,24, fill=color)
        if len(letter) > 1:
            w.create_text(12,12, text=letter, font=("Helvetica", 10))
        else:
            w.create_text(12,12, text=letter, font=("Helvetica", 12))
        w.create_text(19,19, text=points, font=("Helvetica", 8))
        w.pack()

    def highlight(self):
        if self.color == 'beige':
            self.draw(self.letter, self.points, 'lightblue')
        else:
            self.draw(self.letter, self.points, 'beige')

    def lock(self):
        self.canvas.bind("<Button-1>", lambda x: 1+1)
        self.draw(self.letter, self.points)


if __name__ == "__main__":
    master = Tk()
    for y in range(5):
        for x in range(5):
            t = Tile(master, letter='', points='',\
                    callback = lambda x: x.widget.master.draw('X','5'))
            t.grid(row=y,column=x)
    mainloop()

