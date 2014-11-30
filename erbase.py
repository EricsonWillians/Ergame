"""
====================================================================

ERGAME v1.0.

"erbase.py", Base Engine File.
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

import os
import pygame
import pygame.mouse as pymo

import bisect
from random import randrange
from random import uniform
from itertools import product

from ercrash import *
from erdat import *
from erfunc import *

# POSITIONS AND DIMENSIONS
# ======================================================== #
		
class EwPos(EwData):
	
	"""
	An EwPos is an abstract data-holder to represent coordinates.
	"""
	
	def __init__(self, x, y):
		
		"""
		Input arguments:
		x <- float
		y <- float
		"""
		
		EwData.__init__(self)
		self["x"] = x
		self["y"] = y
		
	def set_pos(self, value):
		if isinstance(value, tuple):
			self["x"] = value[0]
			self["y"] = value[1]
		else:
			raise NotMemberOfError("tuple")
		
class EwMovable(EwPos):
	
	"""
	An EwMovable translates EwPos coordinates.
	"""
	
	def __init__(self, x, y):
		
		"""
		Input arguments:
		x <- float
		y <- float
		"""
		
		EwPos.__init__(self, x, y)
	
	def move(self, condition, direction=NORTH, step=1):
		if condition:
			if direction() == NORTH:
				self["y"] -= step
			if direction() == SOUTH:
				self["y"] += step
			if direction() == WEST:
				self["x"] -= step
			if direction() == EAST:
				self["x"] += step
			return True
	
	def setup_movement(self, movement_type, step_pattern):
		key = pygame.key.get_pressed
		if isinstance(step_pattern, list):
			steps = step_pattern
		else:
			raise NotMemberOfError("basestring")
		if movement_type == ARROWS:
			self.move(key()[pygame.K_UP], NORTH, steps[0])
			self.move(key()[pygame.K_DOWN], SOUTH, steps[1])
			self.move(key()[pygame.K_LEFT], WEST, steps[2])
			self.move(key()[pygame.K_RIGHT], EAST, steps[3])
		elif movement_type == WASD:
			self.move(key()[pygame.K_w], NORTH, steps[0])
			self.move(key()[pygame.K_s], SOUTH, steps[1])
			self.move(key()[pygame.K_a], WEST, steps[2])
			self.move(key()[pygame.K_d], EAST, steps[3])
		elif movement_type == BOTH:
			self.move(key()[pygame.K_UP], NORTH, steps[0])
			self.move(key()[pygame.K_DOWN], SOUTH, steps[1])
			self.move(key()[pygame.K_LEFT], WEST, steps[2])
			self.move(key()[pygame.K_RIGHT], EAST, steps[3])
			self.move(key()[pygame.K_w], NORTH, steps[0])
			self.move(key()[pygame.K_s], SOUTH, steps[1])
			self.move(key()[pygame.K_a], WEST, steps[2])
			self.move(key()[pygame.K_d], EAST, steps[3])
		
	def teleport(self, condition, new_x, new_y):
		if condition:
			self["x"] = new_x
			self["y"] = new_y
			
class EwMeasurable(EwMovable):
	
	"""
	An EwMeasurable is an abstract data-holder to represent measures.
	"""
	
	def __init__(self, x, y, w, h):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""
		
		EwMovable.__init__(self, x, y)
		self["w"] = w
		self["h"] = h
	
	def width(self):
		return self["w"]
		
	def half_width(self):
		return self["w"] / 2
		
	def height(self):
		return self["h"]
		
	def half_height(self):
		return self["h"] / 2
	
	def top(self):
		return self["y"]
	
	def bottom(self):
		return self["y"] + self["h"]
	
	def left(self):
		return self["x"]
		
	def right(self):
		return self["x"] + self["w"]

# Object Manipulation
# ======================================================== #

class EwDrawable(EwMeasurable):
	
	"""
	An EwDrawable is a wrapper for pygame surfaces.
	"""
	
	def __init__(self, x, y, w, h):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""
		
		EwMeasurable.__init__(self, x, y, w, h)
		self.generate_surface(self["w"], self["h"])
	
	def generate_surface(self, w, h):
		self["surface"] = pygame.Surface((w, h))
		self["surface"].set_colorkey(self["surface"].get_at((0,0)), pygame.RLEACCEL)
		
	def get_pygame_rect(self):
		return self["surface"].get_rect()

class EwFocusable(EwDrawable):
	
	"""
	An EwFocusable holds the functionality that allows an abstract EwMeasurable to be focused.
	Since all EwObjects inherit from EwFocusable, everything can be focused.
	"""
	
	def __init__(self, x, y, w, h):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""
		
		EwDrawable.__init__(self, x, y, w, h)
		self["has_focus"] = False
	
	def focused(self):
		return self["has_focus"]
	
	def watch_for_focus(self):
		if EwMouseCol(pygame.mouse.get_pos(), self)() and push_left_mouse():
			self["has_focus"] = True
		if not EwMouseCol(pygame.mouse.get_pos(), self)() and push_left_mouse():
			self["has_focus"] = False

class EwClickable(EwFocusable):
	
	"""
	An EwClickable holds the functionality for an abstract clickable area.
	Since all EwObjects inherit from EwClickable, everything can be a button by default.
	"""
	
	def __init__(self, x, y, w, h):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""
		
		EwFocusable.__init__(self, x, y, w, h)
		self["released"] = False
		self["hovered"] = False
		self["pressed"] = False
		
	def hover(self):
		if EwMouseCol(pygame.mouse.get_pos(), self)():
			self["hovered"] = True
		if not EwMouseCol(pygame.mouse.get_pos(), self)():
			self["hovered"] = False
	
	def click(self, mouse_button=LMB1):
		if EwMouseCol(mpos(), self)() and push_mouse(mouse_button):
			self["pressed"] = True
		if EwMouseCol(mpos(), self)() and release_mouse(mouse_button):
			self["pressed"] = False
			self["released"] = True
		else:
			self["released"] = False
	
	def toggle(self, mouse_button=LMB1):
		if self["pressed"] == False:
			self["released"] = True
		elif self["pressed"] == True:
			self["released"] = False
		if EwMouseCol(mpos(), self)() and push_mouse(mouse_button):
			if self["pressed"] == False:
				self["pressed"] = True
			elif self["pressed"] == True:
				self["pressed"] = False
	
	def click_and_hover(self, mouse_button=LMB1):
		self.hover()
		self.click(mouse_button)
		
	def toggle_and_hover(self, mouse_button=LMB1):
		self.hover()
		self.toggle(mouse_button)
			
	def get_states(self):
		return {"released": self["released"], "hovered": self["hovered"], "pressed": self["pressed"]}

class EwRotatable(EwClickable):
	
	"""
	An EwRotatable holds the functionality that allows an abstract EwMeasurable to be rotated.
	"""
	
	def __init__(self, x, y, w, h):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""
		
		EwClickable.__init__(self, x, y, w, h)
		self["rot_surfaces"] = None
		self["manager"] = 0
	
	def create_rotations(self, start_angle=0, final_angle=360, step=10):
		def rot(angle):
			orig_rect = self["surface"].get_rect()
			rot_image = pygame.transform.rotate(self["surface"], angle)
			rot_rect = orig_rect.copy()
			rot_rect.center = rot_image.get_rect().center
			rot_image = rot_image.subsurface(rot_rect).copy()
			return rot_image
		self["rot_surfaces"] = [rot(n) for n in range(start_angle, final_angle, step)]
	
	def rotate(self, direction=1):
		if self["rot_surfaces"] is not None:
			self["surface"] = self["rot_surfaces"][self["manager"]]
			if direction == 0:
				self["manager"] += 1
				if self["manager"] > len(self["rot_surfaces"])-1:
					self["manager"] = 0
			elif direction == 1:
				self["manager"] -= 1
				if self["manager"] < -(len(self["rot_surfaces"])-1):
					self["manager"] = 0
			
class EwObject(EwClickable):
	
	"""
	Although small, EwObject is the most important class in the whole engine.
	An EwObject is, by default, movable, measurable, drawable, focusable and clickable.
	"""
	
	def __init__(self, x, y, w, h):

		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		"""

		EwClickable.__init__(self, x, y, w, h)
		
	def get_app(self):
		if EwData.app is not None:
			return EwData.app

