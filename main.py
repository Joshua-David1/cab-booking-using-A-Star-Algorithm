import pygame
import sys
import random
from queue import PriorityQueue
import time

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = WIDTH
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2-D A* PATH FINDING ALGO GAME")

def draw(screen,node_list):
	screen.fill((255,255,255))

	for row in node_list:
		for node in row:
			node.draw_node(screen)

	pygame.display.update()

def trigger_draw(screen,node_list):
	draw(screen,node_list)

def heuristic_function(cur_node, end_node):
	x1,y1 = cur_node
	x2,y2 = end_node

	return abs(x1-x2) + abs(y1 - y2)



class A_star_search(object):
	def __init__(self,taxi_list):
		self.taxi_list = taxi_list
		# print(taxi_list)
		self.taxi_paths = {}

	def backtrack_path(self,taxi,parent_node,draw,screen,node_list,is_taxi):
		FPS = 30
		self.taxi_paths[taxi] = parent_node
		# print(taxi)
		current_node = taxi
		tem_current_node = taxi
		parent_node = self.taxi_paths[taxi]
		while current_node in parent_node:
			fpsClock.tick(FPS)
			current_node  = parent_node[current_node]
			current_node.node_color = (128,0,128)
			draw(screen,node_list)
		current_node.node_color = (255, 128 ,0)
		if not is_taxi:
			current_node.node_color = (255,0,0)
		draw(screen,node_list)
		font = pygame.font.SysFont("Arial",32)
		if is_taxi:
			text = font.render("PRESS SPACE to BOOK THE TAXI!!!",True,(0,0,0),(255,255,255))
		else:
			text = font.render("PRESS SPACE TO REACH Destination!!",True,(0,0,0),(255,255,255))
		while True:
			
			screen.blit(text,(150,4))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:	
						FPS = 3
						current_node = tem_current_node
						while current_node in parent_node:
							fpsClock.tick(FPS)
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									sys.exit()
							current_node.node_color = (255,255,255)
							current_node = parent_node[current_node]
							current_node.node_color = (255,200,0)
							draw(screen,node_list)
						return
				pygame.display.update()

	def find_shortest_path(self,draw,screen,grid, start_node,end_node,is_taxi = True):
		FPS = 150
		end_node.taxi = False
		count = 0
		open_set = PriorityQueue()
		open_set.put((0,count,start_node))
		g_score = {node:float("inf") for row in grid for node in row }
		g_score[start_node] = 0
		f_score = {node: float("inf") for row in grid for node in row }
		f_score[start_node] = heuristic_function((start_node.row,start_node.col),(end_node.row,end_node.col))
		parent_node = {}
		open_set_hash = {start_node}
		
		while not open_set.empty():
			fpsClock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			current_node = open_set.get()[2]
			open_set_hash.remove(current_node)

			if current_node == end_node:
				if is_taxi == True:
					current_node.node_color = (64, 224, 208)
					end_node.taxi = True
				else:
					current_node.node_color = (255,128,0)
				self.taxi_paths[end_node]=parent_node
				if not is_taxi:
					self.backtrack_path(end_node,parent_node,draw,screen,grid,False)
				return True

			for neighbor in current_node.neighbours:
				if neighbor.blocked == False and neighbor.taxi == False and neighbor.end == False or (neighbor.taxi == end_node and neighbor.end == False) or (neighbor.end == True and not is_taxi):
					temp_neigh_g_score = g_score[current_node] + 1

					if temp_neigh_g_score < g_score[neighbor]:
						parent_node[neighbor] =current_node
						g_score[neighbor] = temp_neigh_g_score
						f_score[neighbor] = temp_neigh_g_score + heuristic_function((neighbor.row,neighbor.col),(end_node.row,end_node.col))
						if neighbor not in open_set_hash:
							count += 1
							open_set.put((f_score[neighbor],count,neighbor))
							open_set_hash.add(neighbor)
							if neighbor.node_color != (128,0,128):
								neighbor.node_color = (0,255,0)

			draw(screen,grid)
			if current_node != start_node and current_node != end_node and current_node.node_color != (128,0,128):
				current_node.node_color = (255,120,250)


	def find_shortest_path_taxi(self,draw,screen,grid):
		shortest_distance = 100000000000000000000000000
		for shortes_len in self.taxi_paths:
			if len(self.taxi_paths[shortes_len]) < shortest_distance:
				shortest_distance = len(self.taxi_paths[shortes_len])
				taxi = shortes_len
			# print(shortes_len)

		self.backtrack_path(taxi, self.taxi_paths[taxi],draw,screen,grid,True)

	def taxi_to_destination(self, draw,screen, grid, start_node,end_node):
		self.find_shortest_path(draw,screen,grid,start_node,end_node,False)

	def for_every_taxi(self, draw,screen, grid,start_node):
		for taxi in self.taxi_list:
			# print(taxi)
			self.find_shortest_path(draw,screen,grid,start_node,taxi)
		self.find_shortest_path_taxi(draw,screen,grid)
		return True

