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
from random import randrange
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
		
class UnknownPatternError(ErgameError):
	
	def __init__(self, _pattern):
		
		ErgameError.__init__(self, "The given pattern does not match the following: {}".format(_pattern))

# CFG
# ======================================================== #

GRAPHICS_PATH = "EWG"
SOUNDS_PATH = "EWS"
MUSIC_PATH = "EWM"
DEFAULT_CFG_PATH = "conf.edt"

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
			
MOUSE_LEFT = 0
MOUSE_SCROLL = 1
MOUSE_RIGHT = 2

# Return Methods:

STRING = 0
INDEX = 1

# Color Constants:

AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CORNFLOWER_BLUE = (100, 149, 237)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAROON = (128, 0, 0)
NAVY_BLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

COLORS = [
	AQUA, 
	BLACK, 
	BLUE, 
	CORNFLOWER_BLUE, 
	FUCHSIA, 
	GRAY, 
	GREEN, 
	LIME, 
	MAROON, 
	NAVY_BLUE, 
	OLIVE, 
	PURPLE, 
	RED, 
	SILVER, 
	TEAL, 
	WHITE, 
	YELLOW
	]
 
# Trigger Constants:

ENDLESS = 0
ONCE = 1
TWICE = 2
THRICE = 3

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
	
	app = None # Variable reserved for Python Black Magick.
	
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

	def __init__(self, initial_state, FPS, scenes=99):
		
		self.state = initial_state
		self.FPS = FPS
		self.scenes = scenes
		self.time_elapsed = 0
		self.clock = pygame.time.Clock()
		self.events = []
		self.scenes  = {}

	def __call__(self, end_message=""):
		if isinstance(end_message, basestring):
			if end_message != "":
				print end_message
		else:
			raise NotMemberOfError("basestring")
		self.state = True
		
	def create(self, id_key, f, state=False):
		self.scenes[id_key] = [state, f]

	def activate(self, id_key):
		self.scenes[id_key][0] = True
		
	def deactivate(self, id_key):
		self.scenes[id_key][0] = False
		
	def run(self):
		while self.state is not True:
			dt = self.clock.tick(self.FPS)
			self.time_elapsed += dt
			self.events = pygame.event.get();
			for scene in self.scenes:
				if self.scenes[scene][0] == True:
					apply(self.scenes[scene][1])
			pygame.display.flip()
			
	def watch_for_exit(self):
		for e in self.events:
			if e.type == pygame.QUIT:
				self()
				
	def set_fps(self, value):
		self.FPS = value
		
class EwApp(EwRunnable, EwData):

	def __init__(self, title, w, h, FPS, fullscreen=False, save=True):
		
		EwRunnable.__init__(self, False, FPS)
		EwData.__init__(self)

		if save == True:
			if os.path.isfile(DEFAULT_CFG_PATH):
				self["TITLE"] = self.load(DEFAULT_CFG_PATH)["TITLE"]
				self["SCREEN_WIDTH"] = self.load(DEFAULT_CFG_PATH)["SCREEN_WIDTH"]
				self["SCREEN_HEIGHT"] = self.load(DEFAULT_CFG_PATH)["SCREEN_WIDTH"]
				self["FPS"] = self.load(DEFAULT_CFG_PATH)["FPS"]
				self["FULLSCREEN"] = self.load(DEFAULT_CFG_PATH)["FULLSCREEN"]
				print "Configuration dictionary loaded:\n===============================\n"
				for item in self.data.items():
					print "{}: {}".format(str(item[0]), str(item[1]))
			else:
				self["TITLE"] = title
				self["SCREEN_WIDTH"] = w
				self["SCREEN_HEIGHT"] = h
				self["FPS"] = FPS
				self["FULLSCREEN"] = fullscreen
				self.write(DEFAULT_CFG_PATH)
				print "Configuration dictionary saved."
		else:
			self["TITLE"] = title
			self["SCREEN_WIDTH"] = w
			self["SCREEN_HEIGHT"] = h
			self["FPS"] = FPS
			self["FULLSCREEN"] = fullscreen
		
		if self["FULLSCREEN"] == True:
			self["screen"] = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]), pygame.DOUBLEBUF | pygame.FULLSCREEN)
		else:
			self["screen"] = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]))
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
		
	def fill_background(self, color):
		self["screen"].fill(color)
		
# STATIC FUNCTIONS
# ======================================================== #

def scroll_up():
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 5:
					return True
					
def scroll_down():
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 4:
					return True
					
def press_left_mouse():
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					return True

def press_middle_mouse():
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 2:
					return True 
	
def press_right_mouse():
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 3:
					return True
					
def press_char(k):
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if isinstance(k, basestring):
					if len(k) == 1:
						if k == str(e.unicode):
							return True
					else:
						raise UnknownPatternError('"char"')
				else:
					raise NotMemberOfError("basestring")
					
def release_key(k):
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYUP:
				if e.key == k:
					return True
					
def release_mouse(button=1):
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONUP:
				if e.button == button:
					return True

def press_up():
	if pygame.key.get_pressed()[pygame.K_UP]:
		return True
		
def press_down():
	if pygame.key.get_pressed()[pygame.K_DOWN]:
		return True
		
def press_left():
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		return True
		
def press_right():
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		return True

def press_enter():
	if pygame.key.get_pressed()[pygame.K_RETURN]:
		return True
		
