"""
====================================================================

ERGAME's Graphical User Interface v1.0.

"ergui.py", Engine GUI.
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
from erdat import *
from erfunc import *
from erbase import *

"""
ERGUI is my humble Graphical User Interface.
ERGUI does not have the concept of "containers" and "components" like Swing from Java,
Therefore, it also does not have the concept of "layout managers".
Everything is drawn in "absolute position" ("null" for layout manager in Swing).
Games are made to be in fullscreen or in window_mode, but not resizable (There are exceptions but, for Nyarlathotep's sake...).
Nevertheless, ERGUI does have concept of "focus", since every object in the engine is focusable by default.
"""

class EwSelectionModel(EwData):
	
	"""
	This class is a generic solution for basic selection problems.
	Games, for example, very often use the concept of "selection" in menus. 
	Menus whose functionality takes as input just the mouse do not need to bother with selection,
	considering that it's just a matter of cursor bounding collision detection.
	But menus whose inputs come from the keyboard or joysticks depend on some kind of 'Selection Model',
	And by that I mean a list of booleans.
	This class handles selection separated from menus or combo-boxes or whatever,
	For these, instead of implementing the functionality within themselves, wisely instantiate the EwSelectionModel.
	"""
	
	def __init__(self, target_list, firstly_activated_index=0):
		
		"""
		Input arguments:
		target_list <- list
		firstly_activated_index <- int
		"""
		
		EwData.__init__(self)
		if firstly_activated_index == LAST:
			self["booleans"] = [False for element in target_list]
			self["booleans"][LAST] = True
		else:
			self["booleans"] = [(lambda x=element: False if target_list.index(x) != firstly_activated_index or firstly_activated_index is None else True)() for element in target_list]
		
	def select(self, cond, _cond, selection_delay=MENU_SELECTION_DELAY):
		
		"""
		Given two conditions, this method sets the next or the previous 
		element in the internal list of booleans to True, given a selection delay in milliseconds."""
		
		if cond: # Forwards.
			if tml(selection_delay):
				i = self.get_true_index()
				for _bool in self["booleans"]:
					
						if i < len(self["booleans"])-1:
							self["booleans"][i+1] = True
							self["booleans"][i] = False
						elif i >= len(self["booleans"])-1:
							self["booleans"][0] = True
							self["booleans"][-1] = False
		elif _cond: # Backwards.
			if tml(selection_delay):
				i = self.get_true_index()
				for _bool in self["booleans"]:
						if i > 0:
							self["booleans"][i-1] = True
							self["booleans"][i] = False
						elif i <= 0:
							self["booleans"][-1] = True
							self["booleans"][0] = False
								
	def select_with_arrows(self, selection_delay=MENU_SELECTION_DELAY): # For menus.
		self.select(press_down(), press_up(), selection_delay)
		
	def go_forward(self, selection_delay):
		i = self.get_true_index()
		for _bool in self["booleans"]:
			if tml(selection_delay):
				if i < len(self["booleans"])-1:
					self["booleans"][i+1] = True
					self["booleans"][i] = False
				elif i >= len(self["booleans"])-1:
					self["booleans"][0] = True
					self["booleans"][-1] = False
							
	def go_backwards(self, selection_delay):
		i = self.get_true_index()
		for _bool in self["booleans"]:
			if tml(selection_delay):
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
		"""  Returns the first True value found on the internal list of booleans."""
		return [self["booleans"].index(boolean) for boolean in self["booleans"] if boolean is True][0]

	def set_selected(self, index):
		if self["booleans"][index] == False:
			self["booleans"][index] = True
			
	def set_to_false(self, index):
		if self["booleans"][index] == True:
			self["booleans"][index] = False
	
	def get_number_of_false_values(self):
		n = 0
		for boolean in self["booleans"]:
			if boolean == False:
				n += 1
		return n
	
	def get_number_of_true_values(self):
		n = 0
		for boolean in self["booleans"]:
			if boolean == True:
				n += 1
		return n
		
	def invert_logic(self):
		for index in range(len(self["booleans"])):
			if self["booleans"][index] == True:
				self["booleans"][index] = False
			elif self["booleans"][index] == False:
				self["booleans"][index] = True

class EwBar(EwRect):
	
	"""
	An EwBar is a fixed-size bar placed NORTH, SOUTH, WEST or EAST in the screen.
	"""
	
	def __init__(self, size, place, color, alpha=SOLID, thickness=FILLED):
		
		"""
		Input arguments:
		size <- float
		place <- int (NORTH, SOUTH, WEST or EAST)
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		self.places = \
		{
			"north": (0, 0, EwData.app["SCREEN_WIDTH"], size), 
			"south": (0, EwData.app["SCREEN_HEIGHT"]-size, EwData.app["SCREEN_WIDTH"], size), 
			"west": (0, 0, size, EwData.app["SCREEN_HEIGHT"]), 
			"east": (EwData.app["SCREEN_WIDTH"]-size, 0, size, EwData.app["SCREEN_HEIGHT"])
		}
		
		if place == NORTH:
			EwRect.__init__(self, self.places["north"][0], self.places["north"][1], self.places["north"][2], self.places["north"][3], color, alpha, thickness)
		elif place == SOUTH:
			EwRect.__init__(self, self.places["south"][0], self.places["south"][1], self.places["south"][2], self.places["south"][3], color, alpha, thickness)
		elif place == WEST:
			EwRect.__init__(self, self.places["west"][0], self.places["west"][1], self.places["west"][2], self.places["west"][3], color, alpha, thickness)
		elif place == EAST:
			EwRect.__init__(self, self.places["east"][0], self.places["east"][1], self.places["east"][2], self.places["east"][3], color, alpha, thickness)
			
		self["place"] = place
			
	def change_place(self, place):
		self["place"] = place
		if self["place"] == NORTH:
			self["x"] = self.places["north"][0]
			self["y"] = self.places["north"][1]
			self.resize(self.places["north"][2], self.places["north"][3])
		elif self["place"] == SOUTH:
			self["x"] = self.places["south"][0]
			self["y"] = self.places["south"][1]
			self.resize(self.places["south"][2], self.places["south"][3])
		elif self["place"] == WEST:
			self["x"] = self.places["west"][0]
			self["y"] = self.places["west"][1]
			self.resize(self.places["west"][2], self.places["west"][3])
		elif self["place"] == EAST:
			self["x"] = self.places["east"][0]
			self["y"] = self.places["east"][1]
			self.resize(self.places["east"][2], self.places["east"][3])
			
class EwRelativeBar(EwRect):
	
	"""
	An EwRelativeBar is a fixed-size bar placed NORTH, SOUTH, WEST or EAST of a given imaginary rectangle.
	"""
	
	def __init__(self, reference_rect, size, place, color, alpha=SOLID, thickness=FILLED):
		
		"""
		Input arguments:
		reference_rect <- tuple <- (x, y, width, height)
		size <- float
		place <- int (NORTH, SOUTH, WEST or EAST)
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		"""
		
		if isinstance(reference_rect, tuple):
			if len(reference_rect) == 4:
				pass
			else:
				raise ErgameError("The given tuple must have 4 elements (x, y, w, h)")
		else:
			raise ErgameError("The given input is not a tuple.")

		self.places = \
		{
			"north": (reference_rect[0], reference_rect[1], reference_rect[2], size), 
			"south": (reference_rect[0], (reference_rect[1]+reference_rect[3])-size, reference_rect[2], size), 
			"west": (reference_rect[0], reference_rect[1], size, reference_rect[3]), 
			"east": ((reference_rect[0]+reference_rect[2])-size, reference_rect[1], size, reference_rect[3])
		}
		
		self["place"] = place
		
		if self["place"] == NORTH:
			EwRect.__init__(self, self.places["north"][0], self.places["north"][1], self.places["north"][2], self.places["north"][3], color, alpha, thickness)
		elif self["place"] == SOUTH:
			EwRect.__init__(self, self.places["south"][0], self.places["south"][1], self.places["south"][2], self.places["south"][3], color, alpha, thickness)
		elif self["place"] == WEST:
			EwRect.__init__(self, self.places["west"][0], self.places["west"][1], self.places["west"][2], self.places["west"][3], color, alpha, thickness)
		elif self["place"] == EAST:
			EwRect.__init__(self, self.places["east"][0], self.places["east"][1], self.places["east"][2], self.places["east"][3], color, alpha, thickness)
			
	def change_place(self, place):
		if self["place"] == NORTH:
			self["x"] = self.places["north"][0]
			self["y"] = self.places["north"][1]
			self.resize(self.places["north"][2], self.places["north"][3])
		elif self["place"] == SOUTH:
			self["x"] = self.places["south"][0]
			self["y"] = self.places["south"][1]
			self.resize(self.places["south"][2], self.places["south"][3])
		elif self["place"] == WEST:
			self["x"] = self.places["west"][0]
			self["y"] = self.places["west"][1]
			self.resize(self.places["west"][2], self.places["west"][3])
		elif self["place"] == EAST:
			self["x"] = self.places["east"][0]
			self["y"] = self.places["east"][1]
			self.resize(self.places["east"][2], self.places["east"][3])

class EwBarMenuItem(EwObject):

	def __init__(self, x, y, w, h, color, alpha=SOLID, thickness=FILLED):
		
		EwObject.__init__(self, x, y, w, h)
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], color, alpha, thickness)
		self["released_color"] = color
		self["hovered_color"] = subrgb(self["released_color"], (DARKNESS_FACTOR, DARKNESS_FACTOR, DARKNESS_FACTOR))
		self["released_font_color"] = subrgb(self["rect"]["color"], (REACHING_LIGHT, REACHING_LIGHT, REACHING_LIGHT))
		self["hovered_font_color"] = addrgb(self["hovered_color"], (ALMOST_THERE , ALMOST_THERE , ALMOST_THERE ))
		self["border"] = border(self["rect"], subrgb(self["released_color"], (BORDER_FACTOR, BORDER_FACTOR, BORDER_FACTOR)), self["rect"]["alpha"], BAR_MENU_ITEM)
		self["label"] = None
		self["filename"] = None
		self["font"] = None
		self["gap"] = 12 # Hateful arbitrary creature.
		self["icon"] = None
		
	def add_label(self, text, filename=None):
		if isinstance(text, basestring):
			self["label"] = text
		else:
			raise ErgameError("The given input is not a string.")
		if isinstance(filename, basestring) or filename is None:
			self["filename"] = filename
		else:
			raise ErgameError("The given input for filename is invalid (It's not None, nor string)")
		self["font"] = EwTransformedFont(self["x"]+self["gap"], self["y"]+(self["gap"]/2), self["w"]-(self["gap"]*2), self["h"]-self["gap"], self["filename"], self["label"], self["released_font_color"])

	def add_icon(self, path, filename):
		self["filename"] = erpath(path, filename)
		self["icon"] = EwImage(self["x"]+self["gap"]/2, self["y"]+self["gap"]/2, self["w"]-self["gap"], self["h"]-self["gap"], self["filename"], self["rect"]["alpha"])

	def draw(self, destination_surface=None):
		self["rect"].draw(destination_surface)
		self["border"].draw(destination_surface)
		try:
			self["font"].draw(destination_surface)
			if self["hovered"]:
				self["rect"].update_color(self["hovered_color"])
				self["font"].update_color(self["hovered_font_color"])
			else:
				self["rect"].update_color(self["released_color"])
				self["font"].update_color(self["released_font_color"])
		except AttributeError:
			pass
		try:
			self["icon"].draw(destination_surface)
			if self["hovered"]:
				self["rect"].update_color(self["hovered_color"])
			else:
				self["rect"].update_color(self["released_color"])
		except AttributeError:
			pass
		self.click_and_hover()

