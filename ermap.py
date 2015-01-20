"""
====================================================================

ERGAME's Map Editor v1.02

"ermap.py", Engine Data.
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

# AS YOU CAN SEE,
# THIS FILE IS UNDER CONSTRUCTION.

from ercrash import *
from erbase import *
from erdat import *
from erfunc import *
from erxec import *
from ergui import *
from erproc import *

if __name__ == "__main__":

	r = EwData()
	r["Screen Width"] = 1024
	r["Screen Height"] = 768
	r["FPS"] = 30
	r["Fullscreen"] = False
	
	app = EwApp("Ergame Map Editor (Ermap)", r["Screen Width"], r["Screen Height"], r["FPS"], r["Fullscreen"])
	_in = EwConsole(32)
	def x(arg0, arg1):
		print("The values are: {0}, {1}".format(arg0, arg1))
	_in.create_command("print", x)
	
	def exec_main():

		app.fill_background(BLACK)
		
		_in.draw()
		
		app.watch_for_exit()
		if press_escape():
			app()
		
	app.create("Main", exec_main, True)
	
	app.run()
