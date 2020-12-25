#################### Santathon : By Filip Hedman ####################
####################        Version : 1.4        ####################
####################          Framemaker         ####################

#Importing stuff.
import pygame
import sys
import random
import os
import math

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
input_release_space = False

input_short_tab = False

input_long_a = False
input_long_d = False

input_short_a = False
input_short_d = False

input_short_enter = False

input_short_1 = False
input_short_2 = False
input_short_3 = False
input_short_4 = False

#RANDOM.
if not os.path.isdir("save"):
	os.mkdir("save")

	#The resolutions of the "internal" and "external" surfaces. (The game always renders at 4k and then downscales it or upscales it to whatever resolution you want to see.)
	#Yes, this does cause lower performance but it is a very easy way to make the game compatible with any resolution as long as it is 16:9 aspect ratio.
	#There are probably better ways to do this but this works well for now.
camera_resolution = [1920, 1080]
window_resolution = [1920, 1080]

	#Player cordinates.
santa_cords = [150, 625]
	
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

	#Used to track location of the score in passive game mode.
passive_score_cords = [865, 435]

	#Tracks what part of the player animation santa is currently on.
santa_frame = 0

	#Timer variable used to track time. Pretty simple.
timer = 20

	#Coordinates of santas hitbox.
santa_r_cords = [santa_cords[0] + 15, santa_cords[1]]

	#Tracks if new tree tile can be spawned.
tree_collided = False

	#Tracks if debug mode is on or off.
debug = False

	#Tree list. Contains tree objects.
tree_list = []

	#Determines if tree will be spawned or not.
tree_spawned = False

	#Speed of all the moving objects on screen.
game_speed = False

	#Determines score multiplier.
score_boost = 1

	#List that keeps all small stone objects.
small_stone_list = []

	#Coordinates for ground gap.
gap_cords = [1920, 725]

	#Size of the ground gap.
gap_resolution = [250, 1080]

	#The positions of the menu options
resolution_sign_cords = [830, 820]
resolution_1_cords = [100, 950] 
resolution_2_cords = [600, 950]
resolution_3_cords = [1100, 950]
resolution_4_cords = [1600, 950]

	#Opacity of resolution options in menus.
resolution_opacity = 255

	#Determines what resolution you have selected at the moment.
current_resolution = "1080"

	#Holds the amount of frames the spacebar has been pressed down.
space_hold = 0

	#List that contains all the snow flake objects.
flake_list = []

	#Sun and moon coordinates.
sunmoon_cords = [1500, 750]

	#Sun and moon direction.
sunmoon_direction = "up"

	#Determines if the sun or the moon is active.
sunmoon_mode = "sun"

	#The oopacity of night_s.
night_s_opacity = 0

	#The speed that the sun and moon moves at (vertically).
sunmoon_speed = -0.5

 	#What mode was sunmoon in last frame?
sunmmon_pastmode = "nothing"

	#Coordinates of mountains.
mountain_cords = [1920, 725 - 256]

	#Mountain Oopacity
mountain_opacity = 0

	#Mountain shader cords.
mountain_shader_cords = [-4, 0]

	#Opacity of the hole darkener.
hole_opacity = 10

	#Ground opacity.
ground_opacity = 0

	#hole background coordinates.
background_cords = [0, 0]

	#Sky color.
sky_color = [150, 200, 255]

	#Target fps.
target_fps = 80

	#Opacity of the second hole_background darkener.
hole_opacity_2 = 100

	#The position to blit the second darkener surface to.
hole_background_darkener_2_cords = [0, 0]

	#The position to blit the darkener surface to.
hole_background_darkener_cords = [0, 0]

#If high score save file exists, load high score from it. Otherwise, just set it to 0.
if os.path.isdir("save"):
	if os.path.isfile("save/high_score.txt"):
		file = open("save/high_score.txt", "r")
		value = file.read()
		if not value == 0:
			high_score = float(value)
		file.seek(0)
		file.close()
	else:
		high_score = 0

#Creating the two main surfaces.
camera = pygame.Surface(camera_resolution)
window = pygame.display.set_mode(window_resolution)


#Floor obstructions.
floor_obstruction_s = pygame.image.load("sprites/static/stone.png").convert_alpha()
floor_obstruction_s = pygame.transform.scale(floor_obstruction_s, (64, 80))

#Trees in the background
tree_s = pygame.image.load("sprites/static/tree.png").convert_alpha()
tree_s = pygame.transform.scale(tree_s, (128, 256))

#Small stones in the ground.
stone_1_s = pygame.image.load("sprites/static/small_stones/1.png").convert_alpha()
stone_1_s = pygame.transform.scale(stone_1_s, (64, 64))

stone_2_s = pygame.image.load("sprites/static/small_stones/2.png").convert_alpha()
stone_2_s = pygame.transform.scale(stone_2_s, (64, 64))

