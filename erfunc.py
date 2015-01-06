"""
====================================================================

ERGAME v1.01.

"erfunc.py", Engine Static Functions.
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
if os.name == "posix":
	import commands
import ctypes
import pygame
from operator import mul
from random import uniform
from random import randrange
from ercrash import *
from erdat import *
from ercol import *

# STATIC FUNCTIONS
# ======================================================== #
# Some of the functions here are just what I call "name wrappers",
# And they're for both pygame and python.
# They're meant to make game development much... less about suffering.

# Input Functions:
# -------------------------------------------------------------------------------------------------------
# ACHTUNG!
# LIFE-OR-DEATH OBSERVATION:
# There's an INCOMMENSURABLY IMPORTANT distinction:
# KEEP AN EYE OUT FOR THE DIFFERENCE BETWEEN THE "WHEN" (PUSH) AND THE "WHILE" (PRESS) WORDS WITHIN AN "INPUT" CONTEXT.

# Mouse
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def scroll_up():
	""" ITERATION OVER EVENTS: Returns True WHEN the mouse-wheel is scrolled up. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == SCROLL_UP:
					return True
					
def scroll_down():
	""" ITERATION OVER EVENTS: Returns True WHEN the mouse-wheel is scrolled down. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == SCROLL_DOWN:
					return True

def lmb(): # Left Mouse Button
	""" Returns True WHILE clicked. """
	if pygame.mouse.get_pressed()[LMB0]:
		return True

def mmb(): # Middle Mouse Button
	""" Returns True WHILE clicked. """
	if pygame.mouse.get_pressed()[MMB0]:
		return True

def rmb(): # Right Mouse Button
	""" Returns True WHILE clicked. """
	if pygame.mouse.get_pressed()[RMB0]:
		return True

def push_left_mouse():
	""" ITERATION OVER EVENTS: Returns True WHEN clicked. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == LMB1:
					return True
					
def push_middle_mouse():
	""" ITERATION OVER EVENTS: Returns True WHEN clicked. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == MMB1:
					return True 
	
def push_right_mouse():
	""" ITERATION OVER EVENTS: Returns True WHEN clicked. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == RMB1:
					return True
					
def push_mouse(mouse_button=LMB1):
	""" ITERATION OVER EVENTS: Returns True WHEN clicked. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == mouse_button:
					return True

def release_mouse(button=LMB1):
	""" ITERATION OVER EVENTS: Returns True WHEN the given mouse-button is released. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.MOUSEBUTTONUP:
				if e.button == button:
					return True

# Generic
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def push_char(k):
	""" ITERATION OVER EVENTS: Returns True WHEN the given char is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if isinstance(k, str):
					if len(k) == 1:
						if k == str(e.unicode):
							return True
					else:
						raise UnknownPatternError('"char"')
				else:
					raise NotMemberOfError("str")

def push_key(k):
	"""ITERATION OVER EVENTS: Returns True WHEN the given pygame-key is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == k:
					return True

def cluster_pushes(*keys):
	"""ITERATION OVER EVENTS: Returns True WHEN one of the given pygame-keys is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if len(keys) > 0:
					for key in keys:
						if e.key == key:
							return e.key
				else:
					raise ErgameError("For Cylon-God's sake! PYGAME-KEY ARGUMENTS!")

def press_key(k):
	""" Returns True WHILE the given pygame-key is being pressed. """
	if pygame.key.get_pressed()[k]:
			return True
			
def print_keys():
	for e in EwData.app.events:
		if e.type == pygame.KEYDOWN:
			print(str(e.key) +  " (" +pygame.key.name(e.key) + ")")

def release_key(k):
	""" ITERATION OVER EVENTS: Returns True WHEN the given pygame-key is released. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYUP:
				if e.key == k:
					return True

# DEFAULT PYGAME
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Default "upper numbers" (Not the keypad ones)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_0():
	""" Returns True WHILE the 0 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_0]:
		return True

def push_0():
	"""ITERATION OVER EVENTS: Returns True WHEN 0 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_0:
					return True

def press_1():
	""" Returns True WHILE the 1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_1]:
		return True
		
def push_1():
	"""ITERATION OVER EVENTS: Returns True WHEN 1 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_1:
					return True
		
def press_2():
	""" Returns True WHILE the 2 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_2]:
		return True
		
def push_2():
	"""ITERATION OVER EVENTS: Returns True WHEN 2 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_2:
					return True
		
def press_3():
	""" Returns True WHILE the 3 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_3]:
		return True
		
def push_3():
	"""ITERATION OVER EVENTS: Returns True WHEN 3 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_3:
					return True
		
