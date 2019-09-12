import pygame
import time
import random
import numpy
import operator

pygame.init()

#dimenstions of the window
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
BLOCK_SIZE = 30

FPS = 1000

font = pygame.font.SysFont("ubuntu", 25)
largefont = pygame.font.SysFont(None, 40)

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)


def draw_snake(snakelist, block_size):
	for x,y in snakelist:
		pygame.draw.rect(gameDisplay, blue, [x, y, block_size, block_size])


def display_score(score):
	text = largefont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [10,10])


def create_text_object(text, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0):
	textSurf, textRect =  create_text_object(msg, color)
	textRect.center = (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2)+y_displace
	gameDisplay.blit(textSurf, textRect)

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


#set up the display
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("PyPyper")


clock = pygame.time.Clock()

def initialize_random_position(display_width, display_height, block_size):
	x = random.randrange(0, display_width, step=block_size)
	y = random.randrange(0, display_height, step=block_size)
	# x = round(random.randrange(0, display_width - block_size,)/float(block_size))*block_size
	# y = round(random.randrange(0, display_height - block_size)/float(block_size))*block_size
	# print(x, y)
	return x, y

# Directions
ALLOWED_DIRS = ["LEFT", "RIGHT", "UP", "DOWN"]

class Agent(object):
    """Base class for all agents."""

    def __init__(self,env):

        self.env = env
        self.q_table = {}
        self.reward = 0
        self.alpha = 0.3
        self.gamma = 0.1
        self.epsilon = 0.1
        self.penalties = []
        self.total_reward = 0.0
        self.counts = 0.0

    def reset(self, destination=None):
        self.reward = 0

    def get_action(self):
        max_q = 0
        
        self.state = self.env.get_state()

        if not self.state in self.q_table:
            self.q_table[self.state] = {ac:0 for ac in self.env.valid_actions}

        action = random.choice(self.env.valid_actions)
        random_action = action

        # Exploration v/s exploitation
        if random.uniform(0, 1)>self.epsilon:
            if len(set(self.q_table[self.state].values())) == 1:
                pass
            else:
                action = max(self.q_table[self.state].items(), key=operator.itemgetter(1))[0]
        return action


    def update(self, action, reward):

        self.total_reward += reward

        self.next_state = self.env.get_state()

        #check if next_state has q_values already
        if self.next_state not in self.q_table:
            self.q_table[self.next_state] = {ac:0 for ac in self.env.valid_actions}

        # Learn policy based on state, action, reward
        old_q_value = self.q_table[self.state][action]

        #maximum q_value for next_state actions
        next_max = max(self.q_table[self.next_state].values())

        # calculate the q_value for the next_max action.
        new_q_value = (1 - self.alpha)*old_q_value + self.alpha*(reward + self.gamma*next_max)
        self.q_table[self.state][action] = new_q_value
        if random.randrange(0,5000) == 5:
            print ("LearningAgent.update(): state = {}, action = {}, reward = {}".format(self.state, action, reward))  # [debug]



class Environment(object):
	def __init__(self,
		         display_width,
		         display_height,
		         block_size,
		         valid_directions):

		self.world_width = display_width
		self.world_height = display_height
		self.block_size = block_size
		self.lead_x = display_width/2
		self.lead_y = display_height/2
		self.lead_x_change = 0
		self.lead_y_change = 0
		self.valid_actions = valid_directions

		self.highest_score_so_far = -1

		self.appleX, self.appleY = initialize_random_position(self.world_width,
			                                                  self.world_height,
			                                                  self.block_size)

	def act(self, action):
		'''
		Given an action, return the reward.
		'''
		reward = -1
		is_boundary = self.is_wall_nearby()

		if is_boundary[action]:
			reward = -5
		else:
			self.move(action)
			if self.is_goal_state(self.lead_x, self.lead_y):
				reward = 20
				self.new_apple()
		return reward

	def move(self, direction):
		x_change = 0
		y_change = 0
		
		if direction in ALLOWED_DIRS:
			if direction == "LEFT":
				x_change = -self.block_size
				y_change = 0
			elif direction == "RIGHT":
				x_change = self.block_size
				y_change = 0
			elif direction == "UP":
				x_change = 0
				y_change = -self.block_size
			elif direction == "DOWN":
				x_change = 0
				y_change = self.block_size
		else:
			print("Invalid direction.")

		self.lead_x += x_change
		self.lead_y += y_change

	def is_wall_nearby(self):
		left, right, up, down = False, False, False, False
		if self.lead_x - self.block_size < 0:
			left = True
		if self.lead_x + self.block_size >= self.world_width:
			right = True
		if self.lead_y - self.block_size < 0:
			up = True
		if self.lead_y + self.block_size >= self.world_height:
			down = True

		return {
			"LEFT":left,
			"RIGHT":right,
			"UP":up,
			"DOWN":down
		}

	def get_state(self):

		head_position = self.get_head_position()
		apple_position = self.get_appple_position()
		# apple_quadrant = self.get_apple_quadrant()
		wall_info = tuple(self.is_wall_nearby().values())
		
		# concatenating the tuples
		return head_position + apple_position + wall_info
		
	def get_next_goal(self):
		return (self.appleX, self.appleY)

	def is_goal_state(self, x, y):
		if (x-self.block_size < self.appleX <x + self.block_size  and 
			y-self.block_size < self.appleY <y + self.block_size):
			return True
		return False

	def get_head_position(self):
		return self.lead_x, self.lead_y

	def get_appple_position(self):
		return self.appleX, self.appleY

	def new_apple(self):
		self.appleX, self.appleY = initialize_random_position(self.world_width, self.world_height, self.block_size)

	def get_apple_quadrant(self):
		appleX, appleY = self.get_appple_position()
		x, y = self.get_head_position()
		quadrant = 0

		#shift the origin
		appleX -= x
		appleY -= y

		if appleX > 0 and appleY > 0: 
			quadrant = 1
		elif appleX < 0 and appleY > 0:
			quadrant = 2
		elif appleX < 0 and appleY < 0:
			quadrant = 3
		elif appleX > 0 and appleY < 0:
			quadrant = 4
		elif appleX == 0:
			if appleY > 0:
				quadrant = random.choice([1, 2])
			if appleY < 0:
				quadrant = random.choice([3, 4])
		elif appleY == 0:
			if appleX > 0:
				quadrant = random.choice([1, 4])
			if appleX < 0:
				quadrant = random.choice([2, 3])
		return quadrant

	def set_high_score(self, val):
		self.highest_score_so_far = val

	def high_score(self):
		return self.highest_score_so_far

