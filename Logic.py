
class BoardSizeError (ValueError):
	def __init__ (self, axis, given_size):
		ValueError.__init__(self, "Boards {0} size must be either 4, 8, 12, 14 or 16. Not {1!s}".format(axis, given_size))

class BoardWinnerError(ValueError):
	def __init__ (self, given_value):
		ValueError.__init__(self, "Winner value can only be '>' or '<'. Not {0!s}".format(given_value))

class BoardPlayerError(ValueError):
	def __init__ (self, given_value):
		ValueError.__init__(self, "First move value can only be 'B' or 'W'. Not {0!s}".format(given_value))

BLACK = "B"
WHITE = "W"
EMPTY = None
SIMPLE = 1
FULL = 2

class Game:
	def __init__ (self, first_move=BLACK, y_size=16, x_size=16, game_winner=">", board=None, game_type=SIMPLE):

		# Board
		if board == None:
			self.Board = []
			for _ in range(y_size):
				row = []
				for _ in range(x_size):
					row.append(None)
				self.Board.append(row)

			# Board Visualisation
			''' size=4
			0	[[None, None, None, None],
			1	 [None, None, None, None],
			2	 [None, None, None, None],
			3	 [None, None, None, None]]
			idx	    0     1     2     3	
			'''		

			# Now lets change the centre peices to b and w
			self.Board[int((y_size/2)-1)][int((x_size/2)-1)] = WHITE	# This addsthe centre peices
			self.Board[int(y_size/2)][int(x_size/2)] = WHITE			# This addsthe centre peices
			self.Board[int((y_size/2)-1)][int(x_size/2)] = BLACK		# This addsthe centre peices
			self.Board[int(y_size/2)][int((x_size/2)-1)] = BLACK		# This addsthe centre peices

			# Board Visualisation
			''' size=4
			0	[[None, None, None, None],
			1	 [None,  W  ,  B  , None],
			2	 [None,  B  ,  W  , None],
			3	 [None, None, None, None]]
			idx	    0     1     2     3	
			'''
		else:
			self.Board=board

		# Size Attrs

		if y_size >= 4 or y_size <= 16:
			if y_size % 2 != 0:
				raise BoardSizeError("y", y_size)
		else:
			raise BoardSizeError("y", y_size)

		if x_size >= 4 or x_size <= 16:
			if x_size % 2 != 0:
				raise BoardSizeError("x", x_size)
		else:
			raise BoardSizeError("x", x_size)

		self.X_Size = x_size
		self.Y_Size = y_size

		# How to win

		if game_winner in [">", "<"]:
			self.Game_Winner = game_winner
		else:
			raise BoardWinnerError(game_winner)

		# First mover
		if first_move in [BLACK, WHITE]:
			self.Current_Player = first_move # This is the player whose turn it currently is.
		else:
			raise BoardPlayerError(first_move)

		if game_type == SIMPLE:
			self.Game_Type = SIMPLE
		else:
			self.Game_Type = FULL

		# Is a game in process
		self.Running = False

	def Start_Game(self):
		self.Running = True
	
	def Next_Move (self, x: int, y: int) -> bool:
		can_move, to_flip = self.Try_Move([y, x])
		if can_move:
			self.Swap_Player()
			if not self.Available_Moves():
				self.Swap_Player()
				if not self.Available_Moves():
					# Check if there are any available moves for the next player, end loop if not
					self.Running = False
					# Game Over
			return True

		if not self.Available_Moves():
				self.Swap_Player()
				if not self.Available_Moves():
					# Check if there are any available moves for the next player, end loop if not
					self.Running = False
					# Game Over
		return False

	def Swap_Player (self):
		# Check the current player, swap them around 
		if self.Current_Player == BLACK:
			self.Current_Player = WHITE
		else:
			self.Current_Player = BLACK
		
	def Try_Move(self, move: list) -> tuple:
		# Try to move, and if its valid, flip the appropriate pieces, otherwise return True
		if self.Game_Type == SIMPLE:
			can_move, to_flip = self.Can_Move_Simple(move)
		else:
			can_move, to_flip = self.Can_Move_Full(move)
		if can_move:
			self.Flip(to_flip)
			self.Add_Peice(move)
			return True, to_flip
		else:
			return False, None

	def Add_Peice (self, place: list): 
		# This will take the players input, so deducting one to turn them into indexes is necessary
		x = place[1] - 1
		y = place[0] - 1

		self.Board[y][x] = self.Current_Player

	def Flip (self, to_flip: list):
		# Flip em!, Just loops through the given list and changes it to the current player
		for coord in to_flip:
			self.Board[coord[1]][coord[0]] = self.Current_Player
	
	def Available_Moves (self) -> bool:
		# Loops through the entire board and try to move to that position
		# Returns Bool, List/None
		# Bool = True if move is possible, else bool = false
		# List = places to flip, None if there are no possible places

		# Return true if any case is possible, otherwise it will return false if the loops finish
		for y_idx in range(len(self.Board)):
			for x_idx in range(len(self.Board[y_idx])):
				if self.Game_Type == SIMPLE:
					can_move, to_flip = self.Can_Move_Simple([y_idx+1, x_idx+1])
				else:
					can_move, to_flip = self.Can_Move_Full([y_idx+1, x_idx+1])
				if can_move:
					return True

		return False

	def Can_Move_Full (self, move: list) -> tuple:
		# Create variables out of the parameters, easier to read the code that way
		y = move[0] - 1 
		x = move[1] - 1 # Minus one to convert to indexes

		# This will be the edges of the board, checking past these will result in an index error
		max_y_size = self.Y_Size - 1 # Again these are indexes
		max_x_size = self.X_Size - 1

		# The opposite player will be checked for in the Board
		if self.Current_Player == BLACK:
			opposite = WHITE
		else:
			opposite = BLACK

		to_flip = []

		# Check if the position is already satisfied
		if self.Board[y][x] != EMPTY:
			return False, None

		# Check the horizontal axis: y remains constant
		# Checking from left to right
		found_same = False

		side = "left"

		maybe_add = []

		for x_val in range(len(self.Board[y])):
			if x_val == x: 
				# Check if the side of the placement has changed, this will affect 
				#how we check if a piece should be flipped
				side = "right"
				found_same = False
				for coord in maybe_add:
					to_flip.append(coord)
				maybe_add = []
				continue
			if side == "left":
				if found_same: # Here we check if we are between two of our peices and if we are,
					# We will check if its an opposite peice and add it to a list to be added
					# to oue to_flip list, this will be cleared if theres an empty spot between
					if self.Board[y][x_val] == opposite:
						maybe_add.append([x_val, y])
					elif self.Board[y][x_val] == EMPTY:
						found_same = False
						maybe_add = []
					elif self.Board[y][x_val] == self.Current_Player:
						maybe_add = []
				else:
					if self.Board[y][x_val] == self.Current_Player:
						found_same = True
			else:
				# this will check if there is an opposite piece and add to a list if so
				# other wise we want to stop if theres an empty place
				# or add everything between the two peices
				if self.Board[y][x_val] == opposite:
					maybe_add.append([x_val, y])
				elif self.Board[y][x_val] == EMPTY:
					break
				else:
					for coord in maybe_add:
						to_flip.append(coord)
					break

		# Check the vertical axis: x remains constant
		# Checking from top to bottom
		found_same = False

		side = "above"

		maybe_add = []

		for y_val in range(len(self.Board)):
			if y_val == y:
				# Check if the side of the placement has changed, this will affect 
				#how we check if a piece should be flipped
				side = "below"
				found_same = False
				for coord in maybe_add:
					to_flip.append(coord)
				maybe_add = []
				continue
			if side == "above": 
				if found_same: # Here we check if we are between two of our peices and if we are,
					# We will check if its an opposite peice and add it to a list to be added
					# to oue to_flip list, this will be cleared if theres an empty spot between
					if self.Board[y_val][x] == opposite:
						maybe_add.append([x, y_val])
					elif self.Board[y_val][x] == EMPTY:
						found_same = False
						maybe_add = []
					elif self.Board[y_val][x] == self.Current_Player:
						maybe_add = []
				else:
					if self.Board[y_val][x] == self.Current_Player:
						found_same = True
			else: # this will check if there is an opposite piece and add to a list if so
				# other wise we want to stop if theres an empty place
				# or add everything between the two peices
				if self.Board[y_val][x] == opposite:
					maybe_add.append([x, y_val])
				elif self.Board[y_val][x] == EMPTY:
					break
				else:
					for coord in maybe_add:
						to_flip.append(coord)
					break

		# Check Diagonal
		# The max amount of places in a grid on the diagonal axis is the smallest size of the board
		# Eg if self.Y_Size is lower than self.X_size, self.Y_Size is the max amount

		max_moves = self.Y_Size if self.Y_Size < self.X_Size else self.X_Size

		# Bottom to top: as x increases, y decreases by the same amount 

		# Because it is diagonal, two of the corner sections are valid moves, lets rule them out first
		if [x, y] in [[0, 0], [0, 1], [1, 0], # Top left
					  [max_x_size-1, max_y_size],  # Bottom Right
					  [max_x_size, max_y_size],
					  [max_x_size, max_y_size-1]]:
			pass # Skip if the piece is in the corner
		else:
			found_same = False

			side = "left"

			maybe_add = []
			
			x_srt = 0  # These will be the start values
			y_srt = 0  # These will be the start values

			# Find the value farthest to the left
			for inc in range(max_moves):
				if x - inc <= 0 or y + inc >= max_y_size:
					x_srt = x - inc
					y_srt = y + inc
					break

			# Now loop
			for inc in range(max_moves):
				if x_srt + inc > max_x_size or y_srt - inc < 0:
					break

				if [x_srt+inc, y_srt-inc] == [x, y]:
					# Check if the side of the placement has changed, this will affect 
					#how we check if a piece should be flipped
					side = "right"
					found_same = False
					for coord in maybe_add:
						to_flip.append(coord)
					maybe_add = []
					continue

				if side == "left":
					if found_same: # Here we check if we are between two of our peices and if we are,
						# We will check if its an opposite peice and add it to a list to be added
						# to oue to_flip list, this will be cleared if theres an empty spot between
						if self.Board[y_srt-inc][x_srt+inc] == opposite:
							maybe_add.append([x_srt+inc, y_srt-inc])
						elif self.Board[y_srt-inc][x_srt+inc] == EMPTY:
							found_same = False
							maybe_add = []
						elif self.Board[y_srt-inc][x_srt+inc] == self.Current_Player:
							maybe_add = []
					else:
						if self.Board[y_srt-inc][x_srt+inc] == self.Current_Player:
							found_same = True
				else:# this will check if there is an opposite piece and add to a list if so
					# other wise we want to stop if theres an empty place
					# or add everything between the two peices
					if self.Board[y_srt-inc][x_srt+inc] == opposite:
						maybe_add.append([x_srt+inc, y_srt-inc])
					elif self.Board[y_srt-inc][x_srt+inc] == EMPTY:
						break
					else:
						for coord in maybe_add:
							to_flip.append(coord)
						break

		# Top to bottom: as x increase, y also increase

		# Because it is diagonal, two of the corner sections are valid moves, lets rule them out first
		if [x, y] in [[0, max_y_size-1],# Bottom Left
					  [0, max_y_size],
					  [1, max_y_size],  
					  [max_x_size-1, 0],# Top right
					  [max_x_size, 0],
					  [max_x_size, 1]]:
			pass # Skip if the piece is in the corner
		else:
			found_same = False

			side = "left"

			maybe_add = []
			
			x_srt = 0  # These will be the start values
			y_srt = 0  # These will be the start values

			# Find the value farthest to the left
			for inc in range(max_moves+1):
				if x - inc <= 0 or y - inc <= 0:
					x_srt = x - inc
					y_srt = y - inc
					break

			# Now Loop
			for inc in range(max_moves):
				if x_srt + inc > max_x_size or y_srt + inc > max_y_size:
					break

				if [x_srt+inc, y_srt+inc] == [x, y]:
					# Check if the side of the placement has changed, this will affect 
					#how we check if a piece should be flipped
					side = "right"
					found_same = False
					for coord in maybe_add:
						to_flip.append(coord)
					maybe_add = []
					continue

				if side == "left":
					if found_same: # Here we check if we are between two of our peices and if we are,
						# We will check if its an opposite peice and add it to a list to be added
						# to oue to_flip list, this will be cleared if theres an empty spot between
						if self.Board[y_srt+inc][x_srt+inc] == opposite:
							maybe_add.append([x_srt+inc, y_srt+inc])
						elif self.Board[y_srt+inc][x_srt+inc] == EMPTY:
							found_same = False
							maybe_add = []
						elif self.Board[y_srt+inc][x_srt+inc] == self.Current_Player:
							maybe_add = []
					else:
						if self.Board[y_srt+inc][x_srt+inc] == self.Current_Player:
							found_same = True
				else:
					# this will check if there is an opposite piece and add to a list if so
					# other wise we want to stop if theres an empty place
					# or add everything between the two peices
					if self.Board[y_srt+inc][x_srt+inc] == opposite:
						maybe_add.append([x_srt+inc, y_srt+inc])
					elif self.Board[y_srt+inc][x_srt+inc] == EMPTY:
						break
					else:
						for coord in maybe_add:
							to_flip.append(coord)
						break

		# Output

		if len(to_flip) >= 1:
			return True, to_flip
		else:
			return False, None


	def Can_Move_Simple (self, move: list) -> tuple:
		# Create variables out of the parameters, easier to read the code that way
		y = move[0] - 1 
		x = move[1] - 1 # Minus one to convert to indexes

		# This will be the edges of the board, checking past these will result in an index error
		max_y_size = self.Y_Size - 1 # Again these are indexes
		max_x_size = self.X_Size - 1

		# The opposite player will be checked for in the Board
		if self.Current_Player == BLACK:
			opposite = WHITE
		else:
			opposite = BLACK

		to_flip = []

		# Check if the position is already satisfied
		if self.Board[y][x] != EMPTY:
			return False, None

		# Check everything around the position
		# Check left: x - 1
		if x == 0:
			pass
		elif self.Board[y][x-1] == opposite:
			to_flip.append([x-1, y])

		# Check right: x + 1
		if x == max_x_size:
			pass
		elif self.Board[y][x+1] == opposite:
			to_flip.append([x+1, y])

		# Check above: y - 1
		if y == 0:
			pass
		elif self.Board[y-1][x] == opposite:
			to_flip.append([x, y-1])

		# Check below: y + 1
		if y == max_y_size:
			pass
		elif self.Board[y+1][x] == opposite:
			to_flip.append([x, y+1])

		# Check above-left: x - 1, y - 1
		if x == 0 or y == 0:
			pass
		elif self.Board[y-1][x-1] == opposite:
			to_flip.append([x-1, y-1])

		# Check above-right: x + 1, y - 1

		if x == max_x_size or y == 0:
			pass
		elif self.Board[y-1][x+1] == opposite:
			to_flip.append([x+1, y-1])

		# Check bottom-right: x + 1, y + 1
		if x == max_x_size or y == max_y_size:
			pass
		elif self.Board[y+1][x+1] == opposite:
			to_flip.append([x+1, y+1])

		# Check bottom-left: x - 1, y + 1
		if x == 0 or y == max_y_size:
			pass
		elif self.Board[y+1][x-1] == opposite:
			to_flip.append([x-1, y+1])

		# Output

		if len(to_flip) >= 1:
			return True, to_flip
		else:
			return False, None
	
	def Get_Discs (self) -> list:
		# Returns a list in the form [b_disc, w_discs]
		b_ammount = 0
		w_ammount = 0

		# Add 1 to the b(lack)_ammount if a black is found
		# Add 1 to the w(hite)_ammount if a white is found
		# Do nothing if a None is found
		for y in self.Board:
			for val in y:
				if val == BLACK:
					b_ammount += 1
				elif val == WHITE:
					w_ammount += 1

		return [b_ammount, w_ammount]

	# End Game

	def Check_Winner (self) -> tuple:
		discs = self.Get_Discs()
		b_ammount = discs[0]
		w_ammount = discs[1]

		# Based on the users chosen way to win, decide who won

		if self.Game_Winner == ">":
			if b_ammount > w_ammount:
				return BLACK, [b_ammount, w_ammount]
			elif b_ammount < w_ammount:
				return WHITE, [b_ammount, w_ammount]
			else:
				return "NO ONE", [b_ammount, w_ammount]
		else:
			if b_ammount < w_ammount:
				return BLACK, [b_ammount, w_ammount]
			elif b_ammount > w_ammount:
				return WHITE, [b_ammount, w_ammount]
			else:
				return "NO ONE", [b_ammount, w_ammount]