def press_4():
	""" Returns True WHILE the 4 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_4]:
		return True
		
def push_4():
	"""ITERATION OVER EVENTS: Returns True WHEN 4 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_4:
					return True
		
def press_5():
	""" Returns True WHILE the 5 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_5]:
		return True
		
def push_5():
	"""ITERATION OVER EVENTS: Returns True WHEN 5 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_5:
					return True

def press_6():
	""" Returns True WHILE the 6 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_6]:
		return True
		
def push_6():
	"""ITERATION OVER EVENTS: Returns True WHEN 6 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_6:
					return True
		
def press_7():
	""" Returns True WHILE the 7 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_7]:
		return True
		
def push_7():
	"""ITERATION OVER EVENTS: Returns True WHEN 7 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_7:
					return True
		
def press_8():
	""" Returns True WHILE the 8 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_8]:
		return True
		
def push_8():
	"""ITERATION OVER EVENTS: Returns True WHEN 8 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_8:
					return True

def press_9():
	""" Returns True WHILE the 9 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_9]:
		return True
		
def push_9():
	"""ITERATION OVER EVENTS: Returns True WHEN 9 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_9:
					return True
		
# Custom "symbol" input wrappers (Shift + Something) - IBM DEFAULT US LAYOUT
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_double_quote():
	""" Returns True WHILE both the RIGHT_SHIFT and the quote keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_QUOTE]:
		return '"' # Can be considered as True.

def press_colon():
	""" Returns True WHILE both the RIGHT_SHIFT and the semicolon keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_SEMICOLON]:
		return ":"
		
def press_less():
	""" Returns True WHILE both the RIGHT_SHIFT and the comma keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_COMMA]:
		return "<"
		
def press_greater():
	""" Returns True WHILE both the RIGHT_SHIFT and the period keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_PERIOD]:
		return ">"
		
def press_question():
	""" Returns True WHILE both the RIGHT_SHIFT and the slash keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_SLASH]:
		return "?"

def press_exclamation():
	""" Returns True WHILE both the RIGHT_SHIFT and the 1 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_1]:
		return "!" # Can be considered as True.
		
def press_at():
	""" Returns True WHILE both the RIGHT_SHIFT and the 2 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_2]:
		return "@"
		
def press_hash():
	""" Returns True WHILE both the RIGHT_SHIFT and the 3 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_3]:
		return "#"
		
def press_dollar():
	""" Returns True WHILE both the RIGHT_SHIFT and the 4 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_4]:
		return "$"
		
def press_percent():
	""" Returns True WHILE both the RIGHT_SHIFT and the 5 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_5]:
		return "%"
		
def press_and():
	""" Returns True WHILE both the RIGHT_SHIFT and the 7 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_7]:
		return "&"
		
def press_asterisk():
	""" Returns True WHILE both the RIGHT_SHIFT and the 8 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_8]:
		return "*"
		
def press_left_parenthesis():
	""" Returns True WHILE both the RIGHT_SHIFT and the 9 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT] and pygame.key.get_pressed()[pygame.K_9]:
		return "("
		
def press_right_parenthesis():
	""" Returns True WHILE both the RIGHT_SHIFT and the 0 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_0]:
		return ")"

# Other 0
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_backquote():
	""" Returns True WHILE the backquote key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_BACKQUOTE]:
		return True
		
def push_backquote():
	"""ITERATION OVER EVENTS: Returns True WHEN backquote is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_BACKQUOTE:
					return True

def press_backslash():
	""" Returns True WHILE the backslash key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_BACKSLASH]:
		return True
		
def push_backslash():
	"""ITERATION OVER EVENTS: Returns True WHEN backslash is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_BACKSLASH:
					return True

def press_backspace():
	""" Returns True WHILE the backspace key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
		return True
	
def push_backspace():
	"""ITERATION OVER EVENTS: Returns True WHEN backspace is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_BACKSPACE:
					return True

def press_print():
	""" Returns True WHILE the print key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_PRINT]:
		return True

def push_print():
	"""ITERATION OVER EVENTS: Returns True WHEN print is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_PRINT:
					return True	

def press_scroll_lock():
	""" Returns True WHILE the scroll lock key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_SCROLLOCK]:
		return True
		
def push_scroll_lock():
	"""ITERATION OVER EVENTS: Returns True WHEN scroll lock is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SCROLLOCK:
					return True	

def press_break():
	""" Returns True WHILE the break key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_BREAK]:
		return True
		
def push_break():
	"""ITERATION OVER EVENTS: Returns True WHEN break is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_BREAK:
					return True	

def press_insert():
	""" Returns True WHILE the insert key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_INSERT]:
		return True
		
def push_insert():
	"""ITERATION OVER EVENTS: Returns True WHEN insert is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_INSERT:
					return True	