class EwBarMenu(EwBar):
	
	def __init__(self, size, place, color, alpha=SOLID, thickness=FILLED):
	
		EwBar.__init__(self, size, place, color, alpha, thickness)
		self["items"] = []
		self["selection_model"] = None
		self["item_color"] = addrgb(self["color"], (25, 25, 25))
	
	def append(self, size):
		if self["place"] == NORTH:
			_dir = "north"
			cond = "horizontal"
		elif self["place"] == SOUTH:
			_dir = "south"
			cond = "horizontal"
		elif self["place"] == WEST:
			_dir = "west"
			cond = "vertical"
		elif self["place"] == EAST:
			_dir = "east"
			cond = "vertical"
		if len(self["items"]) == EMPTY:
			if cond == "horizontal":
				self["items"].append(EwBarMenuItem(self.places[_dir][0]+BAR_MENU_ITEM, self.places[_dir][1]+BAR_MENU_ITEM, size-BAR_MENU_ITEM, self.places[_dir][3]-(BAR_MENU_ITEM*2), self["item_color"], self["alpha"], self["thickness"]))
			elif cond == "vertical":
				self["items"].append(EwBarMenuItem(self.places[_dir][0]+BAR_MENU_ITEM, self.places[_dir][1]+BAR_MENU_ITEM, self.places[_dir][2]-(BAR_MENU_ITEM*2), size-BAR_MENU_ITEM, self["item_color"], self["alpha"], self["thickness"]))
		elif len(self["items"]) > EMPTY:
			if cond == "horizontal":
				new_x = self["items"][len(self["items"])-1]["x"]+self["items"][len(self["items"])-1]["w"]
				self["items"].append(EwBarMenuItem(new_x+BAR_MENU_ITEM, self.places[_dir][1]+BAR_MENU_ITEM, size-BAR_MENU_ITEM, self.places[_dir][3]-(BAR_MENU_ITEM*2), self["item_color"], self["alpha"], self["thickness"]))
			elif cond == "vertical":
				new_y = self["items"][len(self["items"])-1]["y"]+self["items"][len(self["items"])-1]["h"]
				self["items"].append(EwBarMenuItem(self.places[_dir][0]+BAR_MENU_ITEM, new_y+BAR_MENU_ITEM, self.places[_dir][2]-(BAR_MENU_ITEM*2), size-BAR_MENU_ITEM, self["item_color"], self["alpha"], self["thickness"]))
	
	def add_label_item(self, text, size, filename=None):
		self.append(size)
		lastel(self["items"]).add_label(text, filename)
		self["selection_model"] = EwSelectionModel(self["items"], None)
		
	def add_icon_item(self, size, path, filename):
		self.append(size)
		lastel(self["items"]).add_icon(path, filename)
		self["selection_model"] = EwSelectionModel(self["items"], None)
				
	def draw_items(self, destination_surface=None):
		[item.draw(destination_surface) for item in self["items"] if len(self["items"]) > EMPTY]

