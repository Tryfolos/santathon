#Importing stuff.
import pygame
import sys

#Initializing pygame.
pygame.init()

#Variables.
game_location = "main_menu"
fade = False
fade2 = False
menu_small_alpha = 255
menu_alpha = 255

input_long_space = False
input_short_space = False

camera_resolution = [3840, 2160]
window_resolution = [1920,1080]

#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)

#Loading font "ebrima.ttf" in different sizes. 
ebrima_main_menu = pygame.font.Font("ebrima.ttf", 256)
ebrima_main_menu_small = pygame.font.Font("ebrima.ttf", 86) 
title_cords = [1280, 500]

#Creating surfaces from fonts.
game_title = ebrima_main_menu.render("Santathon", True, (0, 0, 0)).convert_alpha()
game_title_small = ebrima_main_menu_small.render("Press The Spacebar", True, (0, 0, 0)).convert_alpha()


#Function for quitting the game.
def exit():
	pygame.quit()
	sys.exit()


#Creating object for tracking time.
clock = pygame.time.Clock()


#Start of main game loop.
while True:

#Checking time spent between frames.
	delta = clock.tick(500)


#Setting the window caption. There are 40 spaces between game title and framerate numbers.
	pygame.display.set_caption(f"Santathon                                        Framerate: {int(clock.get_fps())}                                        Delta Time: {delta}")



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
			title_cords[1] += 0.06 * (700 - title_cords[1])
			menu_small_alpha -= 12
			game_title_small.set_alpha(menu_small_alpha)
		if (700 - title_cords[1]) < 1:
			fade = False
			fade2 = True

	#Drawing the game title and the instruction below it.
		camera.blit(game_title, title_cords)
		camera.blit(game_title_small, (1500, 870))


	#The second phase concists of the game title fading away as the alpha value gets lower.
		if fade2 == True:
			menu_alpha -= 8
			game_title.set_alpha(menu_alpha)


	#If the second fade is over the main game will start.
		if menu_alpha < 0:
			game_location == "active_game"


	#If the player presses the spacebar the main menu will start to fade away.
		if input_short_space == True:
			fade = True

#Active game logic
	if game_location == "active_game":
		pass
	#




#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.flip()
