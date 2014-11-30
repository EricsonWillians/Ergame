"""
====================================================================

ESNAKE

Written with Ergame.
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
Game and Engine written by Ericson Willians, a brazilian composer and programmer.

CONTACT: ericsonwrp@gmail.com
AS A COMPOSER: http://www.youtube.com/user/poisonewein
TWITTER: https://twitter.com/poisonewein

====================================================================
"""

import os, sys
import pygame
from random import randrange

from ercrash import *
from erbase import *
from erdat import *
from erfunc import *
from erxec import *
from ergui import *
from erproc import *

if __name__ == "__main__":

	r = EwData() # Raw

	r["FPS"] = 40
	r["FONT"] = "Squares Bold Free.otf"
	r["Screen Width"] = 1024
	r["Screen Height"] = 768
	r["Fullscreen"] = True
	r["Delay Between Screens"] = 25
	r["Menu Selection Delay"] = 500

	r["Options File"] = EwData()
	r["Colors File"] = EwData()

	if check_file(DEFAULT_OPTIONS_PATH):
		r["Options File"].load(DEFAULT_OPTIONS_PATH)
		r["Screen Width"] = int(r["Options File"]["Resolution"].split('x')[0])
		r["Screen Height"] = int(r["Options File"]["Resolution"].split('x')[1])
		if r["Options File"]["Font Quality"] == "Very Low":
			r["Font Quality"] = 8
		elif r["Options File"]["Font Quality"] == "Low":
			r["Font Quality"] = 16
		elif r["Options File"]["Font Quality"] == "Medium":
			r["Font Quality"] = 32
		elif r["Options File"]["Font Quality"] == "High":
			r["Font Quality"] = 64
		elif r["Options File"]["Font Quality"] == "Very High":
			r["Font Quality"] = 128
		elif r["Options File"]["Font Quality"] == "Perfect":
			r["Font Quality"] = 224
		app = EwApp("Esnake", r["Screen Width"], r["Screen Height"], r["FPS"], r["Fullscreen"])
		EwMusic.set_volume(r["Options File"]["Music Volume"])
	else:
		r["Font Quality"] = 16
		app = EwApp("Esnake", r["Screen Width"], r["Screen Height"], r["FPS"], r["Fullscreen"])
	EwMusic("Esnake Theme.mid")
	EwMusic.play()

	r["Background Scrolling Speed"] = 6
	r["Background Scrolling Speed Increment"] = 0.2
	r["Background"] = EwScrollingImage(0, 0, r["Screen Width"], r["Screen Height"], "bg.jpg", 75, NORTH, r["Background Scrolling Speed"])
	r["Background Rect"] = EwRect(0, 0, r["Screen Width"], r["Screen Height"], (50, 0, 0), 75, 0)
	r["Error Counter"] = 0
	r["End Message"] = ""
	r["Font Color"] = (25, 125, 25)
	r["Font Highlight Color"] = (25, 200, 25)
	r["Scenes"] = EwData()
	r["Main Menu"] = EwCentralizedSimpleTextMenu(192, 64, r["FONT"], r["Font Color"], ["Start Game", "Options", "Highscore", "Exit Game"], 255, r["Font Quality"])
	r["Modes Menu"] = EwCentralizedSimpleTextMenu(192, 64, r["FONT"], r["Font Color"], ["Classic", "Mazy", "Field", "Lengthy"], 255, r["Font Quality"])
	r["Mazy Menu"] = EwCentralizedSimpleTextMenu(r["Screen Width"]/2, 64, r["FONT"], r["Font Color"], ["Float Randrange", "Float Threshold", "Wall Length"], 255, r["Font Quality"])
	r["Digestion Menu"] = EwCentralizedSimpleTextMenu(192, 64, r["FONT"], r["Font Color"], ["Normal", "Random", "Spawn"], 255, r["Font Quality"])
	r["Options Menu"] = EwCentralizedSimpleTextMenu(192, 32, r["FONT"], r["Font Color"], ["Resolution", "Font Quality", "Fullscreen", "Game Speed", "Game Size", "Music Volume", "Score Counter", "Game Grid", "", "", "", "Return"], 255, r["Font Quality"])
	r["Game Mode"] = None
	r["Options From"] = None
	r["Pause Menu"] = EwCentralizedSimpleTextMenu(192, 64, r["FONT"], r["Font Color"], ["Resume Game", "New Game", "Options", "Highscore", "Exit Game"], 255, r["Font Quality"])
	r["Game Speed"] = 40
	r["Score"] = 0
	r["Digestion"] = 0
	r["Mazy Score"] = 0
	r["Mazy Float Randrange"] = 1.9
	r["Mazy Float Threshold"] = 0.5
	r["Mazy Wall Length"] = 8
	r["Mazy Safety Factor"] = 3
	r["Field Score"] = 0
	r["Field Levels Cleared"] = 0
	r["Locomotion Score"] = 0
	r["Lengthy Score"] = 0
	r["Highscore File"] = EwData()
	if check_file(DEFAULT_HIGHSCORE_PATH):
		r["Highscore File"].load(DEFAULT_HIGHSCORE_PATH)
		r["Highscore"] = r["Highscore File"]["Highscore"]
	else:
		r["Highscore"] = {"Classic": {"Normal Digestion": 0, "Random Digestion": 0}, "Field": {"Normal Digestion": {"Food Score": 0, "Field Score": 0, "Field Levels Cleared": 0}, "Random Digestion": {"Food Score": 0, "Field Score": 0, "Field Levels Cleared": 0}}, "Mazy": {"Normal Digestion": {"Score": 0, "Maze CFG": [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]}, "Random Digestion": {"Score": 0, "Maze CFG": [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]}}, "Lengthy": {"Score": 0, "Locomotion Score": 0, "Maze CFG": [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]}}
		
	r["Highscore From"] = None
	r["Highscore List"] = []
	if check_file(DEFAULT_OPTIONS_PATH):
		r["Options File"].load(DEFAULT_OPTIONS_PATH)
		r["Element Size"] = r["Options File"]["Game Size"]
	else:
		r["Element Size"] = 12
	r["Element Alpha"] = 255
	r["Element Thickness"] = 0
	
	r["Grid Color"] = (0, 25, 0)
	r["Grid Alpha"] = 200
	r["Grid Thickness"] = 1
	r["Grid"] = EwGrid(0, 0, r["Screen Width"], r["Screen Height"], r["Grid Color"], r["Grid Alpha"], r["Grid Thickness"], r["Element Size"], r["Element Size"])
	
	r["Snake"] = EwData()
	r["Snake"]["Color"] = GREEN
	r["Snake"]["Digestive Color"] = addrgb(GREEN, (0, 125, 0))
	r["Snake"]["Length"] =[[int((r["Screen Width"]/r["Element Size"])/2), int((r["Screen Width"]/r["Element Size"])/2)], [int((r["Screen Width"]/r["Element Size"])/2), int((r["Screen Width"]/r["Element Size"])/2)], [int((r["Screen Width"]/r["Element Size"])/2), int((r["Screen Width"]/r["Element Size"])/2)]]
	r["Snake"]["Directions"] = [NORTH, SOUTH, WEST, EAST]
	r["Snake"]["Present Direction"] = r["Snake"]["Directions"][0]
	r["Snake"]["Digestion Part"] = 0
	
	r["Food"] = EwData()
	r["Food"]["Color"] = SILVER
	try:
		r["Food"]["Rect"] = EwRect(r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"]))), 
			r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"]))),
			r["Element Size"],
			r["Element Size"],
			r["Food"]["Color"],
			r["Element Alpha"],
			r["Element Thickness"])
	except ValueError:
		raise ErgameError("The engine has tried to spawn food off-limits. You've probably saved a game size number greater than the screen, which means that each individual cell is greater than the screen itself (Causing countless index-related errors, the first one being related to the food spawn). In this case, since you're not going to be able to run the game, just erase the 'options.edt' file in the game folder, or edit the game size in the file manually to a value smaller than the screen size.")

	r["Maze"] = None
	r["Warper Square-Sign"] = EwRect(-2, -1, r["Screen Width"], r["Screen Height"], YELLOW, 125, 4)

	r["Field Randrange"] = 20
	r["Field Threshold"] = 0.2
	r["Field"] = EwRectField(0, 0, r["Screen Width"], r["Screen Height"], RED, 255, 0, r["Element Size"], r["Element Size"], r["Field Randrange"], r["Field Threshold"]) 

	r["Exit"] = EwData()
	r["Exit"]["Color"] = addrgb(TEAL, (75, 75, 75))
	r["Exit"]["Rect"] = EwRect(r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"]))), 
				r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"]))),
				r["Element Size"],
				r["Element Size"],
				r["Exit"]["Color"],
				r["Element Alpha"],
				r["Element Thickness"])
	r["Food"]["Taken"] = False

	# Value Choosers:

	r["Resolution Value Chooser"] = EwValueChooser(
		ctx(44*3.5), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["800x600", "800x800", "1024x768", "1280x800", "1360x768", "1600x1050", "1680x1040"], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])

	r["Font Quality Value Chooser"] = EwValueChooser(
		ctx(44*3), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["Very Low", "Low", "Medium", "High", "Very High", "Perfect"], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])

	r["Fullscreen Value Chooser"] = EwValueChooser(
		ctx(44), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["ON", "OFF"], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])

	r["Game Speed Value Chooser"] = EwValueChooser(
		ctx(44*5), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["Huge Cells", "Lame", "Slow","Classic", "Just a bit", "Nice", "Pro", "Sick", "Retarded", "You'll die."], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])

	r["Music Volume Value Chooser"] = EwValueChooser(
		ctx(44*3), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		[1, 0.8, 0.6, 0.4, 0.2, 0], 
		44, 
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])

	r["Score Counter Value Chooser"] = EwValueChooser(
		ctx(44*2), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["Decimal", "Binary", "Hex", "Octal"], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"],
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])
		
	r["Grid Value Chooser"] = EwValueChooser(
		ctx(44), 
		r["Options Menu"]["y"]-r["Screen Height"]/8, 
		["ON", "OFF"], 
		44,  
		r["Grid Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["Font Highlight Color"], 
		r["Element Alpha"], 
		r["Element Thickness"], 
		r["FONT"],
		SILVER,
		r["Element Alpha"],
		False,
		r["Font Quality"])
	
	# Inputs:
		
	r["Game Size Input"] = EwInput(EwKeyboardLayout(US_LAYOUT), ctx(r["Options Menu"]["w"]), r["Options Menu"]["y"]-r["Screen Height"]/8, 32, "N: ", r["FONT"], SILVER)
	r["Game Size Input"].impose_charset(NUMBERS)
	r["Game Size Input"].disable_spacebar()

	# Option Loading:

	if check_file(DEFAULT_OPTIONS_PATH):
		r["Options File"].load(DEFAULT_OPTIONS_PATH)
		print "The following options were loaded:"
		[sys.stdout.write(str(opt[0]) + ": " + str(opt[1]) + "\n") for opt in r["Options File"].data.items()]
		r["Resolution Value Chooser"].set_selected(r["Options File"]["Resolution"])
		r["Font Quality Value Chooser"].set_selected(r["Options File"]["Font Quality"])
		r["Fullscreen Value Chooser"].set_selected(r["Options File"]["Fullscreen"])
		r["Screen Width"] = int(r["Options File"]["Resolution"].split('x')[0])
		r["Screen Height"] = int(r["Options File"]["Resolution"].split('x')[1])
		if r["Fullscreen"] == True:
			r["screen"] = pygame.display.set_mode((r["Screen Width"], r["Screen Height"]), pygame.DOUBLEBUF | pygame.FULLSCREEN)
		else:
			r["screen"] = pygame.display.set_mode((r["Screen Width"], r["Screen Height"]), pygame.DOUBLEBUF)
		r["Game Speed Value Chooser"].set_selected(r["Options File"]["Game Speed"])
		r["Music Volume Value Chooser"].set_selected(r["Options File"]["Music Volume"])
		pygame.mixer.music.set_volume(r["Music Volume Value Chooser"]["value"])
		r["Score Counter Value Chooser"].set_selected(r["Options File"]["Score Counter"])
		r["Grid Value Chooser"].set_selected(r["Options File"]["Grid"])
	else:
		r["Resolution Value Chooser"].set_selected("1024x768")
		r["Font Quality Value Chooser"].set_selected("Low")
		r["Game Speed Value Chooser"].set_selected("Nice")
		r["Music Volume Value Chooser"].set_selected(1)
		pygame.mixer.music.set_volume(r["Music Volume Value Chooser"]["value"])
	
	# Procedures:
					
	def return_random_gridpos_while_watching_for_maze_wall_presence():
		rx = randrange(0, int(r["Screen Width"]/r["Element Size"]))
		ry = randrange(0, int(r["Screen Height"]/r["Element Size"]))
		for horizontal_wall in r["Maze"]["horizontal_maze"]["walls"]:
			for horizontal_rect in horizontal_wall["rects"]:
				for vertical_wall in r["Maze"]["vertical_maze"]["walls"]:
					for vertical_rect in vertical_wall["rects"]:
						if (r["Grid"].get_row_pos(rx) != horizontal_rect["x"] and r["Grid"].get_row_pos(ry) != horizontal_rect["y"]) and (r["Grid"].get_row_pos(rx) != vertical_rect["x"] and r["Grid"].get_row_pos(ry) != vertical_rect["y"]):
							return [rx, ry]
						elif (r["Grid"].get_row_pos(rx) == horizontal_rect["x"] and r["Grid"].get_row_pos(ry) == horizontal_rect["y"]) or (r["Grid"].get_row_pos(rx) == vertical_rect["x"] and r["Grid"].get_row_pos(ry) == vertical_rect["y"]):
							return_random_gridpos_while_watching_for_maze_wall_presence()
							
	def respawn_food(): # For mazy modes.
		food_pos = return_random_gridpos_while_watching_for_maze_wall_presence()
		r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(food_pos[0])
		r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(food_pos[1])
		for horizontal_wall in r["Maze"]["horizontal_maze"]["walls"]:
			for horizontal_rect in horizontal_wall["rects"]:
				if col(r["Food"]["Rect"], horizontal_rect):
						respawn_food()
		for vertical_wall in r["Maze"]["vertical_maze"]["walls"]:
			for vertical_rect in vertical_wall["rects"]:
				if col(r["Food"]["Rect"], vertical_rect):
						respawn_food()
						
	def reset_exit(): # For mazy modes.
		exit_pos = return_random_gridpos_while_watching_for_maze_wall_presence()
		r["Exit"]["Rect"]["x"] = r["Grid"].get_row_pos(exit_pos[0])
		r["Exit"]["Rect"]["y"] = r["Grid"].get_column_pos(exit_pos[1])
		for horizontal_wall in r["Maze"]["horizontal_maze"]["walls"]:
			for horizontal_rect in horizontal_wall["rects"]:
				if col(r["Exit"]["Rect"], horizontal_rect):
						reset_exit()
		for vertical_wall in r["Maze"]["vertical_maze"]["walls"]:
			for vertical_rect in vertical_wall["rects"]:
				if col(r["Exit"]["Rect"], vertical_rect):
						reset_exit()

	def fill_highscore_list():
		def recdict(_dict):
			for key in _dict.keys():
				if isinstance(_dict[key], dict):
					r["Highscore List"].append(str(key) + str((lambda: " Mode >\n" if not ("Normal" and "Digestion") in str(key) else ":\n")()))
					recdict(_dict[key])
				else:
					r["Highscore List"].append(">>> " + str(key) + ": " + str(_dict[key]) + "\n")
		recdict(r["Highscore"])

	def update_highscore_list():
		r["Highscore List"] = []
		fill_highscore_list()

	def draw_main_score(var):
		w = r["Screen Width"]-16
		h =  r["Screen Height"]-16
		x = 16
		y = 16
		if r["Score Counter Value Chooser"]["value"] == "Decimal":
			EwTransformedFont(x, y, w, h, r["FONT"],  str(var), (0, 25, 0), 255, False, r["Font Quality"]).draw()
		elif r["Score Counter Value Chooser"]["value"] == "Binary":
			EwTransformedFont(x, y, w, h, r["FONT"],  str(bin(var))[2:], (0, 25, 0), 255, False, r["Font Quality"]).draw()
		elif r["Score Counter Value Chooser"]["value"] == "Hex":
			EwTransformedFont(x, y, w, h, r["FONT"],  str(hex(var))[2:], (0, 25, 0), 255, False, r["Font Quality"]).draw()
		elif r["Score Counter Value Chooser"]["value"] == "Octal":
			EwTransformedFont(x, y, w, h, r["FONT"],  oct(var), (0, 25, 0), 255, False, r["Font Quality"]).draw()

	def save_highscore():
		if check_file(DEFAULT_HIGHSCORE_PATH):
			if r["Game Mode"] == "Classic":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore File"]["Highscore"]["Classic"]["Normal Digestion"]:
						r["Highscore"]["Classic"]["Normal Digestion"] = r["Score"]
						print ">> New highscore saved for classic game mode with normal digestion: " + str(r["Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore File"]["Highscore"]["Classic"]["Random Digestion"]:
						r["Highscore"]["Classic"]["Random Digestion"] = r["Score"]
						print ">> New highscore saved for classic game mode with random digestion: " + str(r["Score"]) + "."
			elif r["Game Mode"] == "Mazy":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore File"]["Highscore"]["Mazy"]["Normal Digestion"]["Score"]:
						r["Highscore"]["Mazy"]["Normal Digestion"]["Score"] = r["Score"]
						r["Highscore"]["Mazy"]["Normal Digestion"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
						print ">> New highscore saved for mazy game mode with normal digestion: " + str(r["Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore File"]["Highscore"]["Mazy"]["Random Digestion"]["Score"]:
						r["Highscore"]["Mazy"]["Random Digestion"]["Score"] = r["Score"]
						r["Highscore"]["Mazy"]["Random Digestion"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
						print ">> New highscore saved for mazy game mode with normal digestion: " + str(r["Score"]) + "."
			elif r["Game Mode"] == "Field":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore File"]["Highscore"]["Field"]["Normal Digestion"]["Food Score"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Food Score"] = r["Score"]
						print ">> New food highscore saved for field game mode with normal digestion: " + str(r["Score"]) + "."
					if r["Field Score"] > r["Highscore File"]["Highscore"]["Field"]["Normal Digestion"]["Field Score"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Field Score"] = r["Field Score"]
						print "New field highscore saved for field game mode with normal digestion: " + str(r["Field Score"]) + "."
					if r["Field Levels Cleared"] > r["Highscore File"]["Highscore"]["Field"]["Normal Digestion"]["Field Levels Cleared"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Field Levels Cleared"] = r["Field Levels Cleared"]
						print ">> New highscore number saved for the number of levels cleared in the field game mode with normal digestion: " + str(r["Field Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore File"]["Highscore"]["Field"]["Random Digestion"]["Food Score"]:
						r["Highscore"]["Field"]["Random Digestion"]["Food Score"] = r["Score"]
						print ">> New random digestion food highscore saved for field game mode: " + str(r["Score"]) + "."
					if r["Field Score"] > r["Highscore File"]["Highscore"]["Field"]["Random Digestion"]["Field Score"]:
						r["Highscore"]["Field"]["Random Digestion"]["Field Score"] = r["Field Score"]
						print ">> New random digestion field highscore saved for field game mode: " + str(r["Field Score"]) + "."
					if r["Field Levels Cleared"] > r["Highscore File"]["Highscore"]["Field"]["Random Digestion"]["Field Levels Cleared"]:
						r["Highscore"]["Field"]["Random Digestion"]["Field Levels Cleared"] = r["Field Levels Cleared"]
						print ">> New highscore number saved for the number of levels cleared in the field game mode with random digestion: " + str(r["Field Score"]) + "."
			elif r["Game Mode"] == "Lengthy":
				if r["Lengthy Score"] > r["Highscore File"]["Highscore"]["Lengthy"]["Score"]:
					r["Highscore File"]["Highscore"]["Lengthy"]["Score"] = r["Lengthy Score"]
					r["Highscore File"]["Highscore"]["Lengthy"]["Locomotion Score"] = r["Locomotion Score"]
					r["Highscore File"]["Highscore"]["Lengthy"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
					print ">> New highscore saved for lengthy game mode: " + str(r["Lengthy Score"]) + "."
			r["Highscore File"]["Highscore"] = r["Highscore"]
			r["Highscore File"].write(DEFAULT_HIGHSCORE_PATH)
		else:
			if r["Game Mode"] == "Classic":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore"]["Classic"]["Normal Digestion"]:
						r["Highscore"]["Classic"]["Normal Digestion"] = r["Score"]
						print ">> New normal digestion highscore saved for classic game mode: " + str(r["Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore"]["Classic"]["Random Digestion"]:
						r["Highscore"]["Classic"]["Random Digestion"] = r["Score"]
						print ">> New random digestion highscore saved for classic game mode: " + str(r["Score"]) + "."
			elif r["Game Mode"] == "Mazy":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore"]["Mazy"]["Normal Digestion"]["Score"]:
						r["Highscore"]["Mazy"]["Normal Digestion"]["Score"] = r["Score"]
						r["Highscore"]["Mazy"]["Normal Digestion"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
						print ">> New highscore saved for mazy game mode with normal digestion: " + str(r["Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore"]["Mazy"]["Random Digestion"]["Score"]:
						r["Highscore"]["Mazy"]["Random Digestion"]["Score"] = r["Score"]
						r["Highscore"]["Mazy"]["Random Digestion"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
						print ">> New highscore saved for mazy game mode with normal digestion: " + str(r["Score"]) + "."
			elif r["Game Mode"] == "Field":
				if r["Digestion"] == 0:
					if r["Score"] > r["Highscore"]["Field"]["Normal Digestion"]["Food Score"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Food Score"] = r["Score"]
						print ">> New normal digestion food highscore saved for field game mode: " + str(r["Score"]) + "."
					if r["Field Score"] > r["Highscore"]["Field"]["Normal Digestion"]["Field Score"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Field Score"] = r["Field Score"]
						print ">> New normal digestion field highscore saved for field game mode: " + str(r["Field Score"]) + "."
					if r["Field Levels Cleared"] > r["Highscore"]["Field"]["Normal Digestion"]["Field Levels Cleared"]:
						r["Highscore"]["Field"]["Normal Digestion"]["Field Levels Cleared"] = r["Field Levels Cleared"]
						print ">> New highscore number saved for the number of levels cleared in the field game mode with normal digestion: " + str(r["Field Score"]) + "."
				elif r["Digestion"] == 1:
					if r["Score"] > r["Highscore"]["Field"]["Random Digestion"]["Food Score"]:
						r["Highscore"]["Field"]["Random Digestion"]["Food Score"] = r["Score"]
						print ">> New random digestion food highscore saved for field game mode: " + str(r["Score"]) + "."
					if r["Field Score"] > r["Highscore"]["Field"]["Random Digestion"]["Field Score"]:
						r["Highscore"]["Field"]["Random Digestion"]["Field Score"] = r["Field Score"]
						print ">> New random digestion field highscore saved for field game mode: " + str(r["Field Score"]) + "."
					if r["Field Levels Cleared"] > r["Highscore"]["Field"]["Random Digestion"]["Field Levels Cleared"]:
						r["Highscore"]["Field"]["Random Digestion"]["Field Levels Cleared"] = r["Field Levels Cleared"]
						print ">> New highscore number saved for the number of levels cleared in the field game mode with random digestion: " + str(r["Field Score"]) + "."
			elif r["Game Mode"] == "Lengthy":
				if r["Lengthy Score"] > r["Highscore"]["Lengthy"]["Score"]:
					r["Highscore"]["Lengthy"]["Score"] = r["Lengthy Score"]
					r["Highscore"]["Lengthy"]["Locomotion Score"] = r["Locomotion Score"]
					r["Highscore"]["Lengthy"]["Maze CFG"] = [r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"]]
					print ">> New highscore saved for lengthy game mode: " + str(r["Lengthy Score"]) + "."
			r["Highscore File"]["Highscore"] = r["Highscore"]
			r["Highscore File"].write(DEFAULT_HIGHSCORE_PATH)
		
		update_highscore_list()
		
	r["Highscore Text Box"] = EwTextBox(64, 64, ''.join(r["Highscore List"]), r["Screen Width"]/48, r["FONT"], r["Font Color"], 255, False, subrgb(r["Font Color"], (0, 125, 0)), BARELY_VISIBLE, 6)

	def default():
		save_highscore()
		
		r["Background"].reset_scroll_speed()
		r["Score"] = 0
		r["Field Score"] = 0
		r["Field Levels Cleared"] = 0

		if r["Game Mode"] == "Mazy":
			r["Maze"] = EwSafeRectWallMaze(0, 0, r["Screen Width"], r["Screen Height"], r["Element Size"], r["Element Size"], r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"], r["Mazy Safety Factor"], RED, 75, r["Element Thickness"])
			respawn_food()
			try:
				snake_pos = return_random_gridpos_while_watching_for_maze_wall_presence()
				r["Snake"]["Length"] = [[snake_pos[0], snake_pos[1]], [snake_pos[0], snake_pos[1]]]
			except TypeError:
				print "Obscure snake-maze-related error captured."
				default()
		elif r["Game Mode"] == "Lengthy":
			r["Maze"] = EwSafeRectWallMaze(0, 0, r["Screen Width"], r["Screen Height"], r["Element Size"], r["Element Size"], r["Mazy Float Randrange"], r["Mazy Float Threshold"], r["Mazy Wall Length"], r["Mazy Safety Factor"], RED, 75, r["Element Thickness"])
			respawn_food()
			reset_exit()
			r["Food"]["Taken"] = False
			try:
				snake_pos = return_random_gridpos_while_watching_for_maze_wall_presence()
				r["Snake"]["Length"] = [[snake_pos[0], snake_pos[1]], [snake_pos[0], snake_pos[1]]]
			except TypeError:
				print "Obscure snake-maze-related error captured."
				default()
		else:
			r["Snake"]["Length"] =[[int((r["Screen Width"]/r["Element Size"])/2), int((r["Screen Width"]/r["Element Size"])/2)],[int((r["Screen Width"]/r["Element Size"])/2), int((r["Screen Width"]/r["Element Size"])/2)]]
			r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
			r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
			r["Field"] = EwRectField(0, 0, r["Screen Width"], r["Screen Height"], subrgb(RED, (75, 0, 0)), 255, 0, r["Element Size"], r["Element Size"], r["Field Randrange"], r["Field Threshold"]) 
		r["Snake"]["Next"] = r["Snake"]["Length"][0]
		
	# Game Modes:
	
	def give_classic_life(): 
		
		try:
			r["Snake"]["Next"] = r["Snake"]["Length"][0]
		except IndexError:
			default()
			r["Error Counter"] += 1
			if r["Error Counter"] == 1:
				print "Obscure recursive deletion error captured 1 time."
			else:
				print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
				r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		r["Snake"]["Rects"] = [EwRect(r["Grid"].get_row_pos(r["Snake"]["Length"][sp][0]),
			r["Grid"].get_column_pos(r["Snake"]["Length"][sp][1]), 
			r["Element Size"], 
			r["Element Size"], 
			r["Snake"]["Color"],
			r["Element Alpha"], 
			r["Element Thickness"]) for sp in range(len(r["Snake"]["Length"]))]
		
		if r["Digestion"] == 1:
			if app.check_if_time_has_elapsed_in_milliseconds(400):
				try:
					r["Snake"]["Digestion Part"] = randrange(0, len(r["Snake"]["Length"])-1)
				except ValueError:
					default()
					r["Error Counter"] += 1
					if r["Error Counter"] == 1:
						print "Obscure recursive deletion error captured 1 time."
					else:
						print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
						r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
					
		if len(r["Snake"]["Length"]) > 0:
			r["Snake"]["Length"].pop()
		if r["Snake"]["Present Direction"] == NORTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]-1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]-1))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == SOUTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]+1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]+1))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == WEST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]-1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]-1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == EAST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]+1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]+1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
	
		# Defaults if the snake collides with itself or with the screen's boundaries.
		[default() for spr in r["Snake"]["Rects"] if col(r["Snake"]["Rects"][0], spr) and spr != r["Snake"]["Rects"][0] and len(r["Snake"]["Length"]) > 2]
		if r["Snake"]["Next"][0] < 0 or r["Snake"]["Next"][0] > (int(r["Screen Width"]/r["Element Size"]))-1:
			default()
		if r["Snake"]["Next"][1] < 0 or r["Snake"]["Next"][1] > (int(r["Screen Height"]/r["Element Size"]))-1:
			default()

		if not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Length"].insert(0, r["Snake"]["Next"])
			if r["Digestion"] == 1:
				r["Snake"]["Rects"][r["Snake"]["Digestion Part"]].update_color(r["Snake"]["Digestive Color"])

		if press_up() or press_key(pygame.K_w) or press_key(pygame.K_KP8):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][0]
			r["Background"].change_direction(SOUTH)
		if press_down() or press_key(pygame.K_s) or press_key(pygame.K_KP2):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][1]
			r["Background"].change_direction(NORTH)
		if press_left() or press_key(pygame.K_a) or press_key(pygame.K_KP4):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][2]
			r["Background"].change_direction(EAST)
		if press_right() or press_key(pygame.K_d) or press_key(pygame.K_KP6):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][3]
			r["Background"].change_direction(WEST)
	
	def give_mazy_life(): 
		
		r["Maze"].draw()
		
		try:
			r["Snake"]["Next"] = r["Snake"]["Length"][0]
		except IndexError:
			default()
			r["Error Counter"] += 1
			if r["Error Counter"] == 1:
				print "Obscure recursive deletion error captured 1 time."
			else:
				print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
				r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		r["Snake"]["Rects"] = [EwRect(r["Grid"].get_row_pos(r["Snake"]["Length"][sp][0]),
			r["Grid"].get_column_pos(r["Snake"]["Length"][sp][1]), 
			r["Element Size"], 
			r["Element Size"], 
			r["Snake"]["Color"],
			r["Element Alpha"], 
			r["Element Thickness"]) for sp in range(len(r["Snake"]["Length"]))]
		
		if r["Digestion"] == 1:
			if app.check_if_time_has_elapsed_in_milliseconds(400):
				try:
					r["Snake"]["Digestion Part"] = randrange(0, len(r["Snake"]["Length"])-1)
				except ValueError:
					default()
					r["Error Counter"] += 1
					if r["Error Counter"] == 1:
						print "Obscure recursive deletion error captured 1 time."
					else:
						print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
						r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		if len(r["Snake"]["Length"]) > 0:
			r["Snake"]["Length"].pop()
		if r["Snake"]["Present Direction"] == NORTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]-1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]-1))
				respawn_food()
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == SOUTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]+1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]+1))
				respawn_food()
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == WEST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]-1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]-1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				respawn_food()
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == EAST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]+1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]+1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				respawn_food()
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
	
		# Defaults if the snake collides with itself or with the screen's boundaries.
		[default() for spr in r["Snake"]["Rects"] if col(r["Snake"]["Rects"][0], spr) and spr != r["Snake"]["Rects"][0] and len(r["Snake"]["Length"]) > 2]
		if r["Snake"]["Next"][0] < 0:
			r["Snake"]["Next"][0] = (int(r["Screen Width"]/r["Element Size"]))-1
		elif r["Snake"]["Next"][0] > (int(r["Screen Width"]/r["Element Size"]))-1:
			r["Snake"]["Next"][0] = 0
		elif r["Snake"]["Next"][1] < 0:
			r["Snake"]["Next"][1] = (int(r["Screen Height"]/r["Element Size"]))-1
		elif r["Snake"]["Next"][1] > (int(r["Screen Height"]/r["Element Size"]))-1:
			r["Snake"]["Next"][1] = 0

		for horizontal_wall in r["Maze"]["horizontal_maze"]["walls"]:
			for horizontal_rect in horizontal_wall["rects"]:
				if col(r["Snake"]["Rects"][0], horizontal_rect):
						default()
		for vertical_wall in r["Maze"]["vertical_maze"]["walls"]:
			for vertical_rect in vertical_wall["rects"]:
				if col(r["Snake"]["Rects"][0], vertical_rect):
						default()

		if not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Length"].insert(0, r["Snake"]["Next"])
			if r["Digestion"] == 1:
				r["Snake"]["Rects"][r["Snake"]["Digestion Part"]].update_color(r["Snake"]["Digestive Color"])

		if press_up() or press_key(pygame.K_w) or press_key(pygame.K_KP8):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][0]
			r["Background"].change_direction(SOUTH)
		if press_down() or press_key(pygame.K_s) or press_key(pygame.K_KP2):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][1]
			r["Background"].change_direction(NORTH)
		if press_left() or press_key(pygame.K_a) or press_key(pygame.K_KP4):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][2]
			r["Background"].change_direction(EAST)
		if press_right() or press_key(pygame.K_d) or press_key(pygame.K_KP6):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][3]
			r["Background"].change_direction(WEST)

		r["Warper Square-Sign"].draw()
	
	def give_field_life(): 
		
		try:
			r["Snake"]["Next"] = r["Snake"]["Length"][0]
		except IndexError:
			default()
			r["Error Counter"] += 1
			if r["Error Counter"] == 1:
				print "Obscure recursive deletion error captured 1 time."
			else:
				print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
				r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		r["Snake"]["Rects"] = [EwRect(r["Grid"].get_row_pos(r["Snake"]["Length"][sp][0]),
			r["Grid"].get_column_pos(r["Snake"]["Length"][sp][1]), 
			r["Element Size"], 
			r["Element Size"], 
			r["Snake"]["Color"],
			r["Element Alpha"], 
			r["Element Thickness"]) for sp in range(len(r["Snake"]["Length"]))]
		
		if r["Digestion"] == 1:
			if app.check_if_time_has_elapsed_in_milliseconds(400):
				try:
					r["Snake"]["Digestion Part"] = randrange(0, len(r["Snake"]["Length"])-1)
				except ValueError:
					default()
					r["Error Counter"] += 1
					if r["Error Counter"] == 1:
						print "Obscure recursive deletion error captured 1 time."
					else:
						print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
						r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
					
		if len(r["Snake"]["Length"]) > 0:
			r["Snake"]["Length"].pop()
		if r["Snake"]["Present Direction"] == NORTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]-1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]-1))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"] == SOUTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]+1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]+1))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"]() == WEST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]-1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]-1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]
		elif r["Snake"]["Present Direction"]() == EAST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]+1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]+1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
				r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(randrange(0, int(r["Screen Width"]/r["Element Size"])))
				r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(randrange(0, int(r["Screen Height"]/r["Element Size"])))
				r["Score"] += 1
				r["Background"]["scroll_speed"] += r["Background Scrolling Speed Increment"]

		r["Field"].draw()
		it = r["Field"].collide(r["Snake"]["Rects"][0]) # Iteration.
		[r["Field"]["walls"].pop(x) for x in range(-1, len(it)-1) if it[x] is True]
		def increase_score(): r["Field Score"] += 1
		[increase_score() for x in range(-1, len(it)-1) if it[x] is True]
		if len(r["Field"]["walls"]) == 0:
			r["Field"] = EwRectField(0, 0, r["Screen Width"], r["Screen Height"], RED, 255, 0, r["Element Size"], r["Element Size"], r["Field Randrange"], r["Field Threshold"]) 
			r["Field Levels Cleared"] += 1
		
		EwTransformedFont(ctx(r["Screen Width"]/4), 8, r["Screen Width"]/4, r["Screen Height"]/48, r["FONT"], "Field levels cleared: " + str(r["Field Levels Cleared"]), SILVER, 255, False, r["Font Quality"]).draw()
		text(ctx(r["Screen Width"]/5), r["Screen Height"]-r["Screen Height"]/48, r["Screen Width"]/5, r["Screen Height"]/48, r["FONT"], "Field score: " + str(r["Field Score"]), SILVER)
		
		# Defaults if the snake collides with itself or with the screen's boundaries.
		[default() for spr in r["Snake"]["Rects"] if col(r["Snake"]["Rects"][0], spr) and spr != r["Snake"]["Rects"][0] and len(r["Snake"]["Length"]) > 2]
		if r["Snake"]["Next"][0] < 0 or r["Snake"]["Next"][0] > (int(r["Screen Width"]/r["Element Size"]))-1:
			default()
		if r["Snake"]["Next"][1] < 0 or r["Snake"]["Next"][1] > (int(r["Screen Height"]/r["Element Size"]))-1:
			default()

		if not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Length"].insert(0, r["Snake"]["Next"])
			if r["Digestion"] == 1:
				r["Snake"]["Rects"][r["Snake"]["Digestion Part"]].update_color(r["Snake"]["Digestive Color"])

		if press_up() or press_key(pygame.K_w) or press_key(pygame.K_KP8):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][0]
			r["Background"].change_direction(SOUTH)
		if press_down() or press_key(pygame.K_s) or press_key(pygame.K_KP2):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][1]
			r["Background"].change_direction(NORTH)
		if press_left() or press_key(pygame.K_a) or press_key(pygame.K_KP4):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][2]
			r["Background"].change_direction(EAST)
		if press_right() or press_key(pygame.K_d) or press_key(pygame.K_KP6):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][3]
			r["Background"].change_direction(WEST)

	def give_lengthy_life(): 
		
		r["Maze"].draw()
		
		try:
			r["Snake"]["Next"] = r["Snake"]["Length"][0]
		except IndexError:
			default()
			r["Error Counter"] += 1
			if r["Error Counter"] == 1:
				print "Obscure recursive deletion error captured 1 time."
			else:
				print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
				r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		r["Snake"]["Rects"] = [EwRect(r["Grid"].get_row_pos(r["Snake"]["Length"][sp][0]),
			r["Grid"].get_column_pos(r["Snake"]["Length"][sp][1]), 
			r["Element Size"], 
			r["Element Size"], 
			r["Snake"]["Color"],
			r["Element Alpha"], 
			r["Element Thickness"]) for sp in range(len(r["Snake"]["Length"]))]
		
		if r["Digestion"] == 1:
			if app.check_if_time_has_elapsed_in_milliseconds(400):
				try:
					r["Snake"]["Digestion Part"] = randrange(0, len(r["Snake"]["Length"])-1)
				except ValueError:
					default()
					r["Error Counter"] += 1
					if r["Error Counter"] == 1:
						print "Obscure recursive deletion error captured 1 time."
					else:
						print "Obscure recursive deletion error captured {} times.".format(r["Error Counter"])
						r["End Message"] = "This error occurs in the random digestion mode for some very obscure reason. The whole snake is a python list, and the digestion part is just a random index of this list considering the snake's length. For the snake to work, it uses pop() and therefore it removes constantly the last element of the list, and considering boundering colisions (offset list movement), and the fact that this index is random in real-time, the snake eventually deletes itself recursively and cries desperately to summon an IndexError until it gets tired of trying giving my almighty try-catch blocks."
		
		def respawn_food_to_snakes_head():
			r["Food"]["Rect"]["x"] = r["Grid"].get_row_pos(r["Snake"]["Next"][0])
			r["Food"]["Rect"]["y"] = r["Grid"].get_column_pos(r["Snake"]["Next"][1])
		
		if len(r["Snake"]["Length"]) > 0:
			r["Snake"]["Length"].pop()
		if r["Snake"]["Present Direction"] == NORTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]-1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Locomotion Score"]  += 1
				r["Food"]["Taken"] = True
				try:
					respawn_food_to_snakes_head()
				except IndexError:
					default()
					print "Ok, you shouldn't get this error. The engine probably tried to 'eat food off-limits'. Just ignore this message :)."
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]-1))
		elif r["Snake"]["Present Direction"] == SOUTH and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0], r["Snake"]["Next"][1]+1]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Locomotion Score"]  += 1
				r["Food"]["Taken"] = True
				try:
					respawn_food_to_snakes_head()
				except IndexError:
					default()
					print "Ok, you shouldn't get this error. The engine probably tried to 'eat food off-limits'. Just ignore this message :)."
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]+1))
		elif r["Snake"]["Present Direction"] == WEST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]-1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Locomotion Score"]  += 1
				r["Food"]["Taken"] = True
				try:
					respawn_food_to_snakes_head()
				except IndexError:
					default()
					print "Ok, you shouldn't get this error. The engine probably tried to 'eat food off-limits'. Just ignore this message :)."
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]-1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
		elif r["Snake"]["Present Direction"] == EAST and not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Next"] = [r["Snake"]["Next"][0]+1, r["Snake"]["Next"][1]]
			if col(r["Snake"]["Rects"][r["Snake"]["Digestion Part"]], r["Food"]["Rect"]):
				r["Locomotion Score"]  += 1
				r["Food"]["Taken"] = True
				try:
					respawn_food_to_snakes_head()
				except IndexError:
					default()
					print "Ok, you shouldn't get this error. The engine probably tried to 'eat food off-limits'. Just ignore this message :)."
				r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0]+1, r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]))
		# Defaults if the snake collides with itself or with the screen's boundaries.
		[default() for spr in r["Snake"]["Rects"] if col(r["Snake"]["Rects"][0], spr) and spr != r["Snake"]["Rects"][0] and len(r["Snake"]["Length"]) > 2]
		if r["Snake"]["Next"][0] < 0:
			r["Snake"]["Next"][0] = (int(r["Screen Width"]/r["Element Size"]))-1
		elif r["Snake"]["Next"][0] > (int(r["Screen Width"]/r["Element Size"]))-1:
			r["Snake"]["Next"][0] = 0
		elif r["Snake"]["Next"][1] < 0:
			r["Snake"]["Next"][1] = (int(r["Screen Height"]/r["Element Size"]))-1
		elif r["Snake"]["Next"][1] > (int(r["Screen Height"]/r["Element Size"]))-1:
			r["Snake"]["Next"][1] = 0

		for horizontal_wall in r["Maze"]["horizontal_maze"]["walls"]:
			for horizontal_rect in horizontal_wall["rects"]:
				if col(r["Snake"]["Rects"][0], horizontal_rect):
						default()
		for vertical_wall in r["Maze"]["vertical_maze"]["walls"]:
			for vertical_rect in vertical_wall["rects"]:
				if col(r["Snake"]["Rects"][0], vertical_rect):
						default()

		if not r["Snake"]["Digestion Part"] >= len(r["Snake"]["Length"]):
			r["Snake"]["Length"].insert(0, r["Snake"]["Next"])
			if r["Digestion"] == 1:
				r["Snake"]["Rects"][r["Snake"]["Digestion Part"]].update_color(r["Snake"]["Digestive Color"])
				
		if col(r["Snake"]["Rects"][0], r["Exit"]["Rect"]):
			if r["Food"]["Taken"] == True:
				r["Lengthy Score"] += 1
				default()
			else:
					EwRect(0, 0, r["Screen Width"], r["Screen Height"], RED, 75, 0).draw()

		if press_up() or press_key(pygame.K_w) or press_key(pygame.K_KP8):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][0]
			r["Background"].change_direction(SOUTH)
		if press_down() or press_key(pygame.K_s) or press_key(pygame.K_KP2):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][1]
			r["Background"].change_direction(NORTH)
		if press_left() or press_key(pygame.K_a) or press_key(pygame.K_KP4):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][2]
			r["Background"].change_direction(EAST)
		if press_right() or press_key(pygame.K_d) or press_key(pygame.K_KP6):
			r["Snake"]["Present Direction"] = r["Snake"]["Directions"][3]
			r["Background"].change_direction(WEST)

		r["Warper Square-Sign"].draw()
		EwTransformedFont(ctx(r["Screen Width"]/3), 8, r["Screen Width"]/3, r["Screen Width"]/48, r["FONT"], "Locomotion Score: " + str(r["Locomotion Score"]), SILVER, 255, False, r["Font Quality"]).draw()
		r["Exit"]["Rect"].draw()

	# Game scenes:

	r["Main Title"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Main Menu"]["y"]-112, r["Screen Width"]/2, r["Screen Width"]/12, r["FONT"], "Esnake", r["Font Highlight Color"], 255, False, r["Font Quality"])
	r["Credits"] = EwTransformedFont(ctx(r["Screen Width"]/3), 8, r["Screen Width"]/3, r["Screen Width"]/48, r["FONT"], "A game by Ericson Willians.", SILVER, 255, False, r["Font Quality"])
	r["Main 0"] = EwTransformedFont(ctx(r["Screen Width"]/5), r["Screen Height"]-32, r["Screen Width"]/5, 32, r["FONT"], "Start a new game.", SILVER, 255, False, r["Font Quality"])
	r["Main 1"] = EwTransformedFont(ctx(r["Screen Width"]/4), r["Screen Height"]-32, r["Screen Width"]/4, 32, r["FONT"], "Change the game options.", SILVER, 255, False, r["Font Quality"])
	r["Main 2"] = EwTransformedFont(ctx(r["Screen Width"]/3), r["Screen Height"]-32, r["Screen Width"]/3, 32, r["FONT"], "Be aware of your highscore.", SILVER, 255, False, r["Font Quality"])
	r["Main 3"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Screen Height"]-32, r["Screen Width"]/2, 32, r["FONT"], "Return to your Windows or Linux or Mac OS or Whatever.", SILVER, 255, False, r["Font Quality"])

	def exec_main():

		app.fill_background(BLACK)
		r["Background"].draw()
		app.set_fps(30)
		r["Grid"].draw()
		
		r["Main Title"].draw()
		r["Credits"].draw()

		r["Main Menu"].draw()
		r["Main Menu"].choose(r["Font Highlight Color"])
		if r["Main Menu"].both_press_and_select_option("Start Game", 1, r["Menu Selection Delay"]):
				app.activate("Modes Menu")
				app.deactivate("Main Menu")
		if r["Main Menu"].both_press_and_select_option("Options", 1, r["Menu Selection Delay"]):
				r["Options From"] = "Main Menu"
				app.activate("Options Menu")
				app.deactivate("Main Menu")	
		if r["Main Menu"].both_press_and_select_option("Highscore", 1, r["Menu Selection Delay"]):
				r["Highscore From"] = "Main Menu"
				update_highscore_list()
				r["Highscore Text Box"].update_text(''.join(r["Highscore List"]))
				app.activate("Highscore")
				app.deactivate("Main Menu")		
		if r["Main Menu"].both_press_and_select_option("Exit Game", 1, r["Menu Selection Delay"]):
			app()
		app.watch_for_exit()
		
		if r["Main Menu"].get_selected() == "Start Game":
			r["Main 0"].draw()
		elif r["Main Menu"].get_selected() == "Options":
			r["Main 1"].draw()
		elif r["Main Menu"].get_selected() == "Highscore":
			r["Main 2"].draw()
		elif r["Main Menu"].get_selected() == "Exit Game":
			r["Main 3"].draw()
	
	r["OPT Upper Text"] = EwTransformedFont(ctx(r["Screen Width"]/6), 8, r["Screen Width"]/6, r["Screen Height"]/48, r["FONT"], DEFAULT_OPTIONS_PATH, SILVER, 255, False, r["Font Quality"])
	r["OPT 0"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Screen Height"]-32, r["Screen Width"]/2, 32, r["FONT"], "Adjust the resolution in order to fit your screen (Restart needed).", SILVER, 255, False, r["Font Quality"])
	r["OPT 1"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Screen Height"]-32, r["Screen Width"]/2, 32, r["FONT"], "Change the font quality (Restart Needed).", SILVER, 255, False, r["Font Quality"])
	r["OPT 2"] = EwTransformedFont(ctx(r["Screen Width"]/3), r["Screen Height"]-32, r["Screen Width"]/3, 32, r["FONT"], "Enable or disable fullscreen (Enter).", SILVER, 255, False, r["Font Quality"])
	r["OPT 3"] = EwTransformedFont(ctx(r["Screen Width"]/3), r["Screen Height"]-32, r["Screen Width"]/3, 32, r["FONT"], "Set the game size.", SILVER, 255, False, r["Font Quality"])
	r["OPT 4"] = EwTransformedFont(ctx(r["Screen Width"]/3), r["Screen Height"]-32, r["Screen Width"]/3, 32, r["FONT"], "Adjust the game speed to suit your skill.", SILVER, 255, False, r["Font Quality"])
	r["OPT 5"] = EwTransformedFont(ctx(r["Screen Width"]/5), r["Screen Height"]-32, r["Screen Width"]/5, 32, r["FONT"], "Adjust the music volume.", SILVER, 255, False, r["Font Quality"])
	r["OPT 6"] = EwTransformedFont(ctx(r["Screen Width"]/4), r["Screen Height"]-32, r["Screen Width"]/4, 32, r["FONT"], "Change the score output format.", SILVER, 255, False, r["Font Quality"])
	r["OPT 7"] = EwTransformedFont(ctx(r["Screen Width"]/4), r["Screen Height"]-32, r["Screen Width"]/4, 32, r["FONT"], "Enable or disable the game grid.", SILVER, 255, False, r["Font Quality"])
	r["OPT 8"] = EwTransformedFont(ctx(r["Screen Width"]/5), r["Screen Height"]-32, r["Screen Width"]/5, 32, r["FONT"], "Return to the previous menu.", SILVER, 255, False, r["Font Quality"])
	r["OPT Warning 0"] = EwTextBox(ctx(r["Screen Width"] - 96), 32, "It's mathematically incoherent to have a cell size\ngreater than the screen size.\nIn this case, it must be less than " + str(r["Screen Height"]) + ".", 26, r["FONT"], RED, 255, False, MAROON)
	r["OPT Warning 1"] = EwTextBox(ctx(r["Screen Width"] - 96), 32, "You're kidding, right?\nNo, you're not. You're trying to crash my bloody game!\nHA! You've failed (This time).\nJust keep in mind that '2' or '4' or whatever\nare really stupid and unplayable values.\nTry 8 if you want something really small and playable.", 26, r["FONT"], RED, 255, False, MAROON)
	
	def exec_opt():
		app.fill_background(BLACK)
		r["Background"].draw()
		app.set_fps(30)
		r["Grid"].draw()
		
		if check_file(DEFAULT_OPTIONS_PATH):
			r["OPT Upper Text"].draw()
		
		r["Options Menu"].draw()
		r["Options Menu"].choose(r["Font Highlight Color"])

		if r["Options Menu"].both_press_and_select_option("Return", 1, r["Menu Selection Delay"]/2) or press_escape():
			r["Options File"] ["Resolution"] = r["Resolution Value Chooser"]["value"]
			r["Options File"] ["Font Quality"] = r["Font Quality Value Chooser"]["value"]
			r["Options File"] ["Fullscreen"] = r["Fullscreen Value Chooser"]["value"]
			if r["Game Size Input"].get_value() == '' or int(r["Game Size Input"].get_value()) <= 1:
				if check_file(DEFAULT_OPTIONS_PATH):
					pass
				else:
					r["Options File"] ["Game Size"] = 16
			else:
				r["Options File"] ["Game Size"] = int(r["Game Size Input"].get_value())
			r["Options File"] ["Game Speed"] = r["Game Speed Value Chooser"]["value"]
			r["Options File"] ["Music Volume"] = r["Music Volume Value Chooser"]["value"]
			r["Options File"] ["Score Counter"] = r["Score Counter Value Chooser"]["value"]
			r["Options File"] ["Grid"] = r["Grid Value Chooser"]["value"]
			r["Options File"] .write(DEFAULT_OPTIONS_PATH)
			
			if tml(r["Delay Between Screens"]):
				if r["Options From"] == "Main Menu":
					r["Main Menu"].set_selected(0)
					app.activate("Main Menu")
					app.deactivate("Options Menu")
				elif r["Options From"] == "Pause Menu":
					r["Pause Menu"].set_selected(0)
					app.activate("Pause Menu")
					app.deactivate("Options Menu")
		
		if r["Options Menu"].get_selected() == "Resolution":
			r["Resolution Value Chooser"].draw()
			r["Resolution Value Chooser"]["has_focus"] = True
			r["Resolution Value Chooser"].select_scrolling()
			r["OPT 0"].draw()
		else:
			r["Resolution Value Chooser"]["has_focus"] = False
			
		if r["Options Menu"].get_selected() == "Font Quality":
			r["Font Quality Value Chooser"].draw()
			r["Font Quality Value Chooser"]["has_focus"] = True
			r["Font Quality Value Chooser"].select_scrolling()
			r["OPT 1"].draw()
		else:
			r["Font Quality Value Chooser"]["has_focus"] = False
		
		if r["Options Menu"].get_selected() == "Fullscreen":
			r["Fullscreen Value Chooser"].draw()
			r["Fullscreen Value Chooser"]["has_focus"] = True
			r["Fullscreen Value Chooser"].select_scrolling()
			r["OPT 2"].draw()
			if press_enter():
				if r["Fullscreen Value Chooser"]["value"] == "ON":
					r["Fullscreen"] = True
				elif r["Fullscreen Value Chooser"]["value"] == "OFF":
					r["Fullscreen"] = False
				if r["Fullscreen"] == True:
					r["screen"] = pygame.display.set_mode((r["Screen Width"], r["Screen Height"]), pygame.DOUBLEBUF | pygame.FULLSCREEN)
				else:
					r["screen"] = pygame.display.set_mode((r["Screen Width"], r["Screen Height"]), pygame.DOUBLEBUF)
		else:
			r["Fullscreen Value Chooser"]["has_focus"] = False
			
		if r["Options Menu"].get_selected() == "Game Size":
			r["Game Size Input"].draw()
			r["Game Size Input"]["has_focus"] = True
			if len(r["Game Size Input"].get_value()) > 0:
				if int(r["Game Size Input"].get_value()) >= r["Screen Height"]:
					r["OPT Warning 0"].draw()
				elif int(r["Game Size Input"].get_value()) < 2:
					r["OPT Warning 1"].draw()
			r["OPT 3"].draw()
		else:
			r["Game Size Input"]["has_focus"] = False
			
		if r["Options Menu"].get_selected() == "Game Speed":
			r["Game Speed Value Chooser"].draw()
			r["Game Speed Value Chooser"]["has_focus"] = True
			r["Game Speed Value Chooser"].select_scrolling()
			r["OPT 4"].draw()
		else:
			r["Game Speed Value Chooser"]["has_focus"] = False
		
		if r["Options Menu"].get_selected() == "Music Volume":
			r["Music Volume Value Chooser"].draw()
			r["Music Volume Value Chooser"]["has_focus"] = True
			r["Music Volume Value Chooser"].select_scrolling()
			r["OPT 5"].draw()
			pygame.mixer.music.set_volume(r["Music Volume Value Chooser"]["value"])
		else:
			r["Music Volume Value Chooser"]["has_focus"] = False
		
		if r["Options Menu"].get_selected() == "Score Counter":
			r["Score Counter Value Chooser"].draw()
			r["Score Counter Value Chooser"]["has_focus"] = True
			r["Score Counter Value Chooser"].select_scrolling()
			r["OPT 6"].draw()
		else:
			r["Score Counter Value Chooser"]["has_focus"] = False
			
		if r["Options Menu"].get_selected() == "Game Grid":
			r["Grid Value Chooser"].draw()
			r["Grid Value Chooser"]["has_focus"] = True
			r["Grid Value Chooser"].select_scrolling()
			r["OPT 7"].draw()
		else:
			r["Grid Value Chooser"]["has_focus"] = False

		if r["Options Menu"].get_selected() == "Return":
			r["OPT 8"].draw()
	
	r["HS Upper Text"] = EwTransformedFont(ctx(r["Screen Width"]/6), 8, r["Screen Width"]/6, r["Screen Height"]/48, r["FONT"], DEFAULT_HIGHSCORE_PATH, SILVER, 255, False, r["Font Quality"])
	
	def exec_hs():
		app.fill_background(BLACK)
		r["Background"].draw()
		r["Background Rect"].draw()
		r["Grid"].draw()
		
		if check_file(DEFAULT_HIGHSCORE_PATH):
			r["HS Upper Text"].draw()
		
		if len(r["Highscore List"]) > 0:
			r["Highscore Text Box"].draw()
		else:
			if check_file(DEFAULT_HIGHSCORE_PATH):
				fill_highscore_list()
				r["Highscore Text Box"].draw()
			else:
				EwFont(64, 64, 16, r["FONT"], "Nope, no higscore yet.. What about playing the game first?", r["Font Color"]).draw()
			
		app.watch_for_exit()
		if press_escape():
			if tml(r["Delay Between Screens"]):
				if r["Highscore From"] == "Main Menu":
					app.activate("Main Menu")
					app.deactivate("Highscore")
				elif r["Highscore From"] == "Pause Menu":
					app.activate("Pause Menu")
					app.deactivate("Highscore")
	
	r["Modes Title"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Main Menu"]["y"]-112, r["Screen Width"]/2, r["Screen Width"]/12, r["FONT"], "Game Modes", r["Font Highlight Color"], 255, False, r["Font Quality"])
	
	r["Modes Upper Text"] = EwTransformedFont(ctx(r["Screen Width"]/2), 8, r["Screen Width"]/2, r["Screen Width"]/56, r["FONT"], "Press F1 over the game mode for help.", SILVER, 255, False, r["Font Quality"])
	
	r["Modes 0"] = EwTransformedFont(ctx(316), r["Screen Height"]-32, 316, 32, r["FONT"], "Play a classic snake game.", SILVER, 255, False, r["Font Quality"])
	r["Modes 1"] = EwTransformedFont(ctx(475), r["Screen Height"]-32, 475, 32, r["FONT"], "Play within a procedurally-generated maze.", SILVER, 255, False, r["Font Quality"])
	r["Modes 2"] = EwTransformedFont(ctx(525), r["Screen Height"]-32, 525, 32, r["FONT"], "Play within a procedurally-generated square field.", SILVER, 255, False, r["Font Quality"])
	r["Modes 3"] = EwTransformedFont(ctx(430), r["Screen Height"]-32, 430, 32, r["FONT"], "Just like mazy, but with a different gameplay.", SILVER, 255, False, r["Font Quality"])
	
	r["Modes Info 0"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "I'm pretty sure that you've played a snake game before.\nThere's not much to talk about this one, \nso just press the arrow keys.", 18, r["FONT"], RED, 255, False, MAROON)
	r["Modes Info 1"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "A 'maze' will be generated procedurally according\nto three inputs: Randrange, Threshold and Wall Length.\nIf the snake touches the walls's bricks, you loose.\nAlso, there are no screen boundaries in order to\navoid food-traps.", 18, r["FONT"], RED, 255, False, MAROON)
	r["Modes Info 2"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "A 'field' will be generated procedurally.\nConsider them as some kind of 'secondary food',\nand you'll earn an alternate score instead of dying\nwhen the snake touches them. ", 18, r["FONT"], RED, 255, False, MAROON)
	r["Modes Info 3"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "A 'maze' will be generated procedurally just like in Mazy Mode.\nOnce the snake reaches the food,\nit will start to grow in a tron-game-like way.\nIn order to score, you'll have to take it to the exit point.", 18, r["FONT"], RED, 255, False, MAROON)
	
	def exec_modes():
		app.fill_background(BLACK)
		r["Background"].draw()
		r["Grid"].draw()
		r["Modes Upper Text"].draw()
		r["Modes Title"].draw()
		
		if not press_key(pygame.K_F1):
			r["Modes Menu"].draw()
			r["Modes Menu"].choose(r["Font Highlight Color"])
		else:
			if r["Modes Menu"].get_selected() == "Classic":
				r["Modes Info 0"].draw()
			elif r["Modes Menu"].get_selected() == "Mazy":
				r["Modes Info 1"].draw()
			elif r["Modes Menu"].get_selected() == "Field":
				r["Modes Info 2"].draw()
			elif r["Modes Menu"].get_selected() == "Lengthy":
				r["Modes Info 3"].draw()
		
		if r["Modes Menu"].both_press_and_select_option("Classic", 1, r["Menu Selection Delay"]):
			r["Game Mode"] = "Classic"
			app.activate("Digestion Menu")
			app.deactivate("Modes Menu")
		if r["Modes Menu"].both_press_and_select_option("Mazy", 1, r["Menu Selection Delay"]):
			r["Game Mode"] = "Mazy"
			app.activate("Mazy CFG")
			app.deactivate("Modes Menu")
		if r["Modes Menu"].both_press_and_select_option("Field", 1, r["Menu Selection Delay"]):
			r["Game Mode"] = "Field"
			app.activate("Digestion Menu")
			app.deactivate("Modes Menu")
		if r["Modes Menu"].both_press_and_select_option("Lengthy", 1, r["Menu Selection Delay"]):
			r["Game Mode"] = "Lengthy"
			app.activate("Mazy CFG")
			app.deactivate("Modes Menu")
		app.watch_for_exit()
		if press_escape():
			app.activate("Main Menu")
			app.deactivate("Modes Menu")
		if press_enter():
			r["Digestion Menu"].set_selected("Normal")
		
		if r["Modes Menu"].get_selected() == "Classic":
			r["Modes 0"].draw()
		elif r["Modes Menu"].get_selected() == "Mazy":
			r["Modes 1"].draw()
		elif r["Modes Menu"].get_selected() == "Field":
			r["Modes 2"].draw()
		elif r["Modes Menu"].get_selected() == "Lengthy":
			r["Modes 3"].draw()
	
	r["Mazy Upper Text"] = EwTransformedFont(ctx(r["Screen Width"]/4), 8, r["Screen Width"]/4, r["Screen Width"]/60, r["FONT"], "Use the mouse wheel...", SILVER, 255, False, r["Font Quality"])
	r["Mazy Lower Text"] = EwTransformedFont(ctx(400), r["Screen Height"]-32, 400, 32, r["FONT"], "And press Return/Enter when you're finished.", SILVER, 255, False, r["Font Quality"])
	r["Mazy Info 0"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "The walls are drawn if a random float number\nis less than a float threshold. Which means:\nIf a random number from 0 to a max randrange is\nless than a threshold, then a wall is created.\nIn other words, the greater the randrange and\nthe lesser the threshold, the sparser the walls.", 18, r["FONT"], RED, 255, False, MAROON)
	r["Mazy Info 1"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "The walls are drawn if a random float number\nis less than a float threshold. Which means:\nIf a random number from 0 to a max randrange is\nless than a threshold, then a wall is created.\nIn other words, the greater the randrange and\nthe lesser the threshold, the sparser the walls.", 18, r["FONT"], RED, 255, False, MAROON)
	r["Mazy Info 2"] = EwTextBox(ctx(r["Screen Width"] - 96), r["Main Menu"]["y"], "This integer defines the number of bricks in each wall.\nThe greater the value, the lesser the walls \n(Since the walls are only drawn by steps of its own length).", 18, r["FONT"], RED, 255, False, MAROON)
	
	def exec_mazy():
		app.fill_background(BLACK)
		r["Background"].draw()
		r["Grid"].draw()
		
		if r["Mazy Menu"].get_selected() == "Float Randrange":
			if scroll_up():
				r["Mazy Float Randrange"] += 0.1
			elif scroll_down():
				if r["Mazy Float Randrange"] > 0.1:
					r["Mazy Float Randrange"] -= 0.1
			text(16, 16, r["Screen Width"]-16, r["Screen Height"]-16, r["FONT"],  str(r["Mazy Float Randrange"]), (0, 25, 0))
		elif r["Mazy Menu"].get_selected() == "Float Threshold":
			if scroll_up():
				r["Mazy Float Threshold"] += 0.1
			elif scroll_down():
				if r["Mazy Float Threshold"] > 0.2:
					r["Mazy Float Threshold"] -= 0.1
			text(16, 16, r["Screen Width"]-16, r["Screen Height"]-16, r["FONT"],  str(r["Mazy Float Threshold"]), (0, 25, 0))
		elif r["Mazy Menu"].get_selected() == "Wall Length":
			if scroll_up():
				r["Mazy Wall Length"] += 1
			elif scroll_down():
				if r["Mazy Wall Length"] > 1:
					r["Mazy Wall Length"] -= 1
			text(16, 16, r["Screen Width"]-16, r["Screen Height"]-16, r["FONT"],  str(r["Mazy Wall Length"]), (0, 25, 0))

		if not press_key(pygame.K_F1):
			r["Mazy Menu"].draw()
			r["Mazy Menu"].choose(r["Font Highlight Color"])
		else:
			if r["Mazy Menu"].get_selected() == "Float Randrange":
				r["Mazy Info 0"].draw()
			elif r["Mazy Menu"].get_selected() == "Float Threshold":
				r["Mazy Info 1"].draw()
			elif r["Mazy Menu"].get_selected() == "Wall Length":
				r["Mazy Info 2"].draw()
		r["Mazy Upper Text"].draw()
		r["Mazy Lower Text"].draw()
		
		if press_enter():
			if tml(r["Delay Between Screens"]):
				if r["Game Mode"] == "Mazy":
					app.activate("Digestion Menu")
					app.deactivate("Mazy CFG")
				elif r["Game Mode"] == "Lengthy":
					r["Digestion"] = 0
					default()
					app.activate("Game")
					app.deactivate("Mazy CFG")
		
		app.watch_for_exit()
		if press_escape():
			if tml(r["Delay Between Screens"]):
				app.activate("Modes Menu")
				app.deactivate("Mazy CFG")
	
	r["Dig Title"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Main Menu"]["y"]-112, r["Screen Width"]/2, r["Screen Width"]/12, r["FONT"], "Digestion", r["Font Highlight Color"], 255, False, r["Font Quality"])
	r["Dig 0"] = EwTransformedFont(ctx(316), r["Screen Height"]-32, 316, 32, r["FONT"], "Oldschool and predictable.", SILVER, 255, False, r["Font Quality"])
	r["Dig 1"] = EwTransformedFont(ctx(300), r["Screen Height"]-32, 300, 32, r["FONT"], "Random digestion mode.", SILVER, 255, False, r["Font Quality"])
	r["Dig 2"] = EwTransformedFont(ctx(180), r["Screen Height"]-32, 180, 32, r["FONT"], "SLITHER!", RED, 255, False, r["Font Quality"])
	
	def exec_digestion():
		app.fill_background(BLACK)
		r["Background"].draw()
		r["Grid"].draw()
		
		if r["Digestion"] == 0:
			draw_main_score("Normal")
		elif r["Digestion"] == 1:
			draw_main_score("Random")
		
		r["Dig Title"].draw()
		
		r["Digestion Menu"].draw()
		r["Digestion Menu"].choose(r["Font Highlight Color"])
		if r["Digestion Menu"].both_press_and_select_option("Normal", 1, r["Menu Selection Delay"]):
			r["Digestion"] = 0
		if r["Digestion Menu"].both_press_and_select_option("Random", 1, r["Menu Selection Delay"]):
			r["Digestion"] = 1
		if r["Digestion Menu"].both_press_and_select_option("Spawn", 1, r["Menu Selection Delay"]):
			r["Grid Color"] = (0, 50, 0)
			r["Grid"].update_color(r["Grid Color"])
			default()
			app.activate("Game")
			app.deactivate("Digestion Menu")		
		app.watch_for_exit()
		if press_escape():
			if r["Game Mode"] == "Mazy" or r["Game Mode"] == "Lengthy":
				app.activate("Mazy CFG")
				app.deactivate("Digestion Menu")
			else:
				app.activate("Modes Menu")
				app.deactivate("Digestion Menu")
			
		if r["Digestion Menu"].get_selected() == "Normal":
			r["Dig 0"].draw()
		elif r["Digestion Menu"].get_selected() == "Random":
			r["Dig 1"].draw()
		elif r["Digestion Menu"].get_selected() == "Spawn":
			r["Dig 2"].draw()

	def exec_game():
		
		app.fill_background(BLACK)
		r["Background"].draw()
		
		# Option-depended code:
		
		if r["Game Speed Value Chooser"]["value"] == "Huge Cells":
			app.set_fps(2)
		elif r["Game Speed Value Chooser"]["value"] == "Lame":
			app.set_fps(5)
		elif r["Game Speed Value Chooser"]["value"] == "Slow":
			app.set_fps(7)
		elif r["Game Speed Value Chooser"]["value"] == "Classic":
			app.set_fps(10)
		elif r["Game Speed Value Chooser"]["value"] == "Just a bit":
			app.set_fps(20)
		elif r["Game Speed Value Chooser"]["value"] == "Nice":
			app.set_fps(30)
		elif r["Game Speed Value Chooser"]["value"] == "Pro":
			app.set_fps(40)
		elif r["Game Speed Value Chooser"]["value"] == "Sick":
			app.set_fps(50)
		elif r["Game Speed Value Chooser"]["value"] == "Retarded":
			app.set_fps(60)
		elif r["Game Speed Value Chooser"]["value"] == "You're going to die!":
			app.set_fps(100)

		if r["Game Mode"] == "Lengthy":
			draw_main_score(r["Lengthy Score"])
		else:
			draw_main_score(r["Score"])
			
		if r["Grid Value Chooser"]["value"] == "ON":
			r["Grid"].draw()
		else:
			EwRect(16, 16, r["Screen Width"], r["Screen Height"], r["Font Color"], 125, 5).draw()
			EwRect(-16, -16, r["Screen Width"], r["Screen Height"], r["Font Color"], 125, 5).draw()
		
		if r["Game Mode"] == "Classic":
			give_classic_life()
		elif r["Game Mode"] == "Mazy":
			give_mazy_life()
		elif r["Game Mode"] == "Field":
			give_field_life()
		elif r["Game Mode"] == "Lengthy":
			give_lengthy_life()
			
		if len(r["Snake"]["Rects"]) < 3:
			r["Snake"]["Length"].append((r["Snake"]["Length"][len(r["Snake"]["Length"])-1][0], r["Snake"]["Length"][len(r["Snake"]["Length"])-1][1]-1))
		
		[sp.draw() for sp in r["Snake"]["Rects"]]
		r["Food"]["Rect"].draw()
		
		app.watch_for_exit()
		if press_escape():
			r["Grid Color"] = (0, 25, 0)
			r["Grid"].update_color(r["Grid Color"])
			save_highscore()
			app.activate("Pause Menu")
			app.deactivate("Game")
	
	r["Pause 0"] = EwTransformedFont(ctx(384), r["Screen Height"]-32, 384, 32, r["FONT"], "Return to the current game you're playing.", SILVER, 255, False, r["Font Quality"])
	r["Pause 1"] = EwTransformedFont(ctx(300), r["Screen Height"]-32, 300, 32, r["FONT"], "Start a new game.", SILVER, 255, False, r["Font Quality"])
	r["Pause 2"] = EwTransformedFont(ctx(312), r["Screen Height"]-32, 312, 32, r["FONT"], "Change the game options.", SILVER, 255, False, r["Font Quality"])
	r["Pause 3"] = EwTransformedFont(ctx(r["Screen Width"]/3), r["Screen Height"]-32, r["Screen Width"]/3, 32, r["FONT"], "Be aware of your highscore.", SILVER, 255, False, r["Font Quality"])
	r["Pause 4"] = EwTransformedFont(ctx(r["Screen Width"]/2), r["Screen Height"]-32, r["Screen Width"]/2, 32, r["FONT"], "Return to your Windows or Linux or Mac OS or Whatever.", SILVER, 255, False, r["Font Quality"])
	
	def exec_pause():
		app.fill_background(BLACK)
		r["Background"].draw()
		app.set_fps(30)
		r["Grid"].draw()
		r["Pause Menu"].draw()
		r["Pause Menu"].choose(r["Font Highlight Color"])
		if r["Pause Menu"].both_press_and_select_option("Resume Game", 1, r["Menu Selection Delay"]):
			r["Grid Color"] = (0, 50, 0)
			r["Grid"].update_color(r["Grid Color"])
			app.activate("Game")
			app.deactivate("Pause Menu")
		if r["Pause Menu"].both_press_and_select_option("New Game", 1, r["Menu Selection Delay"]):
			default()
			if tml(r["Delay Between Screens"]):
				app.activate("Modes Menu")
				app.deactivate("Pause Menu")
		if r["Pause Menu"].both_press_and_select_option("Options", 1, r["Menu Selection Delay"]):
				r["Options From"] = "Pause Menu"
				app.activate("Options Menu")
				app.deactivate("Pause Menu")
		if r["Pause Menu"].both_press_and_select_option("Highscore", 1, r["Menu Selection Delay"]):
				r["Highscore From"] = "Pause Menu"
				update_highscore_list()
				r["Highscore Text Box"].update_text(''.join(r["Highscore List"]))
				app.activate("Highscore")
				app.deactivate("Pause Menu")		
		if r["Pause Menu"].both_press_and_select_option("Exit Game", 1, r["Menu Selection Delay"]):
			default()
			app(r["End Message"])
			
		if r["Pause Menu"].get_selected() == "Resume Game":
			r["Pause 0"].draw()
		elif r["Pause Menu"].get_selected() == "New Game":
			r["Pause 1"].draw()
		elif r["Pause Menu"].get_selected() == "Options":
			r["Pause 2"].draw()
		elif r["Pause Menu"].get_selected() == "Highscore":
			r["Pause 3"].draw()
		elif r["Pause Menu"].get_selected() == "Exit Game":
			r["Pause 4"].draw()
		
	# Creation of game-scenes:
		
	app.create("Main Menu", exec_main, True)
	app.create("Options Menu", exec_opt, False)
	app.create("Highscore", exec_hs, False)
	app.create("Modes Menu", exec_modes, False)
	app.create("Mazy CFG", exec_mazy, False)
	app.create("Digestion Menu", exec_digestion, False)
	app.create("Game", exec_game, False)
	app.create("Pause Menu", exec_pause, False)
	
	app.run()