def press_home():
	""" Returns True WHILE the home key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_HOME]:
		return True

def push_home():
	"""ITERATION OVER EVENTS: Returns True WHEN home is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_HOME:
					return True	
					
def press_page_up():
	""" Returns True WHILE the page up key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_PAGEUP]:
		return True

def push_page_up():
	"""ITERATION OVER EVENTS: Returns True WHEN page up is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_PAGEUP:
					return True	

def press_delete():
	""" Returns True WHILE the delete key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_DELETE]:
		return True
		
def push_delete():
	"""ITERATION OVER EVENTS: Returns True WHEN delete is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_DELETE:
					return True

def press_end():
	""" Returns True WHILE the end key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_END]:
		return True
		
def push_end():
	"""ITERATION OVER EVENTS: Returns True WHEN end is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_END:
					return True		

def press_page_down():
	""" Returns True WHILE the page down key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
		return True

def push_page_down():
	"""ITERATION OVER EVENTS: Returns True WHEN page up is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_PAGEDOWN:
					return True	

def press_capslock():
	""" Returns True WHILE the capslock key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_CAPSLOCK]:
		return True
		
def push_capslock():
	"""ITERATION OVER EVENTS: Returns True WHEN capslock is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_CAPSLOCK:
					return True	

def press_mode():
	""" Returns True WHILE the mode key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_MODE]:
		return True
		
def push_mode():
	"""ITERATION OVER EVENTS: Returns True WHEN mode is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_MODE:
					return True	

def press_tab():
	""" Returns True WHILE the tab key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_TAB]:
		return True
		
def push_tab():
	"""ITERATION OVER EVENTS: Returns True WHEN tab is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_TAB:
					return True

def press_slash():
	""" Returns True WHILE the slash key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_SLASH]:
		return True
		
def push_slash():
	"""ITERATION OVER EVENTS: Returns True WHEN slash is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SLASH:
					return True

def press_semicolon():
	""" Returns True WHILE the semicolon key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_SEMICOLON]:
		return True
		
def push_semicolon():
	"""ITERATION OVER EVENTS: Returns True WHEN semicolon is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SEMICOLON:
					return True

def press_period():
	""" Returns True WHILE the period key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_PERIOD]:
		return True
		
def push_period():
	"""ITERATION OVER EVENTS: Returns True WHEN period is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_PERIOD:
					return True

def press_comma():
	""" Returns True WHILE the comma key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_COMMA]:
		return True
		
def push_comma():
	"""ITERATION OVER EVENTS: Returns True WHEN comma is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_COMMA:
					return True

# Arrows
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_up():
	""" Returns True WHILE the up arrow key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_UP]:
		return True

def push_up():
	"""ITERATION OVER EVENTS: Returns True WHEN up is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_UP:
					return True	

def press_down():
	""" Returns True WHILE the down arrow key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_DOWN]:
		return True
		
def push_down():
	"""ITERATION OVER EVENTS: Returns True WHEN down is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_DOWN:
					return True	
		
def press_left():
	""" Returns True WHILE the left arrow key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		return True
		
def push_left():
	"""ITERATION OVER EVENTS: Returns True WHEN left is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LEFT:
					return True	
		
def press_right():
	""" Returns True WHILE the right arrow key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		return True
		
def push_right():
	"""ITERATION OVER EVENTS: Returns True WHEN right is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RIGHT:
					return True	

# Other 1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_minus():
	""" Returns True WHILE the minus key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_MINUS]:
		return True

def push_minus():
	"""ITERATION OVER EVENTS: Returns True WHEN minus is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_MINUS:
					return True	

def press_equals():
	""" Returns True WHILE the minus key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_EQUALS]:
		return True
		
def push_equals():
	"""ITERATION OVER EVENTS: Returns True WHEN equals is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_EQUALS:
					return True	

def press_enter():
	""" Returns True WHILE the enter/return key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RETURN]:
		return True
		
def push_enter():
	"""ITERATION OVER EVENTS: Returns True WHEN enter is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RETURN:
					return True	
		
def press_return():
	""" Returns True WHILE the enter/return key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RETURN]:
		return True
		
def push_return():
	"""ITERATION OVER EVENTS: Returns True WHEN return is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RETURN:
					return True	

def press_quote():
	""" Returns True WHILE the quote key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_QUOTE]:
		return True
		
def push_quote():
	"""ITERATION OVER EVENTS: Returns True WHEN quote is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_QUOTE:
					return True	

def press_escape():
	""" Returns True WHILE the esc/escape key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		return True
		
def push_escape():
	"""ITERATION OVER EVENTS: Returns True WHEN escape is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					return True	

