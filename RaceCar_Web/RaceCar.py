import pygame
import time
import random
pygame.init()
display_width = 500
display_height = 400
black = (0, 0, 0)
white = (255, 255,255)
block_color = ( 53, 115, 255)

car_width = 73
car_height = 73
gameDisplay = pygame.display.set_mode((display_width, display_height))    #Displays(width,length)
pygame.display.set_caption('A bit racey')
clock = pygame.time.Clock()
carImg = pygame.image.load("racecar.png")  ##uploading image

def things(thingx, thingy,thingw, thingh, color):
	pygame.draw.rect(gameDisplay, color, [thingx, thingy,thingw, thingh])

def things_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("dodged" + str(count), True, black)
	gameDisplay.blit(text,(0,0))

def car(x,y):
	
	gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()
def message_display(text):
	largeText = pygame.font.Font("freesansbold.ttf", 115)#font type and size
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2), (display_height/2))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()

	time.sleep(2)
	game_loop()

def crash():
	message_display("You Crashed")




def game_loop():

	x = (display_width * 0.45)
	y = (display_height * 0.8)
	x_change = 0
	y_change = 0
	
	thing_startx = random.randrange(0, display_width)
	thing_starty = -600 # so that it apears a little slower
	thing_speed = 10
	thing_width = 100
	thing_height = 100 #pixels
	dodged = 0

	
	gameExit = False
	while not gameExit:
	###########event handling loop###########
		#logging.info("starting event handling loop")
		for event in pygame.event.get():    #it gets any event that happens...movenment of mouse or clicking etc
			if event.type == pygame.QUIT:   # when we will click X it will quit the window
				pygame.quit()
				quit()



	################This event will handle situation when ever any key will be pressed UP##################################
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:#pressing left arrow will decrease x-axis coordinate
					x_change = -7
				if event.key == pygame.K_RIGHT:#pressing right arrow will increase x-axis coordinate
					x_change = 7
				if event.key == pygame.K_UP:#pressing UP arrow will decrease Y-axis coordinate
					y_change = -7
				if event.key == pygame.K_DOWN:#pressing Down arrow will increase x-axis coordinate
					y_change = 7
	################This event will handle situation when ever any key will be pressed UP##################################
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change = 0
		#logging.info("updating the value of x")
		x += x_change
		#logging.info("updating the value of y")
		y += y_change
		#logging.info("making the back display white")
		gameDisplay.fill(white)


		#things(thingx, thingy,thingw thingh, color)
		things(thing_startx, thing_starty, thing_width, thing_height, block_color)
		thing_starty += thing_speed
		#logging.info("calling the function of car")
		car(x,y)
		things_dodged(dodged)

		if x > display_width - car_width or x < 0:
			crash()
		if y > display_height - car_height or y < 0:
			crash()
		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0, display_width)
			dodged += 1
			thing_speed += 0.5
			thing_width += (dodged * 1.2)

		if y < thing_starty + thing_height:
			
			if x>thing_startx and x<thing_startx+thing_width or x+car_width>thing_startx and x+car_width<thing_startx+thing_width:
				crash()
		pygame.display.update()
		clock.tick(60)  ## it will just make thing move faster
game_loop()
pygame.quit()
quit()
