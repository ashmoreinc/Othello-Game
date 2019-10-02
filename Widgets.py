from tkinter import Canvas

COL_BLACK = "black"
COL_WHITE = "white"

class Disc (Canvas): # This will be the widget of the discs
    def __init__ (self, parent, main_window, col=None, bg="#009900", diameter=50, mode="game",
                    command=None):
        Canvas.__init__(self, parent, width=diameter, height=diameter)
        self.configure(highlightthickness=1, highlightbackground="black",
                        borderwidth=1, bg=bg)
        
        self.Main_Window = main_window

        # Do we create the disc initially or not?
        if col == None:
            self.Visible = False
        else:
            self.Visible = True
        if self.Visible:
            self.Disc = self.create_oval((0, 0, diameter, diameter), fill=col, tags="Disc")
        else:
            self.Disc = None
    
        self.Mode = mode

        # Display Attributes
        self.diameter = diameter

        # Disc Attribute
        self.Current_Color = col

        # Binds
        self.command = command
        self.bind("<Button-1>", self._Onclick)

        self.bind("<Configure>", self._Onresize)

    def Cycle (self):
        # Cycle: Black -> White, White -> Empty, Empty -> Black
        if self.Current_Color == COL_BLACK:
            self.Current_Color = COL_WHITE
        elif self.Current_Color == COL_WHITE:
            self.Current_Color = None
        elif self.Current_Color == None:
            self.Current_Color = COL_BLACK

        self.Redraw()

    def Set_Piece_Color (self, col: str): # Set the Disc color
        self.Current_Color = col
        self.Redraw()

    def Redraw(self): # Redraw the piece, clear the canvas and redraw all
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if self.Current_Color != None:
            if h > w:
                self.Disc = self.create_oval((0, 0, w, w), fill=self.Current_Color, tags="Disc")
            else:
                self.Disc = self.create_oval((0, 0, h, h), fill=self.Current_Color, tags="Disc")

    def _Onresize(self, event): # Resize the piece when the canvas is resized by its parent
        self.delete("all")
        self.Redraw()

    def _Onclick (self, event): # Run the given command (if any) when clicked
        if self.Mode == "setup":
            self.Cycle()
        else:
            if self.command == None:
                pass                 
            else:
                self.command()