def press_space():
	""" Returns True WHILE the space-bar key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_SPACE]:
		return True
		
def push_space():
	"""ITERATION OVER EVENTS: Returns True WHEN space is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					return True	

# Fs
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_f1():
	""" Returns True WHILE the f1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F1]:
		return True
		
def push_f1():
	"""ITERATION OVER EVENTS: Returns True WHEN f1 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F1:
					return True	
		
def press_f2():
	""" Returns True WHILE the f2 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F2]:
		return True
		
def push_f2():
	"""ITERATION OVER EVENTS: Returns True WHEN f2 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F2:
					return True	
		
def press_f3():
	""" Returns True WHILE the f1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F3]:
		return True
		
def push_f3():
	"""ITERATION OVER EVENTS: Returns True WHEN f3 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F3:
					return True	
		
def press_f4():
	""" Returns True WHILE the f4 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F4]:
		return True
		
def push_f4():
	"""ITERATION OVER EVENTS: Returns True WHEN f4 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F4:
					return True	
		
def press_f5():
	""" Returns True WHILE the f1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F5]:
		return True
		
def push_f5():
	"""ITERATION OVER EVENTS: Returns True WHEN f5 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F5:
					return True	
		
def press_f6():
	""" Returns True WHILE the f1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F6]:
		return True

def push_f6():
	"""ITERATION OVER EVENTS: Returns True WHEN f6 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F6:
					return True	

def press_f7():
	""" Returns True WHILE the f7 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F7]:
		return True

def push_f7():
	"""ITERATION OVER EVENTS: Returns True WHEN f7 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F7:
					return True	

def press_f8():
	""" Returns True WHILE the f8 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F8]:
		return True
		
def push_f8():
	"""ITERATION OVER EVENTS: Returns True WHEN f8 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F8:
					return True	
		
def press_f9():
	""" Returns True WHILE the f9 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F9]:
		return True
		
def push_f9():
	"""ITERATION OVER EVENTS: Returns True WHEN f9 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F9:
					return True	
		
def press_f10():
	""" Returns True WHILE the f10 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F10]:
		return True
		
def push_f10():
	"""ITERATION OVER EVENTS: Returns True WHEN f10 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F10:
					return True	
		
def press_f11():
	""" Returns True WHILE the f11 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F11]:
		return True
		
def push_f11():
	"""ITERATION OVER EVENTS: Returns True WHEN f11 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F11:
					return True	
		
def press_f12():
	""" Returns True WHILE the f12 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_F12]:
		return True
		
def push_f12():
	"""ITERATION OVER EVENTS: Returns True WHEN f12 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_F12:
					return True	

# KPs
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_numlock():
	""" Returns True WHILE the numlock key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_NUMLOCK]:
		return True
		
def push_numlock():
	"""ITERATION OVER EVENTS: Returns True WHEN numlock is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_NUMLOCK:
					return True	

def press_kp0():
	""" Returns True WHILE the KEYPAD 0 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP0]:
		return True
		
def push_kp0():
	"""ITERATION OVER EVENTS: Returns True WHEN kp0 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP0:
					return True	
		
def press_kp1():
	""" Returns True WHILE the KEYPAD 1 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP1]:
		return True
		
def push_kp1():
	"""ITERATION OVER EVENTS: Returns True WHEN kp1 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP1:
					return True	
		
def press_kp2():
	""" Returns True WHILE the KEYPAD 2 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP2]:
		return True

def push_kp2():
	"""ITERATION OVER EVENTS: Returns True WHEN kp2 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP2:
					return True	

def press_kp3():
	""" Returns True WHILE the KEYPAD 3 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP3]:
		return True

def push_kp3():
	"""ITERATION OVER EVENTS: Returns True WHEN kp3 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP3:
					return True	

def press_kp4():
	""" Returns True WHILE the KEYPAD 4 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP4]:
		return True

def push_kp4():
	"""ITERATION OVER EVENTS: Returns True WHEN kp4 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP4:
					return True	

def press_kp5():
	""" Returns True WHILE the KEYPAD 5 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP5]:
		return True

def push_kp5():
	"""ITERATION OVER EVENTS: Returns True WHEN kp5 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP5:
					return True	

def press_kp6():
	""" Returns True WHILE the KEYPAD 6 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP6]:
		return True

def push_kp6():
	"""ITERATION OVER EVENTS: Returns True WHEN kp6 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP6:
					return True	

def press_kp7():
	""" Returns True WHILE the KEYPAD 7 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP7]:
		return True

def push_kp7():
	"""ITERATION OVER EVENTS: Returns True WHEN kp7 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP7:
					return True	

def press_kp8():
	""" Returns True WHILE the KEYPAD 8 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP8]:
		return True

def push_kp8():
	"""ITERATION OVER EVENTS: Returns True WHEN kp8 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP8:
					return True	

