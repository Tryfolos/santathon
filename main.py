#Importing stuff.
import pygame
import sys

#Initializing pygame.
pygame.init()

#Variables.
game_location = "main_menu"
fade = False

input_long_space = False
input_short_space = False

#Loading font "ebrima.ttf" in different sizes.
ebrima_main_menu = pygame.font.Font("ebrima.ttf", 256) 
title_cords = [1280, 600]

camera_resolution = [3840, 2160]
window_resolution = [1920,1080]

#Function for quitting the game.
def exit():
	pygame.quit()
	sys.exit()


#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)


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
		if fade == True:
			title_cords[1] += 0.05 * (700 - title_cords[1])
		if (700 - title_cords[1]) < 1:
			fade = False
		game_title = ebrima_main_menu.render("Santathon", True, (0, 0, 0))
		camera.blit(game_title, title_cords)
		if input_short_space == True:
			fade = True




#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.flip()