#The sun.
sun_s = pygame.image.load("sprites/static/sun.png").convert_alpha()
sun_s = pygame.transform.scale(sun_s, (128, 128))

#The moon.
moon_s = pygame.image.load("sprites/static/moon.png").convert_alpha()
moon_s = pygame.transform.scale(moon_s, (128, 128))

#Mountains.
mountain_s = pygame.image.load("sprites/static/mountains.png").convert_alpha()
mountain_s = pygame.transform.scale(mountain_s, (512, 256))

#Mountain shader.
mountain_shader = pygame.Surface((1, 1)).convert_alpha()
mountain_shader.fill((0, 0, 0))

#Shading mountains.
thing = [0, 0, 0, 0]
while mountain_opacity < 130:
	mountain_opacity += 0.5
	mountain_shader.set_alpha(mountain_opacity)
	mountain_shader_cords[1] += 1
	mountain_shader_cords[0] = -1
	while mountain_shader_cords[0] < 512:
		if mountain_shader_cords[0] > -1:
			if mountain_shader_cords[0] < 512:
				if mountain_shader_cords[1] > 0:
					if mountain_shader_cords[1] < 256:
						thing = mountain_s.get_at(mountain_shader_cords)
		if not thing[3] < 255:
			mountain_s.blit(mountain_shader, (mountain_shader_cords))
		mountain_shader_cords[0] += 1

#Ground surface(single color) and ground rect.
ground_s = pygame.Surface((1920, 355)).convert()
ground_s.fill((255, 255, 255))

ground_r = ground_s.get_rect()
ground_r.topleft = (0, 725)

#Shading ground surface.
ground_s_shader = pygame.Surface((1920, 4)).convert_alpha()
ground_s_shader.fill((0, 0, 0))
while ground_opacity < 25:
	ground_s_shader.set_alpha(ground_opacity)
	ground_s.blit(ground_s_shader, (0, ground_opacity*16))
	ground_opacity += 0.25


#Tree class.
class tree_o():
	def __init__(self):
		self.image = tree_s
		self.rect = self.image.get_rect()
		self.cords = [1920, 725 - 256]
		self.rect.topleft = self.cords
	def logic(self):
		#self.cords[0] -= game_speed
		self.rect.topleft = self.cords
		if self.cords[0] < -512:
			return "destroy"
		if self.rect.colliderect(void_r):
			return "destroy"

#Floor obstruction constructors.
	#Object number 1.
class floor_obstruction():
	def __init__(self):
		self.image = floor_obstruction_s
		self.rect = pygame.Rect(0, 0, 50, 70)
		self.cords = [1920, 725 - 80]
	def logic(self):
		#self.cords[0] -= game_speed
		self.rect.topleft = (self.cords[0] + 7, self.cords[1] + 10)
		if self.cords[0] < -128:
			return "destroy"
		if self.rect.colliderect(void_r):
			return "destroy"

#Small stones.
class small_stone():
	def __init__(self):
		self.image = random.choice((stone_1_s, stone_2_s))
		self.cords = [1920, random.randint(725, 1050)]
	def logic(self):
		self.cords[0] -= game_speed
		camera.blit(self.image, self.cords)
		if self.cords[0] < 0 - 64:
			return "destroy"


#Snow flake that fall from the top of the screen.
class snow_flake():
	def __init__(self):
		self.image = pygame.Surface((4, 4))
		self.image.fill((255, 255, 255))
		self.cords = [random.randint(0, 10000), -4]
		self.speed = random.randint(4, 8)
		self.swing = random.randint(0, 1)
		self.timer = 100
	def logic(self):
		self.timer -= 1 * delta
		if self.timer < 0:
			self.timer = 100
			if self.swing == 0:
				self.swing = 1
			else:
				self.swing = 0
		if self.swing == 0:
			self.cords[0] -= (self.timer/50)*delta
		if self.swing == 1:
			self.cords[0] += (self.timer/50)*delta
		self.cords[1] += self.speed * delta
		self.cords[0] -= game_speed
		camera.blit(self.image, self.cords)
		if self.cords[1] > 10000:
			return "destroy"


#Darkness surface during night time.
night_s = pygame.Surface((camera_resolution)).convert_alpha()
night_s.fill((0, 0, 0))
night_s.set_alpha(night_s_opacity)

#Hole in ground entity.
void_s = pygame.Surface(gap_resolution)
void_s.fill((150, 200, 255))
void_r = pygame.Rect(gap_cords[0], 1920, 64 + santa_running_speed/100, 1080)


#Background of ground hole.
hole_background = pygame.Surface(gap_resolution).convert_alpha()
hole_background.fill((255, 255, 255))
hole_background_darkener = pygame.Surface((gap_resolution[0], 4)).convert_alpha()
hole_background_darkener.fill((0, 0, 0))
hole_background_darkener_2 = pygame.Surface((4, 355)).convert_alpha()
hole_background_darkener_2.fill((0, 0, 0))