def press_kp9():
	""" Returns True WHILE the KEYPAD 9 key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP9]:
		return True

def push_kp9():
	"""ITERATION OVER EVENTS: Returns True WHEN kp9 is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP9:
					return True	

def press_kp_divide():
	""" Returns True WHILE the KEYPAD DIVIDE key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_DIVIDE]:
		return True

def push_kp_divide():
	"""ITERATION OVER EVENTS: Returns True WHEN kp divide is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_DIVIDE:
					return True	

def press_kp_enter():
	""" Returns True WHILE the KEYPAD ENTER key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
		return True
		
def push_kp_enter():
	"""ITERATION OVER EVENTS: Returns True WHEN kp enter is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_ENTER:
					return True	
		
def press_kp_equals():
	""" Returns True WHILE the KEYPAD EQUALS key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_EQUALS]:
		return True
		
def push_kp_equals():
	"""ITERATION OVER EVENTS: Returns True WHEN kp equals is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_EQUALS:
					return True	
		
def press_kp_minus():
	""" Returns True WHILE the KEYPAD MINUS key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
		return True
		
def push_kp_minus():
	"""ITERATION OVER EVENTS: Returns True WHEN kp minus is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_MINUS:
					return True	
		
def press_kp_multiply():
	""" Returns True WHILE the KEYPAD MULTIPLY key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_MULTIPLY]:
		return True
		
def push_kp_multiply():
	"""ITERATION OVER EVENTS: Returns True WHEN kp multiply is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_MULTIPLY:
					return True	
		
def press_kp_period():
	""" Returns True WHILE the KEYPAD PERIOD key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_PERIOD]:
		return True
		
def push_kp_period():
	"""ITERATION OVER EVENTS: Returns True WHEN kp period is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_MULTIPLY:
					return True	
		
def press_kp_plus():
	""" Returns True WHILE the KEYPAD PLUS key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
		return True
		
def push_kp_plus():
	"""ITERATION OVER EVENTS: Returns True WHEN kp plus is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_KP_PLUS:
					return True	

# Lefties
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_left_alt():
	""" Returns True WHILE the left alt key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_LALT]:
		return True
		
def push_left_alt():
	"""ITERATION OVER EVENTS: Returns True WHEN left alt is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LALT:
					return True	
		
def press_left_control():
	""" Returns True WHILE the left control key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_LCTRL]:
		return True
		
def push_left_control():
	"""ITERATION OVER EVENTS: Returns True WHEN left control is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LCTRL:
					return True	

def press_left_shift():
	""" Returns True WHILE the left shift key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_LSHIFT]:
		return True
		
def push_left_shift():
	"""ITERATION OVER EVENTS: Returns True WHEN left shift is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_LSHIFT:
					return True	

# Righties
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_right_alt():
	""" Returns True WHILE the right alt key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RALT]:
		return True
		
def push_right_alt():
	"""ITERATION OVER EVENTS: Returns True WHEN right alt is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RALT:
					return True	

def press_right_control():
	""" Returns True WHILE the right control key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RCTRL]:
		return True

def push_right_control():
	"""ITERATION OVER EVENTS: Returns True WHEN right control is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RCTRL:
					return True	

def press_right_shift():
	""" Returns True WHILE the right shift key is being pressed. """
	if pygame.key.get_pressed()[pygame.K_RSHIFT]:
		return True
		
def push_right_shift():
	"""ITERATION OVER EVENTS: Returns True WHEN right shift is pressed. """
	if EwData.app is not None:
		for e in EwData.app.events:
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RSHIFT:
					return True	
	
