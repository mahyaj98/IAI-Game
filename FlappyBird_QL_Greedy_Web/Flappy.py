import random
import sys
import random
import pygame
train = True


    def __init__(self,train):
        self.train = train
        self.episode = 0
        self.discount_factor = 0.95
        self.learning_rate = 0.7
        self.previous_state = [96,47,0]
        self.previous_action = 0
        self.moves = []
        self.scores = []
        self.max_score = 0
        self.xdim = 130
        self.ydim = 130
        self.vdim = 20
        self.qvalues = []
        for _ in range(self.xdim):
            tmp1 = []
            for _ in range(self.ydim):
                tmp2 = []
                for _ in range(self.vdim):
                    tmp2.append([0,0])
                tmp1.append(tmp2)
            self.qvalues.append(tmp1)	
        self.initialize_model()

    def initialize_model(self):
        	pass
		
    def act(self, xdist, ydist, vely):
        # store the transition from previous state to current state
        if self.train:
            state = [xdist,ydist,vely]
            self.moves.append([self.previous_state,self.previous_action,state,0])
            self.previous_state = state

        # get action with max qvalue for current state
        if self.qvalues[xdist][ydist][vely][0] >= self.qvalues[xdist][ydist][vely][1]:
            self.previous_action = 0
        else:
            self.previous_action = 1
        return self.previous_action

    def record(self,reward):
        # set reward to the last transition
        self.moves[-1][3] = reward

    def update_qvalues(self, score):
        self.episode += 1
        self.max_score = max(self.max_score, score)
        print("Episode: " + str(self.episode) + " Score: " + str(score) + " Max Score: " + str(self.max_score))
        self.scores.append(score)
        
        if self.train:
            history = list(reversed(self.moves))			
            first = True
            second = True
            jump = True
            if history[0][1] < 69:
                jump = False
            for move in history:
                [x,y,v] = move[0]
                action = move[1]
                [x1,y1,z1] = move[2]
                reward = move[3]
                # penalize last 2 states before crash
                if first or second:
                    reward = -1000000
                    if first:
                        first = False
                    else:
                        second = False
                # penalize last jump before crash
                if jump and action:
                    reward = -1000000
                    jump = False
                self.qvalues[x][y][v][action] = (1- self.learning_rate) * (self.qvalues[x][y][v][action]) + (self.learning_rate) * ( reward + (self.discount_factor)*max(self.qvalues[x1][y1][z1][0],self.qvalues[x1][y1][z1][1]))
            self.moves = []

    def save_model(self):
        # write the episode, qvalues to qvalues.txt
        data = str(self.episode) + "\n"
        for x in range(self.xdim):
            for y in range(self.ydim):
                for v in range(self.vdim):
                    for a in range(2):
                        data += str(x) + ", " + str(y) + ", " + str(v) + ", " + str(a) + ", " + str(self.qvalues[x][y][v][a]) + "\n"
        qfile = open("qvalues.txt","w")
        qfile.write(data)
        qfile.close()
        
        # append the scores to scores.txt
        data1 = ''
        for i in range(len(self.scores)):
            data1 += str(self.scores[i]) + "\n"
        sfile = open("scores.txt","a+")
        sfile.write(data1)
        sfile.close() 

