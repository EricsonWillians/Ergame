Ergame
======

An open-source object-oriented engine for game development in Python 2.7 with Pygame.

[Check out the Ergame wiki I'm writing in order to learn how to use it](https://github.com/EricsonWillians/Ergame/wiki).

Download **ergame.py** and check out how easy it is to setup a basic window with working close operation with just a few lines of code!

```
import ergame as er

if __name__ == "__main__":
	
	app = er.EwApp("Bloody Example", 1024, 768, 50)
	
	def update():	
		app.watch_for_exit()
		
	app.run(update)

```
