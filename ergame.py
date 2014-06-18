import pygame
import os

PATH = "EWG"

# ======================================================== #

class EwRunnable():
	
	def __init__(self, initial_state):
		
		self.state = initial_state
		
	def run(self, f, *args):
		while self.state is not True:
			apply(f, args)
		
class EwApp(EwRunnable):
	
	def __init__(self, title, w, h, state=False):
		
		pygame.init()
		pygame.font.init()
		
		EwRunnable.__init__(self, state)
		
		self.screen = pygame.display.set_mode((w, h))
		pygame.display.set_caption(title)

# ======================================================== #

class EwScene():
	
	def __init__(self, scene):
		
		self.scene = scene
		
class EwPlot():
	
	def __init__(self, *scenes):
		
		self.data = list(scenes)
		if len(self.data) > 0:
			self.current = self.data[0]
		
	def get_scene(self):
		return self.current
		
	def change_scene(self, new_scene):
		self.current = new_scene
		
def get_standard_plot():
	
	scene = [EwScene("S"+str(x)) for x in range(99)]
	opt = [EwScene("OPT"+str(x)) for x in range(99)]
	inv = [EwScene("INV"+str(x)) for x in range(99)]
	l = []
	l.append(EwScene("MAIN"))
	l.extend(scene)
	l.extend(opt)
	l.extend(inv)
	return EwPlot(l)
		
# ======================================================== #

class EwData():
	
	def __init__(self):
		
		self.data = {}
		
	def __setitem__(self, key, value):
		self.data[key] = value
		
	def __getitem__(self, key):
		return self.data[key]
		
	def get_data(self):
		return self.data
		
class EwPos():
	
	def __init__(self, x, y):
		
		self.x = x
		self.y = y
		
	def get_x(self):
		return self.x
		
	def set_x(self, value):
		self.x = value
		
	def get_y(self):
		return self.y

	def set_y(self, value):
		self.y = value
		
class EwMovable(EwPos):
	
	def __init__(self, x, y, direction=0, step=1):
		
		EwPos.__init__(self, x, y)
		
		self.direction = direction
		self.step = step
	
	def move(self, condition, direction=None, step=None):
		if direction is None: direction = self.direction
		if step is None: step = self.step
		if condition:
			if direction == 0:
				self.y -= step
			if direction == 1:
				self.y += step
			if direction == 2:
				self.x -= step
			if direction == 3:
				self.x += step
	
	def move_generically(self, condition, new_x, new_y):
		if condition:
			self.x = new_x
			self.y = new_y
		
	def get_direction(self):
		return self.direction
		
	def set_direction(self, value):
		self.direction = value
	
	def get_step(self):
		return self.step
		
	def set_step(self, value):
		self.step = value
			
class EwResizable():
	
	def __init__(self, w, h):
		
		self.w = w
		self.h = h
		
	def get_w(self):
		return self.w
		
	def set_w(self, value):
		self.w = value
		
	def get_h(self):
		return self.h
		
	def set_h(self, value):
		self.h = value
			
# ======================================================== #

class EwObject(EwData, EwMovable, EwResizable):
	
	def __init__(self, x, y, w, h):
		
		EwData.__init__(self)
		EwMovable.__init__(self, x, y)
		EwResizable.__init__(self, w, h)
		
	def get(self):
		return (self.x, self.y, self.w, self.h)
		
# ======================================================== #
		
class EwImage(EwObject):
	
	def __init__(self, x, y, w, h, filename):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.filename = filename
		if ".png" not in self.filename:
			self.image = pygame.image.load(os.path.join(PATH, filename)).convert()
		else:
			self.image = pygame.Surface.convert_alpha(pygame.image.load(os.path.join(PATH, filename)))
			
		self.transform()
			
	def transform(self):
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		
	def transform_custom(self, w, h):
		self.image = pygame.transform.scale(self.image, (w, h))
			
	def draw(self, destination_surface):
		destination_surface.blit(self.image, (self.x, self.y))
		
