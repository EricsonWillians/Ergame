"""
====================================================================

ERGAME v1.0

"erxec.py", Engine Execution.
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
from erdat import *

# EXECUTION
# ======================================================== #

class EwRunnable:

	"""
	An EwRunnable holds the engine "execution" functionality.
	It serves as a wrapper for the basic "main loop" app/game structure.
	"""

	def __init__(self, initial_state, FPS, scenes=99):
		
		"""
		Input arguments:
		initial_state <- boolean
		FPS <- int
		scenes <- int
		"""
		
		self.state = initial_state
		self.FPS = FPS
		self.scenes = scenes
		self.dt = None
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
			self.dt = dt
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

	"""
	An EwApp is both an EwRunnable and EwData.
	It represents the app/game pygame window.
	"""

	def __init__(self, title, w, h, FPS, fullscreen=False, sound_buffer=1024):
		
		"""
		Input arguments:
		title <- string
		w <- int
		h <- int
		FPS <- int
		fullscreen <- boolean
		sound_buffer <- int
		"""
		
		EwRunnable.__init__(self, False, FPS)
		EwData.__init__(self)

		self["TITLE"] = title
		self["SCREEN_WIDTH"] = w
		self["SCREEN_HEIGHT"] = h
		self["FPS"] = FPS
		self["FULLSCREEN"] = fullscreen
		self["SOUND_BUFFER"] = sound_buffer
		
		pygame.mixer.pre_init(44100, -16, 2, 1024) 
		pygame.init()
		pygame.font.init()
		
		if self["FULLSCREEN"] == True:
			self["screen"] = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]), pygame.DOUBLEBUF | pygame.FULLSCREEN)
		else:
			self["screen"] = pygame.display.set_mode((self["SCREEN_WIDTH"], self["SCREEN_HEIGHT"]))
		pygame.display.set_caption(self["TITLE"])

		EwData.app = self
	
	def check_if_time_has_elapsed_in_milliseconds(self, milliseconds):
		self.time_elapsed += self.dt
		if self.time_elapsed > milliseconds:
			self.time_elapsed = 0
			return True
		else:
			return False
			
	def check_if_time_has_elapsed_in_seconds(self, seconds):
		self.time_elapsed += self.dt
		if self.time_elapsed > seconds*1000:
			self.time_elapsed = 0
			return True
		else:
			return False
			
	def check_if_time_has_elapsed_in_minutes(self, minutes):
		self.time_elapsed += self.dt
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