class QLearningAgentGreedy(object):

    def __init__(self,train):
        self.train = train
        self.episode = 0
        self.discount_factor = 0.95
        self.learning_rate = 0.7
        self.previous_state = [96,47,0]
        self.previous_action = 0
        self.epsilon = 0.1
        self.final_epsilon = 0.0
        self.epsilon_decay = 0.00001
        self.max_score = 0
        self.xdim = 130
        self.ydim = 130
        self.vdim = 20
        self.moves = []
        self.scores = []
        # initialize matrix to store qvalues
        self.qvalues = []
        for _ in range(self.xdim):
            tmp1 = []
            for _ in range(self.ydim):
                tmp2 = []
                for _ in range(self.vdim):
                    tmp2.append([0,0])
                tmp1.append(tmp2)
            self.qvalues.append(tmp1)
        self.initialize_model()

    def initialize_model(self):
        pass
        
    def act(self, xdist, ydist, vely):
        # store the transition from previous state to current state
        if self.train:
            state = [xdist,ydist,vely]
            self.moves.append([self.previous_state,self.previous_action,state,0])
            self.previous_state = state

            # get an action epsilon greedy policy
            if random.random() <= self.epsilon:
                self.previous_action = random.randrange(2)
            elif self.qvalues[xdist][ydist][vely][0] >= self.qvalues[xdist][ydist][vely][1]:
                self.previous_action = 0
            else:
                self.previous_action = 1
        else:
            if self.qvalues[xdist][ydist][vely][0] >= self.qvalues[xdist][ydist][vely][1]:
                self.previous_action = 0
            else:
                self.previous_action = 1
        
        return self.previous_action

    def record(self,reward):
        # set reward to the last transition
        self.moves[-1][3] = reward

    def update_qvalues(self, score):
        self.episode += 1
        self.max_score = max(self.max_score, score)
        print("Episode: " + str(self.episode) + " Epsilon: " + str(self.epsilon) + " Score: " + str(score) + " Max Score: " + str(self.max_score))
        self.scores.append(score)
        
        if self.train:
            history = list(reversed(self.moves))
            first = True
            second = True
            jump = True
            if history[0][1] < 69:
                jump = False
            for move in history:
                [x,y,v] = move[0]
                action = move[1]
                [x1,y1,z1] = move[2]
                reward = move[3]
                # penalize last 2 states before crash
                if first or second:
                    reward = -1
                    if first:
                        first = False
                    else:
                        second = False
                # penalize last jump before crash
                if jump and action:
                    reward = -1
                    jump = False
                self.qvalues[x][y][v][action] = (1- self.learning_rate) * (self.qvalues[x][y][v][action]) + (self.learning_rate) * ( reward + (self.discount_factor)*max(self.qvalues[x1][y1][z1][0],self.qvalues[x1][y1][z1][1]))

            self.moves = []
            # decay epsilon linearly
            if self.epsilon > self.final_epsilon:
                self.epsilon -= self.epsilon_decay
        
    def save_model(self):
        # write the episode, epsilon, qvalues to qvalues.txt
        data = str(self.episode) + "," + str(self.epsilon) + "\n"
        for x in range(self.xdim):
            for y in range(self.ydim):
                for v in range(self.vdim):
                    for a in range(2):
                        data += str(x) + ", " + str(y) + ", " + str(v) + ", " + str(a) + ", " + str(self.qvalues[x,y,v,a]) + "\n"
        qfile = open("qvalues_greedy.txt","w")
        qfile.write(data)
        qfile.close()
        
        # append the scores to scores.txt
        data1 = ''
        for i in range(len(self.scores)):
            data1 += str(self.scores[i]) + "\n"
        sfile = open("scores_greedy.txt","a+")
        sfile.write(data1)
        sfile.close() 
Agent = QLearningAgentGreedy(train)


FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

try:
    xrange
except NameError:
    xrange = range

def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
    playerIndexGen = [0, 1, 2, 1]
    return {
        'playery': playery,
        'basex': 0,
        'playerIndexGen': playerIndexGen,
    }

def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps
    reward = 0
    i = 0 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if train:
                    Agent.save_model()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
        
        # calculate the data             
        xdist_pipe = lowerPipes[0]['x'] - playerx + 30
        if xdist_pipe > 0: 
            PipeNo = 0
        else: 
            PipeNo = 1
        x_dist_lpipe = lowerPipes[PipeNo]['x'] - playerx
        y_dist_lpipe = lowerPipes[PipeNo]['y'] - playery

        # feed parameters to agent which in turn returns action
        if Agent.act(int((x_dist_lpipe + 60)/5),int((y_dist_lpipe + 225)/5),int(playerVelY + 9)):
            if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    
        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                            upperPipes, lowerPipes)
        if crashTest[0]:
            Agent.update_qvalues(score)
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
            }
            
        reward = 1
        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                reward = 5
        if train:        
            Agent.record(reward)

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = playerIndexGen[(i+1) % len(playerIndexGen) ]
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)
        
        playerSurface = IMAGES['player'][playerIndex]
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if train:
                    Agent.save_model()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return
        return
        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()

def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                    player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()