class Node(object):
	def __init__(self, row,col, size):
		self.row = row
		self.col = col
		self.node_size = size
		self.node_color = (255,255,255)
		self.blocked = False
		self.taxi = False
		self.occupied = False
		self.neighbours = []
		self.end = False

	def draw_node(self, screen):
		pygame.draw.rect(screen,self.node_color,((self.row * self.node_size) - self.node_size,(self.col * self.node_size) - self.node_size,self.node_size, self.node_size))


	def add_neighbours(self,grid):
		if self.row > 0 and self.row < grid.tot_rows - 1:
			self.neighbours.append(grid.node_list[self.row - 2][self.col - 1])
			self.neighbours.append(grid.node_list[self.row][self.col - 1])

		if self.col -1> 0 and self.col -1< grid.tot_rows - 1:
			self.neighbours.append(grid.node_list[self.row - 1][self.col - 2])
			self.neighbours.append(grid.node_list[self.row - 1][self.col])

		if self.row -1 == 0:
			self.neighbours.append(grid.node_list[self.row ][self.col - 1])

		if self.row -1 == grid.tot_rows - 1:
			self.neighbours.append(grid.node_list[self.row - 2][self.col - 1])

		if self.col -1 == 0:
			self.neighbours.append(grid.node_list[self.row - 1][self.col])

		if self.col -1 == grid.tot_rows - 1:
			self.neighbours.append(grid.node_list[self.row - 1][self.col - 2])



# def draw_mark_spots(screen,spots_list):
# 	screen.fill((255,255,255))
# 	pass


class Grid(object):
	def __init__(self, width,size):
		tot_rows = width // size
		self.tot_rows = tot_rows
		self.node_list = []
		self.start = None
		self.end = None
		self.end_node = None
		self.start_search = False 
		self.search_over = False
		for i in range(1,tot_rows+1):
			temp = []
			for j in range(1,tot_rows+1):
				temp.append(Node(i,j,size))
			self.node_list.append(temp.copy())


	def add_neighbours_to_nodes(self, grid):
		for row in self.node_list:
			for node in row:
				node.add_neighbours(grid)

	def draw_spot(self,screen):
		for row in self.node_list:
			for spot in row:
				spot.draw_node(screen)

	def check_mark(self,x,y):
		cur_node = self.node_list[x][y]
		if self.start is None:
			cur_node.node_color = (255, 128 ,0)
			self.start = True
			cur_node.occupied = True
		elif self.end is None:
			cur_node.node_color = (255,0,0)
			self.end = True
			self.end_node = cur_node
			cur_node.end = True
			cur_node.occupied = True
		else:
			if cur_node.taxi == False and cur_node.end == False:
				cur_node.node_color = (0,0,0)
				cur_node.blocked = True
				cur_node.occupied = True

class Taxi(object):
	def __init__(self, size,grid):
		self.taxi_list = []
		taxi_count = random.randint(1,size)
		for i in range(taxi_count):
			x_val,y_val = random.randint(2,grid.tot_rows-2), random.randint(2,grid.tot_rows-2)
			taxi = grid.node_list[x_val][y_val]
			if taxi.occupied == False:
				taxi.node_color = (255,200,0)
				taxi.occupied = True
				taxi.taxi = True
				self.taxi_list.append(taxi)



#fonts

font = pygame.font.SysFont("Arial",16)
start_node_text = font.render(" -> Player",True,(0,0,0),(255,255,255))
end_node_text = font.render(" -> Destination",True,(0,0,0),(255,255,255))
taxi_text = font.render(" -> Taxi",True,(0,0,0),(255,255,255))
visited_text = font.render(" -> visited",True,(0,0,0),(255,255,255))