#Adding small stones to hole_background.
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_1_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))

hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64))) 
hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))
hole_background.blit(stone_2_s, (random.randint(0, 250 - 64), random.randint(0, 355 - 64)))


#Blits darkener surface to hole background surface to make a fade effect where it gets darker the further down the hole it gets.
while True:
	hole_background_darkener.set_alpha(hole_opacity)
	hole_opacity += 2
	hole_background_darkener_cords[1] += 4
	hole_background.blit(hole_background_darkener, hole_background_darkener_cords)
	if hole_background_darkener_cords[1] > 355:
		break

#Blits second darkener surface from left to right of on top of the hole_background surface. It is the brightest in the middle and darkest at the edges.
while True:
	hole_background_darkener_2.set_alpha(hole_opacity_2)
	hole_background_darkener_2_cords[0] += 4
	if hole_background_darkener_2_cords[0] < 125:
		hole_opacity_2 -= 2.5
	if hole_background_darkener_2_cords[0] > 125:
		hole_opacity_2 += 2.5
	if hole_opacity_2 < 0:
		hole_opacity_2 = 0
	hole_background.blit(hole_background_darkener_2, hole_background_darkener_2_cords)
	if hole_background_darkener_2_cords[0] > 250:
		break


#Rect object that tracks if a new tree object should spawn or not.
tree_checker = pygame.Rect(1920 + (7 + santa_running_speed/200), 725 - 256, 128, 256)

#Loading font "ebrima.ttf" in different sizes. 
ebrima_main_menu = pygame.font.Font("ebrima.ttf", 128)
ebrima_main_menu_small = pygame.font.Font("ebrima.ttf", 42)
ebrima_active_game = pygame.font.Font("ebrima.ttf", 42)
ebrima_active_game_status = pygame.font.Font("ebrima.ttf", 26)
title_cords = [640, 250]


#Creating text surfaces from fonts.
game_title = ebrima_main_menu.render("Santathon", True, (0, 0, 0)).convert_alpha()
game_title_small = ebrima_main_menu_small.render("Hold Spacebar", True, (0, 0, 0)).convert_alpha()

passive_title = ebrima_main_menu.render("Game Over", True, (0, 0, 0)).convert_alpha()
passive_title_small = ebrima_main_menu_small.render(f"Score: {score}", True, (0, 0, 0)).convert_alpha()

text_double_score = ebrima_active_game_status.render("Double score!", True, (255, 255, 0)).convert_alpha()

#Menu settings.
	#Title of resolution setting section of main menu.
resolution_sign_s = ebrima_main_menu_small.render("Resolutions", True, (0, 0, 0)).convert_alpha()

	#Resolution settings that have not been chosen (They remain black while it is not the selected option).
resolution_off_1_s = ebrima_main_menu_small.render("1280x720", True, (0, 0, 0)).convert_alpha()
resolution_off_2_s = ebrima_main_menu_small.render("1920x1080", True, (0, 0, 0)).convert_alpha()
resolution_off_3_s = ebrima_main_menu_small.render("2560x1440", True, (0, 0, 0)).convert_alpha()
resolution_off_4_s = ebrima_main_menu_small.render("3840x2160", True, (0, 0, 0)).convert_alpha()

	#Resolution settings that have been chosen (They are yellow while they are chosen).
resolution_on_1_s = ebrima_main_menu_small.render("1280x720", True, (255, 255, 0)).convert_alpha()
resolution_on_2_s = ebrima_main_menu_small.render("1920x1080", True, (255, 255, 0)).convert_alpha()
resolution_on_3_s = ebrima_main_menu_small.render("2560x1440", True, (255, 255, 0)).convert_alpha()
resolution_on_4_s = ebrima_main_menu_small.render("3840x2160", True, (255, 255, 0)).convert_alpha()


#Setting up player assets and stuff.
#           (Santa Claus)
santa_s_running_1 = pygame.image.load("sprites/animations/running/santa_running_1.png").convert_alpha()
santa_s_running_1 = pygame.transform.scale(santa_s_running_1, (96, 100))

santa_s_running_2 = pygame.image.load("sprites/animations/running/santa_running_2.png").convert_alpha()
santa_s_running_2 = pygame.transform.scale(santa_s_running_2, (96, 100))

santa_s_running_3 = pygame.image.load("sprites/animations/running/santa_running_3.png").convert_alpha()
santa_s_running_3 = pygame.transform.scale(santa_s_running_3, (96, 100))

santa_s_running_4 = pygame.image.load("sprites/animations/running/santa_running_4.png").convert_alpha()
santa_s_running_4 = pygame.transform.scale(santa_s_running_4, (96, 100))