class EwVerticalScrollBar(EwObject):

	"""
	An EwVerticalScrollBar is an EwObject that assembles EwRects into a Scroll Bar.
	Warning: The scroll bar is meant to be used with small lists. Be prepared to face the consequences if you do not show some respect to it.
	"""

	def __init__(self, x, y, w, h, color, alpha, items, pos=0):
			
			"""
			Input arguments:
			x <- float
			y <- float
			w <- float
			h <- float
			color <- tuple <- (3 floats from 0 to 255)
			alpha <- float from 0 to 255
			items <- list
			pos <- int
			"""
			
			EwObject.__init__(self, x, y, w, h)
			self["color"] = color
			self["alpha"] = alpha
			if isinstance(items, list) and len(items) > 0:
				self["items"] = items
			else:
				raise ErgameError("The given input is not a list or is an empty one.")
			try:
				self["positions"] = range(0, self["h"], self["h"]/len(self["items"]))
				self["error"] = False
			except ValueError:
				self["positions"] = range(len(self["items"]))
				self["error"] = True
			if isinstance(pos, int) and pos > -1 and pos < len(self["positions"]):
				self["pos"] = pos
			else:
				raise ErgameError("The given pos is less than or greater than the number of items that can be scrolled.")
			self["bar_distance"] = 3
			self["bar_height"] = (self["h"]/len(self["items"]))-(self["bar_distance"]*2)
			try:
				self["bg_rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], 0)
				self["bar_rect"] = EwRect(self["x"]+self["bar_distance"], self["y"]+(self["bar_distance"]+self["positions"][self["pos"]]), self["w"]-(self["bar_distance"]*2), self["bar_height"], subrgb(self["color"], (125, 125, 125)), self["alpha"], 0)
			except (pygame.error, IndexError):
				if self["error"]:
					self["bg_bar_height"] = len(self["items"]) + (INNER_SCROLL_BAR_HEIGHT_LIMIT+self["bar_distance"])
				else:
					self["bg_bar_height"] = self["h"]
				self["bg_rect"] = EwRect(self["x"], self["y"], self["w"], self["bg_bar_height"], self["color"], self["alpha"], 0)
				self["bar_rect"] = EwRect(self["x"]+self["bar_distance"], self["y"]+(self["bar_distance"]+self["positions"][self["pos"]]), self["w"]-(self["bar_distance"]*2), INNER_SCROLL_BAR_HEIGHT_LIMIT, subrgb(self["color"], (125, 125, 125)), self["alpha"], 0)
			self["has_scrolled"] = False
	
	def has_scrolled(self):
		return self["has_scrolled"]
	
	def fix_pos(self):
		if self["pos"] > len(self["positions"])-1:
			self["pos"] = len(self["positions"])-1
		elif self["pos"] < 0:
			self["pos"] = 0
	
	def update_bar(self):
		self["bar_rect"]["y"] = self["y"]+(self["bar_distance"]+self["positions"][self["pos"]])
		try:
			self["bar_rect"].update(str(self["pos"]))
		except AttributeError:
			pass
	
	def slide(self, external_focus=None):
		if external_focus is not None:
			if isinstance(external_focus, EwObject):
				if self["has_focus"] or external_focus["has_focus"]:
					if lmb() and mcol(self["bg_rect"]) or (scroll_up() or scroll_down()):
						if (mpos()[1] > self["bar_rect"]["y"] + self["bar_rect"]["h"] or scroll_up()) and self["pos"] < len(self["positions"])-2:
							self["pos"] += 1
							self.update_bar()
							self["has_scrolled"] = True
						if (mpos()[1] < self["bar_rect"]["y"] or scroll_down()) and self["pos"] > 0:
							self["pos"] -= 1
							self.update_bar()
							self["has_scrolled"] = True
						self.fix_pos()
			else:
				raise ErgameError("The given input for external_focus is not an EwObject, therefore, it does not have focus.")
		else:
			if isinstance(external_focus, EwObject):
				if self["has_focus"]:
					if lmb() and mcol(self["bg_rect"]) or (scroll_up() or scroll_down()):
						if (mpos()[1] > self["bar_rect"]["y"] + self["bar_rect"]["h"] or scroll_up()) and self["pos"] < len(self["positions"])-2:
							self["pos"] += 1
							self.update_bar()
							self["has_scrolled"] = True
						if (mpos()[1] < self["bar_rect"]["y"] or scroll_down()) and self["pos"] > 0:
							self["pos"] -= 1
							self.update_bar()
							self["has_scrolled"] = True
						self.fix_pos()
	
	def draw(self, destination_surface=None):
		self["bg_rect"].draw(destination_surface)
		self["bar_rect"].draw(destination_surface)
		self.watch_for_focus()
		self["has_scrolled"] = False

class EwRectPanel(EwObject):
	
	""" 
	An EwRectPanel is an EwObject that assembles EwRects into an abstract graphical panel.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, border_thickness=6, border_distance=6):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		border_thickness <- int
		border_distance <- float
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["color"] = color
		self["border_color"] = subrgb(self["color"], (125, 125, 125))
		self["alpha"] = alpha
		self["border_thickness"] = border_thickness
		self["border_distance"] = (border_distance + self["border_thickness"])
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], 0)
		self["border"] = EwRect(self["x"] + (self["border_distance"]/2), self["y"] + (self["border_distance"]/2), self["w"] - self["border_distance"], self["h"] - self["border_distance"], self["border_color"], self["alpha"], self["border_thickness"])
		
	def draw(self, destination_surface=None):
		self["rect"].draw(destination_surface)
		self["border"].draw(destination_surface)

class EwListItem(EwObject):
	
	"""
	An EwListItem is an EwObject that assembles an EwFont and an EwRect into an abstract graphical "item".
	"""
	
	def __init__(self, x, y, w, font_color, font_size, text, font_filename=None, font_bold=False, rect_color=WHITE, alpha=SOLID):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		font_color <- tuple <- (3 floats from 0 to 255)
		font_size <- int
		text <- string
		font_filename <- string
		font_bold <- boolean
		rect_color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		"""
		
		EwObject.__init__(self, x, y, w, 1)
		self["font_color"] = font_color
		self["font_size"] = font_size
		self["text"] = text
		self["font_filename"] = font_filename
		self["font_bold"] = font_bold
		self["color"] = rect_color
		self["alpha"] = alpha
		self["font"] = EwFont(self["x"], self["y"], self["font_size"], self["font_filename"], self["text"], self["font_color"], self["alpha"], False)
		self["h"] = self["font"]["font"].get_height()
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], 0)
		
	def draw(self, draw_rect=False, destination_surface=None):
		if draw_rect:
			self["rect"].draw(destination_surface)
		self["font"].draw(destination_surface)
		self.watch_for_focus()