def press_escape():
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		return True

def press_space():
	if pygame.key.get_pressed()[pygame.K_SPACE]:
		return True

def press_left_shift():
	if pygame.key.get_pressed()[pygame.K_LSHIFT]:
		return True

def press_right_shift():
	if pygame.key.get_pressed()[pygame.K_RSHIFT]:
		return True

def press_backspace():
	if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
		return True

def press_delete():
	if pygame.key.get_pressed()[pygame.K_DELETE]:
		return True

def press_key(k):
	if pygame.key.get_pressed()[k]:
			return True
			
def click_left():
	if pygame.mouse.get_pressed()[0]:
		return True
		
def click_scroll():
	if pygame.mouse.get_pressed()[1]:
		return True
		
def click_right():
	if pygame.mouse.get_pressed()[2]:
		return True

def mpos():
	return pygame.mouse.get_pos()

def ctx(value):
	return (EwData.app["SCREEN_WIDTH"]/2)-(value/2)
		
def cty(value):
	return (EwData.app["SCREEN_HEIGHT"]/2)-(value/2)
	
def ctr(reference, value):
	return (reference/2)-(value/2)
	
def tml(value):
		return EwData.app.check_if_time_has_elapsed_in_milliseconds(value)
		
def ts(value):
		return EwData.app.check_if_time_has_elapsed_in_seconds(value)
		
def tm(value):
		return EwData.app.check_if_time_has_elapsed_in_minutes(value)
				
def randcolor():
	return COLORS[randrange(0, len(COLORS)-1)]
	
				
# POSITIONS AND DIMENSIONS
# ======================================================== #
		
class EwPos(EwData):
	
	def __init__(self, x, y):
		
		EwData.__init__(self)
		self["x"] = x
		self["y"] = y
		
	def set_pos(self, value):
		if isinstance(value, tuple):
			self["x"] = value[0]
			self["y"] = value[1]
		else:
			raise NotMemberOfError("tuple")

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
				self["y"] -= step
			if direction() == 1 or direction() == "SOUTH":
				self["y"] += step
			if direction() == 2 or direction() == "WEST":
				self["x"] -= step
			if direction() == 3 or direction() == "EAST":
				self["x"] += step
			return True
	
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
			self["x"] = new_x
			self["y"] = new_y
			
class EwResizable(EwMovable):
	
	def __init__(self, x, y, w, h):
		
		EwMovable.__init__(self, x, y)
		self["w"] = w
		self["h"] = h

# Collision Detection
# ======================================================== #

class EwCol(EwData):
	
	def __init__(self, o, _o):
		
		EwData.__init__(self)
		self['o'] = o
		self["_o"] = _o
		self["ox"] = self['o']["x"]
		self["oy"] = self['o']["y"]
		self["ow"] = self['o']["w"]
		self["oh"] = self['o']["h"]
		self["_ox"] = self["_o"]["x"]
		self["_oy"] = self["_o"]["y"]
		self["_ow"] = self["_o"]["w"]
		self["_oh"] = self["_o"]["h"]
		
	def __call__(self):
		
		if ((((self["ox"] + self["ow"]) > self["_ox"]) 
				and (self["ox"] < (self["_ox"] + self["_ow"]))) 
				and (((self["oy"] + self["oh"]) > self["_oy"]) 
				and (self["oy"] < (self["_oy"] + self["_oh"])))):
			return True
		else:
			return False
			
class EwMouseCol(EwData):
	
	def __init__(self, o, _o): # The Mouse-Position-Tuple must come first for obvious reasons.
		
		EwData.__init__(self)
		self['o'] = o
		self["_o"] = _o
		self["ox"] = self['o'][0] # Obvious reason 1.
		self["oy"] = self['o'][1] # Obvious reason 2.
		self["_ox"] = self["_o"]["x"]
		self["_oy"] = self["_o"]["y"]
		self["_ow"] = self["_o"]["w"] 
		self["_oh"] = self["_o"]["h"]
		
	def __call__(self):
		
		if (((self["ox"] > self["_ox"]) 
				and (self["ox"] < (self["_ox"] + self["_ow"]))) 
				and ((self["oy"] > self["_oy"]) 
				and (self["oy"] < (self["_oy"] + self["_oh"])))):
			return True
		else:
			return False

# Static Functions:

def col(o, _o):
	return EwCol(o, _o)()

def mcol(o):
	return EwMouseCol(mpos(), o)()

def colf(o, oo, f, *args):
	if EwCol(o, oo)():
		apply(f, args)
		
def multi_col(*args):
	if len(args) > 0:
		for arg in args:
			if isinstance(arg, tuple) or isinstance(arg, list):
				if len(arg) == 2:
					break
				else:
					raise ErgameError("One of the given tuples does not have the length of 2. Each tuple must shelter 2 Ergame Objects.")
			else:
				raise NotMemberOfError("tuple nor list")
		return [EwCol(o[0], o[1])() for o in args]
		
# Object Manipulation
# ======================================================== #

class EwDrawable(EwResizable):
	
	def __init__(self, x, y, w, h):
		
		EwResizable.__init__(self, x, y, w, h)
		self["surface"] = pygame.Surface((w, h))
		self["surface"].set_colorkey(self["surface"].get_at((0,0)), pygame.RLEACCEL)

