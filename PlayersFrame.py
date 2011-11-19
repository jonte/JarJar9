from Tkinter import *

class PlayersFrame(Frame):
    player1Variable = StringVar()
    player2Variable = StringVar()

    def __init__(self, parent, **options):
        Frame.__init__(self, parent.root)
        self.parent = parent
        player1Lbl = Label(self, textvariable=self.player1Variable)
        player2Lbl = Label(self, textvariable=self.player2Variable)

        player1Lbl.grid(row=1, column=0, sticky=W)
        player2Lbl.grid(row=1, column=1, sticky=E)

    def setPlayerText(self, number, name, score):
        if number == 1:
            self.player1Variable.set("%s: %s" % (name, score))
        elif number == 2:
            self.player2Variable.set("%s: %s" % (name, score))

#if __name__ == "__main__":
#    tk = Tk()
#    pf = PlayersFrame(tk)
#    pf.grid(row=0, column=0)
#    mainloop()