class EwImage(EwObject):
	
	"""
	An EwImage is an EwObject with an image drawn into a pygame surface.
	"""
	
	def __init__(self, x, y, w, h, filename, alpha=SOLID):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		filename <- string
		alpha <- float from 0 to 255
		"""
		
		EwObject.__init__(self, x, y, w, h)
		
		self["filename"] = filename
		self["alpha"] = alpha
		
		if ".png" in self["filename"]:
			self["surface"] = pygame.image.load(os.path.join(GRAPHICS_PATH, filename)).convert_alpha()
		else:
			self["surface"] = pygame.image.load(os.path.join(GRAPHICS_PATH, filename)).convert_alpha()
		
		self["surface"].fill((255, 255, 255, self["alpha"]), None, pygame.BLEND_RGBA_MULT)
		self.transform()
			
	def transform(self):
		self["surface"] = pygame.transform.scale(self["surface"], (self["w"], self["h"]))
		
	def transform_freely(self, w, h):
		self["surface"] = pygame.transform.scale(self["surface"], (w, h))
		
	def fade_in(self, speed, limit=255):
		if (self["alpha"] < limit) and (self["alpha"] < 255):
			self["alpha"] += speed
			self["surface"].fill((255, 255, 255, self["alpha"]), None, pygame.BLEND_RGBA_MULT)
		
	def fade_out(self, speed, limit=0):
		if (self["alpha"] > limit) and (self["alpha"] > 0):
			self["alpha"] -= speed
			self["surface"].fill((255, 255, 255, self["alpha"]), None, pygame.BLEND_RGBA_MULT)
			
	def is_faded_in(self, value=255):
		if self["alpha"] >= value:
			return True
		else:
			return False 
			
	def is_faded_out(self, value=0):
		if self["alpha"] <= value:
			return True
		else:
			return False 
			
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]))
		self.watch_for_focus()
		
class EwScrollingImage(EwImage):
	
	"""
	An EwScrollingImage is an EwImage that scrolls in a given direction under a given speed.
	"""
	
	def __init__(self, x, y, w, h, filename, alpha=255, scroll_direction=NORTH, scroll_speed=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		filename <- string
		alpha <- float from 0 to 255
		scroll_direction <- int
		scroll_speed <- float
		"""
		
		EwImage.__init__(self, x, y, w, h, filename, alpha)
		
		self["scroll_direction"] = scroll_direction
		self["scroll_speed"] = scroll_speed
		self["default_scroll_speed"] = self["scroll_speed"]
		self["initial_y"] = self["y"]
		self["y0_reset_point"] = self["initial_y"] - self["h"]
		self["y1_reset_point"] = self["initial_y"] + self["h"]
		self["initial_x"] = self["x"]
		self["x2_reset_point"] = self["initial_x"] - self["w"]
		self["x3_reset_point"] = self["initial_x"] + self["w"]
		
	def draw(self, destination_surface=None):
		def blit(_dir):
			if destination_surface is None:
				if _dir == 0:
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]+self["h"]))
				elif _dir == 1:
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]-self["h"]))
				elif _dir == 2:
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
					EwData.app["screen"].blit(self["surface"], (self["x"]+self["w"], self["y"]))
				elif _dir == 3:
					EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
					EwData.app["screen"].blit(self["surface"], (self["x"]-self["w"], self["y"]))
			else:
				if _dir == 0:
					destination_surface.blit(self["surface"], (self["x"], self["y"]))
					destination_surface.blit(self["surface"], (self["x"], self["y"]+self["h"]))
				elif _dir == 1:
					destination_surface.blit(self["surface"], (self["x"], self["y"]))
					destination_surface.blit(self["surface"], (self["x"], self["y"]-self["h"]))
				elif _dir == 2:
					destination_surface.blit(self["surface"], (self["x"], self["y"]))
					destination_surface.blit(self["surface"], (self["x"]+self["w"], self["y"]))
				elif _dir == 3:
					destination_surface.blit(self["surface"], (self["x"], self["y"]))
					destination_surface.blit(self["surface"], (self["x"]-self["w"], self["y"]))	
		if self["scroll_direction"] == NORTH:
			self["y"] -= self["scroll_speed"]
			if self["y"] < self["y0_reset_point"]:
				self["y"] = self["initial_y"]
			blit(0)
		elif self["scroll_direction"] == SOUTH:
			self["y"] += self["scroll_speed"]
			if self["y"] > self["y1_reset_point"]:
				self["y"] = self["initial_y"]
			blit(1)
		elif self["scroll_direction"] == WEST:
			self["x"] -= self["scroll_speed"]
			if self["x"] < self["x2_reset_point"]:
				self["x"] = self["initial_x"]
			blit(2)
		elif self["scroll_direction"] == EAST:
			self["x"] += self["scroll_speed"]
			if self["x"] > self["x3_reset_point"]:
				self["x"] = self["initial_x"]
			blit(3)
		self.watch_for_focus()

	def change_direction(self, _dir):
		self["x"] = 0
		self["y"] = 0
		self["initial_y"] = 0
		self["y0_reset_point"] = self["initial_y"] - self["h"]
		self["y1_reset_point"] = self["initial_y"] + self["h"]
		self["initial_x"] = 0
		self["x2_reset_point"] = self["initial_x"] - self["w"]
		self["x3_reset_point"] = self["initial_x"] + self["w"]
		self["scroll_direction"] = _dir

	def reset_scroll_speed(self):
		self["scroll_speed"] = self["default_scroll_speed"]
		
