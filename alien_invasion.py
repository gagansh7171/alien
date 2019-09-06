import pygame
import sys
from pygame.sprite import Group       # to create group of live bullets
from settings import Settings
from alien import Alien
from ship import Ship
import game_functions as gf
from button import Button
from scoreboard import Scoreboard
from game_stats import GameStats
ai_settings=Settings()
def run_game():
	pygame.init()
	screen=pygame.display.set_mode(
		(ai_settings.screen_width ,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	
	
	#Make the play button
	play_button= Button(ai_settings,screen,"Play")
	
	#Make a ship
	ship=Ship(ai_settings,screen)                                  #instance of Ship class
	
	#Make a group to store bullets in
	bullets=Group()
	
	#Make a fleet of alien   
	aliens=Group()
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	#Make stats
	stats=GameStats(ai_settings)
	
	#Make a score board
	sb= Scoreboard(ai_settings,screen,stats)
	
	#Start main loop for the game
	while True:
		gf.check_events(ai_settings,screen,stats,play_button,ship,bullets,aliens)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
			gf.check_bullet_alien_collision(ai_settings, screen,stats,sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings,stats,ship,aliens,screen,bullets)
		
		#Redraw the screen during each pass through the loop
		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)		 

run_game()