# Other combos
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def press_select_all():
	""" Returns True WHILE the LEFT ALT and F4 keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_a]:
		return True

def press_close():
	""" Returns True WHILE the LEFT CTRL and 'a' keys are being pressed. """
	if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]:
		return True
	
def press_shift():
	""" Returns True WHILE the left or right shift are being pressed. """
	if press_key(pygame.K_LSHIFT) or press_key(pygame.K_RSHIFT):
		return True
		
def altgr():
	""" Returns True WHILE the left control and the left alt keys are being pressed."""
	if press_key(pygame.K_LCTRL) and press_key(pygame.K_LALT):
		return True

# KEYBOARD-LAYOUT SPECIFIC (Only presses)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# IBM-PC CLASSIC US

def us_circumflex():
	""" Returns True WHILE one of the SHIFTS and the us 6 keys are being pressed. """
	if press_key(pygame.K_6) and press_shift():
		return True

def us_acute():
	""" Returns True WHILE the us acute key is being pressed. """
	return press_key(US_ACUTE)
	
def us_back_quote():
	""" Returns True WHILE the us back quote key is being pressed. """
	return press_key(US_BACK_QUOTE)
	
def us_open_quote():
	""" Returns True WHILE the us open quote key is being pressed. """
	return press_key(US_OPEN_QUOTE)
	
def us_grave():
	""" Returns True WHILE the us grave key is being pressed. """
	return press_key(US_GRAVE)
	
def us_tilde():
	""" Returns True WHILE one of the SHIFTS and the us acute keys are being pressed. """
	if press_key(US_ACUTE) and press_shift():
		return True
	
def us_open_bracket():
	""" Returns True WHILE the us open bracket key is being pressed. """
	return press_key(US_OPEN_BRACKET)
	
def us_open_brace():
	""" Returns True WHILE one of the SHIFTS and the us open bracket keys are being pressed. """
	if press_key(US_OPEN_BRACKET) and press_shift():
		return True
		
def us_open_curly_bracket():
	""" Returns True WHILE one of the SHIFTS and the us open bracket keys are being pressed. """
	if press_key(US_OPEN_BRACKET) and press_shift():
		return True
		
def us_close_bracket():
	""" Returns True WHILE the us close bracket key is being pressed. """
	return press_key(US_CLOSE_BRACKET)
	
def us_close_brace():
	""" Returns True WHILE one of the SHIFTS and the us close bracket keys are being pressed. """
	if press_key(US_CLOSE_BRACKET) and press_shift():
		return True
		
def us_close_curly_bracket():
	""" Returns True WHILE one of the SHIFTS and the us close bracket keys are being pressed. """
	if press_key(US_CLOSE_BRACKET) and press_shift():
		return True
		
def us_semicolon():
	""" Returns True WHILE the us semicolon key is being pressed. """
	return press_key(US_SEMICOLON)
	
def us_colon():
	""" Returns True WHILE one of the SHIFTS and the us semicolon keys are being pressed. """
	if press_key(US_SEMICOLON) and press_shift():
		return True
		
def us_apostrophe():
	""" Returns True WHILE the us apostrophe key is being pressed. """
	return press_key(US_APOSTROPHE)
	
def us_single_quote():
	""" Returns True WHILE the us single_quote key is being pressed. """
	return press_key(US_SINGLE_QUOTE)
	
def us_quotation_mark():
	""" Returns True WHILE one of the SHIFTS and the us apostrophe keys are being pressed. """
	if press_key(US_APOSTROPHE) and press_shift():
		return True
		
def us_comma():
	""" Returns True WHILE the us comma key is being pressed. """
	return press_key(US_COMMA)
	
def us_less():
	""" Returns True WHILE one of the SHIFTS and the us comma keys are being pressed. """
	if press_key(US_COMMA) and press_shift():
		return True
		
def us_period():
	""" Returns True WHILE the us period key is being pressed. """
	return press_key(US_PERIOD)
	
def us_greater():
	""" Returns True WHILE one of the SHIFTS and the us period keys are being pressed. """
	if press_key(US_PERIOD) and press_shift():
		return True
		
def us_slash():
	""" Returns True WHILE the us forward slash key is being pressed. """
	return press_key(US_FORWARD_SLASH)
	
def us_forward_slash():
	""" Returns True WHILE the us forward slash key is being pressed. """
	return press_key(US_FORWARD_SLASH)	

def us_solidus():
	""" Returns True WHILE the us solidus key is being pressed. """
	return press_key(US_SOLIDUS)
	
def us_virgule():
	""" Returns True WHILE the us virgule key is being pressed. """
	return press_key(US_VIRGULE)
	
def us_whack():
	""" Returns True WHILE the us whack key is being pressed. """
	return press_key(US_WHACK)

def us_question_mark():
	""" Returns True WHILE one of the SHIFTS and the us forward slash keys are being pressed. """
	if press_key(US_FORWARD_SLASH) and press_shift():
		return True
		
def us_backslash():
	""" Returns True WHILE the us backslash key is being pressed. """
	return press_key(US_BACKSLASH)
	
def us_reverse_solidus():
	""" Returns True WHILE the us reverse solidus key is being pressed. """
	return press_key(US_REVERSE_SOLIDUS)

def us_pipe():
	""" Returns True WHILE one of the SHIFTS and the us backslash keys are being pressed. """
	if press_key(US_BACKSLASH) and press_shift():
		return True
		
def us_vertical_bar():
	""" Returns True WHILE one of the SHIFTS and the us backslash keys are being pressed. """
	if press_key(US_BACKSLASH) and press_shift():
		return True
		
# ABNT2 PORTUGUESE

def abnt2_trema():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla 6 estiverem pressionadas. """
	if press_key(pygame.K_6) and press_shift():
		return True

