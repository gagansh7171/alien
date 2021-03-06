import pygame.font

class Scoreboard():
	"""A class to report scoring information"""
	def __init__(self,ai_settings,screen,stats):
		"""Initialize scorekeeping attribute"""
		self.screen= screen
		self.screen_rect= screen.get_rect()
		self.ai_settings= ai_settings
		self.stats= stats
		
		#Font settings for scoring information
		self.text_color=(30,30,30)
		self.font= pygame.font.SysFont(None,48)
		
		#prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		
	def prep_score(self):
		"""Turn score imto rendered image"""
		score_str= str(self.stats.score)
		self.score_image= self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
		
		
		#Display scoree at the right top of rthe screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right= self.screen_rect.right-20
		self.score_rect.top=20	
	
	
	def show_score(self):
		"""Draw score to the screen"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		
	def prep_high_score(self):
		"""Turn the high score into rendered image"""
		high_score= int(round(self.stats.high_score,-1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.ai_settings.bg_color) 	
		
		#Center the high score at the top of the screen
		self.high_score_rect= self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
		
