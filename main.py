#Importing stuff.
import pygame
import sys
import random


#Initializing pygame.
pygame.init()


#Variables.
	#This is a simple variable that describes in what state the game is currently in. It is nothing more than an organizer.
game_location = "main_menu"

	#These variables determine if it is time to fade away the main menu yet.
fade = False
fade2 = False

	#These are the variables that sets the alpha value of the text in the main menu.
menu_small_alpha = 255
menu_alpha = 255

	#This is your in game score.
score = 0

	#Keyboard inputs.
input_long_space = False
input_short_space = False

	#The resolutions of the "internal" and "external" surfaces. (The game always renders at 4k and then downscales it or upscales it to whatever resolution you want to see.)
	#Yes, this does cause lower performance but it is a very easy way to make the game compatible with any resolution as long as it is 16:9 aspect ratio.
	#There are probably better ways to do this but this works well for now.
camera_resolution = [3840, 2160]
window_resolution = [1920, 1080]

	#Player cordinates.
santa_cords = [300, 1250]
	
	#The jumping velocity of santa claus.
santa_jump_speed = 0

  
	#The horizontal velocity of santa claus.
santa_running_speed = 1


	#Random number that determines what obstruction object should be spawned next.
obstruction_object = 0 


	#List used as a container for floor obstruction objects.
obstruction_list = []


	#List used as a container for ground tile objects.
ground_list = []


	#Limit to how fast the objects can spawn.
spawn_timer = 80

	#Used to track location of the score in passive game mode.
passive_score_cords = [1730, 870]

	#Tracks what part of the player animation santa is currently on.
santa_frame = 0

	#Timer variable used to track time. Pretty simple.
timer = 20


	#Coordinates of santas hitbox.
santa_r_cords = [santa_cords[0] + 30, santa_cords[1]]


	#Tracks if new ground tile can be spawned.
tile_collided = False 


#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)


#Loading sprite assets.
#Some asset loads consist of multiple lines and are therefore clustered together to symbolize what belongs together.
	#Floor obstructions.
floor_obstruction_1_s = pygame.image.load("sprites/static/floor_obstruction_1.png").convert_alpha()
floor_obstruction_1_s = pygame.transform.scale(floor_obstruction_1_s, (128, 128))

	#Ground tiles.
ground_tile_s = pygame.image.load("sprites/static/ground_tile.png").convert_alpha()
ground_tile_s = pygame.transform.scale(ground_tile_s, (128, 128))


#Ground tile class.
ground = pygame.Surface((3840, 10)).convert_alpha()
class ground_tile():
	def __init__(self):
		self.image = ground_tile_s
		self.rect = self.image.get_rect()
		self.cords = [3840, 1450]
		self.rect.topleft = self.cords
	def logic(self):
		self.cords[0] -= 15 + int(santa_running_speed/150)
		self.rect.topleft = self.cords
		camera.blit(self.image, self.cords)
		#pygame.draw.rect(camera, (255, 0, 255), self.rect)
		#print(type(self.image))
		if self.cords[0] < - 128:
			return "destroy"

#Floor obstruction constructors.
	#Object number 1.
class floor_obstruction_1():
	def __init__(self):
		self.image = floor_obstruction_1_s
		self.rect = self.image.get_rect()
		self.cords = [3840, 1450 - 128]
		self.rect.topleft = self.cords
	def logic(self):
		self.cords[0] -= 15 + int(santa_running_speed/150)
		self.rect.topleft = (self.cords[0] - 16, self.cords[1])
		camera.blit(self.image, self.cords)
		if self.cords[0] < -128:
			return "destroy"

	#Object number 2.
class floor_obstruction_2():
	def __init__(self):
		pass


#Rect object that tracks if a new ground tile should spawn or not.
ground_checker = pygame.Rect(3840 + (15 + int(santa_running_speed/150)), 1450, 128, 128)


#Loading font "ebrima.ttf" in different sizes. 
ebrima_main_menu = pygame.font.Font("ebrima.ttf", 256)
ebrima_main_menu_small = pygame.font.Font("ebrima.ttf", 86) 
ebrima_active_game = pygame.font.Font("ebrima.ttf", 82)
title_cords = [1280, 500]


#Creating surfaces from fonts.
game_title = ebrima_main_menu.render("Santathon", True, (0, 0, 0)).convert_alpha()
game_title_small = ebrima_main_menu_small.render("Press The Spacebar", True, (0, 0, 0)).convert_alpha()