class EwRotatable(EwDrawable):
	
	def __init__(self, x, y, w, h):
		
		EwDrawable.__init__(self, x, y, w, h)
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
			
class EwObject(EwDrawable):
	
	def __init__(self, x, y, w, h):

		EwDrawable.__init__(self, x, y, w, h)
		self["has_focus"] = False
		
	def get(self):
		return (self["x"], self["y"], self["w"], self["h"])
		
	def get_app(self):
		if EwData.app is not None:
			return EwData.app
			
	def watch_for_focus(self):
		if EwMouseCol(pygame.mouse.get_pos(), self)() and press_left_mouse():
			self["has_focus"] = True
		if EwMouseCol(pygame.mouse.get_pos(), self)() and press_right_mouse():
			self["has_focus"] = False
			
class EwImage(EwObject):
	
	def __init__(self, x, y, w, h, filename, alpha=255):
		
		EwObject.__init__(self, x, y, w, h)
		
		self["filename"] = filename
		self["alpha"] = alpha
		
		if ".png" not in self["filename"]:
			self["surface"] = pygame.image.load(os.path.join(GRAPHICS_PATH, filename)).convert()
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
		
class EwScrollingImage(EwImage):
	
	def __init__(self, x, y, w, h, filename, scroll_direction=0, scroll_speed=1):
		
		EwImage.__init__(self, x, y, w, h, filename)
		
		if isinstance(scroll_direction, EwDirection):
			self["scroll_direction"] = scroll_direction
		else:
			raise NotMemberOfError("EwDirection")
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
		if self["scroll_direction"]() == 0 or self["scroll_direction"]() == "NORTH":
			self["y"] -= self["scroll_speed"]
			if self["y"] < self["y0_reset_point"]:
				self["y"] = self["initial_y"]
			blit(0)
		elif self["scroll_direction"]() == 1 or self["scroll_direction"]() == "SOUTH":
			self["y"] += self["scroll_speed"]
			if self["y"] > self["y1_reset_point"]:
				self["y"] = self["initial_y"]
			blit(1)
		elif self["scroll_direction"]() == 2 or self["scroll_direction"]() == "WEST":
			self["x"] -= self["scroll_speed"]
			if self["x"] < self["x2_reset_point"]:
				self["x"] = self["initial_x"]
			blit(2)
		elif self["scroll_direction"]() == 3 or self["scroll_direction"]() == "EAST":
			self["x"] += self["scroll_speed"]
			if self["x"] > self["x3_reset_point"]:
				self["x"] = self["initial_x"]
			blit(3)

	def reset_scroll_speed(self):
		self["scroll_speed"] = self["default_scroll_speed"]
			
class EwFont(EwObject):
	
	def __init__(self, x, y, w, h, filename, text, color, alpha=255, bold=False):
		
		EwObject.__init__(self, x, y, w, h)
		
		self["filename"] = filename
		if isinstance(text, basestring):
			pass
		else:
			text = str(text)
		self["text"] = text
		self["color"] = color
		self["alpha"] = alpha
		if self["filename"] is not None:
			self["font"] = pygame.font.Font(os.path.join(GRAPHICS_PATH, filename), 128)
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

def text(x, y, w, h, filename, text, color, alpha=255, bold=False):
	EwFont(x, y, w, h, filename, text, color, alpha, bold).draw()

def draw_mouse_coordinates(destination_surface=None, w=None, h=None, color=(255,0,0)):
	if w is None or h is None:
		w = 64
		h = 16
	pos = EwFont(pymo.get_pos()[0]+16, pymo.get_pos()[1], w, h, None, str((pymo.get_pos()[0], pymo.get_pos()[1])), color)
	pos.draw(destination_surface)

class EwShape(EwObject):
	
	def __init__(self, x, y, w, h, color, alpha, thickness):
		
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
		
class EwRect(EwShape):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		pygame.draw.rect(self["surface"], self["color"], (0, 0, w, h), self["thickness"])
		
	def update_color(self, color):
		self["color"] = color
		pygame.draw.rect(self["surface"], self["color"], (0, 0, self["w"], self["h"]), self["thickness"])
		
class EwRotatableRect(EwShape, EwRotatable):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		EwRotatable.__init__(self, x, y, w, h)
		pygame.draw.rect(self["surface"], self["color"], ((self["w"]/2)-(self["w"]/1.4)/2, (self["h"]/2)-(self["h"]/1.4)/2, self["w"]/1.4, self["h"]/1.4), self["thickness"])

class EwTrigger(EwRect):
	
	def __init__(self, x, y, w, h, color=(175,0,75), alpha=75, thickness=0, trigger_mode=ENDLESS):
		
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
		
		EwShape.__init__(self, None, None, None, None, color, alpha, thickness)
		self["pointlist"] = pointlist
		pygame.draw.polygon(self["surface"], self["color"], self["pointlist"], self["thickness"])
		
class EwCircle(EwShape):
	
	def __init__(self, x, y, radius, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, radius*2, radius*2, color, alpha, thickness)
		self["radius"] = radius
		pygame.draw.circle(self["surface"], self["color"], (0, 0, self["radius"], self["thickness"]))
		