class EwList(EwObject):
	
	"""
	An EwList is an EwObject that assembles EwListItems into an abstract graphical List.
	Warning: The scroll bar is meant to be used with small lists. Be prepared to face the consequences if you do not show some respect to it.
	"""
	
	def __init__(self, x, y, w, font_color, font_size, texts, item_limit, font_filename=None, font_bold=False, alpha=SOLID):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		font_color <- tuple <- (3 floats from 0 to 255)
		font_size <- int
		texts <- list of strings
		item_limit <- int
		font_filename <- string
		font_bold <- boolean
		alpha <- float from 0 to 255
		"""
		
		EwObject.__init__(self, x, y, w, 1)
		self["font_color"] = font_color
		self["font_size"] = font_size
		if isinstance(texts, list):
			self["texts"] = [str(x) for x in texts]
			self["backup"] = [str(x) for x in texts]
		else:
			raise ErgameError("The input must be a list of strings.")
		self["color"] = subrgb(self["font_color"], (175, 175, 175))
		self["alpha"] = alpha
		self["item_limit"] = item_limit
		self["visible_texts"] = self["texts"][:self["item_limit"]]
		self["font_filename"] = font_filename
		self["font_bold"] = font_bold
		temp_font = EwFont(self["x"], self["y"], self["font_size"], self["font_filename"], self["texts"][0], self["font_color"], self["alpha"], False)
		self["font_height"] = temp_font["font"].get_height()
		self["h"] = (self["font_height"]+(self["font_size"]/2))*len(self["visible_texts"])
		self["item_positions"] = [self["y"]+((self["font_height"]+(self["font_size"]/2))*n) for n in range(len(self["visible_texts"]))]
		self["items"] = [EwListItem(self["x"], y_pos, self["w"], self["font_color"], self["font_size"], self["visible_texts"][self["item_positions"].index(y_pos)], self["font_filename"], self["font_bold"], self["color"], self["alpha"]) for y_pos in self["item_positions"]]
		self["rect"] = EwRect(self["x"]-(self["font_size"]/2), self["y"]-(self["font_size"]/2), self["w"]+(self["font_size"]/2), self["h"]+(self["font_size"]/2), self["color"], self["alpha"], 0)
		self["scroll_bar"] = EwVerticalScrollBar(self["x"]+self["w"], self["rect"]["y"], self["font_size"], self["rect"]["h"], self["font_color"], self["alpha"], self["texts"][self["item_limit"]-1:])
		self["selection_rect"] = EwRect(self["x"] - (self["scroll_bar"]["bar_distance"]*2), self["item_positions"][0] - self["scroll_bar"]["bar_distance"], self["w"], self["font_height"] + self["scroll_bar"]["bar_distance"], addrgb(self["color"], (125, 25, 25)), SOLID, 1)
		self.generate_booleans()
		self.generate_selection_data()
		self["errors"] = 0
	
	def generate_booleans(self):
		self["selection_model"] = EwSelectionModel(self["texts"])
		self["selected_items"] = EwSelectionModel(self["texts"], None)
		
	def get_booleans(self):
		return self["selection_model"]["booleans"]
		
	def get_selection_booleans(self):
		return self["selected_items"]["booleans"]

	def update_visible_texts(self):
		self["visible_texts"] = self["texts"][self["scroll_bar"]["pos"]:(self["scroll_bar"]["pos"]+self["item_limit"])]
		self["items"] = [EwListItem(self["x"], self["y"]+((self["font_height"]+(self["font_size"]/2))*n), self["w"], self["font_color"], self["font_size"], self["visible_texts"][n], self["font_filename"], self["font_bold"], self["color"], self["alpha"]) for n in range(len(self["visible_texts"]))]
		self.watch_for_focus()

	def generate_selection_data(self):
		self["true_index"] = self["selection_model"].get_true_index()
		self["number_of_selected_items"] = self["selection_model"].get_number_of_true_values()
		self["last_visible_index"] = len(self["item_positions"])-1
		self["last_index"] = len(self.get_booleans())-1
		self["last_visible_index_end"] = self["last_index"]-self["last_visible_index"]

	def handle_scrolling(self): 
		if self["true_index"] == 0 or self["scroll_bar"]["pos"] < 0:
			self["scroll_bar"]["pos"] = 0
		if self["true_index"] == self["last_index"]:
			self["scroll_bar"]["pos"] = len(self["selection_model"]["booleans"]) - self["item_limit"]
			self["selection_rect"]["y"] = self["item_positions"][self["last_visible_index"]] - self["scroll_bar"]["bar_distance"]
		if push_down() or scroll_up() or press_kp2():
			self["selection_model"].go_forward(NO_DELAY)
			self.generate_selection_data()
			try:
				self["selection_rect"]["y"] = self["item_positions"][self["true_index"]] - self["scroll_bar"]["bar_distance"]
			except IndexError:
				self["scroll_bar"]["pos"] += 1
		elif push_up() or scroll_down() or press_kp8():
			self["selection_model"].go_backwards(NO_DELAY)
			self.generate_selection_data()
			try:
				if self["true_index"] <= self["last_visible_index"]:
					self["scroll_bar"]["pos"] -= 1
				self["selection_rect"]["y"] = self["item_positions"][self["true_index"]] - self["scroll_bar"]["bar_distance"]
			except IndexError:
				self["scroll_bar"]["pos"] -= 1
		self.update_visible_texts()
		try:
			self["scroll_bar"].update_bar()
		except IndexError:
			self["scroll_bar"]["pos"] = len(self["scroll_bar"]["positions"])-1
	
	def handle_selection(self, destination_surface):
		if push_enter() or (push_left_mouse() and not mcol(self["scroll_bar"])):
			index_to_be_selected = self["true_index"]
			if self["selected_items"]["booleans"][index_to_be_selected] == True:
				self["selected_items"]["booleans"][index_to_be_selected] = False
				self["texts"][index_to_be_selected] = self["backup"][index_to_be_selected]
			elif self["selected_items"]["booleans"][index_to_be_selected] == False:
				self["selected_items"]["booleans"][index_to_be_selected] = True	
				self["texts"][index_to_be_selected] = "-> " + self["texts"][index_to_be_selected]
		self["selection_rect"].draw(destination_surface)

	def get_selected_items(self):
		selected = {}
		for bindex in range(len(self["selected_items"]["booleans"])):
			if self["selected_items"]["booleans"][bindex] == True:
				selected[bindex] = self["backup"][bindex]
		return selected
		
	def get_deselected_items(self):
		deselected = {}
		for bindex in range(len(self["selected_items"]["booleans"])):
			if self["selected_items"]["booleans"][bindex] == False:
				deselected[bindex] = self["backup"][bindex]
		return deselected

	def draw(self, enable_selection=True, draw_scroll_bar=False, draw_bg_rect=True, destination_surface=None):
		if draw_bg_rect:
			[rect["rect"].draw(destination_surface) for rect in self["items"]]
			self["rect"].draw()
		try:
			self.handle_scrolling()
		except IndexError:
			self["errors"] += 1
			print "%s index errors found on: %r" % (self["errors"], self)
		if enable_selection:
			self.handle_selection(destination_surface)
		[rect["font"].draw(destination_surface) for rect in self["items"]]
		if draw_scroll_bar:
			self["scroll_bar"].draw(destination_surface)
		if self["scroll_bar"].has_scrolled():
			self.update_visible_texts()

class EwAbstractBoolean(EwObject):
	
	"""
	An EwAbstractBoolean is an EwObject that holds boolean-functionality for a graphical button made out of an EwRect.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, thickness, pressed=False, pressed_darkness=150):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		pressed <- boolean
		pressed_darkness <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["color"] = color
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["pressed"] = pressed
		self["pressed_darkness"] = pressed_darkness
		self["pressed_color"] = subrgb(self["color"], (self["pressed_darkness"], self["pressed_darkness"], self["pressed_darkness"]))
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], self["thickness"])
	
	def darken(self):
		if self["pressed"] is True:
			self["rect"].update_color(self["pressed_color"])
		elif self["pressed"] is False:
			self["rect"].update_color(self["color"])
			
	def switch(self, color):
		if self["pressed"] is True:
			self["rect"].update_color(color)
		elif self["pressed"] is False:
			self["rect"].update_color(self["color"])
	
	def draw(self, mouse_button=LMB1, destination_surface=None):
		self["rect"].draw(destination_surface)
		self.darken()
		self.toggle_and_hover(mouse_button)
		
	def draw_switch(self, color, mouse_button=LMB1, destination_surface=None):
		self["rect"].draw(destination_surface)
		self.switch(color)
		self.toggle_and_hover(mouse_button)