santa_r = pygame.Rect(santa_r_cords, (50, 100))

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
	global gap_cords
	global resolution_opacity
	global sunmoon_speed
	global sunmoon_cords
	global sunmoon_mode
	global sunmoon_direction
	global night_s_opacity
	global sky_color
	santa_running_speed = 0
	santa_cords = [150, 600]
	santa_jump_speed = 0
	for f in obstruction_list:
		obstruction_list.clear()
	fade = False
	fade2 = False
	menu_alpha = 255
	menu_small_alpha = 255
	title_cords = [640, 250]
	game_location = "passive_game"
	passive_title.set_alpha(255)
	passive_title_small.set_alpha(255)
	gap_cords = [1920, 725]
	resolution_opacity = 255
	sunmoon_speed = -0.5
	sunmoon_cords = [1500, 750]
	sunmoon_mode = "sun"
	sunmoon_direction = "up"
	night_s_opacity = 0
	sky_color = [150, 200, 255]


#Creating object for tracking time.
clock = pygame.time.Clock()

#Start of main game loop.
while True:

#Checking time spent between frames.
	delta = clock.tick(target_fps)
	delta = delta/12.5
	print(delta)

#Changing framerate depending on which one of the number keys you pressed the most recently. 
	if input_short_1 == True:
		target_fps = 30
	if input_short_2 == True:
		target_fps = 60
	if input_short_3 == True:
		target_fps = 80
	if input_short_4 == True:
		target_fps = 120

#Setting the window caption. There are 40 spaces between game title and framerate numbers.
	pygame.display.set_caption(f"Santathon                                        Version: 1.4DEV                                        Framerate: {int(clock.get_fps())}")

#Setting the window icon.
	icon = pygame.image.load("icon.png").convert_alpha()
	pygame.display.set_icon(icon)


#Resetting camera surface each frame. No leftovers from last frame allowed!
	camera.fill(sky_color)
	#camera.fill((0, 0, 0)) 

#Taking all inputs. Quitting the game if the "x" in the corner is pressed.
	input_short_space = False
	input_short_tab = False
	input_short_a = False
	input_short_d = False
	input_short_enter = False
	input_release_space = False
	input_short_1 = False
	input_short_2 = False
	input_short_3 = False
	input_short_4 = False
	for f in pygame.event.get():
		if f.type == pygame.QUIT:
			exit()
		if f.type == pygame.KEYDOWN:
			if f.key == pygame.K_SPACE:
				input_long_space = True
				input_short_space = True
			if f.key == pygame.K_TAB:
				input_short_tab = True
			if f.key == pygame.K_a:
				input_long_a = True
				input_short_a = True
			if f.key == pygame.K_d:
				input_long_d = True
				input_short_d = True
			if f.key == pygame.K_1:
				input_short_1 = True
			if f.key == pygame.K_2:
				input_short_2 = True
			if f.key == pygame.K_3:
				input_short_3 = True
			if f.key == pygame.K_4:
				input_short_4 = True
			if f.key == pygame.K_RETURN:
				input_short_enter = True


		if f.type == pygame.KEYUP:
			if f.key == pygame.K_SPACE:
				input_long_space = False
				input_release_space = True
			if f.key == pygame.K_a:
				input_long_a = False
			if f.key == pygame.K_d:
				input_long_d = False


