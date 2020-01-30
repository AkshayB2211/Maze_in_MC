
import random
import mcpi.block as block
from mcpi.minecraft import Minecraft
from collections import deque

mc = Minecraft.create()

rows = 15
cols = 15
size = 3


class Cell:
	def __init__(self, i, j, pos):
		self.i = i
		self.j = j
		self.pos = pos
		self.visited = False

	def break_walls(self, other):
		if other.i < self.i :
			# removing right and left walls
			for i in range(size):
				remove(tuple(map(lambda i, j: i + j, self.pos, (0, i, 1))))
				remove(tuple(map(lambda i, j: i + j, self.pos, (0, i, 2))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (3, i, 1))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (3, i, 2))))

		if other.i > self.i :
			# removing right and left walls
			for i in range(size):
				remove(tuple(map(lambda i, j: i + j, self.pos, (3, i, 1))))
				remove(tuple(map(lambda i, j: i + j, self.pos, (3, i, 2))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (0, i, 1))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (0, i, 2))))

		if other.j < self.j :
			# removing top and bottom walls
			for i in range(size):
				remove(tuple(map(lambda i, j: i + j, self.pos, (1, i, 0))))
				remove(tuple(map(lambda i, j: i + j, self.pos, (2, i, 0))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (1, i, 3))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (2, i, 3))))

		if other.j > self.j :
			# removing top and bottom walls
			for i in range(size):
				remove(tuple(map(lambda i, j: i + j, self.pos, (1, i, 3))))
				remove(tuple(map(lambda i, j: i + j, self.pos, (2, i, 3))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (1, i, 0))))
				remove(tuple(map(lambda i, j: i + j, other.pos, (2, i, 0))))

def remove(pos):
	x, y, z = pos
	mc.setBlock(x, y, z, 0)

def fill(pos, a, b, c, block=0):
	x, y, z = pos
	for i in range(a):
		for j in range(b):
			for k in range(c):
				mc.setBlock(x+i, y+k, z+j, block)


def draw_rect(pos, w, h, block):
	x, y, z = pos
	for i in range(w):
		mc.setBlock(x+i, y, z, block)
		mc.setBlock(x+i, y, z+h-1, block)
	for i in range(h):
		mc.setBlock(x, y, z+i, block)
		mc.setBlock(x+w-1, y, z+i, block)

def draw_grid(pos, block):
	# draw the grid in minecraft
	# store its properties in a grig of cell class
	grid = []
	x, y, z = pos
	for i in range(rows):
		grid.append([])
		for j in range(cols):
			pos = (x + size*i, y, z + size*j)
			grid[i].append(Cell(i, j, pos))
			for k in range(size):
				pos = (x + size*i, y + k, z + size*j)
				draw_rect(pos, size+1, size+1, block)

	current = grid[0][0]
	current.visited = True
	stack = deque()
	stack.append(current)	# stack for back tracking

	# main loop
	running = True
	while running:
		next_ = next_cell(current, grid)
		if next_ is None:
			try:
				current = stack.pop()
			except:
				break;
		else:
			current.break_walls(next_)
			current = next_
			current.visited = True
			stack.append(current)


# return a valid neighbor cell
def next_cell(current, grid):
	i = current.i
	j = current.j

	opt = []
	# add to the list if cell is not visited
	# and also taking care of edge cases
	if i < rows-1 and not grid[i+1][j].visited:
		opt.append(grid[i+1][j])

	if i > 0 and not grid[i-1][j].visited:
		opt.append(grid[i-1][j])

	if j < cols-1 and not grid[i][j+1].visited:
		opt.append(grid[i][j+1])

	if j > 0 and not grid[i][j-1].visited:
		opt.append(grid[i][j-1])

	try:
		return random.choice(opt)
		print('random')
	except:
		return None



def main():
	block1 = block.LEAVES.id
	block2 = block.DIRT.id
	x, y, z = mc.player.getPos()				# get player position
	pos = (x, y, z)
	fill(pos, rows*size, cols*size, 5)			# clear the space
	fill(pos, rows*size, cols*size, 1, block2)	# fill the base
	pos = (x, y+1, z)
	draw_grid(pos, block1)						# draw the maze on top of base


if __name__=='__main__':
	main()