class EwFont(EwObject):
	
	"""
	An EwFont is an EwObject with text.
	"""
	
	def __init__(self, x, y, size, filename, text, color, alpha=255, bold=False):
		
		"""
		Input arguments:
		x <- float
		y <- float
		size <- int
		filename <- string
		text <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		bold <- boolean
		"""
		
		EwObject.__init__(self, x, y, 1, 1)
		
		self["size"] = size
		self["filename"] = filename
		if isinstance(text, basestring):
			pass
		else:
			text = str(text)
		self["text"] = text
		self["color"] = color
		self["alpha"] = alpha
		self["bold"] = bold
		if self["filename"] is not None:
			self["font"] = pygame.font.Font(os.path.join(GRAPHICS_PATH, filename), self["size"])
		else:
			self["font"] = pygame.font.Font(None, self["size"])
		if bold:
			self["font"].set_bold(True)
		self["surface"] = self["font"].render(self["text"], True, self["color"])
		pygame.Surface.convert_alpha(self["surface"])
		self["surface"].fill((255, 255, 255, self["alpha"]), None, pygame.BLEND_RGBA_MULT)
		self["w"] = self["surface"].get_width()
		self["h"] = self["surface"].get_height()
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]))
		self.watch_for_focus()

	def update(self, value):
		if isinstance(value, basestring):
			pass
		else:
			value = str(value)
		self["text"] = value
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
		
	def update_color(self, color):
		self["color"] = color
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
	
	def __call__(self, value):
		if isinstance(value, basestring):
			pass
		else:
			value = str(value)
		self["text"] = value
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
			