class EwBoolean(EwObject):
	
	"""
	An EwBoolean is an EwObject that assembles EwRects into a graphical binary component.
	"""
	
	def __init__(self, x, y, w, h, colors, alpha, thickness, pressed=False, outer_darkness=125, line_thickness=6):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w<- float
		h <- float
		colors <- list <- two rgb-tuples (Or the first index with a rgb-tuple and the second index with a None value)
		alpha <- float from 0 to 255
		thickness <- int
		pressed <- boolean
		outer_darkness <- int
		line_thickness <- int
		"""
		
		EwObject.__init__(self, x, y, w, h)
		if isinstance(colors, list) or isinstance(colors, tuple):
			if len(colors) > 2 or len(colors) < 2:
				raise ErgameError("The given list or tuple must have exactly two colors.")
			else:
				self["colors"] = colors
		else:
			raise ErgameError("The given color input is not a list nor tuple.")
		self["alpha"] = alpha
		self["thickness"] = thickness
		self["released"] = True
		self["hovered"] = False
		self["pressed"] = pressed
		self["outer_darkness"] = outer_darkness
		self["line_thickness"] = line_thickness
		self["pressed_color"] = subrgb(self["colors"][0], (self["outer_darkness"], self["outer_darkness"], self["outer_darkness"]))
		self["line_color"] = addrgb(self["pressed_color"], (25, 25, 25))
		self["outer_rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["pressed_color"], self["alpha"], self["thickness"])
		self["button_width"] = self.width()-(self.width()/3)
		self["button_height"] = self.height()-(self.height()/3)
		self["button"] = EwAbstractBoolean(self["x"]+((self["button_width"]-(self["button_width"]/2))/2), self["y"]+((self["button_height"]-(self["button_height"]/2))/2), self["button_width"], self["button_height"], self["colors"][0], self["alpha"], self["thickness"], self["pressed"])
		self["lines"] = [
			EwLine((self["x"]+(self["line_thickness"]/2), self["y"]), (self["button"]["x"], self["button"]["y"]), self["line_color"], self["alpha"], self["line_thickness"]),
			EwLine((self["button"].right(), self["button"]["y"]), (self.right()-self["line_thickness"], self["y"]), self["line_color"], self["alpha"], self["line_thickness"]),
			EwLine((self["x"], self.bottom()-self["line_thickness"]), (self["button"]["x"], self["button"].bottom()), self["line_color"], self["alpha"], self["line_thickness"]),
			EwLine((self["button"].right(), self["button"].bottom()), (self.right()-self["line_thickness"], self.bottom()-(self["line_thickness"]/2)), self["line_color"], self["alpha"], self["line_thickness"])
		]
		self["outer_border"] = border(self["outer_rect"], self["line_color"], self["alpha"], self["line_thickness"]/2)
		self["button_border"] = border(self["button"], self["line_color"], self["alpha"], self["line_thickness"]/2)
		self["w"] = self["outer_border"]["w"]
		self["h"] = self["outer_border"]["h"]
		
	def draw(self, mouse_button=LMB1, destination_surface=None):
		self["outer_rect"].draw(destination_surface)
		[line.draw(destination_surface) for line in self["lines"]]
		self["outer_border"].draw(destination_surface)
		self["button_border"].draw(destination_surface)
		if self["colors"][1] is not None:
			self["button"].draw_switch(self["colors"][1], mouse_button, destination_surface)
		else:
			self["button"].draw(mouse_button, destination_surface)
		self["released"] = self["button"]["released"]
		self["hovered"] = self["button"]["hovered"]
		self["pressed"] = self["button"]["pressed"]
		
	def is_pressed(self):
		return self["button"]["pressed"]

class EwTextButton(EwObject):
	
	"""
	An EwTextButton is an EwObject that uses an EwTransformedFont to create a "clickable text" (Good for menus).
	It is meant to be used with a background rect or image (Or None).
	This is the first button I've implemented in the engine. 
	Although it inherits from EwObject, it does not use the later implementation of "EwClickable" (It has a "pressing" and "hovering" system of its own).
	That's because it does not share the same philosophy of "states". 
	A Text Button is meant to return True when pressed over (In order to change the screen with a "Start Game", for example), or to change its text color when hovered, and that's all.
	I'd adapt this class to inherit the functionality from EwClickable, but all my menus are using this one,
	It would not be worth the change, since they don't actually need states (Nevertheless, you could actually access their states of released, hovered and pressed from EwClickable, since it's an EwObject. But I discourage the practice, because it's stupid :)).
	"""
	
	def __init__(self, x, y, font_width, font_height, font_filename, text, font_color, font_alpha=SOLID, bold=False, font_quality=64):
		
		"""
		Input arguments:
		x <- float
		y <- float
		font_width <- float
		font_height <- float
		font_filename <- string
		text <- string
		font_color <- tuple <- (3 floats from 0 to 255)
		font_alpha <- float from 0 to 255
		bold <- boolean
		font_quality <- int
		"""
		
		EwObject.__init__(self, x, y, font_width, font_height)
		self["x"] = x
		self["y"] = y
		self["font_width"] = font_width
		self["font_height"] = font_height
		self["font_filename"] = font_filename
		self["text"] = text
		self["font_color"] = font_color
		self["font_alpha"] = font_alpha
		self["font_bold"] = bold
		self["font_quality"] = font_quality
		self["font_backup_color"] = font_color
		self["font"] = EwTransformedFont(self["x"], self["y"], self["font_width"], self["font_height"], self["font_filename"], self["text"], self["font_color"], self["font_alpha"], self["font_bold"], self["font_quality"])
	
	def hover(self, target="rect"):
		if EwMouseCol(pygame.mouse.get_pos(), self[target])():
			return True
		if not EwMouseCol(pygame.mouse.get_pos(), self[target])():
			return False
				
	def press(self, mouse_button=LMB1, key=None, target="rect"):
		if EwMouseCol(mpos(), self[target])() and push_mouse(mouse_button):
			return True
		if not EwMouseCol(mpos(), self[target])() and push_mouse(mouse_button):
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
		
class EwSimpleImageButton(EwTextButton, EwImage):
	
	"""
	An EwSimpleImageButton is an EwTextButton with an EwImage.
	"""
	
	def __init__(self, x, y, w, h, filename, font_width, font_height, font_filename, text, font_color, font_alpha=SOLID, bold=False):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		filename <- string
		font_width <- float
		font_height <- float
		font_filename <- string
		text <- string
		font_color <- tuple <- (3 floats from 0 to 255)
		font_alpha <- float from 0 to 255
		bold <- boolean
		"""
		
		EwTextButton.__init__(self, x+font_width/2, y+font_height/2, font_width, font_height, font_filename, text, font_color, font_alpha, bold)
		EwImage.__init__(self, x, y, w, h, filename)
		
