Ergame
======

An open-source object-oriented engine for game development in Python with Pygame.

[Check out the Ergame wiki I'm writing in order to learn how to use it](https://github.com/EricsonWillians/Ergame/wiki).

Download and **ergame.py** and check out with this minimum code how easy it is to setup a basic window with working close operation right now!

```
import ergame as er

if __name__ == "__main__":
	
	app = er.EwApp("Bloody Example", 1024, 768, 50)
	
	def update():	
		app.watch_for_exit()
		
	app.run(update)

```
