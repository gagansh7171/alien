class Settings():   
	"""A class to store all settings for Alien Invasion."""
	def __init__(self):
		"""Initialize the game's static settings."""      
		    # Screen settings      
		        
		self.screen_height = 720        
		self.bg_color = (197.5, 122.3725, 197.5)        #197,122,197
		self.screen_width = 1200
		
		#ship settings
		self.ship_limit=2
		
		
		#Bullet settings
		self.bullet_width= 50
		self.bullet_height=9
		self.bullet_color=60,60,60
		self.bullets_allowed=6
		
		#Alien settigs
		self.fleet_drop_speed=4
		
		
		#How quickly the game speeds up
		self.speedup_scale=1.5
		
		#scoring
		self.alien_points=50
		
		#How quickly the alien point value should increase
		self.score_scale= 1.5
		
		self.initialize_dynamic_settings()
	
	
	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed_factor= 1.5
		self.bullet_speed_factor=3
		self.alien_speed_factor=1
		#1 for right and -1 for left		
		self.fleet_direction=1	
	
	def increase_speed(self):
		"""Increase speed settings and alien points value"""
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale
		
		self.alien_points= int(self.alien_points*self.score_scale)
		print(self.alien_points)	