#Main menu logic.
	if game_location == "main_menu":

	#If the player holds the spacebar for 0.5 seconds the main menu will start to fade away.
		if space_hold >= 40:
			fade = True
			

	#This is what happens when the fade has begun.
		if fade == True:
			title_cords[1] += (0.1 * (350 - title_cords[1])) * delta
			menu_small_alpha -= 16 * delta
			game_title_small.set_alpha(menu_small_alpha)
			resolution_opacity -= 16 * delta
		if (350 - title_cords[1]) < 1:
			fade = False
			fade2 = True

	#Drawing the game title and the instruction below it.
		camera.blit(game_title, title_cords)
		camera.blit(game_title_small, (800, 435))


	#If the spacebar is held down, the space_hold variable will add +1 every frame.
		if input_long_space == True:
			space_hold += 1 * delta
		if input_long_space == False:
			space_hold = 0

	#Resolution settings.
		#This text will always be the same no matter what resolution is selected since it is the title of the resolution settings section of the main menu.
		camera.blit(resolution_sign_s, resolution_sign_cords)

		#Setting the opacity of the resolution settings.
		resolution_sign_s.set_alpha(resolution_opacity)

		resolution_off_1_s.set_alpha(resolution_opacity)
		resolution_off_2_s.set_alpha(resolution_opacity)
		resolution_off_3_s.set_alpha(resolution_opacity)
		resolution_off_4_s.set_alpha(resolution_opacity)

		resolution_on_1_s.set_alpha(resolution_opacity)
		resolution_on_2_s.set_alpha(resolution_opacity)
		resolution_on_3_s.set_alpha(resolution_opacity)
		resolution_on_4_s.set_alpha(resolution_opacity)

		#Drawing resolution settings using current_resolution variable to determine what settings should be colored yellow instead of black. There is also an animation where the text rises up a little bit when it is selected.
		if current_resolution == "720":
			camera.blit(resolution_on_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_1_cords[1] > 900:
				resolution_1_cords[1] -= ((resolution_1_cords[1] - 900)/5) * delta
		else:
			if resolution_1_cords[1] < 950:
				resolution_1_cords[1] += ((950 - resolution_1_cords[1])/5) * delta

		if current_resolution == "1080":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_on_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_2_cords[1] > 900:
				resolution_2_cords[1] -= ((resolution_2_cords[1] - 900)/5) * delta
		else:
			if resolution_2_cords[1] < 950:
				resolution_2_cords[1] += ((950 - resolution_2_cords[1])/5) * delta

		if current_resolution == "1440":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_on_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_3_cords[1] > 900:
				resolution_3_cords[1] -= ((resolution_3_cords[1] - 900)/5) * delta
		else:
			if resolution_3_cords[1] < 950:
				resolution_3_cords[1] += ((950 - resolution_3_cords[1])/5) * delta

		if current_resolution == "2160":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_on_4_s, resolution_4_cords)
			if resolution_4_cords[1] > 900:
				resolution_4_cords[1] -= ((resolution_4_cords[1] - 900)/5) * delta
		else:
			if resolution_4_cords[1] < 950:
				resolution_4_cords[1] += ((950 - resolution_4_cords[1])/5) * delta

		#Taking input and changing current_resolution setting.
		if input_short_a == True:
			if current_resolution == "720":
				current_resolution = "2160"
			elif current_resolution == "1080":
				current_resolution = "720"
			elif current_resolution == "1440":
				current_resolution = "1080"
			elif current_resolution == "2160":
				current_resolution = "1440"
				

		if input_short_d == True:
			if current_resolution == "720":
				current_resolution = "1080"
			elif current_resolution == "1080":
				current_resolution = "1440"
			elif current_resolution == "1440":
				current_resolution = "2160"
			elif current_resolution == "2160":
				current_resolution = "720"

		#Activating selected resolution setting if user presses enter or space (short).
		if current_resolution == "720":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [1280, 720]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "1080":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [1920, 1080]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "1440":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [2560, 1440]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "2160":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [3840, 2160]
				window = pygame.display.set_mode(window_resolution)


	#The second phase concists of the game title fading away as the alpha value gets lower.
		if fade2 == True:
			menu_alpha -= 12 * delta
			game_title.set_alpha(menu_alpha)


	#If the second fade is over the main game will start.
		if menu_alpha < 0:
			game_location = "active_game"
			

#Passive game logic
	if game_location == "passive_game":


	#If the spacebar is held down, the space_hold variable will add +1 every frame.
		if input_long_space == True:
			space_hold += 1 * delta
		if input_long_space == False:
			space_hold = 0

	#If the player holds the spacebar for 0.5 seconds the main menu will start to fade away.
		if space_hold >= 40:
			fade = True

