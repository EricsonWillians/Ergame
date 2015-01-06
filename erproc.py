"""
====================================================================

ERGAME v1.0

"erproc.py", Procedural Generation.
Copyright (C) <2014>  <Ericson Willians.>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

====================================================================
Engine written by Ericson Willians, a brazilian composer and programmer.

CONTACT: ericsonwrp@gmail.com
AS A COMPOSER: http://www.youtube.com/user/poisonewein
TWITTER: https://twitter.com/poisonewein

====================================================================
"""

import pygame
from random import uniform
from erbase import *
from erfunc import *

class EwHorizontalRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["walls"] = [EwHorizontalRectWall(x, y, self["brick_width"], self["brick_height"], self["wall_length"], self["color"], self["alpha"], self["thickness"]) for x in range(self["x"], self["w"], (self["brick_width"]*self["wall_length"])) for y in range(self["y"], self["h"], (self["brick_height"]*self["wall_length"])) if uniform(0, self["max_randrange"]) < self["threshold"]]

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in self["walls"]]
		
class EwSafeHorizontalRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, safety_factor, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["safety_factor"] = safety_factor
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["walls"] = [EwHorizontalRectWall(x+(self["brick_width"]*2), y, self["brick_width"], self["brick_height"], self["wall_length"], self["color"], self["alpha"], self["thickness"]) for x in range(self["x"], self["w"], (self["brick_width"]*self["wall_length"])) for y in range(self["y"], self["h"], (self["brick_height"]*self["wall_length"])) if uniform(0, self["max_randrange"]) < self["threshold"]]

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in self["walls"]]

class EwVerticalRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["walls"] = [EwVerticalRectWall(x, y, self["brick_width"], self["brick_height"], self["wall_length"], self["color"], self["alpha"], self["thickness"]) for x in range(self["x"], self["w"], (self["brick_width"]*self["wall_length"])) for y in range(self["y"], self["h"], (self["brick_height"]*self["wall_length"])) if uniform(0, self["max_randrange"]) < self["threshold"]]

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in self["walls"]]

class EwSafeVerticalRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, safety_factor, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["safety_factor"] = safety_factor
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["walls"] = [EwVerticalRectWall(x, y+(self["brick_height"]*self["safety_factor"]), self["brick_width"], self["brick_height"], self["wall_length"], self["color"], self["alpha"], self["thickness"]) for x in range(self["x"], self["w"], (self["brick_width"]*self["wall_length"])) for y in range(self["y"], self["h"], (self["brick_height"]*self["wall_length"])) if uniform(0, self["max_randrange"]) < self["threshold"]]

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in self["walls"]]
		
class EwRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["horizontal_maze"] = EwHorizontalRectWallMaze(x, y, w, h, self["brick_width"], self["brick_height"], self["max_randrange"], self["threshold"], self["wall_length"], self["color"], self["alpha"], self["thickness"])
		self["vertical_maze"] = EwVerticalRectWallMaze(x, y, w, h, self["brick_width"], self["brick_height"], self["max_randrange"], self["threshold"], self["wall_length"], self["color"], self["alpha"], self["thickness"])

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in [self["horizontal_maze"], self["vertical_maze"]]]
		
	def detect_closed_areas(self):
		for horizontal_wall in self["horizontal_maze"]["walls"]:
			for vertical_wall in self["vertical_maze"]["walls"]:
				if col(horizontal_wall["rects"][0], vertical_wall["rects"][0]):
					EwRect(horizontal_wall["rects"][0]["x"], horizontal_wall["rects"][0]["y"], horizontal_wall["w"], vertical_wall["h"], GREEN, 255, 0).draw()
					
class EwSafeRectWallMaze(EwMaze):
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold, wall_length, safety_factor, color, alpha, thickness):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["wall_length"] = wall_length
		self["safety_factor"] = safety_factor
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["horizontal_maze"] = EwSafeHorizontalRectWallMaze(x, y, w, h, self["brick_width"], self["brick_height"], self["max_randrange"], self["threshold"], self["wall_length"], self["safety_factor"], self["color"], self["alpha"], self["thickness"])
		self["vertical_maze"] = EwSafeVerticalRectWallMaze(x, y, w, h, self["brick_width"], self["brick_height"], self["max_randrange"], self["threshold"], self["wall_length"], self["safety_factor"], self["color"], self["alpha"], self["thickness"])

	def draw(self, destination_surface=None):
		[m.draw(destination_surface) for m in [self["horizontal_maze"], self["vertical_maze"]]]
		
	def detect_closed_areas(self):
		for horizontal_wall in self["horizontal_maze"]["walls"]:
			for vertical_wall in self["vertical_maze"]["walls"]:
				if col(horizontal_wall["rects"][0], vertical_wall["rects"][0]):
					EwRect(horizontal_wall["rects"][0]["x"], horizontal_wall["rects"][0]["y"], horizontal_wall["w"], vertical_wall["h"], GREEN, 255, 0).draw()

class EwRectField(EwMaze):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, brick_width, brick_height, max_randrange, threshold):
		
		EwMaze.__init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold)
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["grid"] = EwGrid(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], 1, self["brick_width"], self["brick_height"])
		self["walls"] = [EwRect(x*self["brick_width"], y*self["brick_height"], self["brick_width"], self["brick_height"], self["color"], self["alpha"], self["thickness"]) for x in range(len(self["grid"]["rows"])) for y in range(len(self["grid"]["columns"])) if uniform(0, self["max_randrange"]) < self["threshold"]]
	
	def collide(self, target):
		return [col(target, wall) for wall in self["walls"]]
	
	def draw(self, draw_grid=False, destination_surface=None):
		if draw_grid is True:
			self["grid"].draw()
		[wall.draw(destination_surface) for wall in self["walls"]]