class EwRectButton(EwTextButton):
	
	"""
	An EwRectButton is an EwTextButton with an EwRect.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, thickness, font_width, font_height, font_filename, text, font_color, font_alpha, bold=False):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		filename <- string
		font_width <- float
		font_height <- float
		font_filename <- string
		text <- string
		font_color <- tuple <- (3 floats from 0 to 255)
		font_alpha <- float from 0 to 255
		bold <- boolean
		"""
		
		EwTextButton.__init__(self, x+(w/2)-(font_width/2), y+(h/2)-(font_height/2), font_width, font_height, font_filename, text, font_color, font_alpha, bold)
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
			
class EwRectButtonMenu(EwData):
	
	"""
	An EwRectButtonMenu is a sequence of EwRectButtons.
	"""
	
	def __init__(self, x, y, w, height_of_each_button, color, alpha, thickness, buttons):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		height_of_each_button <- int
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		buttons <- list of eight-element lists
		"""
		
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
							raise ErgameError("The given option does not match any button font text.")
			else:
				raise ErgameError("The given int does not represent any mouse button. Please choose a number between 0 and 2.")
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
		
	"""
	An EwSimpleTextMenu is a sequence of EwTextButtons made out of a list of strings.
	"""
		
	def __init__(self, x, y, w, height_of_each_font, filename, color, alpha, strings, font_quality=64):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		height_of_each_font <- int
		filename <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		strings <- list of strings
		font_quality <- int
		"""
		
		EwData.__init__(self)
		self["x"] = x
		self["y"] = y
		self["w"] = w
		self["height_of_each_font"] = height_of_each_font
		self["filename"] = filename
		self["color"] = color
		self["alpha"] = alpha
		self["font_quality"] = font_quality
		if isinstance(strings, list):
			self["strings"] = strings
		else:
			raise NotMemberOfError("list")
		self["buttons"] = [EwTextButton(self["x"],   
				self["y"]+(n*self["height_of_each_font"]), 
				self["w"], 
				self["height_of_each_font"], 
				self["filename"], 
				self["strings"][n], 
				self["color"], 
				self["alpha"],
				False,
				self["font_quality"]) for n in range(len(self["strings"]))]
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
		
	def press(self, mouse_button=LMB1, option=None):
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

# The purpose of these simplifications is to reduce the number of arguments.
# Thus making it easier to have a working menu without too much bureaucracy.

class EwCentralizedSimpleTextMenu(EwData, EwSimpleTextMenu):
	
	"""
	An EwCentralizedSimpleTextMenu is an EwSimpleTextMenu whose position is centered on the screen by default.
	"""
	
	def __init__(self, w, height_of_each_font, filename, color, strings, alpha=SOLID, font_quality=64):
		
		"""
		Input arguments:
		w <- float
		height_of_each_font <- int
		filename <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		strings <- list of strings
		font_quality <- int
		"""
		
		EwData.__init__(self)
		EwSimpleTextMenu.__init__(self, ctx(w), cty(height_of_each_font*len(strings)), w, height_of_each_font, filename, color, alpha, strings, font_quality)
		
class EwSimplestMenu(EwData, EwSimpleTextMenu):
	
	"""
	An EwSimplestMenu is a simple centered menu that requires only two arguments to work.
	"""
	
	def __init__(self, w, strings, filename=None, color=WHITE, alpha=SOLID):
		
		"""
		Input arguments:
		w <- float
		strings <- list of strings
		filename <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		"""
		
		EwData.__init__(self)
		EwSimpleTextMenu.__init__(self, ctx(w), cty((w/4)*len(strings)), w, w/4, filename, color, alpha, strings)
		
class EwCarret(EwObject):
	
	"""
	An EwCarret is an oldschool terminal-looking blinking carret.
	"""
	
	def __init__(self, x, y, w, h, color, alpha, thickness, blinking_delay):
		
		"""
		Input arguments:
		x <- float
		y <- float
		w <- float
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		blinking_delay <- float
		"""
		
		EwObject.__init__(self, x, y, w, h)
		self["blinking_delay"] = blinking_delay
		self["rect"] = EwRect(x, y, w, h, color, alpha, thickness)
		self["counter"] = 0
	
	def move_forwards(self, value):
		self["rect"]["x"] += value
		
	def move_backwards(self, value):
		self["rect"]["x"] -= value
	
	def draw(self, destination_surface=None):
		self["counter"] += 1
		if self["counter"] < self["blinking_delay"]:
			self["rect"].draw(destination_surface)
		elif self["counter"] >= self["blinking_delay"]*2:
			self["counter"] = 0