class EwTransformedFont(EwObject):
	
	"""
	An EwTransformedFont is an EwObject with resized text (With dimensions defined like a rectangle).
	"""
	
	def __init__(self, x, y, w, h, filename, text, color, alpha=255, bold=False, quality=16):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		filename <- string
		text <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		bold <- boolean
		quality <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		
		self["filename"] = filename
		if isinstance(text, basestring):
			pass
		else:
			text = str(text)
		self["text"] = text
		self["color"] = color
		self["alpha"] = alpha
		self["bold"] = bold
		self["quality"] = quality
		if self["filename"] is not None:
			self["font"] = pygame.font.Font(os.path.join(GRAPHICS_PATH, filename), self["quality"])
		else:
			self["font"] = pygame.font.Font(None, 128)
		if bold:
			self["font"].set_bold(True)
		self["surface"] = self["font"].render(self["text"], True, self["color"])
		pygame.Surface.convert_alpha(self["surface"])
		self["surface"].fill((255, 255, 255, self["alpha"]), None, pygame.BLEND_RGBA_MULT)
		self.transform()
		
	def transform(self):
		self["surface"] = pygame.transform.scale(self["surface"], (self["w"], self["h"]))
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]))
		self.watch_for_focus()

	def update(self, value):
		if isinstance(value, basestring):
			pass
		else:
			value = str(value)
		self["text"] = value
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
		self.transform()
		
	def update_color(self, color):
		self["color"] = color
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
		self.transform()
	
	def __call__(self, value):
		if isinstance(value, basestring):
			pass
		else:
			value = str(value)
		self["text"] = value
		self["surface"] = self["font"].render(self["text"], 1, self["color"])
		self.transform()

# Static Functions:

# ================================ <

def text(x, y, w, h, filename, text, color, alpha=255, bold=False):
	EwTransformedFont(x, y, w, h, filename, text, color, alpha, bold).draw()

