import tkinter 		as tk
import Widgets 		as wg
import Logic   		as lgc
from   tkinter.ttk 	import Separator
from   tkinter.messagebox import showerror, showinfo

# Fonts that we can utilise
FONTS = {"large":("Helvetica", 20), "medium":("Helvetica", 16), "small":("Helvetica", 12)}

class Handler: # Handles the window and the Game interaction
	def __init__(self):

		# Game Handle
		self.Game = None
		self.GameParams = {}

		# Window Handle
		self.Window = Window(self)
		self.Window.mainloop()

	def Replay (self): # Reset attributes and classes
		self.GameParams = {}
		del self.Game
		self.Game = None
		
	def Is_Running (self):
		return self.Game.Running

	def Start_Game(self): # Begin the game, run the updates needed.
		self.Game = lgc.Game(**self.GameParams)
		self.Game.Start_Game()

		# Update Game page
		self.Update_Game()
		self.Window.Pages["Game"].Update_Game_Type()

	def Get_Current_Player(self) -> str: # get the current player whose turn it is
		if self.Game.Running:
			if self.Game.Current_Player == "B":
				return "black"
			else:
				return "white"
		else:
			return "None"

	def Get_Game_Type(self) -> str: # Get the game rule type
		g = self.Game.Game_Type
		if g == 1:
			return "SIMPLE"
		else:
			return "FULL"

	def Get_Score(self) -> tuple: # Get the current score
		s = self.Game.Get_Discs()
		return s[0], s[1] # b, w

	def Move(self, x: int, y: int) -> bool: # Make a move on a given place
		complete = self.Game.Next_Move(x, y)
		if complete:
			self.Update_Game()
			self.Game_Complete_Check()
			return True
		self.Update_Game()
		self.Game_Complete_Check()
		return False

	def Get_Winner(self) -> tuple: # Gets the winner of the game
		return self.Game.Check_Winner()

	def Game_Complete_Check(self): # Check if the game is over and act accordingly
		if self.Is_Running() == False:
			# Run Game Over feature here
			self.Window.showPage("Postgame")
			# Update the post page
			self.Window.Pages["Postgame"].Update()

	def Update_Game(self): # Run a full update on the game
		self.Window.Pages["Game"].Full_Update()