class EwKeyboardLayout(EwData):

	"""
	An EwKeyboardLayout is an abstract data-holder to represent different keyboard layouts. 
	"""

	def __init__(self, layout=US_LAYOUT):
		
		"""
		Input arguments:
		layout <- int
		"""
		
		EwData.__init__(self)
		self["layout"] = layout
		if self["layout"] == US_LAYOUT:
			self[US_ACUTE] = '`'
			self[US_ACUTE + SPECIAL] = '~'
			self[US_OPEN_BRACKET] = '['
			self[US_OPEN_BRACKET + SPECIAL] = '{'
			self[US_CLOSE_BRACKET] = ']'
			self[US_CLOSE_BRACKET + SPECIAL] = '}'
			self[US_SEMICOLON] = ";"
			self[US_SEMICOLON + SPECIAL] = ":"
			self[US_APOSTROPHE] = "'"
			self[US_APOSTROPHE + SPECIAL] = '"'
			self[US_COMMA] = ','
			self[US_COMMA + SPECIAL] = '<'
			self[US_PERIOD] = '.'
			self[US_PERIOD + SPECIAL] = '>'
			self[US_FORWARD_SLASH] = '/'
			self[US_FORWARD_SLASH + SPECIAL] = '?'
			self[US_BACKSLASH] = '\\'
			self[US_BACKSLASH + SPECIAL] = '|'
		elif self["layout"] == ABNT2_LAYOUT:
			self[ABNT2_APOSTROFO] = "'"
			self[ABNT2_APOSTROFO + SPECIAL] = '"'
			self[ABNT2_AGUDO] = '\xc2'
			self[ABNT2_AGUDO + SPECIAL] = '`'
			self[ABNT2_ABRE_COLCHETE] = '['
			self[ABNT2_ABRE_COLCHETE + SPECIAL] = '{'
			self[ABNT2_FECHA_COLCHETE] = ']'
			self[ABNT2_FECHA_COLCHETE + SPECIAL] = '}'
			self[ABNT2_TIL] = '~'
			self[ABNT2_TIL + SPECIAL] = '^'
			self[ABNT2_CEDILHA] = '\xc3'
			self[ABNT2_VIRGULA] = ','
			self[ABNT2_VIRGULA + SPECIAL] = '<'
			self[ABNT2_PONTO_FINAL] = '.'
			self[ABNT2_PONTO_FINAL + SPECIAL] = '>'
			self[ABNT2_PONTO_E_VIRGULA] = ";"
			self[ABNT2_PONTO_E_VIRGULA + SPECIAL] = ":"
			self[ABNT2_BARRA_INVERTIDA] = '\\'
			self[ABNT2_BARRA_INVERTIDA + SPECIAL] = '|'
			
	def __call__(self):
		return self["layout"]

class EwInput(EwFont):
	
	"""
	An EwInput is a self-updating EwFont with an EwCarret that watches the keyboard input.
	"""
	
	def __init__(self, layout, x, y, size, label="Input: ", filename=None, color=GREEN, alpha=255, bold=False):
		
		"""
		Input arguments:
		layout <- EwKeyboardLayout
		x <- float
		y <- float
		size <- int
		label <- string
		filename <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		bold <- boolean
		"""
		
		EwFont.__init__(self, x, y, size, filename, label, color, alpha, bold)
		if isinstance(layout, EwKeyboardLayout):
			self["layout"] = layout
		else:
			raise ErgameError("The given input for layout is not an instance of the EwKeyboardLayout class")
		self["label"] = label
		self["label_font"] = EwFont(self["x"], self["y"], self["size"], self["filename"], self["label"], self["color"], self["alpha"], self["bold"])
		self["single_char_font"] = EwFont(self["x"], self["y"], self["size"], self["filename"], self["label"][0], self["color"], self["alpha"], self["bold"])
		self["label_distance"] = self["label_font"]["w"]
		self["carret"] = EwCarret(self["x"]+self["label_distance"], self["y"], CARRET_SIZE, self["h"], addrgb(self["color"], (125, 125, 125)), self["alpha"]/2, FILLED, CARRET_BLINKING_DELAY)
		self["charset_imposed"] = False
		self["spacebar_disabled"] = False

	def get_value(self):
		return self["text"].split(self["label"])[-1]

	def split_from_label(self):
		split = self["text"].split(self["label"])[-1]
		listed_split = list(split)
		if listed_split != EMPTY:
			return listed_split

	def generate_booleans(self):
		if len(self.split_from_label()) != EMPTY:
			self["selection_model"] = EwSelectionModel(self.split_from_label(), LAST)
		else:
			self["selection_model"] = None
		
	def get_booleans(self):
		try:
			booleans = self["selection_model"]["booleans"]
			return booleans
		except (KeyError, TypeError):
			pass

	def get_carret_pos(self):
		if self.get_booleans() is not None:
			for boolean in self.get_booleans():
				if boolean is True:
					self["index"] = self.get_booleans().index(boolean)
		try:
			self["selection_model"].force_single_selection(self["index"])
		except (UnboundLocalError, KeyError, AttributeError):
			self["index"] = len(self["text"])
		lenbel = len(self["label"])
		carret_pos_text = self["text"][0:(lenbel+self["index"])+1]
		temp_font = EwFont(self["x"], self["y"], self["size"], self["filename"], carret_pos_text, self["color"], self["alpha"], self["bold"])
		self["w"] = temp_font["w"]
		return temp_font["x"] + self["w"]

	def add_code(self, c): 
		self.update(self["text"] + pygame.key.name(c))
		self.generate_booleans()
		
	def add_string(self, s): 
		self.update(self["text"] + s)
		self.generate_booleans()
	
	def impose_charset(self, charset):
		self["charset_imposed"] = True
		if isinstance(charset, list):
			self["charset"] = charset
		else:
			raise ErgameError("The given charset input is not a list.")
	
	def disable_spacebar(self):
		self["spacebar_disabled"] = True
	
	def update_message(self):
		if not self["charset_imposed"]:
			for e in EwData.app.events:
				if e.type == pygame.KEYDOWN:
					
					if e.key in UPPER_NUMBERS:
						self.add_code(e.key)
					if e.key in LETTERS:
						if get_capslock_state() or press_shift():
							self.add_string(pygame.key.name(e.key).upper())
						else:
							self.add_string(pygame.key.name(e.key).lower())
					if get_numlock_state():
						if e.key in KP_NUMBERS:
							self.add_string(pygame.key.name(e.key).replace('[', '').replace(']', ''))
							
					# Keyboard Layouts:
					
					def special(n):
						if e.key == n:
							if not press_shift():
								self.add_string(self["layout"][n])
							else:
								self.add_string(self["layout"][n + SPECIAL])
					def special_number(n, c):
						if e.key == n:
							if not press_shift():
								pass
							else:
								self.update(self["text"][:len(self["text"])-1] + c)

					special_number(pygame.K_1, '!')
					special_number(pygame.K_2, '@')
					special_number(pygame.K_3, '#')
					special_number(pygame.K_4, '$')
					special_number(pygame.K_5, '%')
					special_number(pygame.K_7, '&')
					special_number(pygame.K_8, '*')
					special_number(pygame.K_9, '(')
					special_number(pygame.K_0, ')')
					
					if e.key == pygame.K_MINUS:
						if not press_shift():
							self.add_code(e.key)
						else:
							self.add_string('_')
					if e.key == pygame.K_EQUALS:
						if not press_shift():
							self.add_code(e.key)
						else:
							self.add_string('+')
					
					if self["layout"]() == US_LAYOUT:
						special(US_ACUTE)
						special(US_OPEN_BRACKET)
						special(US_CLOSE_BRACKET)
						special(US_SEMICOLON)
						special(US_APOSTROPHE)
						special(US_COMMA)
						special(US_PERIOD)
						special(US_FORWARD_SLASH)
						special(US_BACKSLASH)
						special_number(pygame.K_6, '^')
					elif self["layout"]() == ABNT2_LAYOUT:
						special(ABNT2_APOSTROFO)
						special(ABNT2_AGUDO)
						special(ABNT2_ABRE_COLCHETE)
						special(ABNT2_FECHA_COLCHETE)
						special(ABNT2_TIL)
						special(ABNT2_CEDILHA)
						special(ABNT2_VIRGULA)
						special(ABNT2_PONTO_FINAL)
						special(ABNT2_PONTO_E_VIRGULA)
						special(ABNT2_BARRA_INVERTIDA)
					if not self["spacebar_disabled"]:
						if e.key == pygame.K_SPACE:
							self.update(self["text"] + " ")
							self["carret"].move_forwards(EwFont(self["x"], self["y"], self["size"], self["filename"], " ", self["color"], self["alpha"], self["bold"])["w"])
							self.generate_booleans()	
		else:
			for e in EwData.app.events:
				if e.type == pygame.KEYDOWN:
					if e.key in self["charset"]:
						if e.key in UPPER_NUMBERS:
							self.add_code(e.key)
						elif e.key in LETTERS:
							if get_capslock_state() or press_shift():
								self.add_string(pygame.key.name(e.key).upper())
							else:
								self.add_string(pygame.key.name(e.key).lower())
						elif get_numlock_state():
							if e.key in KP_NUMBERS:
								self.add_string(pygame.key.name(e.key).replace('[', '').replace(']', ''))
						else:
							self.add_code(e.key)
					if not self["spacebar_disabled"]:
						if e.key == pygame.K_SPACE:
							self.update(self["text"] + " ")
							self["carret"].move_forwards(EwFont(self["x"], self["y"], self["size"], self["filename"], " ", self["color"], self["alpha"], self["bold"])["w"])
							self.generate_booleans()	
							
		if press_backspace():
			if self["text"] != self["label"]:
				try:
					self.update(self["text"][:len(self["text"])-1])
					self.generate_booleans()
				except IndexError:
					pass
		if press_delete():
			self.update(self["label"])
			self["carret"]["rect"]["x"] = self["x"]+self["label_distance"]
	
	def draw(self, destination_surface=None):
		self.watch_for_focus()
		if destination_surface is None:
			EwData.app["screen"].blit(self["surface"], (self["x"], self["y"]))
		else:
			destination_surface.blit(self["surface"], (self["x"], self["y"]))
		if self.focused():
			self["carret"].draw(destination_surface)
			self.update_message()
		try:
			self["selection_model"].select(press_right(), press_left(), INPUT_SELECTION_DELAY)
		except (AttributeError, KeyError):
			pass
		self["carret"]["rect"]["x"] = self.get_carret_pos()
	
