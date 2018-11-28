from objects import *
from tkinter import *
from path import *

class Board(Canvas):

	def __init__(self, root):

		Canvas.__init__(self, width = 300, height = 300, bg='pink')
		self.root = root

		root.bind("<space>", self.set_pause)
		root.bind("<n>", self.new_game)
		root.bind("<q>", self.quit_game)
		root.bind("<g>", self.show_grid)

		self.snake = Snake(self, root)
		self.apple = Apple(self, 0, 0)
		self.grid_b = False
		self.pause = False
		self.lose = False
		self.start = True
		self.delay = 90
		self.msg = ""
		self.pathLines = []

		self.snake.initialize(1)

	def set_pause(self, event):
		if not self.lose:
			if self.pause:
				self.pause = False
				self.delete(self.msg)
				self.nextMove()
			else:
				self.pause = True
				self.msg = self.create_text(150, 150, text="PAUSE", fill='white', font="system 70 bold italic")

	def new_game(self, event):

		self.delete("all")

		self.apple = Apple(self, 0, 0)
		self.lose, self.pause, self.start = False, False, True

		self.snake.initialize(1)

	def nextMove(self):

		if self.lose or self.pause or self.start:
			return None

		s = self.snake
		s.step()

		head = (s[-1].x, s[-1].y)
		if head in ((b.x, b.y) for b in s[:-1]):
			self.end_game()
			return

		if head == (self.apple.x, self.apple.y):
			s.eat(self.apple)

			self.apple.move(0, 0)
			while self.inSnake(self.apple):
				self.apple.move(0, 0)
		
		snakePos = (self.snake[-1].y//10, self.snake[-1].x//10)
		applePos = (self.apple.y//10, self.apple.x//10)
		tab = self.getMat(self.snake, self.apple)
		mat = Matrix(30, 30, tab)
		print("lol")
		path = next(mat.bfs_paths(snakePos, applePos))
		self.drawPath(path)

		self.after(self.delay-int(len(self.snake)), self.nextMove)


	def drawPath(self, path):
		for line in self.pathLines:
				self.delete(line)

		for i in range(len(path)-1):
			x1, y1 = path[i]
			x2, y2 = path[i+1]
			self.pathLines += [self.create_line(y1*10 + 5, x1*10 + 5, y2*10 + 5, x2*10 + 5)]

	def end_game(self):

		if self.lose:
			return

		self.lose = True
		self.create_text(150, 150, text="WASTED", font='system 70 bold italic', fill='white')
		self.create_text(150, 200, text="SCORE: %d" % self.snake.score, font='system 25 bold italic', fill='red')

	def quit_game(self, event):
		self.root.destroy()

	def inSnake(self, apple):

		for part in self.snake:
			if (apple.x, apple.y) == (part.x, part.y):
				return True

		return False

	def show_grid(self, event):

		if not self.grid_b:
			self.grid_b = True
			self.grid = []
			for i in range(1, 50):
				self.grid += [self.create_line(i*10, 0, i*10, 500)]
				self.grid += [self.create_line(0, i*10, 500, i*10)]
		else:
			self.grid_b = False
			for line in self.grid:
				self.delete(line)

	def getMat(self, snake, apple):
		mat = []
		snakePos = snake.getPos()
		applePos = apple.getPos()

		for i in range(len(snakePos)):
			snakePos[i] = (snakePos[i][1], snakePos[i][0])
		applePos = (applePos[1], applePos[0])

		for i in range(30):
			mat += [[]]
			for j in range(30):
				mat[i] += [0]
		for pos in snakePos:
			x, y = pos
			mat[x][y] = 1
		mat[snakePos[-1][1]][snakePos[-1][0]] = 0

		return mat