#Resolution settings.
		#This text will always be the same no matter what resolution is selected since it is the title of the resolution settings section of the main menu.
		camera.blit(resolution_sign_s, resolution_sign_cords)

		#Setting the opacity of the resolution settings.
		resolution_sign_s.set_alpha(resolution_opacity)

		resolution_off_1_s.set_alpha(resolution_opacity)
		resolution_off_2_s.set_alpha(resolution_opacity)
		resolution_off_3_s.set_alpha(resolution_opacity)
		resolution_off_4_s.set_alpha(resolution_opacity)

		resolution_on_1_s.set_alpha(resolution_opacity)
		resolution_on_2_s.set_alpha(resolution_opacity)
		resolution_on_3_s.set_alpha(resolution_opacity)
		resolution_on_4_s.set_alpha(resolution_opacity)

		#Drawing resolution settings using current_resolution variable to determine what settings should be colored yellow instead of black. There is also an animation where the text rises up a little bit when it is selected.
		if current_resolution == "720":
			camera.blit(resolution_on_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_1_cords[1] > 900:
				resolution_1_cords[1] -= ((resolution_1_cords[1] - 900)/5) * delta
		else:
			if resolution_1_cords[1] < 950:
				resolution_1_cords[1] += ((950 - resolution_1_cords[1])/5) * delta

		if current_resolution == "1080":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_on_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_2_cords[1] > 900:
				resolution_2_cords[1] -= ((resolution_2_cords[1] - 900)/5) * delta
		else:
			if resolution_2_cords[1] < 950:
				resolution_2_cords[1] += ((950 - resolution_2_cords[1])/5) * delta

		if current_resolution == "1440":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_on_3_s, resolution_3_cords)
			camera.blit(resolution_off_4_s, resolution_4_cords)
			if resolution_3_cords[1] > 900:
				resolution_3_cords[1] -= ((resolution_3_cords[1] - 900)/5) * delta
		else:
			if resolution_3_cords[1] < 950:
				resolution_3_cords[1] += ((950 - resolution_3_cords[1])/5) * delta

		if current_resolution == "2160":
			camera.blit(resolution_off_1_s, resolution_1_cords)
			camera.blit(resolution_off_2_s, resolution_2_cords)
			camera.blit(resolution_off_3_s, resolution_3_cords)
			camera.blit(resolution_on_4_s, resolution_4_cords)
			if resolution_4_cords[1] > 900:
				resolution_4_cords[1] -= ((resolution_4_cords[1] - 900)/5) * delta
		else:
			if resolution_4_cords[1] < 950:
				resolution_4_cords[1] += ((950 - resolution_4_cords[1])/5) * delta

		#Taking input and changing current_resolution setting.
		if input_short_a == True:
			if current_resolution == "720":
				current_resolution = "2160"
			elif current_resolution == "1080":
				current_resolution = "720"
			elif current_resolution == "1440":
				current_resolution = "1080"
			elif current_resolution == "2160":
				current_resolution = "1440"
				

		if input_short_d == True:
			if current_resolution == "720":
				current_resolution = "1080"
			elif current_resolution == "1080":
				current_resolution = "1440"
			elif current_resolution == "1440":
				current_resolution = "2160"
			elif current_resolution == "2160":
				current_resolution = "720"


		#Activating selected resolution setting if user presses enter or space (short).
		if current_resolution == "720":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [1280, 720]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "1080":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [1920, 1080]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "1440":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [2560, 1440]
				window = pygame.display.set_mode(window_resolution)

		if current_resolution == "2160":
			if input_short_enter == True or input_release_space == True:
				window_resolution = [3840, 2160]
				window = pygame.display.set_mode(window_resolution)


	#This is what happens when the fade has begun.
		if fade == True:
			title_cords[1] += (0.1 * (350 - title_cords[1])) * delta
			menu_small_alpha -= 16 * delta
			passive_title_small.set_alpha(menu_small_alpha)
			resolution_opacity -= 16 * delta
		if (350 - title_cords[1]) < 1:
			fade = False
			fade2 = True

	#Drawing the passive title and the score below it. Also updating score font surface to match current score.
		passive_title_small = ebrima_main_menu_small.render(f"Score: {int(score)}", True, (0, 0, 0)).convert_alpha()
		passive_title_small.set_alpha(menu_small_alpha)
		passive_title_high_score = ebrima_main_menu_small.render(f"High Score: {int(high_score)}", True, (0, 0, 0)).convert_alpha()
		passive_title_high_score.set_alpha(menu_small_alpha)
		camera.blit(passive_title, (title_cords[0] - 15, title_cords[1]))
		camera.blit(passive_title_small, passive_score_cords)
		camera.blit(passive_title_high_score, (passive_score_cords[0] - 45, passive_score_cords[1] + 50))


	#The second phase concists of the passive title fading away as the alpha value gets lower.
		if fade2 == True:
			menu_alpha -= 12 * delta
			passive_title.set_alpha(menu_alpha)


	#If the second fade is over the main game will start.
		if menu_alpha < 0: 
			game_location = "active_game"
			score = 0