class EwValueChooser(EwObject):
	
	"""
	An EwValueChooser is an EwObject that assembles EwRects into a resulting graphical value chooser out of a list of python objects.
	"""
	
	def __init__(self, x, y, values, h, color, alpha, thickness, value_rect_color, value_rect_alpha, value_rect_thickness, font_filename, font_color, font_alpha, bold=False, font_quality=64):

		"""
		Input arguments:
		x <- float
		y <- float
		values <- list of python objects
		h <- float
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		thickness <- int
		value_rect_color <- tuple <- (3 floats from 0 to 255)
		value_rect_alpha <- float from 0 to 255
		value_rect_thickness <- int
		font_filename <- string
		font_color <- tuple <- (3 floats from 0 to 255)
		font_alpha <- float from 0 to 255
		bold <- boolean
		font_quality <- int
		"""

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
		self["font_quality"] = font_quality
		self["rect"] = EwRect(self["x"], self["y"], self["w"], self["h"], self["color"], self["alpha"], self["thickness"])
		self["value_positions"] = [self["rect"]["x"] + n for n in range(0, self["rect"]["w"], self["rect"]["w"]/len(self["values"]))]
		self["inner_rects"] = [EwRect(pos, self["y"], self["w"]/len(self["values"]), self["h"], self["value_rect_color"], self["value_rect_alpha"], 6) for pos in self["value_positions"]]
		self["value_rect"] = EwRect(self["x"], self["y"], self["w"]/len(self["values"]), self["h"], self["value_rect_color"], self["value_rect_alpha"], self["value_rect_thickness"])
		self["selection_model"] = EwSelectionModel(self["values"])
		self["value"] = self["values"][0]
		self["font"] = EwTransformedFont(self["x"], self["y"]-self["h"], self["w"], self["h"], self["font_filename"], self["value"], self["font_color"], self["font_alpha"], self["bold"], self["font_quality"])
	
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
		
class EwTextBox(EwObject):
	
	"""
	An EwTextBox is an EwObject that creates EwFonts by spliting a given string by '\n' escape characters.
	"""
	
	def __init__(self, x, y, text, font_size=32, filename=None, color=WHITE, alpha=SOLID, bold=False, rect_color=(100, 100, 100), rect_alpha=125, rect_thickness=0):
		
		"""
		Input arguments:
		x <- float
		y <- float
		text <- string
		font_size <- int
		filename <- string
		color <- tuple <- (3 floats from 0 to 255)
		alpha <- float from 0 to 255
		bold <- boolean
		rect_color <- tuple <- (3 floats from 0 to 255)
		rect_alpha <- float from 0 to 255
		rect_thickness <- int
		"""
		
		EwObject.__init__(self, x, y, 1, 1)
		self["font_size"] = font_size
		self["filename"] = filename
		self["color"] = color
		self["alpha"] = alpha
		self["bold"] = bold
		self["rect_color"] = rect_color
		self["rect_alpha"] = rect_alpha
		self["rect_thickness"] = rect_thickness
		if isinstance(text, basestring):
			self.update_text(text)
		else:
			raise NotMemberOfError("basestring")
	
	def update_text(self, text):
		self["text"] = text
		self["split_text"] = self["text"].split('\n')
		self.generate_fonts()
	
	def generate_fonts(self):
		temp_base_font = EwFont(0, 0, self["font_size"], self["filename"], "Irrelevant String", self["color"], self["alpha"], self["bold"])
		self["fonts"] = [EwFont(self["x"], self["y"]+(temp_base_font["h"]*n), self["font_size"], self["filename"], self["split_text"][n], self["color"], self["alpha"], self["bold"]) for n in range(len(self["split_text"]))]
		temp_base_font = EwFont(0, 0, self["font_size"], self["filename"], [s for s in self["split_text"] if len(s) == max([len(sn) for sn in self["split_text"]])][0], self["color"], self["alpha"], self["bold"])
		self["rect_panel"] = EwRectPanel(self["x"]-self["font_size"], self["y"]-self["font_size"], temp_base_font["w"]+(self["font_size"]*2), temp_base_font["h"]*len(self["split_text"])+(self["font_size"]*2), self["rect_color"], self["rect_alpha"], self["rect_thickness"])
		
	def draw(self, destination_surface=None):
		self["rect_panel"].draw(destination_surface)
		[f.draw(destination_surface) for f in self["fonts"]]
