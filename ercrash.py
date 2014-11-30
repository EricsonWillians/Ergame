"""
====================================================================

ERGAME v1.0

"ercrash.py", Exceptions.
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
