from Tkinter import *
from Tile import Tile

class ControlsFrame(Frame):
    def __init__(self, parent, **options):
        Frame.__init__(self, parent.root)
        self.parent = parent

    def drawControls(self):
        syncBtn = Button(self, text="Check for moves",\
                         command=lambda: self.parent.syncAction())
        playBtn = Button(self, text="Play!",\
                        command=lambda: self.parent.playPieces())

        syncBtn.grid(row=0, column=0, sticky=W)
        playBtn.grid(row=0, column=1, sticky=E)

#if __name__ == "__main__":
#    tk = Tk()
#    cf = ControlsFrame(tk)
#    cf.drawControls()
#    cf.grid(row=0, column=0)
#    mainloop()