def draw_mouse_coordinates(destination_surface=None, w=None, h=None, color=(255,0,0)):
	if w is None or h is None:
		w = 64
		h = 16
	pos = EwTransformedFont(pymo.get_pos()[0]+16, pymo.get_pos()[1], w, h, None, str((pymo.get_pos()[0], pymo.get_pos()[1])), color)
	pos.draw(destination_surface)

# ================================ <

class EwShape(EwObject):
	
	"""
	EwShape is the base EwObject class for all pygame shapes.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, thickness):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		pygame.Surface.convert_alpha(self["surface"])
		self["surface"].set_alpha(self["alpha"])
		
	def __call__(self):
		return (self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], self["thickness"])

	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]), (0, 0, self["w"], self["h"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]), (0, 0, self["w"], self["h"]))
		self.watch_for_focus()
		
class EwRect(EwShape):
	
	"""
	An EwRect is an EwShape, with a pygame rectangle drawn into a pygame surface.
	"""
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		self.draw_rect(0, 0, self["w"], self["h"])
	
	def draw_rect(self, x, y, w, h):
		pygame.draw.rect(self["surface"], self["color"], (x, y, w, h), self["thickness"])

	def resize(self, w, h):
		self["w"] = w
		self["h"] = h
		self.generate_surface(self["w"], self["h"])
		self.draw_rect(0, 0, self["w"], self["h"])

	def update_color(self, color):
		self["color"] = color
		self.draw_rect(0, 0, self["w"], self["h"])

def border(rect, color, alpha, thickness):
	return EwRect(rect["x"]-thickness, rect["y"]-thickness, rect["w"]+thickness*2, rect["h"]+thickness*2, color, alpha, thickness)

class EwRotatableRect(EwShape, EwRotatable):
	
	"""
	An EwRotatableRect is an EwShape with a pygame rectangle drawn into a pygame surface, that is able to rotate.
	"""
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		EwRotatable.__init__(self, x, y, w, h)
		self.draw_rect((self["w"]/2)-(self["w"]/1.4)/2, (self["h"]/2)-(self["h"]/1.4)/2, self["w"]/1.4, self["h"]/1.4)

	def draw_rect(self, x, y, w, h):
		pygame.draw.rect(self["surface"], self["color"], (x, y, w, h), self["thickness"])

class EwTrigger(EwRect):
	
	"""
	An EwTrigger is an EwRect whose area serves as a trigger.
	"""
	
	def __init__(self, x, y, w, h, color=(175,0,75), alpha=75, thickness=0, trigger_mode=ENDLESS):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		trigger_mode <- int
		"""
		
		EwRect.__init__(self, x, y, w, h, color, alpha, thickness)
		self["trigger_mode"] = trigger_mode
		self["activated"] = True
		self["activation_counter"] = 0
		
	def trigger(self, target, f, *args):
		if EwCol(self, target)():
			self["activation_counter"] += 1
			if self["activation_counter"]  <= self["trigger_mode"]:
				self["activated"] = True
			else:
				self["activated"] = False
			if self["activated"] == True or self["trigger_mode"] == ENDLESS:
				apply(f, args)
				
	def detect(self, target):
		if EwCol(self, target)():
			self["activation_counter"] += 1
			if self["activation_counter"]  <= self["trigger_mode"]:
				self["activated"] = True
			else:
				self["activated"] = False
			if self["activated"] == True or self["trigger_mode"] == ENDLESS:
				return True
			
class EwPolygon(EwShape):
	
	def __init__(self, pointlist, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		pointlist <- sequence of tuple-coordinates
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, None, None, None, None, color, alpha, thickness)
		self["pointlist"] = pointlist
		pygame.draw.polygon(self["surface"], self["color"], self["pointlist"], self["thickness"])
		
	def update_color(self, color):
		self["color"] = color
		pygame.draw.polygon(self["surface"], self["color"], self["pointlist"], self["thickness"])
		
class EwCircle(EwShape):
	
	"""
	An EwCircle is an EwShape with a pygame circle drawn into a pygame surface.
	"""
	
	def __init__(self, x, y, radius, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		radius <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, x, y, radius*2, radius*2, color, alpha, thickness)
		self["radius"] = radius
		pygame.draw.circle(self["surface"], self["color"], (0, 0, self["radius"], self["thickness"]))
	
	def update_color(self, color):
		self["color"] = color
		pygame.draw.circle(self["surface"], self["color"], (0, 0, self["radius"], self["thickness"]))
	
