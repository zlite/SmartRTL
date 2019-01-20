'''
modification of a drawing app to show SmartRTL
'''

import ui
#import photos
import console
import math
#import time
#import operator
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

#paths = [[0],[0],[0]] # x,y,distance from start
paths = []
distances = []
#bins = []
#binnums = 10
current = []
lines = []
node = []
shortest_path = []
#current.append(0)
#current.append(0)
#for i in range(binnums):  # initialize bins
#	bins.append(0)
points = 0

class Graph:
    def __init__(self):
        # dictionary containing keys that map to the corresponding vertex object
        self.vertices = {}

    def add_vertex(self, key):
        """Add a vertex with the given key to the graph."""
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        """Return vertex object with the corresponding key."""
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, src_key, dest_key, weight=1):
        """Add edge from src_key to dest_key with given weight."""
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def does_edge_exist(self, src_key, dest_key):
        """Return True if there is an edge from src_key to dest_key."""
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, key):
        self.key = key
        # dictionary containing destination vertices mapped to the weight of the
        # edge with which they are joined to this vertex
        self.points_to = {}

    def get_key(self):
        """Return key corresponding to this vertex object."""
        return self.key

    def add_neighbour(self, dest, weight):
        """Make this vertex point to dest with given edge weight."""
        self.points_to[dest] = weight

    def get_neighbours(self):
        """Return all vertices pointed to by this vertex."""
        return self.points_to.keys()

    def get_weight(self, dest):
        """Get weight of edge from this vertex to dest."""
        return self.points_to[dest]

    def does_it_point_to(self, dest):
        """Return True if this vertex points to dest."""
        return dest in self.points_to


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        return self.items.pop(0)


def find_shortest_paths(src):
    """Returns tuple of two dictionaries: (parent, distance)

    parent contains vertices mapped to their parent vertex in the shortest
    path from src to that vertex.
    distance contains vertices mapped to their shortest distance from src.
    """
    parent = {src: None}
    distance = {src: 0}

    visited = set()
    q = Queue()
    q.enqueue(src)
    visited.add(src)
    while not q.is_empty():
        current = q.dequeue()
        for dest in current.get_neighbours():
            if dest not in visited:
                visited.add(dest)
                parent[dest] = current
                distance[dest] = distance[current] + 1
                q.enqueue(dest)
    return (parent, distance)


# The PathView class is responsible for tracking
# touches and drawing the current stroke.
# It is used by SketchView.

class PathView (ui.View):

	def __init__(self, frame):
		self.frame = frame
		self.flex = 'WH'
		self.path = None
		self.action = None

	def touch_began(self, touch):
		x, y = touch.location
		self.path = ui.Path()
		self.path.line_width = 8.0
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.move_to(x, y)

	def touch_moved(self, touch):
		global points
		x, y = touch.location
#		print(x,y)
		distance = math.sqrt(x*x + y*y)
		paths.append(points)
		paths[points]=int(x),int(y),int(distance)
		points = points+1
		self.path.line_to(x, y)
		self.set_needs_display()

	def touch_ended(self, touch):
		# Send the current path to the SketchView:
		if callable(self.action):
			self.action(self)
		# Clear the view (the path has now been rendered
		# into the SketchView's image view):
		self.path = None
#		print(paths)
		self.set_needs_display()

	def draw(self):
		if self.path:
			self.path.stroke()

# The main SketchView contains a PathView for the current
# line and an ImageView for rendering completed strokes.
# It also manages the 'Clear' and 'Save' ButtonItems that
# are shown in the title bar.

class SketchView (ui.View):
	def __init__(self, width=1024, height=1024):
		self.bg_color = 'white'
		iv = ui.ImageView(frame=(0, 0, width, height))
		pv = PathView(frame=self.bounds)
		ui.View(alpha=0.5)
		pv.action = self.path_action
		self.add_subview(iv)
		self.add_subview(pv)
		save_button = ui.ButtonItem()
		save_button.title = 'RTL'
		save_button.action = self.rtl_action
		clear_button = ui.ButtonItem()
		clear_button.title = 'Clear'
		clear_button.tint_color = 'red'
		clear_button.action = self.clear_action
		self.right_button_items = [save_button, clear_button]
		self.image_view = iv

	def path_action(self, sender):
		path = sender.path
		old_img = self.image_view.image
		width, height = self.image_view.width, self.image_view.height
		with ui.ImageContext(width, height) as ctx:
			if old_img:
				old_img.draw()
			path.stroke()
			self.image_view.image = ctx.get_image()

	def clear_action(self, sender):
		self.image_view.image = None

	def rtl_action(self, sender):
		self.path = ui.Path()
		g = Graph()
		old_img = self.image_view.image
		global line_total
		line_total = 0
