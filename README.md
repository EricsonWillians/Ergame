### WARNING: The engine is going through critical updates, and the examples on the wiki might not work. I'm getting closer and closer to a stable release, and I'll update the entire wiki when I get there. 

Ergame
======
The encapsulated and object-oriented solution for Game Development with Python.

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

Learning how to program by my own was really hard, and I've painfully discovered how hard it is to do anything related to game development at first. That's why I've created Ergame: To do my best to make things easier for you (And for me, considering that this is the engine I'll use in all my games).
