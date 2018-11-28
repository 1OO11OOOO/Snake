class Matrix():
	def __init__(self, height, width, tab):
		self.height = height
		self.width = width
		self.mat = tab
		self.visited = []

		for i in range(height):
			self.visited += [[]]
			for j in range(width):
				self.visited[i] += [tab[i][j]]


	def printMat(self):
		for i in range(self.height):
			print(self.mat[i])
		print('\n')

	def inBounds(self, point):
		x, y = point
		return 0<=x<self.height and 0<=y<self.height


	def getNeighboors(self, point):
		x, y = point
		neighboors = []

		for i in range(-1,2):
			for j in range(-1,2):
				if self.inBounds((x+i, y+j)) and (abs(i)+abs(j))%2 == 1:
					if self.mat[x+i][y+j] == 0:
						neighboors += [(x+i, y+j)]
		return neighboors


	def bfs_paths(self, start, goal):
		queue = [(start, [start])]
		self.visited[start[0]][start[1]] = 1
		while queue:
			(vertex, path) = queue.pop(0)
			for next in self.getNeighboors(vertex):
				if next == goal:
					yield path + [next]
				elif not self.visited[next[0]][next[1]]:
					queue.append((next, path + [next]))
					self.visited[next[0]][next[1]] = 1