def abnt2_apostrofo():
	""" Retorna True ENQUANTO a tecla apostrofo estiver pressionada. """
	return press_key(ABNT2_APOSTROFO)
	
def abnt2_abre_aspas():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla apostrofo estiverem pressionadas. """
	if press_key(ABNT2_APOSTROFO) and press_shift():
		return True
		
def abnt2_agudo():
	""" Retorna True ENQUANTO a tecla agudo estiver pressionada. """
	return press_key(ABNT2_AGUDO)
	
def abnt2_crase():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla agudo estiverem pressionadas. """
	if press_key(ABNT2_AGUDO) and press_shift():
		return True
		
def abnt2_abre_colchete():
	""" Retorna True ENQUANTO a tecla abre colchete estiver pressionada. """
	return press_key(ABNT2_ABRE_COLCHETE)
	
def abnt2_abre_chave():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla abre colchete estiverem pressionadas. """
	if press_key(ABNT2_ABRE_COLCHETE) and press_shift():
		return True
		
def abnt2_fecha_colchete():
	""" Retorna True ENQUANTO a tecla fecha colchete estiver pressionada. """
	return press_key(ABNT2_FECHA_COLCHETE)
	
def abnt2_fecha_chave():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla fecha colchete estiverem pressionadas. """
	if press_key(ABNT2_FECHA_COLCHETE) and press_shift():
		return True
		
def abnt2_til():
	""" Retorna True ENQUANTO a tecla til estiver pressionada. """
	return press_key(ABNT2_TIL)
	
def abnt2_circumflexo():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla circumflexo estiverem pressionadas. """
	if press_key(ABNT2_TIL) and press_shift():
		return True
		
def abnt2_cedilha():
	""" Retorna True ENQUANTO a tecla cedilha estiver pressionada. """
	return press_key(ABNT2_CEDILHA)
	
def abnt2_virgula():
	""" Retorna True ENQUANTO a tecla virgula estiver pressionada. """
	return press_key(ABNT2_VIRGULA)
	
def abnt2_menor():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla virgula estiverem pressionadas. """
	if press_key(ABNT2_VIRGULA) and press_shift():
		return True
		
def abnt2_ponto_final():
	""" Retorna True ENQUANTO a tecla ponto final estiver pressionada. """
	return press_key(ABNT2_PONTO_FINAL)
	
def abnt2_maior():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla ponto final estiverem pressionadas. """
	if press_key(ABNT2_PONTO_FINAL) and press_shift():
		return True
		
def abnt2_ponto_e_virgula():
	""" Retorna True ENQUANTO a tecla ponto e virgula estiver pressionada. """
	return press_key(ABNT2_PONTO_E_VIRGULA)
	
def abnt2_dois_pontos():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla ponto e virgula estiverem pressionadas. """
	if press_key(ABNT2_PONTO_E_VIRGULA) and press_shift():
		return True
		
def abnt2_barra():
	""" Retorna True ENQUANTO o alt direito e a tecla q estiverem pressionadas. """
	if (altgr() or press_right_alt()) and press_key(pygame.K_q):
		return True
	
def abnt2_ponto_de_interrogacao():
	""" Retorna True ENQUANTO o alt direito e a tecla w estiverem pressionadas. """
	if (altgr() or press_right_alt()) and press_key(pygame.K_w):
		return True
		
def abnt2_barra_invertida():
	""" Retorna True ENQUANTO a tecla barra invertida estiver pressionada. """
	return press_key(ABNT2_BARRA_INVERTIDA)
	
def abnt2_barra_vertical():
	""" Retorna True ENQUANTO um dos SHIFTS e a tecla barra invertida estiverem pressionadas. """
	if press_key(ABNT2_BARRA_INVERTIDA) and press_shift():
		return True

# Coordinate Functions:
# -------------------------------------------------------------------------------------------------------

def set_mouse_pos(pos):
	""" Updates/changes the coordinates of the mouse cursor. """
	pygame.mouse.set_pos(pos)

def mpos():
	""" Returns a tuple with the coordinates of the mouse cursor. """
	return pygame.mouse.get_pos()

def ctx(width):
	""" Returns the center x-coordinate in the screen given a width value. """
	return (EwData.app["SCREEN_WIDTH"]/2)-(width/2)
		
def cty(height):
	""" Returns the center x-coordinate in the screen given a height value. """
	return (EwData.app["SCREEN_HEIGHT"]/2)-(height/2)

# Time Functions:
# -------------------------------------------------------------------------------------------------------
# For "Cooldown" purposes.

def tml(value): 
		return EwData.app.check_if_time_has_elapsed_in_milliseconds(value)
		
