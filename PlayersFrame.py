from Tkinter import *

class PlayersFrame(Frame):

    def initVar(self, sv):
        self.player1Lbl.configure(textvariable=sv)

    def __init__(self, parent, **options):
        Frame.__init__(self, parent)
        self.player1Variable = StringVar(master = parent)
        self.player2Variable = StringVar(master = parent)
        self.parent = parent
        self.player1Lbl = Label(self, textvariable=self.player1Variable)
        self.player2Lbl = Label(self, textvariable=self.player2Variable)

        self.player1Lbl.grid(row=1, column=0, sticky=W)
        self.player2Lbl.grid(row=1, column=1, sticky=E)

    def setPlayerText(self, number, name, score):
        if number == 0:
            self.player1Variable.set("%s: %s" % (name, score))
        elif number == 1:
            self.player2Variable.set("%s :%s" % (score, name))

if __name__ == "__main__":
    tk = Tk()
    pf = PlayersFrame(tk)
    pf.grid(row=0, column=0)
    mainloop()
