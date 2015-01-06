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
	
	def exec_main():

		app.fill_background(BLACK)
		app.watch_for_exit()
		if press_escape():
			app()
		
	app.create("Main", exec_main, True)
	
	app.run()