passive_title = ebrima_main_menu.render("Game Over", True, (0, 0, 0)).convert_alpha()
passive_title_small = ebrima_main_menu_small.render(f"Score: {score}", True, (0, 0, 0)).convert_alpha()


#Setting up player assets and stuff.
#           (Santa Claus)
santa_s_running_1 = pygame.image.load("sprites/animations/running/santa_running_1.png").convert_alpha()
santa_s_running_1 = pygame.transform.scale(santa_s_running_1, (192, 200))

santa_s_running_2 = pygame.image.load("sprites/animations/running/santa_running_2.png").convert_alpha()
santa_s_running_2 = pygame.transform.scale(santa_s_running_2, (192, 200))

santa_s_running_3 = pygame.image.load("sprites/animations/running/santa_running_3.png").convert_alpha()
santa_s_running_3 = pygame.transform.scale(santa_s_running_3, (192, 200))

santa_s_running_4 = pygame.image.load("sprites/animations/running/santa_running_4.png").convert_alpha()
santa_s_running_4 = pygame.transform.scale(santa_s_running_4, (192, 200))


santa_r = pygame.Rect(santa_r_cords, (100, 200)) 


#Function for quitting the game.
def exit():
	pygame.quit()
	sys.exit()



#Game over function.
def game_over():
	global santa_running_speed
	global santa_cords
	global santa_jump_speed
	global fade
	global fade2
	global menu_alpha
	global menu_small_alpha
	global title_cords
	global game_location
	santa_running_speed = 0
	santa_cords = [300, 1200]
	santa_jump_speed = 0
	for f in obstruction_list:
		obstruction_list.clear()
	fade = False
	fade2 = False
	menu_alpha = 255
	menu_small_alpha = 255
	title_cords = [1280, 500]
	game_location = "passive_game"
	passive_title.set_alpha(255)
	passive_title_small.set_alpha(255)


#Creating object for tracking time.
clock = pygame.time.Clock()


#Start of main game loop.
while True:

#Checking time spent between frames.
	delta = clock.tick(80)


#Setting the window caption. There are 40 spaces between game title and framerate numbers.
	pygame.display.set_caption(f"Santathon                                        Framerate: {int(clock.get_fps())}                                        Delta Time: {delta}")

#Setting the window icon.
	icon = pygame.image.load("icon.png").convert_alpha()
	pygame.display.set_icon(icon)



#Resetting camera surface each frame. No leftovers from last frame allowed!
	camera.fill((150, 240, 255))

#Taking all inputs. Quitting the game if the "x" in the corner is pressed.
	input_short_space = False
	for f in pygame.event.get():
		if f.type == pygame.QUIT:
			exit()
		if f.type == pygame.KEYDOWN:
			if f.key == pygame.K_SPACE:
				input_long_space = True
				input_short_space = True
		if f.type == pygame.KEYUP:
			if f.key == pygame.K_SPACE:
				input_long_space = False


#Main menu logic.
	if game_location == "main_menu":

	#If the player presses the spacebar the main menu will start to fade away.
		if input_short_space == True:
			fade = True

	#This is what happens when the fade has begun.
		if fade == True:
			title_cords[1] += 0.1 * (700 - title_cords[1])
			menu_small_alpha -= 16
			game_title_small.set_alpha(menu_small_alpha)
		if (700 - title_cords[1]) < 1:
			fade = False
			fade2 = True

	#Drawing the game title and the instruction below it.
		camera.blit(game_title, title_cords)
		camera.blit(game_title_small, (1500, 870))


	#The second phase concists of the game title fading away as the alpha value gets lower.
		if fade2 == True:
			menu_alpha -= 12
			game_title.set_alpha(menu_alpha)


	#If the second fade is over the main game will start.
		if menu_alpha < 0:
			game_location = "active_game"


	#If the player presses the spacebar the main menu will start to fade away.
		if input_short_space == True:
			fade = True