def ts(value):
		return EwData.app.check_if_time_has_elapsed_in_seconds(value)
		
def tm(value):
		return EwData.app.check_if_time_has_elapsed_in_minutes(value)

# Color Functions:
# -------------------------------------------------------------------------------------------------------

def randcolor():
	""" Returns a random color from the internal list of predefined colors. """
	return COLORS[randrange(0, len(COLORS)-1)]

def addrgb(c0, c1): # Color Tuple 0 and 1.
	""" Combine the rgb-values of two color-tuples, and returns a new one. """
	r = c0[0] + c1[0]
	g = c0[1] + c1[1]
	b = c0[2] + c1[2]
	if r > VIVID:
		r = VIVID
	if g > VIVID:
		g = VIVID
	if b > VIVID:
		b = VIVID
	return (r, g, b)

def subrgb(c0, c1): # Color Tuple 0 and 1.
	""" Subtract the rgb-values of two color-tuples, and returns a new one. """
	if c0 == BLACK or c1 == BLACK:
		return (0, 0, 0)
	else:
		cd = lambda value: True if c0[value] > DARKNESS_THRESHOLD else False # Color Delimiter.
		if cd(0) or cd(1) or cd(2):
			r = c0[0] - c1[0]
			g = c0[1] - c1[1]
			b = c0[2] - c1[2]
		else:
			r = c0[0] - int(c1[0]/2)
			g = c0[1] - int(c1[0]/2)
			b = c0[2] - int(c1[0]/2)
		if r < VOID:
			r = 1
		if g < VOID:
			g = 1
		if b < VOID:
			b = 1
		return (r, g, b)
	
# Collision Functions:
# -------------------------------------------------------------------------------------------------------

def col(o, _o):
	""" Returns True if EwObject 'o' intersects with EwObject '_o' """
	return EwCol(o, _o)()

def mcol(o):
	""" Returns True if the mouse cursor intersects with EwObject 'o' """
	return EwMouseCol(mpos(), o)()

def colf(o, _o, f, *args):
	""" Executes function 'f' with N number of arguments if EwObject 'o' intersects with EwObject '_o' """
	if EwCol(o, _o)():
		apply(f, args)
		
def multi_col(*args):
	""" Experimental :) (Never tested) """
	if len(args) > EMPTY:
		for arg in args:
			if isinstance(arg, tuple) or isinstance(arg, list):
				if len(arg) == 2:
					break
				else:
					raise ErgameError("One of the given tuples does not have the length of 2. Each tuple must shelter 2 Ergame Objects.")
			else:
				raise NotMemberOfError("tuple nor list")
		return [EwCol(o[0], o[1])() for o in args]

# System Functions:
# -------------------------------------------------------------------------------------------------------

def check_file(string_path):
	""" Returns True if the file exists in the given path. """
	if os.path.isfile(string_path):
		return True
	else:
		return False

def erpath(path, filename):
	if isinstance(path, str) and isinstance(filename, str):
			full_path = os.path.join(path, filename)
			return full_path
	else:
		raise ErgameError("The given input for path or filename is not a string.")

def get_numlock_state():
	if os.name == "nt":
		dll = ctypes.WinDLL("User32.dll")
		VK_NUMLOCK = 0x90
		return dll.GetKeyState(VK_NUMLOCK)
	elif os.name == "posix":
		return int(commands.getoutput('xset q | grep LED')[65])

def get_capslock_state():
	if os.name == "nt":
		dll = ctypes.WinDLL("User32.dll")
		VK_CAPITAL = 0x14
		return dll.GetKeyState(VK_CAPITAL)
	elif os.name == "posix":
		return int(commands.getoutput('xset q | grep LED')[65])
	
def get_scrolllock_state():
	if os.name == "nt":
		dll = ctypes.WinDLL("User32.dll")
		VK_SCROLL = 0x91
		return dll.GetKeyState(VK_SCROLL)
	elif os.name == "posix":
		return int(commands.getoutput('xset q | grep LED')[65])

# Sequence Functions:
# -------------------------------------------------------------------------------------------------------

# Random element of sequence.
randel = lambda l: l[randrange(0, len(l)-1)]

# Last element of.
lastel = lambda l: l[len(l)-1]

# Math Functions:
# -------------------------------------------------------------------------------------------------------

# Multiples:
muples = lambda whole_number, count_limit: map(mul, [whole_number for n in range(count_limit)], range(count_limit))
# Random Multiple.
randple = lambda whole_number, count_limit: randel(map(mul, [whole_number for n in range(count_limit)], range(count_limit)))

# ETC
# -------------------------------------------------------------------------------------------------------

# Useless condition
null = lambda: True if 666 > 999 else False
