import pygame as pg
import random

window_height = 400
window_width = 400
window_dim = (window_height,window_width)

bg_color = (255,255,255)

object_height = 100
object_width = 100

#intialize window
pg.init()
disp = pg.display.set_mode(window_dim)
pg.display.set_caption('ABOT')

clk = pg.time.Clock()

neutral_ball = pg.image.load('./resources/ball1.jpg')
negative_ball = pg.image.load('./resources/ball2.jpg')
positive_ball = pg.image.load('./resources/ball3.jpg')
pos_x = [0,100,200,300]
pos_y = [0,100,200,300]

def draw(obj,disp,x_pos,y_pos):
    disp.blit(obj,(x_pos,y_pos))

def display_msg(text,pg,disp):
    text_font = pg.font.Font('freesansbold.ttf',16)
    surface = text_font.render(text,True, (0,0,0))
    surface_area = surface.get_rect()
    surface_area.center = (100,20)
    disp.blit(surface,surface_area)

def maximum(a,b):
    if a>b:
        return a
    else:
        return b

def minimum(a,b):
    if a>b:
        return b
    else:
        return a

def clamp(number,lower_bound,upper_bound):
    new_num = number
    new_num = maximum(lower_bound,new_num)
    new_num = minimum(upper_bound,new_num)
    return new_num

def state_transition(state,action):
    #if new ball_type ball is being generated
    output_state = []
    nball_x = state[3]
    if state[2] == 3:
        ball_y= 0
        nball_x = clamp(nball_x + action,0,3)
        for ball_x in range(0,4):
            for ball_type in range(-1,2,2):
                output_state.append((ball_type,ball_x,ball_y,nball_x))
    else:
        ball_y = state[2]+1
        nball_x = clamp(nball_x + action,0,3)
        ball_x = state[1]
        ball_type = state[0]
        output_state.append((ball_type,ball_x,ball_y,nball_x))
    return output_state

"""Reward of being in certain state is evaluated by balls coordinate
    and ball_type"""
def reward(state):
    if state[2] == 3 and state[1] == state[3]:
        #ball_type itself defines the reward
        return state[0]
    else:
        return 0

"""Transition probability defines the chaces of ending up in a state
    if certain action is taken on a certain state"""
def transition_probability(current_state,action,next_state):
    """if ball is in last row, then any move leading to some state
        will be uniform as random number generator utilized is uniform
        in nature"""
##  Commented code runs faster
##    if current_state[2] == 3:
##        return (1/8)
##    else:
##        if next_state[0] == state_transition(current_state,action):
##            return 1
##        else:
##            return 0
    possible_states = state_transition(current_state,action)
    if next_state in possible_states:
        probability =  1.0/len(possible_states)
    else:
        probability = 0
    return probability

iteration = 10
gamma = 0.8
"""Utilities for value iteration algorithm"""
def get_state_value(state,state_value):
    if state[0] == -1:
        return state_value[0][state[1]][state[2]][state[3]]
    else:
        return state_value[state[0]][state[1]][state[2]][state[3]]

def set_state_value(state,state_value,new_value):
    if state[0] == -1:
        state_value[0][state[1]][state[2]][state[3]] = new_value
    else:
        state_value[state[0]][state[1]][state[2]][state[3]] = new_value

def set_action_value(state,action_value,action):
    if state[0] == -1:
        action_value[0][state[1]][state[2]][state[3]] = action
    else:
        action_value[state[0]][state[1]][state[2]][state[3]] = action

"""Generates all states in list, easy to iterate in value iteration algorithm"""
def generate_states():
    output = []
    for i in range(-1,2,2):
        for j in range(0,4):
            for k in range(0,4):
                for l in range(0,4):
                    output.append((i,j,k,l))
    return output

"""Value iteration algorithm is an iterative version of solving
    Markove Decision Process where state information are observable.
    gamma is the learing factor and higher iteration will give
    state value at higher precision but higher iteraton are not
    useful as only action value are required which will be same no
    matter how many iteration the algorithm runs"""
def learn():
    #initialize the value and action as a function of state
    state_value = []
    for _ in range(2):
        tmp1 = []
        for _ in range(4):
            tmp2 = []
            for _ in range(4):
                tmp2.append([0,0,0,0])
            tmp1.append(tmp2)
        state_value.append(tmp1)
    action_value = []
    for _ in range(2):
        tmp1 = []
        for _ in range(4):
            tmp2 = []
            for _ in range(4):
                tmp2.append([0,0,0,0])
            tmp1.append(tmp2)
        action_value.append(tmp1)
    states = generate_states()
    actions = [0,-1,1]

    #Control the iteration from variable
    for i in range(0,iteration):
        for state in states:
            for action in actions:
                
                possible_states = state_transition(state,action)
                summation = 0
                
                for new_state in possible_states:
                    summation +=  transition_probability(state,action,new_state)*get_state_value(new_state,state_value)
                q_value = reward(state) + gamma*summation
                
                if get_state_value(state,state_value) < q_value:
                    set_state_value(state,state_value,q_value)
                    set_action_value(state,action_value,action)
    
    #print state_value
    return action_value

def start_game():
    abort = False
    x = 0
    y = 0
    b_x = 0
    b_y = 3
    ball_type = 0
    points = 0
    while not abort:
        #Capture all events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                abort = True
            #print(event)
            """Handling differnet events"""
            #(b_x,b_y) = handle_event(event,pg,b_x,b_y)
        
        disp.fill(bg_color)
        
        
        
        draw(neutral_ball,disp,pos_x[b_x],pos_y[b_y])
        if collision(b_x, b_y, x, y):
            if ball_type == 0:
                points = points - 1
                print(points)
            elif ball_type == 1:
                points = points + 1
                print(points)
            
        elif ball_type == 0:
            draw(negative_ball,disp,pos_x[x],pos_y[y])
        elif ball_type == 1:
            draw(positive_ball,disp,pos_x[x],pos_y[y])
            
        (b_x,b_y) = handle_event_agent(ball_type,x,y,b_x)
        
        y = y+1
        
        if y > 3:
            y = 0
            x = random.randrange(0,4)
            ball_type = random.randrange(0,2)

        pg.display.update()
        clk.tick(6)

"""Define end game"""
def end_game():
    pg.quit()
    quit()
def collision(x1,y1,x2,y2):
    if (x1==x2) and (y1==y2):
        return True
    return False

def handle_event(event,pg,x,y):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_LEFT:
            x = maximum(x-1,0)
        if event.key == pg.K_RIGHT:
            x = minimum(x+1,3)
    return (x,y)

action_output = learn()

def handle_event_agent(ball_type,x,y,b_x):
    return (clamp(b_x + int(action_output[ball_type][x][y][b_x]),0,3),3)
        
start_game()
end_game()