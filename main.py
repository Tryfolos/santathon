#Importing stuff.
import pygame
import sys

#Initializing pygame.
pygame.init()

#Variables.
game_location = "main_menu"

camera_resolution = [1920, 1080]
window_resolution = [1920, 1080]

#Function for quitting the game.
def exit():
	pygame.quit()
	sys.exit()


#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)


#Start of main game loop.
while True:
	
#Resetting camera surface each frame. No leftovers from last frame allowed!
	room.fill((255, 255, 255))
	camera.fill((255, 255, 255))

#Taking all inputs. Quitting the game if the "x" in the corner is pressed.
	for f in pygame.event.get():
		if f.type == pygame.QUIT:
			exit()



#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.update()