# Initialize the environment	
env = Environment(DISPLAY_WIDTH,
	              DISPLAY_HEIGHT,
	              BLOCK_SIZE,
	              ALLOWED_DIRS)

agent = Agent(env)

gameExit = False
gameOver = False

snakelist = []
snakeLength = 1

direction = ''

while True:
	
	# for event in pygame.event.get():
	# 	if event.type == pygame.QUIT:
	# 		gameExit = True
	# 		gameOver = False
	# 	if event.type == pygame.KEYDOWN:
	# 		if event.key == pygame.K_LEFT:
	# 			direction = 'LEFT'
	# 		elif event.key == pygame.K_RIGHT:
	# 			direction = 'RIGHT'
	# 		elif event.key == pygame.K_UP:
	# 			direction = 'UP'
	# 		elif event.key == pygame.K_DOWN:
	# 			direction = 'DOWN'

	direction = agent.get_action()
	
	# Draw apple and background
	gameDisplay.fill(BACKGROUND_COLOR)
	apple = env.get_appple_position()

	if direction:
		
		reward = env.act(direction)

		agent.update(direction, reward)

		# Head of the snake
		snake_head = env.get_head_position()
		snakelist.append(snake_head)
		score = snakeLength-1

		# check if the snake hit the wall
		if reward < -1:
			gameOver = True
			if score > env.high_score():
				print("score:",score, env.high_score())
				env.set_high_score(score)
				snakelist = []
				snakeLength = 1
		
		if len(snakelist) > snakeLength:
			del(snakelist[0])

		#when snake runs into itself
		# if snake_head in snakelist[:-1] and snakeLength>1:
		# 	print("snake ran over itself",snakeLength-1)
		# 	gameOver = True

		if reward > 0:
			snakeLength += 1

		pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
		draw_snake(snakelist, BLOCK_SIZE)
		display_score(snakeLength-1)

	pygame.display.update()
	clock.tick(FPS)





def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=Fa
    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    penalties_count_after_training = a.penalties.count(1)
    print( penalties_count_after_training)
    #running 10 trials without exploration to see whether we've learned enough or not.
    a.epsilon = 0.0
    sim.run(n_trials=100)
    penalties_count_after_testing = a.penalties.count(1) - penalties_count_after_training
    print (penalties_count_after_testing)


def comprehensive_test():

    alphas = [0.3,0.5,0.7,0.9]
    gammas = [0.1,0.3,0.5,0.7]
    epsilons = [0.01, 0.1, 0.2]
    results = {}
    best_choice_alpha = []
    best_choice_gamma = []
    best_choice_epsilon = []
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials
    for n in range(10):
        for alpha in alphas:
            for gamma in gammas:
                for epsilon in epsilons:
                    penalties_count_before_trials = a.penalties.count(1)
                    a.alpha = alpha
                    a.gamma = gamma
                    a.epsilon = epsilon
                    sim = Simulator(e, update_delay=0.0001, display=False)
                    sim.run(n_trials=100)
                    penalties_count_after_trials = a.penalties.count(1) - penalties_count_before_trials
                    results[(alpha,gamma,epsilon)] = {'ratio' : a.total_reward/a.counts,
                   									   'penalties' : penalties_count_after_trials
                   									   }
        x,y,z =  max(results.iteritems(), key=operator.itemgetter(1))[0]
        best_choice_alpha.append(x)
        best_choice_gamma.append(y)
        best_choice_epsilon.append(z)
    sorted_reults = sorted(results.items(), key=lambda x: x[1]['penalties'], reverse=True)
    print (sorted_reults)
    best_choice = (max(set(best_choice_alpha), key=best_choice_alpha.count), max(set(best_choice_gamma), key=best_choice_gamma.count), max(set(best_choice_epsilon), key=best_choice_epsilon.count))
    print ("This the best choice", best_choice)
    #comes out to be (0.3,0.1,0.1)

if __name__ == '__main__':
   run()
 