class GameStats():
	"""Track statistics for Alien Invasion"""
	def __init__(self,ai_settings):
		"""Initialize statistics"""
		#High score should never be reset
		self.high_score=0
		self.ai_settings=ai_settings
		self.reset_stats()
		
		#start alien invasion in an inactive mode
		self.game_active=False
		
	def reset_stats(self):
		"""Initialize statistics that can change during the course of the game"""
		self.ships_left=self.ai_settings.ship_limit
		self.score=0
		self.ai_settings.alien_points=50