class EwEllipse(EwShape):
	
	"""
	An EwEllipse is an EwShape with a pygame ellipse drawn into a pygame surface.
	"""
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		self.draw_ellipse(0, 0, self["w"], self["h"])

	def draw_ellipse(self, x, y, w, h):
		pygame.draw.ellipse(self["surface"], self["color"], (x, y, w, h), self["thickness"])

	def resize(self, w, h):
		self["w"] = w
		self["h"] = h
		self.generate_surface(self["w"], self["h"])
		self.draw_ellipse(0, 0, self["w"], self["h"])

	def update_color(self, color):
		self["color"] = color
		self.draw_ellipse(0, 0, self["w"], self["h"])

class EwArc(EwShape):
	
	"""
	An EwArc is an EwShape with a pygame arc drawn into a pygame surface.
	"""
	
	def __init__(self, x, y, w, h, start_angle, stop_angle, color=(255,255,255), alpha=255, thickness=1):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		start_angle <- float
		stop_angle <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		self["start_angle"] = start_angle
		self["stop_angle"] = stop_angle
		pygame.draw.arc(self["surface"], self["color"], (0, 0, self["w"], self["h"]), self["start_angle"], self["stop_angle"], self["thickness"])
		
	def update_color(self, color):
		self["color"] = color
		pygame.draw.arc(self["surface"], self["color"], (0, 0, self["w"], self["h"]), self["start_angle"], self["stop_angle"], self["thickness"])

class EwLine(EwShape):
	
	"""
	An EwLine is an EwShape with a pygame line drawn into a pygame surface.
	"""
	
	def __init__(self, start_pos, end_pos, color=(255,255,255), alpha=255, thickness=1):
	
		"""
		Input arguments:
		start_pos <- float
		end_pos <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
	
		EwShape.__init__(self, 0, 0, EwData.app["SCREEN_WIDTH"], EwData.app["SCREEN_HEIGHT"], color, alpha, thickness)
		self["start_pos"] = start_pos
		self["end_pos"] = end_pos
		pygame.draw.line(self["surface"], self["color"], self["start_pos"], self["end_pos"], self["thickness"])
		
	def update_color(self, color):
		self["color"] = color
		pygame.draw.line(self["surface"], self["color"], self["start_pos"], self["end_pos"], self["thickness"])
	
class EwLines(EwData):
	
	"""
	An "EwLines" instance holds a sequence of "EwLine" EwShapes.
	"""
	
	def __init__(self, lines):

		"""
		Input arguments:
		lines <- sequence of "EwLine" EwShapes.
		"""

		EwData.__init__(self)
		self["lines"] = lines
	
	def draw(self, destination_surface=None):
		
		if len(self["lines"]) > 0:
			for line in self["lines"]:
				if isinstance(line, EwLine):
					line.draw(destination_surface)
				else:
					raise NotMemberOfError("EwLine")
		
class EwGrid(EwObject):
	
	"""
	An EwGrid is an EwObject that creates a grid out of EwLines.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, thickness, cell_width, cell_height):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		cell_width <- int
		cell_height <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["cell_width"] = cell_width
		self["cell_height"] = cell_height
		self["rows"] = range(self["x"], self["w"], self["cell_width"])
		self["columns"] = range(self["y"], self["h"], self["cell_height"])
		[pygame.draw.line(self["surface"], self["color"], (z, self["y"]), (z, self["h"]), self["thickness"]) for z in self["rows"]]
		[pygame.draw.line(self["surface"], self["color"], (self["x"], z), (self["w"], z), self["thickness"]) for z in self["columns"]]
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]), (0, 0, self["w"], self["h"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]), (0, 0, self["w"], self["h"]))
		
	def _reset(self):
		self.__init__(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], self["thickness"], self["cell_width"], self["cell_height"])
		
	def get_cells(self):
		return [(x, y) for x in self["rows"] for y in self["columns"]]
		
	def get_pos(self, target_pos):
		return (self["rows"][target_pos[0]], self["columns"][target_pos[1]])
		
	def get_row_pos(self, target_pos):
		return self["rows"][target_pos]
		
	def get_column_pos(self, target_pos):
		return self["columns"][target_pos]
		
	def snap_to_grid(self, target):
		target["x"] = self["rows"][bisect.bisect_left(self["rows"], target["x"])-1]
		target["y"] = self["columns"][bisect.bisect_left(self["columns"], target["y"])-1]
		
	def navigate(self, target, condition, direction=NORTH, step=1):
		if condition:
			if direction == NORTH:
				bi = bisect.bisect_left(self["columns"], target["y"])-step
				if bi > -1:
					target["y"] -= step
					target["y"] = self["columns"][bi]
			if direction == SOUTH:
				bi = bisect.bisect_left(self["columns"], target["y"])+step
				if bi < len(self["columns"]):
					target["y"] += step
					target["y"] = self["columns"][bi]
			if direction == WEST:
				bi = bisect.bisect_left(self["rows"], target["x"])-step
				if bi > -1:
					target["x"] -= step
					target["x"] = self["rows"][bi]
			if direction == EAST:
				bi = bisect.bisect_left(self["rows"], target["x"])+step
				if bi < len(self["rows"]):
					target["x"] += step
					target["x"] = self["rows"][bi]
					
	def setup_navigation(self, target, movement_type, step_pattern):
		if isinstance(step_pattern, tuple) or isinstance(step_pattern, list):
			if len(step_pattern) == 4:
				for n in step_pattern:
					if isinstance(n, int):
						pass
					else:
						raise NotMemberOfError("int")
			if len(step_pattern) == 1:
				step_pattern = [step_pattern[0] for n in range(4)]
				if movement_type == ARROWS:
					self.navigate(target, press_up(), NORTH, step_pattern[0])
					self.navigate(target, press_down(), SOUTH, step_pattern[1])
					self.navigate(target, press_left(), WEST, step_pattern[2])
					self.navigate(target, press_right(), EAST, step_pattern[3])
				elif movement_type == WASD:
					self.navigate(target, press_key(pygame.K_w), NORTH, step_pattern[0])
					self.navigate(target, press_key(pygame.K_s), SOUTH, step_pattern[1])
					self.navigate(target, press_key(pygame.K_a), WEST, step_pattern[2])
					self.navigate(target, press_key(pygame.K_d), EAST, step_pattern[3])
				elif movement_type == BOTH:
					self.navigate(target, press_up(), NORTH, step_pattern[0])
					self.navigate(target, press_down(), SOUTH, step_pattern[1])
					self.navigate(target, press_left(), WEST, step_pattern[2])
					self.navigate(target, press_right(), EAST, step_pattern[3])
					self.navigate(target, press_key(pygame.K_w), NORTH, step_pattern[0])
					self.navigate(target, press_key(pygame.K_s), SOUTH, step_pattern[1])
					self.navigate(target, press_key(pygame.K_a), WEST, step_pattern[2])
					self.navigate(target, press_key(pygame.K_d), EAST, step_pattern[3])
			else:
				raise UnknownPatternError("[int, int, int, int]")

	def update_color(self, color):
		self["color"] = color
		[pygame.draw.line(self["surface"], self["color"], (z, self["y"]), (z, self["h"]), self["thickness"]) for z in self["rows"]]
		[pygame.draw.line(self["surface"], self["color"], (self["x"], z), (self["w"], z), self["thickness"]) for z in self["columns"]]

