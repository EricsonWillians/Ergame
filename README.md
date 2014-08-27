Ergame
======
The encapsulated solution for Game Development with Python.

* Ergame is an open-source object-oriented engine for game development with [Python 2.7](https://www.python.org/download/releases/2.7/) and [Pygame](http://www.pygame.org/news.html) (You only need to have these installed).

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
