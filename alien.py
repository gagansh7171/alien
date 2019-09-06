import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self,ai_settings,screen):	
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		
		#load alien image and set its rect attribute
		self.image=pygame.image.load('images/alien.bmp')
		self.rect=self.image.get_rect()
		
		#Start each new alien near top left of the scren
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height
		
		#store alien's exact position
		self.x=float(self.rect.x)
		
	def blitme(self):
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""Move IITians right"""
		self.x+=self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction
		self.rect.x=self.x
	
	def check_edges(self):
		"""Return True if alien is at edge of screen"""
		screen_rect=self.screen.get_rect()
		if self.rect.right>= screen_rect.right:
			return True
		elif self.rect.left<=0:
			return True
						
