"""
====================================================================

ERGAME
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
import pygame.mouse as pymo
import json
import os
import bisect
from itertools import product

# EXCEPTIONS
# ======================================================== #

class ErgameError(Exception):
	
	def __init__(self, message):
		
		Exception.__init__(self, message)

class InvalidDirectionError(ErgameError):
	
	def __init__(self):
		
		ErgameError.__init__(self, "Only 0, 1, 2 and 3 are valid values as direction numbers.")

class NotMemberOfError(ErgameError):
	
	def __init__(self, _class):
		
		ErgameError.__init__(self, "The given object is not a member of the <{}> class(es).".format(_class))
		
class FileNotFoundError(ErgameError):
	
	def __init__(self, _file):
		
		ErgameError.__init__(self, "The file {} could not be found.".format(_file))
		
class MoreColorsThanButtonsError(ErgameError):
	
	def __init__(self, difference):
		
		ErgameError.__init__(self, "You've given more colors than there are available buttons. {}, precisely. What's on your mind?".format(difference))

class MoreKeysThanButtonsError(ErgameError):
	
	def __init__(self, difference):
		
		ErgameError.__init__(self, "You've given more keys than there are available buttons. {}, precisely. What's on your mind?".format(difference))

# CFG
# ======================================================== #

GRAPHICS_PATH = "EWG"
SOUNDS_PATH = "EWS"
MUSIC_PATH = "EWM"

# CONSTANTS
# ======================================================== #

ARROWS = 0
WASD = 1
BOTH = 2
ACCEPTABLE_KEYS = [pygame.K_PERIOD, pygame.K_COMMA, pygame.K_SLASH, pygame.K_BACKSLASH, pygame.K_LEFTBRACKET, 
				   pygame.K_RIGHTBRACKET, pygame.K_MINUS, pygame.K_EQUALS, pygame.K_SEMICOLON,
				   pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
				   pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
				   pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
				   pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]

# DATA MANIPULATION
# ======================================================== #

def loadSound(path, name):

	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	fullname = os.path.join(path, name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print "Cannot load sound:", name
		raise SystemExit, message
	return sound
	
class EwSerializable:
	
	def __init__(self):
		
		self.file = None
		
	def serialize(self, path, mode):	
		try:
			self.file = open(path, mode)
		except:
			raise FileNotFoundError()
		if self.file is not None:
			return self.file
			self.file.close()

class EwData(EwSerializable):
	
	app = None
	
	def __init__(self):
		
		EwSerializable.__init__(self)
		self.data = {}
		
	def __setitem__(self, key, value):
		self.data[key] = value
		
	def __getitem__(self, key):
		return self.data[key]
		
	def get_data(self):
		return self.data
		
	def write(self, path):
		self.serialize(path, "w").write(json.dumps(self.get_data()))
		
	def load(self, path):
		json_data = open(path, "r")
		self.data = json.load(json_data)
		json_data.close()
		return self.data

# EXECUTION
# ======================================================== #

pygame.mixer.pre_init(44100, -16, 2, 2048*2) 
pygame.init()
pygame.font.init()

class EwRunnable:

	def __init__(self, initial_state, FPS):
		
		self.state = initial_state
		self.FPS = FPS
		self.time_elapsed = 0
		self.clock = pygame.time.Clock()
		self.events = []
		
	def __call__(self):
		self.state = True
		
	def run(self, f, *args):
		while self.state is not True:
			dt = self.clock.tick(self.FPS)
			self.time_elapsed += dt
			self.events = pygame.event.get();
			apply(f, args)
			pygame.display.flip()
			
	def watch_for_exit(self):
		for e in self.events:
			if e.type == pygame.QUIT:
				self()
		
class EwApp(EwRunnable, EwData):

	def __init__(self, title, w, h, FPS, fullscreen=False, state=False):

		EwRunnable.__init__(self, state, FPS)
		EwData.__init__(self)
		
		if os.path.isfile("conf.edt"):
			self["TITLE"] = self.load("conf.edt")["TITLE"]
			self["SCREEN_WIDTH"] = self.load("conf.edt")["SCREEN_WIDTH"]
			self["SCREEN_HEIGHT"] = self.load("conf.edt")["SCREEN_WIDTH"]
			self["FPS"] = self.load("conf.edt")["FPS"]
			self["FULLSCREEN"] = self.load("conf.edt")["FULLSCREEN"]
			print "Configuration dictionary loaded:\n===============================\n"
			for item in self.data.items():
				print "{}: {}".format(str(item[0]), str(item[1]))
		else:
			self["TITLE"] = title
			self["SCREEN_WIDTH"] = w
			self["SCREEN_HEIGHT"] = h
			self["FPS"] = FPS
			self["FULLSCREEN"] = fullscreen
			self.write("conf.edt")
			print "Configuration dictionary saved."
		
		if self["FULLSCREEN"] == True:
			self.screen = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]), pygame.DOUBLEBUF | pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]))
		pygame.display.set_caption(self["TITLE"])
		EwData.app = self
		

	def check_if_time_has_elapsed_in_milliseconds(self, milliseconds):
		if self.time_elapsed > milliseconds:
			self.time_elapsed = 0
			return True
		else:
			return False
			
	def check_if_time_has_elapsed_in_seconds(self, seconds):
		if self.time_elapsed > seconds*1000:
			self.time_elapsed = 0
			return True
		else:
			return False
			
	def check_if_time_has_elapsed_in_minutes(self, minutes):
		if self.time_elapsed > minutes*60000:
			self.time_elapsed = 0
			return True
		else:
			return False
			
	def get_center_x(self, width):
		return (self["SCREEN_WIDTH"]/2)-(width/2)
		
	def get_center_y(self, height):
		return (self["SCREEN_HEIGHT"]/2)-(height/2)

# POSITIONS AND DIMENSIONS
# ======================================================== #
		
class EwPos:
	
	def __init__(self, x, y):
		
		self.x = x
		self.y = y
		
	def __getitem__(self, key):
		
		if key == "x":
			return self.x
		elif key == "y":
			return self.y
		elif key == "(xy)":
			return (self.x, self.y)
		elif key == "[xy]":
			return [self.x, self.y]
		
	def __setitem__(self, key, value):
		
		if key == "x":
			self.x = value
		elif key == "y":
			self.y = value
		
	def __call__(self):
		return (self.x, self.y)
		
	def get_x(self):
		return self.x
		
	def set_x(self, value):
		self.x = value
		
	def get_y(self):
		return self.y

	def set_y(self, value):
		self.y = value

class EwDirection:
	
	DIRECTIONS = ["NORTH", "SOUTH", "WEST", "EAST"]
	
	def __init__(self, value=0):
		
		self.value = value
		
		if isinstance(self.value, basestring):
			if self.value.upper() in ["UP", "DOWN", "LEFT", "RIGHT"]:
				if self.value.upper() == "UP":
					self.value = "NORTH"
				elif self.value.upper() == "DOWN":
					self.value = "SOUTH"
				elif self.value.upper() == "LEFT":
					self.value = "WEST"
				elif self.value.upper() == "RIGHT":
					self.value = "EAST"
		else:
			if self.value in range(0, 3):
				if self.value == 0:
					self.value = "NORTH"
				elif self.value == 1:
					self.value = "SOUTH"
				elif self.value == 2:
					self.value = "WEST"
				elif self.value == 3:
					self.value = "EAST"
				
	def __call__(self):
		return self.value
		
	def get(self):
		return self.value

class EwMovable(EwPos):
	
	def __init__(self, x, y):
		
		EwPos.__init__(self, x, y)
	
	def move(self, condition, direction=0, step=1):
		if isinstance(direction, EwDirection):
			self.direction = direction
		else:
			direction = EwDirection(direction)
		if condition:
			if direction() == 0 or direction() == "NORTH":
				self.y -= step
			if direction() == 1 or direction() == "SOUTH":
				self.y += step
			if direction() == 2 or direction() == "WEST":
				self.x -= step
			if direction() == 3 or direction() == "EAST":
				self.x += step
	
	def setup_movement(self, movement_type, step_pattern):
		key = pygame.key.get_pressed
		if isinstance(step_pattern, list):
			steps = step_pattern
		else:
			raise NotMemberOfError("basestring")
		if movement_type == ARROWS:
			self.move(key()[pygame.K_UP], EwDirection("NORTH"), steps[0])
			self.move(key()[pygame.K_DOWN], EwDirection("SOUTH"), steps[1])
			self.move(key()[pygame.K_LEFT], EwDirection("WEST"), steps[2])
			self.move(key()[pygame.K_RIGHT], EwDirection("EAST"), steps[3])
		elif movement_type == WASD:
			self.move(key()[pygame.K_w], EwDirection("NORTH"), steps[0])
			self.move(key()[pygame.K_s], EwDirection("SOUTH"), steps[1])
			self.move(key()[pygame.K_a], EwDirection("WEST"), steps[2])
			self.move(key()[pygame.K_d], EwDirection("EAST"), steps[3])
		elif movement_type == BOTH:
			self.move(key()[pygame.K_UP], EwDirection("NORTH"), steps[0])
			self.move(key()[pygame.K_DOWN], EwDirection("SOUTH"), steps[1])
			self.move(key()[pygame.K_LEFT], EwDirection("WEST"), steps[2])
			self.move(key()[pygame.K_RIGHT], EwDirection("EAST"), steps[3])
			self.move(key()[pygame.K_w], EwDirection("NORTH"), steps[0])
			self.move(key()[pygame.K_s], EwDirection("SOUTH"), steps[1])
			self.move(key()[pygame.K_a], EwDirection("WEST"), steps[2])
			self.move(key()[pygame.K_d], EwDirection("EAST"), steps[3])
		
	def teleport(self, condition, new_x, new_y):
		if condition:
			self.x = new_x
			self.y = new_y
		
	def get_direction(self):
		return self.direction
		
	def set_direction(self, value):
		self.direction = value
	
	def get_step(self):
		return self.step
		
	def set_step(self, value):
		self.step = value
			
class EwResizable:
	
	def __init__(self, w, h):
		
		self.w = w
		self.h = h
		
	def __getitem__(self, key):
		
		if key == "w":
			return self.w
		elif key == "h":
			return self.h
		elif key == "(wh)":
			return (self.w, self.h)
		elif key == "[wh]":
			return [self.w, self.h]
		
	def __setitem__(self, key, value):
		
		if key == "w":
			self.w = value
		elif key == "h":
			self.h = value
		
	def get_w(self):
		return self.w
		
	def set_w(self, value):
		self.w = value
		
	def get_h(self):
		return self.h
		
	def set_h(self, value):
		self.h = value

# Collision Detection
# ======================================================== #

class EwCol:
	
	def __init__(self, o, oo):
		
		self.o = o
		self.oo = oo
		self.ox = self.o.x
		self.oy = self.o.y
		self.ow = self.o.w
		self.oh = self.o.h
		self.oox = self.oo.x
		self.ooy = self.oo.y
		self.oow = self.oo.w
		self.ooh = self.oo.h
		
	def __call__(self):
		
		if ((((self.ox + self.ow) > self.oox) and (self.ox < (self.oox + self.oow))) and (((self.oy + self.oh) > self.ooy) and (self.oy < (self.ooy + self.ooh)))):
			return True
		else:
			return False
			
class EwMouseCol:
	
	def __init__(self, o, oo):
		
		self.o = o
		self.oo = oo
		self.ox = self.o[0]
		self.oy = self.o[1]
		self.oox = self.oo.x
		self.ooy = self.oo.y
		self.oow = self.oo.w
		self.ooh = self.oo.h
		
	def __call__(self):
		
		if (((self.ox > self.oox) and (self.ox < (self.oox + self.oow))) and ((self.oy > self.ooy) and (self.oy < (self.ooy + self.ooh)))):
			return True
		else:
			return False

# Object Manipulation
# ======================================================== #

class EwDrawable(EwMovable, EwResizable):
	
	def __init__(self, x, y, w, h):
		
		EwMovable.__init__(self, x, y)
		EwResizable.__init__(self, w, h)
		self.surface = pygame.Surface((w, h))
		self.surface.set_colorkey(self.surface.get_at((0,0)), pygame.RLEACCEL)
		
	def __call__(self):
		return self.surface
		
	def draw(self, destination_surface):
		pass
		
class EwRotatable(EwDrawable):
	
	def __init__(self, x, y, w, h):
		
		EwDrawable.__init__(self, x, y, w, h)
		self.rot_surfaces = None
		self.manager = 0
	
	def create_rotations(self, start_angle=0, final_angle=360, step=10):
		def rot(angle):
			orig_rect = self.surface.get_rect()
			rot_image = pygame.transform.rotate(self.surface, angle)
			rot_rect = orig_rect.copy()
			rot_rect.center = rot_image.get_rect().center
			rot_image = rot_image.subsurface(rot_rect).copy()
			return rot_image
		self.rot_surfaces = [rot(n) for n in range(start_angle, final_angle, step)]
	
	def rotate(self, direction=1):
		if self.rot_surfaces is not None:
			self.surface = self.rot_surfaces[self.manager]
			if direction == 0:
				self.manager += 1
				if self.manager > len(self.rot_surfaces)-1:
					self.manager = 0
			elif direction == 1:
				self.manager -= 1
				if self.manager < -(len(self.rot_surfaces)-1):
					self.manager = 0
			
class EwObject(EwDrawable, EwData):
	
	def __init__(self, x, y, w, h):
		
		EwDrawable.__init__(self, x, y, w, h)
		EwData.__init__(self)		
		self.has_focus = False
		
	def get(self):
		return (self.x, self.y, self.w, self.h)
		
	def get_app(self):
		if EwData.app is not None:
			return EwData.app
			
	def watch_for_focus(self):
		if EwMouseCol(pygame.mouse.get_pos(), self)() and pygame.mouse.get_pressed()[0]:
			self.has_focus = True
		if EwMouseCol(pygame.mouse.get_pos(), self)() and pygame.mouse.get_pressed()[2]:
			self.has_focus = False
			
class EwImage(EwObject):
	
	def __init__(self, x, y, w, h, filename, alpha=255):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.filename = filename
		self.alpha = alpha
		
		if ".png" not in self.filename:
			self.surface = pygame.image.load(os.path.join(GRAPHICS_PATH, filename)).convert()
		else:
			self.surface = pygame.image.load(os.path.join(GRAPHICS_PATH, filename)).convert_alpha()
		
		self.surface.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
		self.transform()
			
	def transform(self):
		self.surface = pygame.transform.scale(self.surface, (self.w, self.h))
		
	def transform_freely(self, w, h):
		self.surface = pygame.transform.scale(self.surface, (w, h))
		
	def fade_in(self, speed, limit=255):
		if (self.alpha < limit) and (self.alpha < 255):
			self.alpha += speed
			self.surface.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
		
	def fade_out(self, speed, limit=0):
		if (self.alpha > limit) and (self.alpha > 0):
			self.alpha -= speed
			self.surface.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
			
	def is_faded_in(self, value=255):
		if self.alpha >= value:
			return True
		else:
			return False 
			
	def is_faded_out(self, value=0):
		if self.alpha <= value:
			return True
		else:
			return False 
			
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app.screen.blit(self.surface, (self.x, self.y))
		else:
			destination_surface.blit(self.surface, (self.x, self.y))
		
class EwScrollingImage(EwImage):
	
	def __init__(self, x, y, w, h, filename, scroll_direction=0, scroll_speed=1):
		
		EwImage.__init__(self, x, y, w, h, filename)
		
		if isinstance(scroll_direction, EwDirection):
			self.scroll_direction = scroll_direction
		else:
			raise NotMemberOfError("EwDirection")
		self.scroll_speed = scroll_speed
		self.default_scroll_speed = self.scroll_speed
		self.initial_y = self.y
		self.y0_reset_point = self.initial_y - self.h
		self.y1_reset_point = self.initial_y + self.h
		self.initial_x = self.x
		self.x2_reset_point = self.initial_x - self.w
		self.x3_reset_point = self.initial_x + self.w
		
	def draw(self, destination_surface=None):
		def blit(_dir):
			if destination_surface is None:
				if _dir == 0:
					EwData.app.screen.blit(self.surface, (self.x, self.y))
					EwData.app.screen.blit(self.surface, (self.x, self.y+self.h))
				elif _dir == 1:
					EwData.app.screen.blit(self.surface, (self.x, self.y))
					EwData.app.screen.blit(self.surface, (self.x, self.y-self.h))
				elif _dir == 2:
					EwData.app.screen.blit(self.surface, (self.x, self.y))
					EwData.app.screen.blit(self.surface, (self.x+self.w, self.y))
				elif _dir == 3:
					EwData.app.screen.blit(self.surface, (self.x, self.y))
					EwData.app.screen.blit(self.surface, (self.x-self.w, self.y))
			else:
				if _dir == 0:
					destination_surface.blit(self.surface, (self.x, self.y))
					destination_surface.blit(self.surface, (self.x, self.y+self.h))
				elif _dir == 1:
					destination_surface.blit(self.surface, (self.x, self.y))
					destination_surface.blit(self.surface, (self.x, self.y-self.h))
				elif _dir == 2:
					destination_surface.blit(self.surface, (self.x, self.y))
					destination_surface.blit(self.surface, (self.x+self.w, self.y))
				elif _dir == 3:
					destination_surface.blit(self.surface, (self.x, self.y))
					destination_surface.blit(self.surface, (self.x-self.w, self.y))	
		if self.scroll_direction() == 0 or self.scroll_direction() == "NORTH":
			self.y -= self.scroll_speed
			if self.y < self.y0_reset_point:
				self.y = self.initial_y
			blit(0)
		elif self.scroll_direction() == 1 or self.scroll_direction() == "SOUTH":
			self.y += self.scroll_speed
			if self.y > self.y1_reset_point:
				self.y = self.initial_y
			blit(1)
		elif self.scroll_direction() == 2 or self.scroll_direction() == "WEST":
			self.x -= self.scroll_speed
			if self.x < self.x2_reset_point:
				self.x = self.initial_x
			blit(2)
		elif self.scroll_direction() == 3 or self.scroll_direction() == "EAST":
			self.x += self.scroll_speed
			if self.x > self.x3_reset_point:
				self.x = self.initial_x
			blit(3)
			
	def get_scroll_direction(self):
		return self.scroll_direction
		
	def set_scroll_direction(self, value):
		self.scroll_direction = value
		
	def get_scroll_speed(self):
		return self.scroll_speed
		
	def set_scroll_speed(self, value):
		self.scroll_speed = value
		
	def reset_scroll_speed(self):
		self.scroll_speed = self.default_scroll_speed
			
class EwFont(EwObject):
	
	def __init__(self, x, y, w, h, filename, text, color, bold=False):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.filename = filename
		self.text = text
		self.color = color
		if self.filename is not None:
			self.font = pygame.font.Font(os.path.join(GRAPHICS_PATH, filename), self.w+self.h*2)
		else:
			self.font = pygame.font.Font(None, self.w+self.h)
		if bold:
			self.font.set_bold(True)
		self.surface = self.font.render(self.text, 1, self.color)
		self.transform()
		
	def transform(self):
		self.surface = pygame.transform.scale(self.surface, (self.w, self.h))
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app.screen.blit(self.surface, (self.x, self.y))
		else:
			destination_surface.blit(self.surface, (self.x, self.y))
		
	def get_text(self):
		return self.text
	
	def update(self, value):
		self.text = value
		self.surface = self.font.render(self.text, 1, self.color)
		self.transform()
		
	def update_color(self, color):
		self.color = color
		self.surface = self.font.render(self.text, 1, self.color)
		self.transform()
	
	def __call__(self, value):
		self.text = value
		self.surface = self.font.render(self.text, 1, self.color)
		self.transform()
	
	def set_text(self, value):
		self.text = value
   
	def get_color(self):
		return self.color
		
	def set_color(self, value):
		self.color = value
		
def draw_mouse_coordinates(destination_surface=None, w=None, h=None, color=(255,0,0)):
	if w is None or h is None:
		w = 64
		h = 16
	pos = EwFont(pymo.get_pos()[0]+16, pymo.get_pos()[1], w, h, None, str((pymo.get_pos()[0], pymo.get_pos()[1])), color)
	pos.draw(destination_surface)

class EwShape(EwObject):
	
	def __init__(self, x, y, w, h, color, alpha, thickness):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.color = color
		self.alpha = alpha
		self.thickness = thickness
		pygame.Surface.convert_alpha(self.surface)
		self.surface.set_alpha(self.alpha)
		
	def __call__(self):
		return (self.x, self.y, self.w, self.h, self.color, self.alpha, self.thickness)
		
	def get_color(self):
		return self.color
		
	def set_color(self, value):
		self.color = value
		
	def get_alpha(self):
		return self.alpha
		
	def set_alpha(self, value):
		self.alpha = value
		
	def get_thickness(self):
		return self.thickness
		
	def set_thickness(self, value):
		self.thickness = value
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app.screen.blit(self.surface, (self.x, self.y), (0, 0, self.w, self.h))
		else:
			destination_surface.blit(self.surface, (self.x, self.y), (0, 0, self.w, self.h))
		
class EwRect(EwShape):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		pygame.draw.rect(self.surface, self.color, (x, y, w, h), self.thickness)
		
class EwRotatableRect(EwShape, EwRotatable):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		EwRotatable.__init__(self, x, y, w, h)
		pygame.draw.rect(self.surface, self.color, ((self.w/2)-(self.w/1.4)/2, (self.h/2)-(self.h/1.4)/2, self.w/1.4, self.h/1.4), self.thickness)

class EwPolygon(EwShape):
	
	def __init__(self, pointlist, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, None, None, None, None, color, alpha, thickness)
		self.pointlist = pointlist
		pygame.draw.polygon(self.surface, self.color, self.pointlist, self.thickness)
		
class EwCircle(EwShape):
	
	def __init__(self, x, y, radius, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, radius*2, radius*2, color, alpha, thickness)
		self.radius = radius
		pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius, self.thickness)

	def get_radius(self):
		return self.radius
		
class EwEllipse(EwRect):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwRect.__init__(self, x, y, w, h, color, alpha, thickness)
		pygame.draw.ellipse(self.surface, self.color, (self.x, self.y, self.w, self.h), self.thickness)

class EwArc(EwShape):
	
	def __init__(self, x, y, w, h, start_angle, stop_angle, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		self.start_angle = start_angle
		self.stop_angle = stop_angle
		pygame.draw.arc(self.surface, self.color, (self.x, self.y, self.w, self.h), self.start_angle, self.stop_angle, self.thickness)

	def get_start_angle(self):
		return self.start_angle
		
	def get_stop_angle(self):
		return self.stop_angle

class EwLine(EwShape):
	
	def __init__(self, start_pos, end_pos, color=(255,255,255), alpha=255, thickness=1):
	
		EwShape.__init__(self, None, None, None, None, color, alpha, thickness)
		self.start_pos = start_pos
		self.end_pos = end_pos
		pygame.draw.line(self.surface, self.color, self.start_pos, self.end_pos, self.thickness)
		
class EwLines:
	
	def __init__(self, lines):

		self.lines = lines
	
	def draw(self, destination_surface=None):
		
		if len(self.lines) > 0:
			for line in self.lines:
				if isinstance(line, EwLine):
					line.draw(destination_surface)
				else:
					raise NotMemberOfError("EwLine")
					
	def __call__(self):
		return self.lines
		
	def get_lines(self):
		return self.lines
		
class EwGrid(EwObject):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, cell_width, cell_height):
		
		EwObject.__init__(self, x, y, w, h)
		self.color = color
		self.alpha = alpha
		self.thickness = thickness
		self.cell_width = cell_width
		self.cell_height = cell_height
		self.rows = range(self.x, self.w, self.cell_width)
		self.columns = range(self.y, self.h, self.cell_height)
		[pygame.draw.line(self.surface, self.color, (z, self.y), (z, self.h), self.thickness) for z in self.rows]
		[pygame.draw.line(self.surface, self.color, (self.x, z), (self.w, z), self.thickness) for z in self.columns]
		
	def draw(self, destination_surface=None):
		if destination_surface is None:
			EwData.app.screen.blit(self.surface, (self.x, self.y), (0, 0, self.w, self.h))
		else:
			destination_surface.blit(self.surface, (self.x, self.y), (0, 0, self.w, self.h))
			
	def get_rows(self):
		return self.rows
		
	def get_columns(self):
		return self.columns
		
	def get_cells(self):
		return [(x, y) for x in self.rows for y in self.columns]
			
	def snap_to_grid(self, target):
		target.x = self.x_positions[bisect.bisect_left(self.rows, target.x)-1]
		target.y = self.y_positions[bisect.bisect_left(self.columns, target.y)-1]

# Screen Management
# ======================================================== #

class EwScene:
	
	def __init__(self, scene):
		
		if isinstance(scene, basestring):
			self.scene = scene
		else:
			raise NotMemberOfError("basestring")
		
class EwPlot:
	
	def __init__(self, scenes):
		
		self.data = scenes
		if len(self.data) > 0:
			
			self.current = self.data[0]
	
	def __call__(self):
		return self.current
	
	def get_scene(self):
		return self.current
	
	def change_scene(self, new_scene):
		self.current = new_scene
		
	def next(self):
		if self.data.index(self.current) != len(self.data)-1:
			self.change_scene(self.data[self.data.index(self.current)+1])
		else:
			self.change_scene(self.data[0])
			
	def previous(self):
		if self.data.index(self.current) != 0:
			self.change_scene(self.data[self.data.index(self.current)-1])
		else:
			self.change_scene(self.data[len(self.data)-1])
		
def get_standard_plot():

	scene = [EwScene("S"+str(x)) for x in range(999)]
	opt = [EwScene("OPT"+str(x)) for x in range(999)]
	inv = [EwScene("INV"+str(x)) for x in range(999)]
	l = []
	l.append(EwScene("MAIN"))
	l.extend(scene)
	l.extend(opt)
	l.extend(inv)
	return EwPlot(l)

# GUI
# ======================================================== #

class EwCarret(EwRect):
	
	def __init__(self, x, y, w, h, color, thickness, blinking_delay):
		
		self.blinking_delay = blinking_delay
		EwRect.__init__(self, x, y, w, h, color, thickness)
		self.rd = EwRect.draw
		self.counter = 0
		
	def draw(self, destination_surface):
		self.counter += 1
		if self.counter < self.blinking_delay:
			self.rd(self, destination_surface)
		elif self.counter >= self.blinking_delay*2:
			self.counter = 0

	def set_blinking_delay(self, value):
		self.blinking_delay = value

class EwInput(EwRect):
	
	def __init__(self, x, y, w, h, carret_color, font_filename, label, font_color, char_limit=100, bold=False, carret=None):
		
		self.label = label
		self.label_font = EwFont(x, y, w/3, h, font_filename, self.label, font_color, bold)
		EwRect.__init__(self, x, y, w, h)
		self.rd = EwRect.draw
		self.font = EwFont((x + self.label_font.w) + 2, y, w/12, h, font_filename, "", font_color, bold)
		self.last_key = None
		self.char_limit = char_limit
		self.message = []
		if carret is None:
			self.carret = EwCarret(self.font.x+(self.w/16)+10, y, w/16, h, carret_color , 0, 40)
		else:
			if isinstance(carret, EwCarret):
				self.carret = carret
			else:
				raise NotMemberOfError("EwCarret")

	def __call__(self):
		return "".join(self.message)

	def update_message(self, destination_surface):
		if self.has_focus:
			if (len(self.message) < self.char_limit):
				for e in EwData.app.events:
					if e.type == pygame.KEYDOWN:
						self.last_key = e.key
						if self.last_key is not None and self.last_key in ACCEPTABLE_KEYS:
							if pygame.key.get_pressed()[pygame.K_RSHIFT]:
								self.message.append(pygame.key.name(int(self.last_key)).upper())
							else:
								self.message.append(pygame.key.name(int(self.last_key)))
							self.font.w += self.w / 16
							self.carret.x += self.w / 16
				if pygame.key.get_pressed()[pygame.K_SPACE]:
					if EwData.app.check_if_time_has_elapsed_in_milliseconds(250):
						self.message.append(" ")
						self.font.w += self.w / 16
						self.carret.x += self.w / 16
			if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
				if len(self.message) > 0:
					if EwData.app.check_if_time_has_elapsed_in_milliseconds(180):
						self.font.w -= self.w / 16
						self.carret.x -= self.w / 16
						self.message.pop()
			else:
				self.carret.draw(destination_surface)
	
	def draw(self, destination_surface):
		self.label_font.draw(destination_surface)
		self.update_message(destination_surface)
		if len(self.message) > 0:
			self.font("".join(self.message))
			self.font.draw(destination_surface)
		
class EwAbstractButton:
	
	def __init__(self, x, y, font_width, font_height, font_filename, text, font_color, bold=False):
		
		self.font = EwFont(x, y, font_width, font_height, font_filename, text, font_color, bold)
	
	def hover(self, mouse_pos):
		if EwMouseCol(mouse_pos, self)():
			return True
		if not EwMouseCol(mouse_pos, self)():
			return False
				
	def press(self, mouse_pos, mouse_button, key=None):
		if EwMouseCol(mouse_pos, self)() and pygame.mouse.get_pressed()[mouse_button]:
			return True
		if not EwMouseCol(mouse_pos, self)() and pygame.mouse.get_pressed()[mouse_button]:
			return False
		if key is not None:
			if pygame.key.get_pressed()[key]:
				return True
			if not pygame.key.get_pressed()[key]:
				return False
		
	def change_font_color_when_hovering(self, color):
		if self.hover(pygame.mouse.get_pos()):
			self.font.update_color(color)
		else:
			self.font.update_color(self.font_backup_color)
		
	def get_font_size(self):
		return self.font_size
		
	def set_font_size(self, value):
		self.font_size = value
		
	def get_font(self):
		return self.font
		
	def set_font(self, new_font):
		self.font = new_font
		
class EwButton(EwAbstractButton, EwImage):
	
	def __init__(self, x, y, w, h, filename, font_width, font_height, font_filename, text, font_color, bold=False):
		
		EwAbstractButton.__init__(self, x+font_width/2, y+font_height/2, font_width, font_height, font_filename, text, font_color, bold)
		EwImage.__init__(self, x, y, w, h, filename)
		
class EwRectButton(EwAbstractButton, EwRect):
	
	def __init__(self, x, y, w, h, color, thickness, font_width, font_height, font_filename, text, font_color, bold=False):
		
		EwAbstractButton.__init__(self, x+(w/2)-(font_width/2), y+(h/2)-(font_height/2), font_width, font_height, font_filename, text, font_color, bold)
		EwRect.__init__(self, x, y, w, h, color, thickness)
		self.rd = EwRect.draw
		self.backup_color = color
		self.font_backup_color = self.font.color
		
	def draw(self, destination_surface=None):
		self.rd(self, destination_surface)
		self.font.draw(destination_surface)
		
	def change_color_when_hovering(self, color):
		if self.hover(pygame.mouse.get_pos()):
			self.color = color
		else:
			self.color = self.backup_color
			
class EwRectMenu(EwRect):
	
	def __init__(self, x, y, w, height_of_each_button, color, thickness, buttons):
		
		self.height_of_each_button = height_of_each_button
		if isinstance(buttons, list):
			self.buttons = [EwRectButton(x, y+(n*height_of_each_button), w, self.height_of_each_button, buttons[n][0], buttons[n][1], 
				w-2, self.height_of_each_button-2, buttons[n][2], buttons[n][3], buttons[n][4], buttons[n][5]) for n in range(len(buttons))]
		else:
			raise NotMemberOfError("list")
		EwRect.__init__(self, x, y, w, self.height_of_each_button*len(self.buttons), color, thickness)
		self.rd = EwRect.draw
		
	def draw(self, destination_surface=None):
		self.rd(self, destination_surface)
		[button.draw(destination_surface) for button in self.buttons]
		
	def change_button_colors_when_hovering(self, colors):
		if isinstance(colors, list):
			if len(colors) > 0:
				for color in colors:
					if isinstance(color, tuple):
						if len(colors) > len(self.buttons):
							raise MoreColorsThanButtonsError(len(colors)-len(self.buttons))
							for button in self.buttons:
								button.change_color_when_hovering(color)
						elif len(colors) < len(self.buttons):
							for button in self.buttons:
								button.change_color_when_hovering(colors[0])
					else:
						raise NotMemberOfError("tuple")
		else:
			raise NotMemberOfError("list")
	
	def hover_over_buttons(self, mouse_pos):
		return [b.hover(mouse_pos) for b in self.buttons]
	
	def press_buttons(self, mouse_pos, mouse_button, keys):
		if isinstance(keys, list):
			if len(keys) > 0:
				if len(keys) > len(self.buttons):
					raise MoreKeysThanButtonsError(len(keys)-len(self.buttons))
				elif len(keys) < len(self.buttons):
					return [b.press(mouse_pos, mouse_button, None) for b in self.buttons]
				else:
					return [b.press(mouse_pos, mouse_button, keys[self.buttons.index(b)]) for b in self.buttons]
		
# Environment
# ======================================================== #

class EwEnvironment(EwData):
	
	def __init__(self):
		
		EwData.__init__(self)

# Game-Specific
# ======================================================== #

class EwCamera(EwObject):
	
	def __init__(self, x, y, w, h):
		
		EwObject.__init__(self, x, y, w, h)

class EwWorld(EwData):
	
	def __init__(self, w, h, cam=None):
		
		EwData.__init__(self)
		self.w = w
		self.h = h
		if cam is None:
			self.cam = EwCamera(0, 0, self.w/2, self.h/2)
		else:
			if isinstance(cam, EwCamera):
				self.cam = cam
			else:
				raise NotMemberOfError("EwCamera")

class HealthBar(EwRect):
		
	def __init__(self, x, y, w, h, value):
			
		self.value = value
		self.green = 255
		self.red = 0
		self.number = EwFont(x+(w/2)-(w/5)/2, y, w/5, h, None, str(self.value), (255, 255, 255))
		EwRect.__init__(self, x, y, w, h, (self.red, self.green, 0), 0)
			
	def subtract_health(self, damage):
			
		self.value -= damage
		if self.green > 0:
			self.green -= 255/self.value
		if self.red < 255:
			self.red += 255/self.value
		if self.green >= 0 and self.red <= 255:
			self.color = (self.red, self.green, 0)