class EwEllipse(EwShape):
	
	def __init__(self, x, y, w, h, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		pygame.draw.ellipse(self["surface"], self["color"], (0, 0, self["w"], self["h"]), self["thickness"])

class EwArc(EwShape):
	
	def __init__(self, x, y, w, h, start_angle, stop_angle, color=(255,255,255), alpha=255, thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, alpha, thickness)
		self["start_angle"] = start_angle
		self["stop_angle"] = stop_angle
		pygame.draw.arc(self["surface"], self["color"], (0, 0, self["w"], self["h"]), self["start_angle"], self["stop_angle"], self["thickness"])

class EwLine(EwShape):
	
	def __init__(self, start_pos, end_pos, color=(255,255,255), alpha=255, thickness=1):
	
		EwShape.__init__(self, None, None, None, None, color, alpha, thickness)
		self["start_pos"] = start_pos
		self["end_pos"] = end_pos
		pygame.draw.line(self["surface"], self["color"], self["start_pos"], self["end_pos"], self["thickness"])
		
class EwLines(EwData):
	
	def __init__(self, lines):

		EwData.__init__(self)
		self["lines"] = lines
	
	def draw(self, destination_surface=None):
		
		if len(self["lines"]) > 0:
			for line in self["lines"]:
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
		
	def navigate(self, target, condition, direction=EwDirection("NORTH"), step=1):
		if isinstance(direction, EwDirection):
			self["direction"] = direction
		else:
			raise NotMemberOfError("EwDirection")
		if condition:
			if self["direction"]() == 0 or self["direction"]() == "NORTH":
				bi = bisect.bisect_left(self["columns"], target["y"])-step
				if bi > -1:
					target["y"] -= step
					target["y"] = self["columns"][bi]
			if self["direction"]() == 1 or self["direction"]() == "SOUTH":
				bi = bisect.bisect_left(self["columns"], target["y"])+step
				if bi < len(self["columns"]):
					target["y"] += step
					target["y"] = self["columns"][bi]
			if self["direction"]() == 2 or self["direction"]() == "WEST":
				bi = bisect.bisect_left(self["rows"], target["x"])-step
				if bi > -1:
					target["x"] -= step
					target["x"] = self["rows"][bi]
			if self["direction"]() == 3 or self["direction"]() == "EAST":
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
					self.navigate(target, press_up(), EwDirection("NORTH"), step_pattern[0])
					self.navigate(target, press_down(), EwDirection("DOWN"), step_pattern[1])
					self.navigate(target, press_left(), EwDirection("LEFT"), step_pattern[2])
					self.navigate(target, press_right(), EwDirection("RIGHT"), step_pattern[3])
				elif movement_type == WASD:
					self.navigate(target, press_key(pygame.K_w), EwDirection("NORTH"), step_pattern[0])
					self.navigate(target, press_key(pygame.K_s), EwDirection("DOWN"), step_pattern[1])
					self.navigate(target, press_key(pygame.K_a), EwDirection("LEFT"), step_pattern[2])
					self.navigate(target, press_key(pygame.K_d), EwDirection("RIGHT"), step_pattern[3])
				elif movement_type == BOTH:
					self.navigate(target, press_up(), EwDirection("NORTH"), step_pattern[0])
					self.navigate(target, press_down(), EwDirection("DOWN"), step_pattern[1])
					self.navigate(target, press_left(), EwDirection("LEFT"), step_pattern[2])
					self.navigate(target, press_right(), EwDirection("RIGHT"), step_pattern[3])
					self.navigate(target, press_key(pygame.K_w), EwDirection("NORTH"), step_pattern[0])
					self.navigate(target, press_key(pygame.K_s), EwDirection("DOWN"), step_pattern[1])
					self.navigate(target, press_key(pygame.K_a), EwDirection("LEFT"), step_pattern[2])
					self.navigate(target, press_key(pygame.K_d), EwDirection("RIGHT"), step_pattern[3])
			else:
				raise UnknownPatternError("[int, int, int, int]")

	def update_color(self, color):
		self["color"] = color
		[pygame.draw.line(self["surface"], self["color"], (z, self["y"]), (z, self["h"]), self["thickness"]) for z in self["rows"]]
		[pygame.draw.line(self["surface"], self["color"], (self["x"], z), (self["w"], z), self["thickness"]) for z in self["columns"]]

# GUI
# ======================================================== #
		
class EwSelectionModel(EwData):
	
	"""
	This class is a generic solution for basic selection problems.
	Games, for example, use very often selection in menus. 
	Menus whose functionality takes as input just the mouse do not need to bother with selection,
	considering that it's just a matter of cursor bounding collision detection.
	But menus whose inputs come from the keyboard or joysticks depend on some kind of 'Selection Model',
	And by that I mean a list of booleans.
	This class handles selection separated from menus or combo-boxes or whatever,
	For these, instead of implementing the functionality within themselves, wisely instantiate the EwSelectionModel."""
	
	def __init__(self, target_list, firstly_activated_index=0):
		
		EwData.__init__(self)
		self["booleans"] = [(lambda x=element: False if target_list.index(x) != firstly_activated_index else True)()  for element in target_list]
		
	def select(self, cond, _cond, selection_delay=500):
		
		"""
		Given two conditions, this method sets the next or the previous 
		element in the internal list of booleans to True, given a selection delay in milliseconds."""
		
		if cond: # Forwards.
			for _bool in self["booleans"]:
				if _bool == True:
					i = self["booleans"].index(_bool)
					if tml(selection_delay):
						if i < len(self["booleans"])-1:
							self["booleans"][i+1] = True
							self["booleans"][i] = False
						elif i >= len(self["booleans"])-1:
							self["booleans"][0] = True
							self["booleans"][-1] = False
		elif _cond: # Backwards.
			for _bool in self["booleans"]:
				if _bool == True:
					i = self["booleans"].index(_bool)
					if tml(selection_delay):
						if i > 0:
							self["booleans"][i-1] = True
							self["booleans"][i] = False
						elif i <= 0:
							self["booleans"][-1] = True
							self["booleans"][0] = False
								
	def select_with_arrows(self, selection_delay=500): # For menus.
		self.select(press_down(), press_up(), selection_delay)
		
	def go_foward(self):
		for _bool in self["booleans"]:
			if _bool == True:
				i = self["booleans"].index(_bool)
				if i < len(self["booleans"])-1:
					self["booleans"][i+1] = True
					self["booleans"][i] = False
				elif i >= len(self["booleans"])-1:
					self["booleans"][0] = True
					self["booleans"][-1] = False
							
	def go_backwards(self):
		for _bool in self["booleans"]:
			if _bool == True:
				i = self["booleans"].index(_bool)
				if i > 0:
					self["booleans"][i-1] = True
					self["booleans"][i] = False
				elif i <= 0:
					self["booleans"][-1] = True
					self["booleans"][0] = False
		
	def force_single_selection(self, index):
		
		""" 
		This method is a generic solution for the single selection problem. 
		Given an index, it sets its equivalent element to True within the Selection Model's list of booleans,
		And it iterates reversely over this very list, in order to set to False all the other 
		elements that do not equal to the index of the True one, and thus asserting the True Single Selection. """
		
		self["booleans"][index] = True
		for n in range(len(self["booleans"])-1, -1, -1): # Reversed
			if n != index:
				self["booleans"][n] = False
				
	def get_true_index(self):
		return [self["booleans"].index(boolean) for boolean in self["booleans"] if boolean is True][0]
		
class EwAbstractButton(EwData):
	
	def __init__(self, x, y, font_width, font_height, font_filename, text, font_color, font_alpha=255, bold=False):
		
		EwData.__init__(self)
		self["font_backup_color"] = font_color
		self["font"] = EwFont(x, y, font_width, font_height, font_filename, text, font_color, font_alpha, bold)
	
	def hover(self, target="rect"):
		if EwMouseCol(pygame.mouse.get_pos(), self[target])():
			return True
		if not EwMouseCol(pygame.mouse.get_pos(), self[target])():
			return False
				
	def press(self, mouse_button=1, key=None, target="rect"):
		if EwMouseCol(mpos(), self[target])() and release_mouse(mouse_button):
			return True
		if not EwMouseCol(mpos(), self[target])() and release_mouse(mouse_button):
			return False
		if key is not None:
			if pygame.key.get_pressed()[key]:
				return True
			if not pygame.key.get_pressed()[key]:
				return False
	
	def change_font_color(self, color):
		self["font"].update_color(color)
		
	def restore_font_color(self):
		self["font"].update_color(self["font_backup_color"])
	
	def change_font_color_under_condition(self, condition, color):
		if condition:
			self.change_font_color(color)
		else:
			self.restore_font_color()
		
	def change_font_color_when_hovering(self, color):
		if self.hover("font"):
			self.change_font_color(color)
		else:
			self.restore_font_color()
		
class EwButton(EwAbstractButton, EwImage):
	
	def __init__(self, x, y, w, h, filename, font_width, font_height, font_filename, text, font_color, font_alpha=255, bold=False):
		
		EwAbstractButton.__init__(self, x+font_width/2, y+font_height/2, font_width, font_height, font_filename, text, font_color, font_alpha, bold)
		EwImage.__init__(self, x, y, w, h, filename)
		
class EwRectButton(EwAbstractButton):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, font_width, font_height, font_filename, text, font_color, font_alpha, bold=False):
		
		EwAbstractButton.__init__(self, x+(w/2)-(font_width/2), y+(h/2)-(font_height/2), font_width, font_height, font_filename, text, font_color, font_alpha, bold)
		self["rect"] = EwRect(x, y, w, h, color, alpha, thickness)
		self["backup_color"] = color
		
	def draw(self, destination_surface=None):
		self["rect"].draw(destination_surface)
		self["font"].draw(destination_surface)
		
	def change_color_when_hovering(self, color):
		if self.hover():
			self["color"] = color
		else:
			self["color"] = self["backup_color"]
			