class EwScrollingImage(EwImage):
	
	def __init__(self, x, y, w, h, filename, scroll_direction=0, scroll_speed=1):
		
		EwImage.__init__(self, x, y, w, h, filename)
		
		self.scroll_direction = scroll_direction
		self.scroll_speed = scroll_speed
		self.default_scroll_speed = self.scroll_speed
		self.initial_y = self.y
		self.y0_reset_point = self.initial_y - self.h
		self.y1_reset_point = self.initial_y + self.h
		self.initial_x = self.x
		self.x2_reset_point = self.initial_x - self.w
		self.x3_reset_point = self.initial_x + self.w
		
	def draw(self, destination_surface):
		if self.scroll_direction == 0:
			self.y -= self.scroll_speed
			if self.y < self.y0_reset_point:
				self.y = self.initial_y
			destination_surface.blit(self.image, (self.x, self.y))
			destination_surface.blit(self.image, (self.x, self.y+self.h))
		if self.scroll_direction == 1:
			self.y += self.scroll_speed
			if self.y > self.y1_reset_point:
				self.y = self.initial_y
			destination_surface.blit(self.image, (self.x, self.y))
			destination_surface.blit(self.image, (self.x, self.y-self.h))
		if self.scroll_direction == 2:
			self.x -= self.scroll_speed
			if self.x < self.x2_reset_point:
				self.x = self.initial_x
			destination_surface.blit(self.image, (self.x, self.y))
			destination_surface.blit(self.image, (self.x+self.w, self.y))
		if self.scroll_direction == 3:
			self.x += self.scroll_speed
			if self.x > self.x3_reset_point:
				self.x = self.initial_x
			destination_surface.blit(self.image, (self.x, self.y))
			destination_surface.blit(self.image, (self.x-self.w, self.y))
			
	def get_scroll_direction(self):
		return self.scroll_direction
		
	def set_scroll_direction(self, value):
		self.scroll_direction = value
		
	def get_scroll_speed(self):
		return self.scroll_speed
		
	def set_scroll_speed(self, value):
		self.scroll_speed = value
		
	def reset_scroll_speed(self):
		self.scroll_speed = self.default_scroll_speed
			
# ======================================================== #

class EwFont(EwObject):
	
	def __init__(self, x, y, w, h, filename, text, color):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.filename = filename
		self.text = text
		self.color = color
		self.font = pygame.font.Font(os.path.join(PATH, filename), self.w+self.h)
		self.image = self.font.render(self.text, 1, self.color)
		self.transform()
		
	def transform(self):
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		
	def draw(self, destination_surface):
		destination_surface.blit(self.image, (self.x, self.y))
		
	def get_text(self):
		return self.text
	
	def set_text(self, value):
		self.text = value
		
	def get_color(self):
		return self.color
		
	def set_color(self, value):
		self.color = value

# ======================================================== #

class EwShape(EwObject):
	
	def __init__(self, x, y, w, h, color, thickness):
		
		EwObject.__init__(self, x, y, w, h)
		
		self.color = color
		self.thickness = thickness
		
	def get_color(self):
		return self.color
		
	def set_color(self, value):
		self.color = value
		
	def get_thickness(self):
		return self.thickness
		
	def set_thickness(self, value):
		self.thickness = value
		
class EwRect(EwShape):
	
	def __init__(self, x, y, w, h, color=(255,255,255), thickness=1):
		
		EwShape.__init__(self, x, y, w, h, color, thickness)
		
	def draw(self, destination_surface):
		pygame.draw.rect(destination_surface, self.color, (self.x, self.y, self.w, self.h), self.thickness)
		
	def draw_ellipse(self, destination_surface):
		pygame.draw.ellipse(destination_surface, self.color, (self.x, self.y, self.w, self.h), self.thickness)

# ======================================================== #

class EwAbstractButton(EwFont):
	
	def __init__(self, action):
		
		self.action = action
	
	def __call__(self):
		apply(action)
		
class EwButton(EwAbstractButton, EwImage):
	
	def __init__(self, x, y, w, h, filename, action):
		
		EwAbstractButton.__init__(self, action)
		EwImage.__init__(self, x, y, w, h, filename)
		
class EwRawButton(EwAbstractButton, EwShape):
	
	def __init__(self, x, y, w, h, color, thickness, action):
		
		EwAbstractButton.__init__(self, ewfont, action)
		EwShape.__init__(self, x, y, w, h, color, thickness)
