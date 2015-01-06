"""
====================================================================

ERGAME v1.0

"erdat.py", Engine Data.
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
import json
import os

# CFG
# ======================================================== #

GRAPHICS_PATH = "EWG"
SOUNDS_PATH = "EWS"
MUSIC_PATH = "EWM"
DEFAULT_CFG_PATH = "conf.edt"
DEFAULT_OPTIONS_PATH = "options.edt"
DEFAULT_HIGHSCORE_PATH = "highscore.edt"

# CONSTANTS
# ======================================================== #

ON = True
OFF = False

# Sequence Constants:
# -------------------------------------------------------------------------------------------------------

EMPTY = 0
LAST = -1
LAST_INCLUDED = 1

# Graphical Constants:
# -------------------------------------------------------------------------------------------------------

CARRET_SIZE = 2
CARRET_TRANSLATION_FACTOR = 0.6
INNER_SCROLL_BAR_HEIGHT_LIMIT = 6

# Input Constants:
# -------------------------------------------------------------------------------------------------------

SPECIAL = 999

# US SPECIFIC

US_LAYOUT = 0
US_ACUTE = 96 # TILDE 
US_BACK_QUOTE = 96 # TILDE 
US_OPEN_QUOTE = 96 # TILDE 
US_GRAVE = 96 # TILDE 
US_OPEN_BRACKET = 91 # OPEN BRACE
US_CLOSE_BRACKET = 93 # CLOSE BRACE
US_SEMICOLON = 59 # COLON
US_APOSTROPHE = 39 # QUOTATION MARK
US_SINGLE_QUOTE = 39 # QUOTATION MARK
US_COMMA = 44 # LESS THAN
US_PERIOD = 46 # GREATER THAN
US_FORWARD_SLASH = 47 # QUESTION MARK
US_SOLIDUS = 47 # QUESTION MARK
US_VIRGULE = 47 # QUESTION MARK
US_WHACK = 47 # QUESTION MARK
US_BACKSLASH = 92 # PIPE
US_REVERSE_SOLIDUS = 92 # PIPE

# ABNT-2 SPECIFIC (PORTUGUESE)

ABNT2_LAYOUT = 1
ABNT2_APOSTROFO = 96 # ABRE ASPAS
ABNT2_AGUDO = 91 # CRASE
ABNT2_ABRE_COLCHETE = 93 # ABRE CHAVE
ABNT2_FECHA_COLCHETE = 92 # FECHA CHAVE
ABNT2_TIL = 39 # CIRCUMFLEXO
ABNT2_CEDILHA = 59
ABNT2_VIRGULA = 44 # MENOR QUE
ABNT2_PONTO_FINAL = 46 # MAIOR QUE
ABNT2_PONTO_E_VIRGULA = 47 # DOIS PONTOS
ABNT2_BARRA_INVERTIDA = 60 # BARRA VERTICAL 

# ENGINE INPUT CONSTANTS
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

ARROWS = 0
WASD = 1
BOTH = 2

LETTERS = list(range(97, 122 + LAST_INCLUDED))
UPPER_NUMBERS = list(range(48, 57 + LAST_INCLUDED))
KP_NUMBERS = list(range(256, 265 + LAST_INCLUDED))
NUMBERS = UPPER_NUMBERS + KP_NUMBERS

MOUSE_LEFT = 0
MOUSE_WHEEL = 1
MOUSE_RIGHT = 2

# Pygame has two different sets of int representations for mouse buttons (0-2) and (1-3).
# The first one represents the indexes of "pygame.mouse.get_pressed()" (Which returns a tuple of three boolean-ints).
# The second one is used when iterating over "pygame.event.get()" (Which returns a list whose length gets updated according to which inputs are triggered, and both MOUSEBUTTONUP and MOUSEBUTTONDOWN type of events have a dictionary with an entry called "button", whose value ranges from 1 to 5 (5 included). It should begin with 0 in order to avoid this unpleasant confusion, but it doesn't).
# They differ and this issue can easily become too time-consuming if you're not careful.
# For this reason, I've created these constants and comments in order to remind me of this bloody detail.

LMB0 = 0
MMB0 = 1
RMB0 = 2

LMB1 = 1
MMB1 = 2
RMB1 = 3
SCROLL_DOWN = 4
SCROLL_UP = 5

# Directional Constants:
# -------------------------------------------------------------------------------------------------------

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

# Return Constants:
# -------------------------------------------------------------------------------------------------------

STRING = 0
INDEX = 1

# Coordenate Constants:
# -------------------------------------------------------------------------------------------------------

ORIGIN = 0

# Color Constants:
# -------------------------------------------------------------------------------------------------------

VIVID = 255
VOID = 1
BORDER_FACTOR = 50
DARKNESS_FACTOR = 100
DARKNESS_THRESHOLD = 150
REACHING_LIGHT = 175
ALMOST_THERE = 200

AQUA = (VOID , VIVID, VIVID)
BLACK = (VOID , VOID , VOID)
BLUE = (VOID , VOID , VIVID)
CORNFLOWER_BLUE = (100, 149, 237)
FUCHSIA = (VIVID, VOID , VIVID)
GRAY = (128, 128, 128)
GREEN = (VOID , 128, VOID)
LIME = (VOID , VIVID, VOID)
MAROON = (128, VOID , VOID)
NAVY_BLUE = (VOID , VOID , 128)
OLIVE = (128, 128, VOID)
PURPLE = (128, 0, 128)
RED = (VIVID, VOID , VOID)
SILVER = (192, 192, 192)
TEAL = (VOID , 128, 128)
WHITE = (VIVID, VIVID, VIVID)
YELLOW = (VIVID, VIVID, VOID)

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
	
# Alpha Constants:
# -------------------------------------------------------------------------------------------------------

SOLID = 255
TRANSPARENT = 125
BARELY_VISIBLE = 25
 
# Thickness Constants:
 # -------------------------------------------------------------------------------------------------------
 
FILLED = 0
BAR_MENU_ITEM = 3
 
# Trigger Constants:
# -------------------------------------------------------------------------------------------------------

ENDLESS = 0
ONCE = 1
TWICE = 2
THRICE = 3

# Delay Constants:
# -------------------------------------------------------------------------------------------------------

NO_DELAY = 0
CARRET_BLINKING_DELAY = 16
INPUT_SELECTION_DELAY = 250
SPACE_INPUT_DELAY = 110
MENU_SELECTION_DELAY = 450

# DATA MANIPULATION
# ======================================================== #

class EwSerializable:
	
	"""
	EwSerializable is the engine's top class.
	It opens a file to be written or read.
	"""
	
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
	
	"""
	EwData is basically a python dictionary with inherited support for serialization (Using JSON).
	"""
	
	app = None # Static variable reserved for Python Black Magick.
	
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