class EwRectMenu(EwData):
	
	def __init__(self, x, y, w, height_of_each_button, color, alpha, thickness, buttons):
		
		EwData.__init__(self)
		self["x"] = x
		self["y"] = y
		self["w"] = w
		self["height_of_each_button"] = height_of_each_button
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		if isinstance(buttons, list):
			self["buttons"] = [EwRectButton(self["x"], 
					self["y"]+(n*self["height_of_each_button"]), 
					self["w"], 
					self["height_of_each_button"], 
					buttons[n][0], 
					buttons[n][1], 
					buttons[n][2], 
					self["w"]-(self["w"]/8), 
					self["height_of_each_button"]-2, 
					buttons[n][3], 
					buttons[n][4], 
					buttons[n][5], 
					buttons[n][6], 
					buttons[n][7]) for n in range(len(buttons))]
		else:
			raise NotMemberOfError("list")
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["height_of_each_button"]*len(self["buttons"]), color, alpha, thickness)
		
	def draw(self, destination_surface=None):
		self["rect"].draw(destination_surface)
		[button.draw(destination_surface) for button in self["buttons"]]
	
	def hover(self):
		return [b.hover() for b in self["buttons"]]

	def press(self, mouse_button=0, option=None):
		if isinstance(mouse_button, int):
			if mouse_button >= 0 and mouse_button < 3:
				if option is None:
					return [b.press(mouse_button, None) for b in self["buttons"]]
				else:
					if isinstance(option, basestring):
						try:
							return [b.press(mouse_button, None) for b in self["buttons"] if self["buttons"][self["buttons"].index(b)]["font"]["text"] == option][0]
						except IndexError:
							raise ErgameError("The given option does not match any button font text. It's worth noticing that the option is case sensitive.")
			else:
				raise ErgameError("The given int does not represent any mouse button. Please choose a number between 0 and 2 for obvious reasons.")
		else:
			raise NotMemberOfError("int")
	
	def change_colors_when_hovering(self, colors):
		if isinstance(colors, list):
			if len(colors) == 1:
				[b.change_color_when_hovering(colors[0]) for b in self["buttons"]]
			elif len(colors)  == len(self["buttons"]):
				[b.change_color_when_hovering(colors[self["buttons"].index(b)]) for b in self["buttons"]]
		elif isinstance(colors, tuple):
			if len(colors) == 3:
				[b.change_color_when_hovering(colors) for b in self["buttons"]]
	
	def change_font_colors_when_hovering(self, colors):
		if isinstance(colors, list):
			if len(colors) == 1:
				[b.change_font_color_when_hovering(colors[0]) for b in self["buttons"]]
			elif len(colors) == len(self["buttons"]):
				[b.change_font_color_when_hovering(colors[self["buttons"].index(b)]) for b in self["buttons"]]
		elif isinstance(colors, tuple):
			if len(colors) == 3:
				[b.change_font_color_when_hovering(colors) for b in self["buttons"]]
	