class Window (tk.Tk): # This will be the main window of the GUI
	def __init__ (self, controller, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.Handler = controller # This is handler between the game and window

		# Root attributes
		self.title("Othello")
		
		try:
			self.iconbitmap("Icon.ico")
		except:
			pass

		self.minsize(600, 600)
		#self.maxsize(1000,1000)

		# Master frame
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		# Set up the pages
		self.Pages = {}
		for page in (Pregame, Custom_Board, Game, Postgame):
			# Initiate each page and add them to the dictionary
			# Dictionary will use the name of the class so that it can be accessed
			# without the knowledge of the clas name
			new = page(self.container, self)
			self.Pages[page.FrameName] = new
			new.grid(row=0, column=0, sticky="nsew")

		# Show the initial page
		self.showPage("Pregame")

	# Window

	def showPage(self, pagename: str): # Show a chosen page
		page = self.Pages[pagename]
		page.tkraise()

	# Game
	def Begin_Game(self): # Start the game
		self.Handler.Start_Game()

	def Get_Current_Player (self) -> str: # Get the current player
		return self.Handler.Get_Current_Player()

	def Replay(self): # Clean up the old game, start an new one
		self.Pages["Pregame"].__GUI_Reset__()
		self.Pages["Game"].Reset_Game()
		self.Handler.Replay()
		self.showPage("Pregame")

class Pregame (tk.Frame): # The 'home' screen
	FrameName = "Pregame"
	def __init__ (self, parent, controller):
		tk.Frame.__init__(self, parent)	

		self.controller = controller
		self.configure(bg="white")

		self.set_vals = []

		self.__GUI_Reset__()

	def __GUI_Reset__(self): #  This will clean the screen and then recreate it, this is essential for replaying the game
		for widget in self.winfo_children():
			widget.destroy()

		# Title Banner
		tk.Label(self, text="Otello", font=FONTS["large"], bg="white").pack(side="top")
		Separator(self, orient="horizontal").pack(side="top", fill="x", padx=10)

		# Rule Set
		rule_set_frame = tk.Frame(self, bg="white")
		rule_set_frame.pack(pady=10)
		# Subheading
		self.rs_label = tk.Label(rule_set_frame, text="Rule Set", font=FONTS["medium"], bg="white")
		self.rs_label.pack(side="top")

		self.full_btn = tk.Button(rule_set_frame, text="FULL", font=FONTS["medium"], bg="#bbbbbb",
			command=lambda:self.Select_Rule_Set("full"))
		self.full_btn.pack()

		self.simple_btn = tk.Button(rule_set_frame, text="SIMPLE", font=FONTS["medium"], bg="#bbbbbb",
			command=lambda:self.Select_Rule_Set("simple"))
		self.simple_btn.pack()

		# Row Size
		row_frame = tk.Frame(self, bg="white")
		row_frame.pack(pady=10)

		self.row_label = tk.Label(row_frame, text="Board Rows", font=FONTS["medium"], bg="white")
		self.row_label.grid(row=0, column=0, columnspan=7)

		self.Rows_Buttons = []

		place = 0
		for rows in [4, 6, 8, 10, 12, 14, 16]:
			x = tk.Button(row_frame, text=str(rows), font=FONTS["small"], bg="#bbbbbb",
				command=lambda rows=rows: self.Select_Rows(rows))
			x.grid(row=1, column=place)
			self.Rows_Buttons.append(x)
			place += 1

		# Column Size
		col_frame = tk.Frame(self, bg="white")
		col_frame.pack(pady=10)

		self.col_label = tk.Label(col_frame, text="Board Columns", font=FONTS["medium"], bg="white")
		self.col_label.grid(row=0, column=0, columnspan=7)

		self.Cols_Buttons = []

		place = 0
		for cols in [4, 6, 8, 10, 12, 14, 16]:
			x = tk.Button(col_frame, text=str(cols), font=FONTS["small"], bg="#bbbbbb",
				command=lambda cols=cols: self.Select_Cols(cols))
			x.grid(row=1, column=place)
			self.Cols_Buttons.append(x)
			place += 1

		# First to Move
		first_move_frame = tk.Frame(self, bg="white")
		first_move_frame.pack(pady=10)

		self.first_move_label = tk.Label(first_move_frame, text="First to move", bg="white", font=FONTS["medium"])
		self.first_move_label.grid(row=0, column=0, columnspan=2)

		self.black_btn = tk.Button(first_move_frame, text="Black", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda:self.Select_First_Move("black"))
		self.black_btn.grid(row=1, column=0)

		self.white_btn = tk.Button(first_move_frame, text="White", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda:self.Select_First_Move("white"))
		self.white_btn.grid(row=1, column=1)

		# How to win
		condition_frame = tk.Frame(self, bg="white")
		condition_frame.pack(pady=10)

		self.condition_label = tk.Label(condition_frame, text="The winner is, the player with..",
			bg="white", font=FONTS["medium"])
		self.condition_label.grid(row=0, column=0, columnspan=2)

		self.greater_score = tk.Button(condition_frame, text="more discs.", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda: self.Select_Condition(">"))
		self.greater_score.grid(row=1, column=0)

		self.lesser_score = tk.Button(condition_frame, text="less discs.", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda: self.Select_Condition("<"))
		self.lesser_score.grid(row=1, column=1)


		# Start the game button
		self.Start_Game_Btn = tk.Button(self, text="Start", bg="#ff2222", activebackground="#992222",
									font=FONTS["medium"])
		self.Start_Game_Btn.pack(side="bottom")

	def Select_Rule_Set(self, _set: str): # sets the rule set of the game
		if _set == "simple":
			self.controller.Handler.GameParams["game_type"] = 1 # Corresponds to the game logic
		else:
			self.controller.Handler.GameParams["game_type"] = 2

		self.full_btn.destroy()
		self.simple_btn.destroy()
		self.rs_label.configure(text="Rule Set: " + _set.upper())

		self.set_vals.append("rules")
		self.Check_Can_Start()

	def Select_Rows(self, rows: int): # Sets the rows of the board
		self.controller.Handler.GameParams["y_size"] = rows

		for button in self.Rows_Buttons:
			button.destroy()

		self.row_label.configure(text="Board Rows: " + str(rows))

		self.set_vals.append("rows")
		self.Check_Can_Start()

	def Select_Cols(self, cols: int): # sets the columns of the board
		self.controller.Handler.GameParams["x_size"] = cols

		for button in self.Cols_Buttons:
			button.destroy()

		self.col_label.configure(text="Board Columns: " + str(cols))
		
		self.set_vals.append("cols")
		self.Check_Can_Start()

	def Select_First_Move (self, mover: str): # Sets the first player to make a move
		if mover == "black":
			self.controller.Handler.GameParams["first_move"] = "B"
		else:
			self.controller.Handler.GameParams["first_move"] = "W"

		self.black_btn.destroy()
		self.white_btn.destroy()

		self.first_move_label.configure(text="First to move: " + mover)

		self.set_vals.append("move")
		self.Check_Can_Start()

	def Select_Condition(self, condition: str):# This will set the game win condition
		self.controller.Handler.GameParams["game_winner"] = condition

		if condition == ">":
			self.condition_label.configure(text="The winner is, the player with more discs.")
		else:
			self.condition_label.configure(text="The winner is, the player with less discs.")

		self.lesser_score.destroy()
		self.greater_score.destroy()

		self.set_vals.append("win")
		self.Check_Can_Start()

	def Check_Can_Start (self): # This will start the game if the game can be started
		if "rules" in self.set_vals and\
		   "rows" in self.set_vals and\
		   "cols" in self.set_vals and\
		   "move" in self.set_vals and\
		   "win"  in self.set_vals:
		   self.Start_Game_Btn.configure(bg="#22ff22", activebackground="#229922",
		   	command=lambda: self.Start_Custom_Board())

	def Start_Custom_Board (self):
		self.controller.Pages["Setup_Board"].Setup_Board()
		self.controller.showPage("Setup_Board")
		self.controller.Pages["Setup_Board"].Instructions_Display()

class Custom_Board (tk.Frame):
	FrameName = "Setup_Board"
	def __init__ (self, parent, controller):
		tk.Frame.__init__ (self, parent)

		self.controller = controller
		self.configure(bg="white")

		# Title bar
		self.Title_Frame = tk.Frame(self, bg="white")
		self.Title_Frame.pack(side="top", fill="x")

		# Title
		tk.Label(self.Title_Frame, text="Create Custom Board", bg="white", font=FONTS["medium"]).pack(side="left")

		# Start Button
		start = tk.Button(self.Title_Frame, text="Play", bg="#22ff22", activebackground="#229922", font=FONTS["medium"],
			command=lambda: self.Start())
		start.pack(side="right")		


		# Use custom Board check button
		self.Use_Board = tk.IntVar()

		Use_Board = tk.Checkbutton(self.Title_Frame, text="Use custom board", font=FONTS["medium"],
			bg="white", activebackground="white",
			var=self.Use_Board, onvalue=1, offvalue=0)
		Use_Board.pack(side="right", padx=10)

		
		# Board
		self.Board_Area = tk.Frame(self, bg="#009900")
		self.Board_Area.pack(side="top", fill="both", expand=True)

		self.Board = []

	def Setup_Board (self):
		for widget in self.Board_Area.winfo_children():
			widget.destroy()
		self.Board = []

		
		for y in range(self.controller.Handler.GameParams["y_size"]):
			row = []
			for x in range(self.controller.Handler.GameParams["x_size"]):
				# Diameter with respond to the length of the shortest side of the board
				height = self.Board_Area.winfo_height()
				width = self.Board_Area.winfo_width()

				if height > width:
					diameter = width/self.controller.Handler.GameParams["x_size"]
				else:
					diameter = height/self.controller.Handler.GameParams["y_size"]

				self.Board_Area.grid_columnconfigure(x, weight=1)
				self.Board_Area.grid_rowconfigure(y, weight=1)

				disc = wg.Disc(self.Board_Area, self.controller, diameter=diameter, mode="setup")
				disc.grid(row=y, column=x, sticky="nsew")
				row.append(disc)

			self.Board.append(row)

	def Parse_Board (self) -> list: # This will parse the GUI board and create a board that will work for the Game()
		new_board = []
		for row in self.Board:
			new_row = []
			for disc in row:
				if disc.Current_Color == "white":
					new_row.append("W")
				elif disc.Current_Color == "black":
					new_row.append("B")
				else:
					new_row.append(None)
			new_board.append(new_row)

		return new_board

	def Instructions_Display(self):
		showinfo("How to use", "Click on a tile to cycle between white, black or empty. Check the \"Use Custom Board\" box to use this board!")

	def Start (self): # This will check if the user wants to use a custom board and then will set Game board to be the users selection
		if self.Use_Board.get():
			self.controller.Handler.GameParams["board"] = self.Parse_Board()
		self.controller.Begin_Game()
		self.controller.Pages["Game"].__GUI_init__()
		self.controller.Pages["Game"].Update_Board()
		self.controller.showPage("Game")

class Game (tk.Frame): # This is the 'stage' where the game will be played.
	FrameName = "Game"
	def __init__ (self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller
		self.configure(bg="white")

		# Status Bar
		self.Status_Bar = tk.Frame(self, bg="white")
		self.Status_Bar.pack(side="top", fill="x")

		self.Status_Bar.grid_columnconfigure(0, weight=1)
		self.Status_Bar.grid_columnconfigure(1, weight=1)
		self.Status_Bar.grid_columnconfigure(2, weight=1)
		self.Status_Bar.grid_rowconfigure(0, weight=1)

		self.Current_Player = tk.Label(self.Status_Bar, text="None", bg="white", font=FONTS["medium"])
		self.Current_Player.grid(row=0, column=0)

		self.Game_Type = tk.Label(self.Status_Bar, text="FULL",  bg="white", font=FONTS["medium"])
		self.Game_Type.grid(row=0, column=1)

		self.Score = tk.Label(self.Status_Bar, text="Black: 2 | 2:White", bg="white", font=FONTS["medium"])
		self.Score.grid(row=0, column=2)

		# Board
		self.Board_Area = tk.Frame(self, bg="#009900")
		self.Board_Area.pack(side="top", fill="both", expand=True)

		self.Board = []

	def __GUI_init__ (self): # This will initiate the game board once all the datya is provided.
		for y in range(self.controller.Handler.GameParams["y_size"]):
			row = []
			for x in range(self.controller.Handler.GameParams["x_size"]):
				# Diameter with respond to the length of the shortest side of the board
				height = self.Board_Area.winfo_height()
				width = self.Board_Area.winfo_width()

				if height > width:
					diameter = width/self.controller.Handler.GameParams["x_size"]
				else:
					diameter = height/self.controller.Handler.GameParams["y_size"]

				self.Board_Area.grid_columnconfigure(x, weight=1)
				self.Board_Area.grid_rowconfigure(y, weight=1)

				disc = wg.Disc(self.Board_Area, self.controller, diameter=diameter,
					command= lambda x=x, y=y: self.Disc_Function(x, y))
				disc.grid(row=y, column=x, sticky="nsew")
				row.append(disc)

			self.Board.append(row)

		self.Update_Board()

	def Reset_Game(self):  #This will reset the game board to its initial state
		self.Board = []
		for widget in self.Board_Area.winfo_children():
			widget.destroy()

	def Disc_Function (self, x: int, y: int): # This is the function run when the player clicks a disc slot/disc
		if not self.controller.Handler.Move(x+1, y+1): # Try run the Move function on the Handler
			self.Invalid_Move()

	def Invalid_Move(self): # This command will run when a player tries to make a move thats not possible
		showerror("Invalid Move", "You cannot move there!")

	def Update_Board (self): # Update the board to mathe the Game() board
		for y in range(len(self.Board)):
			for x in range(len(self.Board[y])):
				game_piece = self.controller.Handler.Game.Board[y][x]
				if game_piece == None:
					pass
				elif game_piece == "B":
					if self.Board[y][x].Current_Color != "black":
						self.Board[y][x].Set_Piece_Color("black")
				elif game_piece == "W":
					if self.Board[y][x].Current_Color != "white":
						self.Board[y][x].Set_Piece_Color("white")

	def Update_Current_Player (self): # Update the current player identifier
		self.Current_Player.config(text="Turn: " + self.controller.Get_Current_Player())

	def Update_Game_Type(self): # Update the game type identifier
		g_type = self.controller.Handler.Get_Game_Type()
		self.Game_Type.configure(text="Rules: " + g_type)

	def Update_Score (self): # Update the score identifier
		b, w = self.controller.Handler.Get_Score()
		self.Score.configure(text="Black: {0!s} | {1!s} :White".format(b, w))

	def Full_Update(self): # Run a full update on the graphics
		self.Update_Score()
		self.Update_Current_Player()
		self.Update_Board()

class Postgame (tk.Frame): # The 'end game' screen
	FrameName = "Postgame"
	def __init__ (self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller
		self.configure(bg="white")

		# Set a page title
		self.Title = tk.Label(self, text="Game Over!", bg="white", font=FONTS["large"])
		self.Title.pack(side="top")

		Separator(self, orient="horizontal").pack(side="top", fill="x", padx=10)

		# Set the winner text object
		self.Winner = tk.Label(self, text="The winner is black-discs.", bg="white", font=FONTS["medium"])
		self.Winner.pack(side="top")

		# Create the replay and exit buttons
		self.Buttons = tk.Frame(self, bg="white")
		self.Buttons.pack()

		Replay = tk.Button(self.Buttons, text="Replay", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda: self.Replay())
		Replay.grid(row=0, column=0)

		Quit = tk.Button(self.Buttons, text="Quit", bg="#bbbbbb", font=FONTS["medium"],
			command=lambda: self.Quit())
		Quit.grid(row=0, column=1)

		# the area for the board output
		self.Board_Area = tk.Frame(self, bg="white")
		self.Board_Area.pack(side="bottom")

		# Score text
		self.Score = tk.Label(self.Board_Area, text="", bg="white", font=FONTS["medium"])
		self.Score.pack()

		# The display for the board
		self.Board_Display = tk.Frame(self.Board_Area, bg="green")
		self.Board_Display.pack()

		self.Board = []

	def Replay(self): # Initiate the Replay
		self.controller.Replay()

	def Quit(self): # Kill the game
		self.controller.destroy()
		exit()

	def Update_Board (self): # Update the game board display, kill old, create new
		for widget in self.Board_Display.winfo_children():
			widget.destroy()

		for y in range(self.controller.Handler.GameParams["y_size"]):
			row = []
			for x in range(self.controller.Handler.GameParams["x_size"]):
				self.Board_Area.grid_columnconfigure(x, weight=1)
				self.Board_Area.grid_rowconfigure(y, weight=1)

				col = None
				place_col = self.controller.Handler.Game.Board[y][x]
				if place_col == "B":
					col = "black"
				elif place_col == "W":
					col = "white"

				disc = wg.Disc(self.Board_Display, self.controller, col=col, diameter=50)
				disc.grid(row=y, column=x, sticky="nsew")
				row.append(disc)

			self.Board.append(row)

	def Update(self): # Update the whole page
		winner, scores = self.controller.Handler.Get_Winner() 
		if winner.lower() == "b":
			winner = "black-discs"
		elif winner.lower() == "w":
			winner = "white-discs"
		else:
			winner == "no one"
		self.Winner.configure(text="The winner is " + winner)
		self.Score.configure(text="Black: {0!s} | {1!s}:White".format(scores[0], scores[1]))
		self.Update_Board()

if __name__ == "__main__":
	Window = Handler()