#Active game logic
	if game_location == "active_game":


	#Adding score each frame.
		score += ((0.01 + (santa_running_speed/7000)) * score_boost) * delta

	#Speed of all the moving objects on screen.
		game_speed = (8 + santa_running_speed/250) * delta


	#Sun and moon logic.
		sunmoon_cords[0] -= 0.35 * delta

		#Changing sunmoon_speed variable based on if direction is "up" or "down"
		if sunmoon_direction == "up":
			sunmoon_speed -= 0.0025 * delta
		if sunmoon_direction == "down":
			sunmoon_speed += 0.0025 * delta


		#Limiting the speed of the sun and the moon
		if sunmoon_speed > 0.5 * delta:
			sunmoon_speed = 0.5 * delta
		if sunmoon_speed < -0.5 * delta:
			sunmoon_speed = -0.5 * delta

		#Moving the sun/moon vertically based on speed variable
		sunmoon_cords[1] += sunmoon_speed


		#Changing direction when sun/moon has reached a certain position in the sky.
		if sunmoon_cords[1] < 180:
			sunmoon_direction = "down"
		if sunmoon_cords[1] > 750:
			sunmoon_direction = "up"

		#Changing between sun and moon every time it reaches it's low state.
		if sunmoon_direction == "up":
			if not sunmoon_speed == -0.6:
				if sunmoon_speed > 0:
					sunmoon_speed = -0.6
					sunmoon_cords[0] = 1500
					if sunmoon_mode == "sun":
						sunmoon_mode = "moon"
					else:
						sunmoon_mode = "sun"

		#Blitting the sun/moon. Changing sky color based on sunmoon_mode.
		if sunmoon_mode == "sun":
			camera.blit(sun_s, sunmoon_cords)
			if sky_color[0] < 150:
				sky_color[0] += 0.565 * delta
			if sky_color[1] < 200:
				sky_color[1] += 0.75 * delta
			if sky_color[2] < 255: 
				sky_color[2] += 0.96 * delta
		if sunmoon_mode == "moon":
			if sky_color[0] > 37:
				sky_color[0] -= 0.565 * delta
			if sky_color[1] > 50:
				sky_color[1] -= 0.75 * delta
			if sky_color[2] > 63:
				sky_color[2] -= 0.96 * delta
			camera.blit(moon_s, sunmoon_cords)

		#Limit sky color so it can't go too high or too low.
			if sky_color[0] > 150:
				sky_color[0] = 150
			if sky_color[1] > 200:
				sky_color[1] = 200
			if sky_color[2] > 255:
				sky_color[2] = 255

			if sky_color[0] < 37:
				sky_color[0] = 37
			if sky_color[1] < 50:
				sky_color[1] = 50
			if sky_color[2] < 63:
				sky_color[2] = 63

	#Mountain logic.
		mountain_cords[0] -= (game_speed/6)

		camera.blit(mountain_s, (mountain_cords[0] - 512*4, mountain_cords[1]))

		camera.blit(mountain_s, (mountain_cords[0] - 512*3, mountain_cords[1]))

		camera.blit(mountain_s, (mountain_cords[0] - 512*2, mountain_cords[1]))

		camera.blit(mountain_s, (mountain_cords[0] - 512, mountain_cords[1]))

		camera.blit(mountain_s, mountain_cords)

		camera.blit(mountain_s, (mountain_cords[0] + 512, mountain_cords[1]))

		camera.blit(mountain_s, (mountain_cords[0] + 512*2, mountain_cords[1]))

		camera.blit(mountain_s, (mountain_cords[0] + 512*3, mountain_cords[1]))

		if mountain_cords[0] < 0:
			mountain_cords[0] = 512*4


	#Cycling through tree list and executing functions within each tree object in the list.
		for f in tree_list:
			thing = f.logic()
			if thing == "destroy":
				tree_list.remove(f)
				thing = "nothing"

	#Rect object that tracks if a new tree object should spawn or not.
		tree_checker = pygame.Rect(1920 + (7 + santa_running_speed/200), 725 - 256, 128, 256) 


	#Blitting trees to camera.
		for f in tree_list:
			f.cords[0] -= game_speed
			camera.blit(f.image, f.cords)


	#Blitting obstacles to camera.
		for f in obstruction_list:
			f.cords[0] -= game_speed
			camera.blit(f.image, f.cords)


	#Blitting ground surface.
		camera.blit(ground_s, (0, 725))

	#Blitting ground line.
		#camera.blit(ground_line_s, (0, 725))

	#Creating new small stones in the ground.
		thing = random.randint(0, 1)
		if thing == 0:
			thing = small_stone()
			small_stone_list.append(thing) 


	#Cycling through small stone list and executing functions within each small stone object in the list.
		for f in small_stone_list:
			thing = f.logic()
			if thing == "destroy":
				small_stone_list.remove(f)
				thing = "nothing"

	#Ground gap object logic.
		#updating position of gap rect.
		void_r = pygame.Rect(100, 100, 250, 1080)
		void_r.topleft = (gap_cords[0], 0)

	#Hole background logic.
		void_s.blit(hole_background, (0, 0))


	#Updating position of gap and blitting to screen. 
		void_s = pygame.transform.scale(void_s, gap_resolution)
		thing = random.randint(0, 150)
		gap_cords[0] -= game_speed
		camera.blit(void_s, gap_cords)		


	#Updating gap resolution and resetting position of "thing" variable is .
		if gap_cords[0] < 0 - 250:
			if thing == 0:
				gap_resolution = [250, 1080]
				gap_cords[0] = 1920


	#Santa logic.
		#Increasing santa speed each frame.
		santa_running_speed += 0.5 * delta

		#Jumping.
		if input_short_space == True:
			if santa_cords[1] > 575:
				if not void_r.contains(santa_r):
					if not ground_r.contains(santa_r):
						santa_jump_speed = -40

		#Adding downwards momentum each frame.
		santa_jump_speed += 2 * delta

		#Limiting the vertical speed of santa.
		if santa_jump_speed > 20 * delta:
			santa_jump_speed = 20 * delta

		#Moving santa vertically based on his speed.
		santa_cords[1] += santa_jump_speed * delta


		#Making sure santa does not move through the floor. 
		if santa_cords[1] > 625:
			if not santa_r.colliderect(ground_r):
				if not void_r.contains(santa_r):
					santa_cords[1] = 625
					santa_jump_speed = 0

		#If santa is falling down a hole. He can not move inside the ground.
		if santa_cords[0] + 90 > gap_cords[0] + 250:
			if ground_r.colliderect(santa_r):
				santa_cords[0] = gap_cords[0] + 250 - 90

		#Falling down holes.
		if santa_cords[1] > 624:
			if void_r.contains(santa_r):
				santa_cords[1] += 4 * delta


		#Once santa has fallen far enough game is over.
		if santa_cords[1] > 1000:
			game_over()
			if score > high_score:
				high_score = score
				if not os.path.isfile("save/high_score.txt"):
					file = open("save/high_score.txt", "w")
					file.close()
				file = open("save/high_score.txt", "r+")
				file.truncate(0)
				file.seek(0)
				file.write(str(int(high_score)))
				file.close()

		#Moving horizontally with a and d keys.
		if input_long_a == True:
			santa_cords[0] -= 10 * delta
		if input_long_d == True:
			santa_cords[0] += 8 * delta

		#Limit how far santa can go to the left and right of the screen.
		if santa_cords[0] < 100:
			santa_cords[0] = 100

		if santa_cords[0] > 1500:
			santa_cords[0] = 1500

		#If santa is running really close to the end of the screen he will get score faster.
		if santa_cords[0] > 960 - 48:
			score_boost = 2
		else:
			score_boost = 1

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
		santa_r_cords = [santa_cords[0] + 15, santa_cords[1]]
		santa_r.topleft = santa_r_cords

		#Collisions with obstruction objects.
		for f in obstruction_list:
			if santa_r.colliderect(f.rect):
				game_over()
				if score > high_score:
					high_score = score
					if not os.path.isfile("save/high_score.txt"):
						file = open("save/high_score.txt", "w")
						file.close()
					file = open("save/high_score.txt", "r+")
					file.truncate(0)
					file.seek(0)
					file.write(str(int(high_score)))
					file.close()

	#Spawning snow flakes two times per frame.
		thing = snow_flake()
		flake_list.append(thing)

		thing = snow_flake()
		flake_list.append(thing)

	#Running snow flakes.
		for f in flake_list:
			thing = f.logic()
			if thing == "destroy":
				flake_list.remove(f)


	#The score that is in the top of the screen.
		text_score = ebrima_active_game.render(f"Score: {int(score)}", True, (0, 0, 0))
		camera.blit(text_score, (890, 25))

	#Blitting double score to camera.
		if score_boost == 2:
			camera.blit(text_double_score, (890, 110))

	#Spawning obstruction objects based on a variable and adding them to the list.
	#Objects will only spawn if the spawn timer is ready (Once a second).
		spawn_timer -= 1
		if spawn_timer == 0:
			obstruction_object = random.randint(1, 2)
			spawn_timer = 80
			if obstruction_object == 1:
				obstruction = floor_obstruction()
				obstruction_list.append(obstruction)

	#Spawning trees when they are no longer colliding with tree checker object.
		tree_spawned = random.randint(1, 80)
		tree_collided = False 
		for f in tree_list:
			if tree_checker.colliderect(f.rect):
				tree_collided = True
		if tree_collided == False:
			if tree_spawned == 1:
				tree = tree_o()
				tree_list.append(tree)


	#Cycling through obstruction list and executing functions within each obstruction object in the list.
		for f in obstruction_list:
			thing = f.logic()
			if thing == "destroy":
				obstruction_list.remove(f)
				thing = "nothing"

	#Blitting darkness during night time when the moon is out.
		if sunmoon_mode == "moon":
			if night_s_opacity < 80:
				night_s_opacity += 0.2
		if sunmoon_mode == "sun":
			if night_s_opacity > 0:
				night_s_opacity -= 0.2
		night_s.set_alpha(night_s_opacity)
		camera.blit(night_s, (0, 0))



	#ACTIVE GAME DEBUG.
		#Changing state of debug with tab key.
		if input_short_tab == True:
			if debug == False:
				debug = True
				print("Debug mode is on.")
			else:
				debug = False

		#What is seen on screen when debug mode is on.  
		if debug == True:
			pygame.draw.rect(camera,(0, 255, 255) ,void_r)
			#pygame.draw.rect(camera,(255, 255, 0) ,ground_r)
			for f in tree_list:
				pygame.draw.rect(camera, (0, 255, 255), f.rect)
			pygame.draw.rect(camera, (255, 0, 255), santa_r)
			for f in obstruction_list:
				pygame.draw.rect(camera, (255, 0, 255), f.rect)

#Blitting camera to window surface.
	window.blit(pygame.transform.scale(camera, window_resolution), (0, 0))

#Updating the window each frame.
	pygame.display.flip()

#Counting down timer variables and resetting it when it hits 0.
	timer -= 1 * delta
	if timer < 0:
		timer = 16-(santa_running_speed/400) 
		santa_frame += 1