class EwSimpleTextMenu(EwData):
		
	def __init__(self, x, y, w, height_of_each_font, filename, color, alpha, strings):
			
		EwData.__init__(self)
		self["x"] = x
		self["y"] = y
		self["w"] = w
		self["height_of_each_font"] = height_of_each_font
		self["filename"] = filename
		self["color"] = color
		self["alpha"] = alpha
		if isinstance(strings, list):
			self["strings"] = strings
		else:
			raise NotMemberOfError("list")
		self["buttons"] = [EwAbstractButton(self["x"],   
				self["y"]+(n*self["height_of_each_font"]), 
				self["w"], 
				self["height_of_each_font"], 
				self["filename"], 
				self["strings"][n], 
				self["color"], 
				self["alpha"]) for n in range(len(self["strings"]))]
		self["selection_model"] = EwSelectionModel(self["buttons"])
					
	def draw(self):
		[b["font"].draw() for b in self["buttons"]]
		
	def choose(self, color=RED):
		for b in self["buttons"]:
			for e in EwData.app.events:
				if e.type != pygame.KEYDOWN:
					if b.hover("font"):
						self["selection_model"].force_single_selection(self["buttons"].index(b))
			if self["selection_model"]["booleans"][self["buttons"].index(b)]:
				b.change_font_color(color)
			else:
				b.restore_font_color()
			
	def select(self, selection_delay=500, return_method=STRING, custom_key=pygame.K_RETURN):
		for b in self["buttons"]:
			if self["selection_model"]["booleans"][self["buttons"].index(b)]:
				if press_key(custom_key):
					if return_method == STRING:
						return b["font"]["text"]
					elif return_method == INDEX:
						return self["buttons"].index(b)
		self["selection_model"].select_with_arrows(selection_delay)
	
	def get_selected(self, return_method=STRING):
		for b in self["buttons"]:
			if self["selection_model"]["booleans"][self["buttons"].index(b)]:
				if return_method == STRING:
					return b["font"]["text"]
				elif return_method == INDEX:
					return self["buttons"].index(b)
	
	def set_selected(self, value):
		for b in self["buttons"]:
			if isinstance(value, basestring):
				if b["font"]["text"] == value:
					self["selection_model"]["booleans"][self["buttons"].index(b)] = True
					self["selection_model"].force_single_selection(self["buttons"].index(b))
			elif isinstance(value, int):
				self["selection_model"]["booleans"][value] = True
				self["selection_model"].force_single_selection(value)
			else:
				raise NotMemberOfError("basestring nor int")
				
	def select_option(self, option, selection_delay=500, custom_key=pygame.K_RETURN):
		for b in self["buttons"]:
			if self["selection_model"]["booleans"][self["buttons"].index(b)]:
				if release_key(custom_key):
					if isinstance(option, basestring):
						if option == b["font"]["text"]:
							return True
					else:
						raise NotMemberOfError("basestring")
		self["selection_model"].select_with_arrows(selection_delay)
		
	def press(self, mouse_button=1, option=None):
		if isinstance(mouse_button, int):
			if mouse_button >= 1 and mouse_button < 4:
				if option is None:
					return [b.press(mouse_button, None, "font") for b in self["buttons"]]
				else:
					if isinstance(option, basestring):
						try:
							return [b.press(mouse_button, None, "font") for b in self["buttons"] if self["buttons"][self["buttons"].index(b)]["font"]["text"] == option][0]
						except IndexError:
							raise ErgameError("The given option does not match any button font text. It's worth noticing that the option is case sensitive.")
			else:
				raise ErgameError("The given int does not represent any mouse button. Please choose a number between 0 and 2 for obvious reasons.")
		else:
			raise NotMemberOfError("int")

	def both_press_and_select_option(self, option, mouse_button=1, selection_delay=500, custom_key=pygame.K_RETURN):
		if self.press(mouse_button, option) or self.select_option(option, selection_delay, custom_key):
			return True