#Passive game logic
	if game_location == "passive_game":


	#If the player presses the spacebar the main menu will start to fade away.
		if input_short_space == True:
			fade = True

	#This is what happens when the fade has begun.
		if fade == True:
			title_cords[1] += 0.1 * (700 - title_cords[1])
			menu_small_alpha -= 16
			passive_title_small.set_alpha(menu_small_alpha)
		if (700 - title_cords[1]) < 1:
			fade = False
			fade2 = True

	#Drawing the passive title and the score below it. Also updating score font surface to match current score.
		passive_title_small = ebrima_main_menu_small.render(f"Score: {int(score)}", True, (0, 0, 0)).convert_alpha()
		passive_title_small.set_alpha(menu_small_alpha)
		camera.blit(passive_title, (title_cords[0] - 30, title_cords[1]))
		camera.blit(passive_title_small, passive_score_cords)


	#The second phase concists of the passive title fading away as the alpha value gets lower.
		if fade2 == True:
			menu_alpha -= 12
			passive_title.set_alpha(menu_alpha)


	#If the second fade is over the main game will start.
		if menu_alpha < 0:
			game_location = "active_game"
			score = 0


#Active game logic
	if game_location == "active_game":

	#Adding score each frame.
		score += 0.01 + (santa_running_speed/10000)

	#Santa logic.
		#Increasing santa speed each frame.
		santa_running_speed += 1


		#Jumping.
		if input_short_space == True:
			if santa_cords[1] > 1150:
					santa_jump_speed = -100

		#Adding downwards momentum each frame.
		santa_jump_speed += 6

		#Limiting the vertical speed of santa.
		if santa_jump_speed > 50:
			santa_jump_speed = 50

		#Moving santa vertically based on his speed.
		santa_cords[1] += santa_jump_speed


		#Making sure santa does not move through the floor.
		if santa_cords[1] > 1250:
			santa_cords[1] = 1250

		#Changing what frame is displayed according to santa_frame variable.
		if timer < 1:
			santa_frame += 1


		#Resetting santa_frame variable once the end of the animation has been reached.
		if santa_frame > 3:
			santa_frame = 0


		#Blitting santa to the camera.
		if santa_frame == 0:
			camera.blit(santa_s_running_1, santa_cords)

		if santa_frame == 1:
			camera.blit(santa_s_running_2, santa_cords)

		if santa_frame == 2:
			camera.blit(santa_s_running_3, santa_cords)

		if santa_frame == 3:
			camera.blit(santa_s_running_4, santa_cords)

		#Putting santas hitbox in the right place and updating coordinates based on santas cords.
		santa_r_cords = [santa_cords[0] + 30, santa_cords[1]]
		santa_r.topleft = santa_r_cords

		#Collisions with obstruction objects.
		for f in obstruction_list:
			#pygame.draw.rect(camera, (255, 0, 255), f.rect)
			if santa_r.colliderect(f.rect):
				game_over()
		#pygame.draw.rect(camera, (255, 0, 255), santa_r)
	

	#Updating ground checkers position every frame.
		ground_checker.topleft = (3840 + (15 + int(santa_running_speed/150)), 1450)


	#The score that is in the top of the screen.
		text_score = ebrima_active_game.render(f"Score: {int(score)}", True, (0, 0, 0))
		camera.blit(text_score, (1780, 50))


	#Spawning obstruction objects based on a variable and adding them to the list.
	#Objects will only spawn if the spawn timer is ready (Once a second).
		spawn_timer -= 1
		if spawn_timer == 0:
			obstruction_object = random.randint(1, 2)
			spawn_timer = 80
			if obstruction_object == 1:
				obstruction = floor_obstruction_1()
				obstruction_list.append(obstruction)

	#Spawning ground tiles when they are no longer colliding with ground checker object.
		tile_collided = False
		for f in ground_list:
			if ground_checker.colliderect(f.rect):
				tile_collided = True
		if tile_collided == False:
			ground = ground_tile()
			ground_list.append(ground)
		print(tile_collided)
		

	#Cycling through obstruction list and executing functions within each obstruction object in the list.
		for f in obstruction_list:
			thing = f.logic()
			if thing == "destroy":
				obstruction_list.remove(f)
				thing = "nothing"

	#Cycling through ground list and executing functions within each object in the list.
		for f in ground_list:
			thing = f.logic()
			if thing == "destroy":
				ground_list.remove(f)
				thing = "nothing"
		pygame.draw.rect(camera, (255, 0, 255), ground_checker)

#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.flip()

#Counting down timer variable and resetting it when it hits 0.
	timer -= 1
	if timer < 0:
		timer = 20-(santa_running_speed/450) 


