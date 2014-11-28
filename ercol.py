"""
====================================================================

ERGAME v1.0

"ercol.py", Collision Detection.
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

from erdat import *

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