class EwCentralizedSimpleTextMenu(EwData, EwSimpleTextMenu):
		
	def __init__(self, w, height_of_each_font, filename, color, strings, alpha=255):
		
		EwData.__init__(self)
		EwSimpleTextMenu.__init__(self, ctx(w), cty(height_of_each_font*len(strings)), w, height_of_each_font, filename, color, alpha, strings)
		
class EwSimplestMenu(EwData, EwSimpleTextMenu):
	
	def __init__(self, w, strings, filename=None, color=WHITE, alpha=255):
		
		EwData.__init__(self)
		EwSimpleTextMenu.__init__(self, ctx(w), cty((w/4)*len(strings)), w, w/4, filename, color, alpha, strings)
		
class EwCarret(EwObject):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, blinking_delay):
		
		EwObject.__init__(self, x, y, w, h)
		self["blinking_delay"] = blinking_delay
		self["rect"] = EwRect(x, y, w, h, color, alpha, thickness)
		self["counter"] = 0
		
	def draw(self, destination_surface=None):
		self["counter"] += 1
		if self["counter"] < self["blinking_delay"]:
			self["rect"].draw(destination_surface)
		elif self["counter"] >= self["blinking_delay"]*2:
			self["counter"] = 0

class EwInput(EwObject):
	
	def __init__(self, x, y, w, h, carret_color, carret_alpha, font_filename, label, font_color, font_alpha, char_limit=100, bold=False, carret=None):
		
		EwObject.__init__(self, x, y, w, h)
		self["carret_color"] = carret_color
		self["carret_alpha"] = carret_alpha
		self["font_filename"] = font_filename
		self["label"] = label
		self["font_color"] = font_color
		self["font_alpha"] = font_alpha
		self["bold"] = bold
		self["label_font"] = EwFont(x, y, w/3, h, self["font_filename"], self["label"], self["font_color"], self["font_alpha"], self["bold"])
		self["rect"] = EwRect(x, y, w, h)
		self["font"] = EwFont((x + self["label_font"]["w"]) + 2, y, w/12, h, self["font_filename"], "", self["font_color"], self["font_alpha"], self["bold"])
		self["last_key"] = None
		self["char_limit"] = char_limit
		self["message"] = []
		if carret is None:
			self["carret"] = EwCarret(self["font"]["x"]+(self["rect"]["w"]/16)+10, y, w/16, h, self["carret_color"], self["carret_alpha"], 0, 600)
		else:
			if isinstance(carret, EwCarret):
				self["carret"] = carret
			else:
				raise NotMemberOfError("EwCarret")

	def __call__(self): 
		return "".join(self["message"])

	def backspace(self):
		self["font"]["w"] -= self["rect"]["w"] / 16
		self["carret"]["rect"]["x"] -= self["rect"]["w"] / 16
		self["message"].pop()

	def update_message(self, destination_surface):
		if self["has_focus"]:
			if (len(self["message"]) < self["char_limit"]):
				for e in EwData.app.events:
					if e.type == pygame.KEYDOWN:
						self["last_key"] = e.key
						if self["last_key"] is not None and self["last_key"] in ACCEPTABLE_KEYS:
							if press_right_shift():
								self["message"].append(pygame.key.name(int(self["last_key"])).upper())
							else:
								self["message"].append(pygame.key.name(int(self["last_key"])))
							self["font"]["w"] += self["rect"]["w"] / 16
							self["carret"]["rect"]["x"] += self["rect"]["w"] / 16
				if press_space():
					if tml(250):
						self["message"].append(" ")
						self["font"]["w"] += self["rect"]["w"] / 16
						self["carret"]["rect"]["x"] += self["rect"]["w"] / 16
			if press_backspace():
				if len(self["message"]) > 0:
					if tml(180):
						self.backspace()
			if press_delete():
				[self.backspace() for c in self["message"]]
			else:
				self["carret"].draw(destination_surface)
	
	def draw(self, destination_surface=None):
		self.watch_for_focus()
		self["label_font"].draw(destination_surface)
		self.update_message(destination_surface)
		if len(self["message"]) > 0:
			self["font"]("".join(self["message"]))
			self["font"].draw(destination_surface)
			