FPS = 30
fpsClock = pygame.time.Clock()

size = 10
grid = Grid(WIDTH,size)
grid.start = True
grid.add_neighbours_to_nodes(grid)
start_node_pos_x,start_node_pos_y = [(grid.tot_rows//2) - 1,(grid.tot_rows//2) + 1]
grid.node_list[start_node_pos_x][start_node_pos_y].node_color = (255,128,0)
grid.node_list[start_node_pos_x][start_node_pos_y].occupied = True
start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
taxi = Taxi(size, grid)
a_star_search = A_star_search(taxi.taxi_list)

# a_star_search = A_Star_Seach(taxi.taxi_list)
# print(a_star_search.available_taxi)

def legend_rendering(screen, size):
	pygame.draw.rect(screen,(255,128,0),(570,6,size,size))
	pygame.draw.rect(screen,(255,0,0),(570,26,size,size))
	pygame.draw.rect(screen,(255,200,0),(570,46,size,size))
	pygame.draw.rect(screen,(64, 224, 208),(570,66,size,size))
	screen.blit(start_node_text,(600,4))
	screen.blit(end_node_text,(600,24))
	screen.blit(taxi_text,(600,44))
	screen.blit(visited_text,(600,64))
running = True
while running:

	fpsClock.tick(FPS)
	screen.fill((255,255,255))
	grid.draw_spot(screen)
	legend_rendering(screen,size)
	# for neigh in start_node.neighbours:
	# 	neigh.node_color = (0,0,0)
	# 	neigh.draw_node(screen)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if start_node_pos_y - 1 >= 0:
					start_node.node_color = (255,255,255)
					start_node.occupied = False
					start_node_pos_y -= 1
					start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
					start_node.node_color = (255,138,0)
					start_node.occupied = True

			if event.key == pygame.K_DOWN:
				if start_node_pos_y + 1 < grid.tot_rows:
					start_node.node_color = (255,255,255)
					start_node.occupied = False
					start_node_pos_y += 1
					start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
					start_node.node_color =(255,138,0)
					start_node.occupied = True

			if event.key == pygame.K_RIGHT:
				if start_node_pos_x + 1 < grid.tot_rows:
					start_node.node_color = (255,255,255)
					start_node.occupied = False
					start_node_pos_x += 1
					start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
					start_node.node_color = (255,138,0)
					start_node.occupied = True

			if event.key == pygame.K_LEFT:
				if start_node_pos_x - 1 >= 0:
					start_node.node_color = (255,255,255)
					start_node.occupied = False
					start_node_pos_x -= 1
					start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
					start_node.node_color = (255,138,0)
					start_node.occupied = True								

			if event.key == pygame.K_SPACE:
				# print("Started[+]")
				grid.start_search = True

			if event.key == pygame.K_RETURN:
				FPS = 30
				fpsClock = pygame.time.Clock()

				size = 10
				grid = Grid(WIDTH,size)
				grid.start = True
				grid.add_neighbours_to_nodes(grid)
				start_node_pos_x,start_node_pos_y = [(grid.tot_rows//2) - 1,(grid.tot_rows//2) + 1]
				grid.node_list[start_node_pos_x][start_node_pos_y].node_color = (255,128,0)
				grid.node_list[start_node_pos_x][start_node_pos_y].occupied = True
				start_node = grid.node_list[start_node_pos_x][start_node_pos_y]
				taxi = Taxi(size, grid)
				a_star_search = A_star_search(taxi.taxi_list)

		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			x_pos,y_pos = pos
			grid.check_mark(x_pos//size,y_pos//size)

	if grid.start_search:
		if a_star_search.for_every_taxi(trigger_draw, screen,grid.node_list,start_node):
			start_node.node_color = (255, 128 ,0)
			screen.blit(font.render("Taxi Arrived!",True,(0,0,0),(255,255,255)),(350,6))
			pygame.display.update()
			time.sleep(5)
			a_star_search.taxi_to_destination(draw,screen, grid.node_list,grid.end_node, start_node)
			start_node = grid.end_node
			start_node.node_color = (255,128,0)
			grid.start_search = False
			screen.blit(font.render("!!!!VISUALIZATION OVER!!!!",True,(0,0,0),(255,255,255)),(350,380))
			pygame.display.update()
			time.sleep(6)
	pygame.display.update()