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
santa_cords = [300, 1200]
	
	#The jumping velocity of santa claus.
santa_jump_speed = 0

  
	#The horizontal velocity of santa claus.
santa_running_speed = 1


	#Random number that determines what obstruction object should be spawned next.
obstruction_object = 0 


	#List used as a container for floor obstruction objects.
obstruction_list = []


	#Limit to how fast the objects can spawn.
spawn_timer = 80


#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)


#Loading sprite assets.
#Some asset loads consist of multiple lines and are therefore clustered together to symbolize what belongs together.
floor_obstruction_1_s = pygame.image.load("sprites/floor_obstruction_1.png").convert_alpha()
floor_obstruction_1_s = pygame.transform.scale(floor_obstruction_1_s, (128, 128))


#The ground.
ground = pygame.Surface((3840, 10)).convert_alpha()


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


#Loading font "ebrima.ttf" in different sizes. 
ebrima_main_menu = pygame.font.Font("ebrima.ttf", 256)
ebrima_main_menu_small = pygame.font.Font("ebrima.ttf", 86) 
ebrima_active_game = pygame.font.Font("ebrima.ttf", 82)
title_cords = [1280, 500]


#Creating surfaces from fonts.
game_title = ebrima_main_menu.render("Santathon", True, (0, 0, 0)).convert_alpha()
game_title_small = ebrima_main_menu_small.render("Press The Spacebar", True, (0, 0, 0)).convert_alpha()


#Setting up player assets and stuff.
#           (Santa Claus)
santa_s = pygame.Surface((200, 250)).convert_alpha()
santa_s.fill((50, 50, 50))
santa_r = santa_s.get_rect() 


#Function for quitting the game.
def exit():
	pygame.quit()
	sys.exit()



#Game over function.
def game_over():
	global score
	global santa_running_speed
	global santa_cords
	global santa_jump_speed
	score = 0
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
	menu_location = "passive_game"


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
	camera.fill((255, 255, 255))

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


#Active game logic
	if game_location == "active_game":

	#Adding score each frame.
		score += 0.01 + (santa_running_speed/10000)

	#Santa logic.
		#Increasing santa speed each frame.
		santa_running_speed += 1


		#Jumping.
		if input_short_space == True:
			if santa_cords[1] > 1110:
					santa_jump_speed = -100

		#Adding downwards momentum each frame.
		santa_jump_speed += 6

		#Limiting the vertical speed of santa.
		if santa_jump_speed > 50:
			santa_jump_speed = 50

		#Moving santa vertically based on his speed.
		santa_cords[1] += santa_jump_speed


		#Making sure santa does not move through the floor.
		if santa_cords[1] > 1200:
			santa_cords[1] = 1200

		#Blitting santa to the camera.
		camera.blit(santa_s, santa_cords)

		#Collisions with obstruction objects.
		santa_r.topleft = santa_cords
		for f in obstruction_list:
			#pygame.draw.rect(camera, (255, 0, 255), f.rect)
			if santa_r.colliderect(f.rect):
				game_over()
		#pygame.draw.rect(camera, (255, 0, 255), santa_r)


	#Blitting ground.
		camera.blit(ground, (0, 1450))

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


	#Cycling through obstruction list and executinf functions within each onstruction object in the list.
		for f in obstruction_list:
			thing = f.logic()
			if thing == "destroy":
				obstruction_list.remove(f)





#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.flip()