# AUDIO
# ======================================================== #
# This section can prove to be a bit unnecessary for the most experient pygame developers.
# Nevertheless, I have to keep my standards and deal with sound under the conventions of the engine.

class EwSound(EwData):
	
	"""
	An EwSound holds a pygame sound object.
	"""
	
	def __init__(self, name, volume=1, path=SOUNDS_PATH):
		
		"""
		Input arguments:
		name <- string
		volume <- float from 0 to 1
		path <- string
		"""
		
		EwData.__init__(self)
		self["full_path"] = os.path.join(path, name)
		if not check_file(self["full_path"]):
			raise ErgameError("It wasn't possible to load the file: " + self["full_path"])
		else:
			self["sound"] = pygame.mixer.Sound(self["full_path"])
		self.set_volume(volume)
	
	def set_volume(self, value):
		self["sound"].set_volume(value)
	
	def play(self):
		self["sound"].play()
		
	def get_pygame_sound(self):
		return self["sound"]
		
class EwMusic(EwData):
	
	"""
	Essentially a "name-wrapper', since this whole pygame "object" is too.. static.
	I could use a function, but then, you could use pygame.mixer.music directly and whatever (So, don't tell me this class is useless, because I know it's all about convention).
	"""
	
	def __init__(self, name, volume=1, path=MUSIC_PATH):
		
		"""
		Input arguments:
		name <- string
		volume <- float from 0 to 1
		path <- string
		"""
		
		EwData.__init__(self) # I wonder why the hell someone would instantiate this class to use this anyway (?).
		self["full_path"] = os.path.join(path, name) # It keeps that path to itself: WOW! How AWESOME!! (lie).
		if not check_file(self["full_path"]):
			raise ErgameError("It wasn't possible to load the file: " + self["full_path"])
		else:
			pygame.mixer.music.load(self["full_path"])
		EwMusic.set_volume(volume)
	
	@staticmethod
	def set_volume(value):
		pygame.mixer.music.set_volume(value)
	
	@staticmethod
	def play(times=-1):
		pygame.mixer.music.play(times)