class EwValueChooser(EwObject):
	
	def __init__(self, x, y, values, h, color, alpha, thickness, value_rect_color, value_rect_alpha, value_rect_thickness, font_filename, font_color, font_alpha, bold=False):

		EwObject.__init__(self, x, y, (h/2)*len(values), h)
		self["values"] = values
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["value_rect_color"] = value_rect_color
		self["value_rect_alpha"] = value_rect_alpha
		self["value_rect_thickness"] = value_rect_thickness
		self["font_filename"] = font_filename
		self["font_color"] = font_color
		self["font_alpha"] = font_alpha
		self["bold"] = bold
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], self["thickness"])
		self["value_positions"] = [self["rect"]["x"] + n for n in range(0, self["rect"]["w"], self["rect"]["w"]/len(self["values"]))]
		self["inner_rects"] = [EwRect(pos, self["y"], self["w"]/len(self["values"]), self["h"], self["value_rect_color"], self["value_rect_alpha"], 6) for pos in self["value_positions"]]
		self["value_rect"] = EwRect(self["x"], self["y"], self["w"]/len(self["values"]), self["h"], self["value_rect_color"], self["value_rect_alpha"], self["value_rect_thickness"])
		self["selection_model"] = EwSelectionModel(self["values"])
		self["value"] = self["values"][0]
		for value in self["values"]:
			if isinstance(value, int) or isinstance(value, float):
				self["font"] = EwFont(self["x"] + ctr(self["w"], self["w"]/4), self["y"]-self["h"], self["w"]/4, self["h"], self["font_filename"], self["value"], self["font_color"], self["font_alpha"], self["bold"])
			else:
				s = str(value)
				if len(s) < 15:
					self["font"] = EwFont(self["x"] + ctr(self["w"], self["w"]), self["y"]-self["h"], self["w"], self["h"], self["font_filename"], self["value"], self["font_color"], self["font_alpha"], self["bold"])
				elif len(s) < 30 and len(s) > 15:
					self["font"] = EwFont(self["x"] + ctr(self["w"], self["w"]*2), self["y"]-self["h"], self["w"]*2, self["h"], self["font_filename"], self["value"], self["font_color"], self["font_alpha"], self["bold"])
				else:
					self["font"] = EwFont(self["x"] + ctr(self["w"], self["w"]*4), self["y"]-self["h"], self["w"]*4, self["h"], self["font_filename"], self["value"], self["font_color"], self["font_alpha"], self["bold"])
	
	def choose(self):
		if self["has_focus"]:
			self["selection_model"].select(press_right(), press_left(), 150)
			self["value"] = [self["values"][self["selection_model"]["booleans"].index(_bool)] for _bool in self["selection_model"]["booleans"] if _bool is True][0]
			for pos in self["value_positions"]:
				if self["selection_model"]["booleans"][self["value_positions"].index(pos)]:
					self["value_rect"]["x"] = pos
		self["font"](self["value"])
		
	def set_selected(self, value):
		if value in self["values"]:
			self["selection_model"][self["values"].index(value)] = True
			self["value"] = value
			self["selection_model"].force_single_selection(self["values"].index(value))
		else:
			raise ErgameError("The given value does not exist in the internal list of values of the Value Chooser EwObject.")
	
	def select_scrolling(self, selection_delay=50):
		self["selection_model"].select(scroll_down(), scroll_up(), selection_delay)
	
	def draw(self, destination_surface=None):
		self.watch_for_focus()
		self["rect"].draw(destination_surface)
		[rect.draw(destination_surface) for rect in self["inner_rects"]]
		self.choose()
		self["value_rect"].draw(destination_surface)
		self["font"].draw(destination_surface)

# Game-Specific
# ======================================================== #

# World:

class EwCamera(EwObject):
	
	def __init__(self, x, y, w, h):
		
		EwObject.__init__(self, x, y, w, h)

class EwWorld(EwData):
	
	def __init__(self, w, h, cam=None):
		
		EwData.__init__(self)
		self["w"] = w
		self["h"] = h
		if cam is None:
			self.cam = EwCamera(0, 0, self["w"]/2, self["h"]/2)
		else:
			if isinstance(cam, EwCamera):
				self.cam = cam
			else:
				raise NotMemberOfError("EwCamera")

# Arcade:

class EwHealthBar(EwData):
		
	def __init__(self, x, y, w, h, alpha, value, number_color=WHITE):
		
		EwData.__init__(self)
		self["alpha"] = alpha
		self["value"] = value
		self["number_color"] = number_color
		self["green"] = 255
		self["red"] = 0
		self["number"] = EwFont(x+(w/2)-(w/5)/2, y, w/5, h, None, str(self["value"]), self["number_color"])
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

# RPG:

class EwSlot(EwButton):
	
	def __init__(self, x, y, w, h, filename, font_width, font_height, font_filename, text, font_color, bold=False):
		
		EwButton.__init__(self, x, y, w, h, filename, font_width, font_height, font_filename, text, font_color, bold=False)
		
class EwRectSlot(EwRectButton):
	
	def __init__(self, x, y, w, h, color, thickness, font_width, font_height, font_filename, text, font_color, bold=False):
		
		EwRectButton.__init__(self, x, y, w, h, color, thickness, font_width, font_height, font_filename, text, font_color, bold=False)
		
class EwInventory(EwGrid):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, slot_width, slot_height):
		
		EwGrid.__init__(self, x, y, w, h, color, alpha, thickness, slot_width, slot_height)
		
class EwRectInventory(EwGrid):
	
	def __init__(self, x, y, w, h, color, alpha, thickness, slot_width, slot_height):
		
		EwGrid.__init__(self, x, y, w, h, color, alpha, thickness, slot_width, slot_height)
		
# Rogue-like:

class EwMaze(EwObject):
	
	pass
