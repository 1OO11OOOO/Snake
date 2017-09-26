from Tkinter import *
from random import randint

class Block():

	def __init__(self, can, x, y, obj = "snake", color = "violet"):

		if obj == "snake":
			self.tk_id = can.create_rectangle(x, y, x+10, y+10, fill=color)
			self.x, self. y = x, y
		elif obj == "apple":
			self.tk_id = can.create_oval(x, y, x+10, y+10, fill="light green")
			self.x, self. y = x, y

class Snake(list):

	def __init__(self, can, root):

		root.bind("<Up>", lambda event: self.change_direction(-2))
		root.bind("<Down>", lambda event: self.change_direction(2))
		root.bind("<Left>", lambda event: self.change_direction(-1))
		root.bind("<Right>", lambda event: self.change_direction(1))
		self.can = can
		self.direction = 1

	def initialize(self, start_dir):

		for block in self:
			self.can.delete(block.tk_id)
		del self[:]

		self.append(Block(self.can, 150, 150))
		self.append(Block(self.can, 160, 150))
		self.append(Block(self.can, 170, 150,"snake", "red"))

		self.direction = start_dir
		self.score = 0
		self.score_msg = self.can.create_text(10+6*len(str(self.score)), 15, text="", font="system 20 bold", fill='red')

	def step(self):

		self.append(self.pop(0))

		# New coordinates of the head
		if self.direction == -2: # Up
			self.move(-1, self[-2].x, self[-2].y-10)
			self.can.itemconfig(self[-2].tk_id, fill='violet')
			self.can.itemconfig(self[-1].tk_id, fill='red')

		elif self.direction == 2: # Down
			self.move(-1, self[-2].x, self[-2].y+10)
			self.can.itemconfig(self[-2].tk_id, fill='violet')
			self.can.itemconfig(self[-1].tk_id, fill='red')

		elif self.direction == -1: # Left
			self.move(-1, self[-2].x-10, self[-2].y)
			self.can.itemconfig(self[-2].tk_id, fill='violet')
			self.can.itemconfig(self[-1].tk_id, fill='red')

		elif self.direction == 1: # Right
			self.move(-1, self[-2].x+10, self[-2].y)
			self.can.itemconfig(self[-2].tk_id, fill='violet')
			self.can.itemconfig(self[-1].tk_id, fill='red')


		# If the snake is not in bounds, gets to the opposite side
		if not (0 <= self[-1].x <= 290 and 0 <= self[-1].y <= 290):
			if   self[-1].x < 0:  self.move(-1, 290, self[-1].y)
			elif self[-1].x > 290: self.move(-1, 0, self[-1].y)
			elif self[-1].y < 0:  self.move(-1, self[-1].x, 290)
			elif self[-1].y > 290: self.move(-1, self[-1].x, 0)

	def move(self, ref, x, y):
		self.can.coords(self[ref].tk_id, x, y, x+10, y+10)
		self[ref].x, self[ref].y = x, y

	def eat(self, apple):

		self.score += int(1000/self.can.delay)
		self.can.delete(self.score_msg)
		self.score_msg = self.can.create_text(10+6*len(str(self.score)), 15, text="%d" % self.score, font="system 20 bold italic", fill='red')
		self.insert(0, Block(self.can, self[0].x, self[0].y))

	def change_direction(self, choice):
		if not (self.can.lose or self.can.pause):
			last_dir = self.direction
			if last_dir + choice != 0:
				self.direction = choice

				if self.can.start:
					self.can.start = False
					self.can.snake.initialize(choice)
					self.can.nextMove()


class Apple(Block):

	def __init__(self, can, x, y):

		if (x,y) == (0,0):
			x,y = randint(0,29)*10, randint(0,29)*10

		Block.__init__(self, can, x, y, "apple")
		self.can = can

	def move(self, x, y):

		if (x,y) == (0,0):
			x,y = randint(0,29)*10, randint(0,29)*10

		self.can.coords(self.tk_id, x, y, x+10, y+10)
		self.x, self.y = x, y

	def __del__(self):
		self.can.delete(self.tk_id)

