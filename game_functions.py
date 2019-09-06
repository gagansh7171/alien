import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False
	elif event.key==pygame.K_UP:
		ship.moving_up=False
	elif event.key==pygame.K_DOWN:
		ship.moving_down=False
	
def check_keydown_events(event,ai_settings,screen,ship,bullets,stats):
	if event.key==pygame.K_RIGHT:
		#MOVE KEY TO RIGHT
		ship.moving_right=True	
	elif event.key==pygame.K_LEFT:
		#Move ship to left
		ship.moving_left=True
	elif event.key==pygame.K_UP:
		#moving ship up
		ship.moving_up=True
	elif event.key==pygame.K_DOWN:
		#moving down
		ship.moving_down=True
	elif event.key==pygame.K_SPACE:
		#fire bullet
		fire_bullets(event,ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		#Another way to exit game
		sys.exit()


def check_events(ai_settings,screen,stats,play_button,ship,bullets,aliens):
	"""Respond to keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
			
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets,stats)
			
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		
		elif event.type== pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""Start a new game when the player clicks play"""
	if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
		
		#rESET GAME settings
		ai_settings.initialize_dynamic_settings()
		
		#Reset game statistics
		stats.reset_stats()
		stats.game_active= True	
		
		#empty liat of alinessand bulets
		bullets.empty()
		aliens.empty()
		
		
		#Create new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
					
			
				
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	"""Update images on the screen  and flip to the new screen"""
	#color the background
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets.Bullets are drawn on thee background color ,dont do other way round
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	#draw ship
	ship.blitme()	
	#draw alien
	for alien in aliens:
		alien.blitme()
	#scoreboard
	
	sb.show_score()	
	#draw play button if the game is inactive
	if not stats.game_active :
		play_button.draw_button()
	#Make most recently screeen visible
	pygame.display.flip()			


def update_bullets(ai_settings,screen,ship,aliens,bullets):
	"""Update position of bullets and get rid of unwanted bullets"""
	#update bullet position
	bullets.update()
	
	#Get rid of bullets that have disappeared .
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)		


def fire_bullets(event,ai_settings,screen,ship,bullets)	:
	"""Fire bullet if limit is not reached"""
	if len(bullets)< ai_settings.bullets_allowed:
				new_bullet=Bullet(ai_settings,screen, ship)
				bullets.add(new_bullet)	

def get_number_aliens_x(ai_settings,alien_width):
	#number of alien in Aa row
	available_space_x= ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x / (2*alien_width) )
	return number_aliens_x


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#create a alien and place in the row
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width + 2*alien_width*alien_number
	alien.rect.y= alien.rect.height +2*alien.rect.height*row_number 
	alien.rect.x=alien.x
	aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
	#Create a full fleet of sliens
	#create an alien and find number of aliens in a row
	#spacing between each alien is one alien width
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	#Create the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
		#Creste an alien and place it in he row
			create_alien(ai_settings,screen,aliens,alien_number,row_number) 


def get_number_rows(ai_settings,ship_height,alien_height):
	"""Determine number of rows that alieens can fill"""
	available_space_y=(ai_settings.screen_height- (3*alien_height)-ship_height)
	number_rows= int(available_space_y/(2*alien_height))
	return number_rows
	
	
def update_aliens(ai_settings,stats,ship,aliens,screen,bullets):
	"""Check if the fleet is at an edge,and then update the positions of all aliens in the fleet"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	#look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
	
	#look for alien at bottom
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
	
	
def check_fleet_edges(ai_settings,aliens):
	"""Respond appropriately if any aliens have reached an edge """
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break


def change_fleet_direction(ai_settings,aliens):
	"""Drop fllet and change direction"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1
	
					
def check_bullet_alien_collision(ai_settings, screen,stats,sb, ship, aliens, bullets):
	"""Respond to bullet ālien collission"""
	#Check for bullets that have hit aliens and if so, get rid of these bullets
	#If so,get rid of the bullets and the alien
	collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)  # first true is for to delete bulletand second true is for delete alien
	
	if collisions:
		stats.score+=ai_settings.alien_points
		sb.prep_score()
		check_high_score(stats,sb)
	
	if len(aliens)==0:
		#Destroy existing bullets and create new fleet
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	"""REspond to ship being hit"""
	if stats.ships_left>0:
		#Decrment Ship left
		stats.ships_left-=1
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
	
		#Create a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		#Pause
		sleep(0.5)
	else:
		stats.game_active=False
		
				


def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	"""Check if any alien reached bottom"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom==screen_rect.bottom:
			#Treat this same as if ship got hit
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break
def check_high_score(stats,sb):
	"""check to see if there's neew high score"""
	if stats.score > stats.high_score:
		stats.high_score= stats.score
		sb.prep_high_score()
