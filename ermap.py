from ercrash import *
from erbase import *
from erdat import *
from erfunc import *
from erxec import *
from ergui import *
from erproc import *

# Small observation for outsiders:
# I use star-imports because the engine was written by ME and therefore I KNOW where everything is.

if __name__ == "__main__":

	r = EwData()
	r["Screen Width"] = 1024
	r["Screen Height"] = 768
	r["FPS"] = 30
	r["Fullscreen"] = False

	app = EwApp("Ergame App", r["Screen Width"], r["Screen Height"], r["FPS"], r["Fullscreen"])
	terminal = EwTerminal(EwKeyboardLayout(), 0, 0, 32)
	terminal["activated"] = False

	def exec_main():
		app.fill_background(BLACK)
		
		if push_key(96):
			if terminal["activated"] == False:
				terminal["activated"] = True
			elif terminal["activated"] == True:
				terminal["activated"] = False
		
		if terminal["activated"] == True:
			terminal.draw()
		
		# print terminal["activated"]
		print_keys()
		
		app.watch_for_exit()
		if press_escape() or press_close():
			app()

	app.create("Main Screen", exec_main, True)
	app.run()