#		for i in range(points):
#				print(paths[i])
#		sortedx = sorted(paths,key = operator.itemgetter(0))
#		sortedy = sorted(paths,key = operator.itemgetter(1))
#		sortedd = sorted(paths,key = operator.itemgetter(2))
#		for j in range(points):
#			distances.append(paths[j][2])
#		n, m, patches = plt.hist(distances,20, normed=0, facecolor='green', alpha=0.5)
		# Tweak spacing to prevent clipping of ylabel
#		plt.subplots_adjust(left=0.15)
#		plt.show()
		# now gradient descent your way home
		# start at end point
#		current[0] = paths[points-11][0] # hop back ten points and start searching
#		current[1] = paths[points-11][1]
#		ui.set_color('black')
#		for i in range(points-1):
#			self.path.line_to(paths[i+1][0], paths[i+1][1])
#			self.set_needs_display()
		# replace points with line segments
		previous_point = 0,0
		for i in range(points):
			delta_x = paths[i][0]-previous_point[0]
			delta_y = paths[i][1]-previous_point[1]
			delta_d = math.sqrt(delta_x*delta_x + delta_y*delta_y)
			if delta_d > 30:
				line = previous_point[0], previous_point[1],paths[i][0],paths[i][1]
				lines.append(line)
				previous_point = paths[i]
				line_total += 1
				# convert each of those lines into a pair of linked vertices
				g.add_vertex(line_total)

		for i in range(line_total):
			if i > 1:
				g.add_edge(i,i-1)
			for j in range(line_total):
				if j < i - 2 or j > i + 2:
					delta_x = lines[i][0]-lines[j][0]
					delta_y = lines[i][1]-lines[j][1]
					distance = math.sqrt(delta_x*delta_x + delta_y*delta_y)
#					print ("Distance, i, j:", distance, i, j)
					if distance < 50:
#						print ("Adding edge", i, j)
						g.add_edge(i,j)
#			print("Vertex",i,g.get_vertex(i+1))
		for v in g:
			for dest in v.get_neighbours():
				w = v.get_weight(dest)
#				print("Neighbors",v.get_key(),dest.get_key(),w)

		with ui.ImageContext(1024, 1024) as ctx:
#			ui.View(background_color = None)
#			ui.View(alpha=0.1)
			self.path.line_width = 2
			ui.set_color('red')
			self.path.move_to(lines[1][0],lines[1][1])
			for i in range(line_total-1):
				self.path.line_to(lines[i+1][2],lines[i+1][3])
				self.path.stroke()
			ui.set_color('green')
			self.path.line_width = 1
			for v in g:
				for dest in v.get_neighbours():
					vert1 = v.get_key()
					vert2 = dest.get_key()
					self.path.move_to(lines[vert1][0],lines[vert1][1])
					self.path.line_to(lines[vert2][0],lines[vert2][1])
					ui.draw_string(str(vert1),rect=(lines[vert1][0],lines[vert1][1], 20, 20), font=('<system>', 12), color='green', alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
					self.path.stroke()
			ui.set_color('#4757ff')
			circle=self.path.oval(lines[line_total-1][2]-5,lines[line_total-1][3]-5,10,10)
			circle.fill()
#			self.image_view.image = ctx.get_image()
			# now find shortest path back
			src = g.get_vertex(line_total-1)
			parent, distance = find_shortest_paths(src)
#			print("shortest path")
			for v in parent:
				if v.get_key() == 1:
					while parent[v] is not None:
#						print(v.get_key(), end = ' ')
						shortest_path.append(v.get_key())
						v = parent[v]
#						print(src.get_key()) # print source vertex
#			print ("Shortest path:", shortest_path)
			for i in shortest_path:
				circle=self.path.oval(lines[i][2]-5,lines[i][3]-5,10,10)
				circle.fill()
			self.image_view.image = ctx.get_image()
# We use a square canvas, so that the same image
# can be used in portrait and landscape orientation.
w, h = ui.get_screen_size()
canvas_size = max(w, h)
sv = SketchView(canvas_size, canvas_size)
sv.name = 'Sketch'
sv.present('fullscreen')