# Arcade:

class EwHealthBar(EwObject):
	
	"""
	An EwHealthBar is an EwObject that serves as a health bar.
	"""
	
	def __init__(self, x, y, w, h, alpha, value, number_color=WHITE):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		alpha <- float from 0 to 255
		value <- float
		number_color <- tuple <- (3 floats from 0 to 255)
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["alpha"] = alpha
		self["value"] = value
		self["number_color"] = number_color
		self["green"] = 255
		self["red"] = 0
		self["number"] = EwTransformedFont(x+(w/2)-(w/5)/2, y, w/5, h, None, str(self["value"]), self["number_color"])
		self["rect"] = EwRect(x, y, w, h, (self["red"], self["green"], 0), self["alpha"], 0)
			
	def subtract_health(self, damage):
		
		self["value"] -= damage
		if self["value"] > 0: # Avoiding zero-division error.
			if self["green"] > 0:
				self["green"] -= 255/self["value"]
			if self["red"] < 255:
				self["red"] += 255/self["value"]
			if self["green"] >= 0 and self["red"] <= 255:
				self["color"] = (self["red"], self["green"], 0)
			
	def draw(self, destination_surface=None):
		if self["red"] < 255 and self["green"] > 0:
			self["rect"].__init__(self["rect"]["x"], self["rect"]["y"], self["rect"]["w"], self["rect"]["h"], (self["red"], self["green"], 0), self["alpha"], 0)
		self["rect"].draw(destination_surface)
		
# Rogue-like:

class EwMaze(EwObject):
	
	"""
	An EwMaze is the EwObject base for mazes.
	"""
	
	def __init__(self, x, y, w, h, brick_width, brick_height, max_randrange, threshold):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		brick_width <- int
		brick_height<- int
		max_randrange <- int
		threshold <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["brick_width"] = brick_width
		self["brick_height"] = brick_height
		self["max_randrange"] = max_randrange
		self["threshold"] = threshold

class EwHorizontalRectWall(EwObject):
	
	"""
	An EwHorizontalRectWall is an EwObject that holds a horizontal sequence of EwRects.
	"""
	
	def __init__(self, x, y, brick_width, brick_height, wall_length, color, alpha, thickness):
		
		"""
		Input arguments:
		x <- float
		y <- float
		brick_width <- int
		brick_height<- int
		wall_length <- int
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwObject.__init__(self, x, y, brick_width*wall_length, brick_height)
		self["brick_width"] = brick_width
		self["brick_height"] = brick_height
		self["wall_length"] = wall_length
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["rects"] = [EwRect(self["x"]+(x*self["brick_width"]), self["y"], self["brick_width"], self["brick_height"], self["color"], self["alpha"], self["thickness"]) for x in range(self["wall_length"])]
		
	def draw(self, destination_surface=None):
		[r.draw(destination_surface) for r in self["rects"]]
		
class EwVerticalRectWall(EwObject):
	
	"""
	An EwVerticalRectWall is an EwObject that holds a vertical sequence of EwRects.
	"""
	
	def __init__(self, x, y, brick_width, brick_height, wall_length, color, alpha, thickness):
		
		"""
		Input arguments:
		x <- float
		y <- float
		brick_width <- int
		brick_height<- int
		wall_length <- int
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		EwObject.__init__(self, x, y, brick_width, brick_height*wall_length)
		self["brick_width"] = brick_width
		self["brick_height"] = brick_height
		self["wall_length"] = wall_length
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["rects"] = [EwRect(self["x"], self["y"]+(y*self["brick_height"]), self["brick_width"], self["brick_height"], self["color"], self["alpha"], self["thickness"]) for y in range(self["wall_length"])]
		
	def draw(self, destination_surface=None):
		[r.draw(destination_surface) for r in self["rects"]]
