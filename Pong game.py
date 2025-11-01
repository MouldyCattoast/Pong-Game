import pygame
import pymunk
from pymunk.vec2d import Vec2d
import math
import random
import itertools
import os
import sys
import pymunk.pygame_util
import paddle




pygame.init()
pygame.font.init()
pygame.mixer.init()

# colours
indigo = (32, 11, 105, 1)
blue = (111, 35, 255, 1)
turquoise = (3, 255, 190, 1)
fuschia = (255, 0, 245, 1)
cyan = (0, 209, 255, 1)


# screen
hztl_size = 600
vtcl_size = 600
screensize = (hztl_size, vtcl_size)
screen = pygame.display.set_mode(screensize)
font_path = pygame.font.match_font("Times")
font = pygame.font.Font(font_path, 24)


# speed
FPS = 60
gamespeed = 1/FPS
default_max_pad_spd = 22
paddle.paddle_a_max_spd = default_max_pad_spd
paddle.paddle_b_max_spd = default_max_pad_spd

# boundaries
left_wall = 0
right_wall = hztl_size
top_wall = 0
bottom_wall = vtcl_size

# corners
topleft = (left_wall, top_wall)
topright = (right_wall, top_wall)
bottomleft = (left_wall, bottom_wall)
bottomright = (right_wall, bottom_wall)



#Game Space


space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
paddle.add_paddle_to_space(space)

# walls
wall_elasticity = 0.96
bottom = pymunk.Segment(space.static_body, bottomleft, bottomright, wall_elasticity)
right = pymunk.Segment(space.static_body, topright, bottomright, wall_elasticity)
top = pymunk.Segment(space.static_body, topleft, topright, wall_elasticity)
left = pymunk.Segment(space.static_body, topleft, bottomleft, wall_elasticity)
walls = [
    bottom,
    right,
    top,
    left,
]

for wall in walls:
    wall.elasticity = wall_elasticity
space.add(*walls)

def create_ball(radius, bounciness, mass, moment):
    ball_spd = random.randint(15, 30)
    a_range = range(30, 60)
    b_range = range(120, 150)
    c_range = range(210, 240)
    d_range = range(300, 330)
    angle_ranges = list(itertools.chain(a_range, b_range, c_range, d_range))
    angle_deg = random.choice(angle_ranges)
    #print(angle_deg)
    angle = math.radians(angle_deg)
    ball_body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    ball_body.position = (300, 300)
    ball_body.velocity = (ball_spd*math.cos(angle), ball_spd*math.sin(angle))
    ball_body.damping = 0.99
    ball = pymunk.Circle(ball_body, radius)
    ball.color = turquoise
    ball.elasticity = bounciness
    space.add(ball_body, ball)
    
    return ball_body, ball



# Objects
ball_body, ball = create_ball(20, 1, 1, 10)
ball_move_x = ball_body.velocity[0]
ball_move_y = ball_body.velocity[1]

# Audio
miss_sound = pygame.mixer.Sound("Miss.wav")
miss_sound.set_volume(0.2)
streak_broken_sound = pygame.mixer.Sound("Streak Broken.wav")
streak_broken_sound.set_volume(0.2)
value_considered_streak = 2
max_streak_count = 5
streak_count = 0
streak_sound_list = ["placeholder",
                     pygame.mixer.Sound("Hit 1.wav"),
                     pygame.mixer.Sound("Hit 2.wav"), 
                     pygame.mixer.Sound("Hit 3.wav"), 
                     pygame.mixer.Sound("Hit 4.wav"), 
                     pygame.mixer.Sound("Hit 5.wav") ]




# Collisons+Scoring

collision_handler = space.add_default_collision_handler()
collision_handler.data["player_a_score"] = 10
collision_handler.data["player_b_score"] = 10

collision_handler.data["paddle.paddle_a_top_stop"] = False
collision_handler.data["paddle.paddle_a_bottom_stop"] = False
collision_handler.data["paddle.paddle_b_top_stop"] = False
collision_handler.data["paddle.paddle_b_bottom_stop"] = False





def detect_collision(a):
    left_wall_collision = left in a.shapes
    right_wall_collision = right in a.shapes
    top_wall_collision = top in a.shapes
    bottom_wall_collision = bottom in a.shapes

    paddle.paddle_a_collision = paddle.paddle_shapes["a"] in a.shapes
    paddle.paddle_b_collision = paddle.paddle_shapes["b"] in a.shapes

    #print(paddle.paddle_shapes["a"])

    ball_collision = ball in a.shapes

    if (paddle.paddle_a_collision and top_wall_collision) :
        return "paddle.paddle_a_top"

    if(paddle.paddle_a_collision and bottom_wall_collision):
        return "paddle.paddle_a_bottom"

    if (paddle.paddle_b_collision and top_wall_collision):
        return "paddle.paddle_b_top"
    
    if(paddle.paddle_b_collision and bottom_wall_collision):
        return "paddle.paddle_b_bottom"
    
    if(left_wall_collision and ball_collision):
        return "l_wall"
    
    if(right_wall_collision and ball_collision):
        return "r_wall"
    
    if(paddle.paddle_a_collision and ball_collision):
        return "ball_and_a"
    
    if(paddle.paddle_b_collision and ball_collision):
        return "ball_and_b"
    


def begin(a, s, data):
    global streak_count
    collision_type = detect_collision(a)

    if collision_type == "l_wall":
        if streak_count >= value_considered_streak:
            streak_count = 0
            pygame.mixer.Sound.play(streak_broken_sound)
        else:
            pygame.mixer.Sound.play(miss_sound)
        
    
    if collision_type == "r_wall":
        if streak_count >= value_considered_streak :
            streak_count = 0
            pygame.mixer.Sound.play(streak_broken_sound)
        else:
            pygame.mixer.Sound.play(miss_sound)

    
        
         
    if collision_type == "l_wall":
        

        data["player_b_score"] += score_increment
        if bar_var_w>bar_midpoint: #if bar above 50%(player a winning)
            paddle.paddle_b_max_spd = default_max_pad_spd - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            paddle.paddle_l_scalefactor_a = min(paddle.max_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor+((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
            paddle.paddle_l_scalefactor_b = max(paddle.min_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor-((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
            paddle.paddle_shapes["a"] = pymunk.Poly(paddle.paddle_a_body, paddle.paddle_a, None, 0)
            paddle.paddle_shapes["b"] = pymunk.Poly(paddle.paddle_b_body, paddle.paddle_b, None, 0)
            paddle.paddle_shapes["a"].elasticity = 1.06
            paddle.paddle_shapes["a"].color = blue
            paddle.paddle_shapes["b"].elasticity = 1.06
            paddle.paddle_shapes["b"].color = blue
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])

        if  bar_var_w<bar_midpoint: #if bar below 50%(player b winning)
            paddle.paddle_a_max_spd = default_max_pad_spd - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            paddle.paddle_l_scalefactor_b = min(paddle.max_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor+((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
            paddle.paddle_l_scalefactor_a = max(paddle.min_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor-((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
            paddle.paddle_shapes["a"] = pymunk.Poly(paddle.paddle_a_body, paddle.paddle_a, None, 0)
            paddle.paddle_shapes["b"] = pymunk.Poly(paddle.paddle_b_body, paddle.paddle_b, None, 0)
            paddle.paddle_shapes["a"].elasticity = 1.06
            paddle.paddle_shapes["a"].color = blue
            paddle.paddle_shapes["b"].elasticity = 1.06
            paddle.paddle_shapes["b"].color = blue
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
        print("a = ", paddle.paddle_l_scalefactor_a)
        print("b = ", paddle.paddle_l_scalefactor_b)
            

    if collision_type == "r_wall":
        data["player_a_score"] += score_increment
        if (bar_var_w>bar_midpoint): #if bar above 50%(player a winning)
            paddle.paddle_b_max_spd = default_max_pad_spd - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            paddle.paddle_l_scalefactor_a = min(paddle.max_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor+((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
            paddle.paddle_l_scalefactor_b = max(paddle.min_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor-((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
            paddle.paddle_shapes["a"] = pymunk.Poly(paddle.paddle_a_body, paddle.paddle_a, None, 0)
            paddle.paddle_shapes["b"] = pymunk.Poly(paddle.paddle_b_body, paddle.paddle_b, None, 0)
            paddle.paddle_shapes["a"].elasticity = 1.06
            paddle.paddle_shapes["a"].color = blue
            paddle.paddle_shapes["b"].elasticity = 1.06
            paddle.paddle_shapes["b"].color = blue
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])

        if (bar_var_w<bar_midpoint): #if bar below 50%(player b winning)
            paddle.paddle_a_max_spd = default_max_pad_spd - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            paddle.paddle_l_scalefactor_b = min(paddle.max_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor+((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
            paddle.paddle_l_scalefactor_a = max(paddle.min_paddle_l_scalefactor, paddle.default_paddle_l_scalefactor-((paddle.max_paddle_l_scalefactor-paddle.default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
            paddle.paddle_shapes["a"] = pymunk.Poly(paddle.paddle_a_body, paddle.paddle_a, None, 0)
            paddle.paddle_shapes["b"] = pymunk.Poly(paddle.paddle_b_body, paddle.paddle_b, None, 0)
            paddle.paddle_shapes["a"].elasticity = 1.06
            paddle.paddle_shapes["a"].color = blue
            paddle.paddle_shapes["b"].elasticity = 1.06
            paddle.paddle_shapes["b"].color = blue
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
        print("a =", paddle.paddle_l_scalefactor_a)
        print("b =", paddle.paddle_l_scalefactor_b)

    if collision_type == "paddle.paddle_a_top":
        data["paddle.paddle_a_top_stop"] = True
        
    if collision_type == "paddle.paddle_a_bottom":
        data["paddle.paddle_a_bottom_stop"] = True

    if collision_type == "paddle.paddle_b_top":
        data["paddle.paddle_b_top_stop"] = True

    if collision_type == "paddle.paddle_b_bottom":
        data["paddle.paddle_b_bottom_stop"] = True

    

   

    return True


def pre_solve(a, s, d):
    return True


def post_solve(a, s, d):

    pass


def separate(a, s, data):
    global streak_count
    collision_type = detect_collision(a)
    magnitude_of_paddle_influence_on_ball  = 0.5 #Anything above 1 is very very obvious

    

    if collision_type == "paddle.paddle_a_top":
        data["paddle.paddle_a_top_stop"] = False
        
    
    if collision_type == "paddle.paddle_a_bottom":
        data["paddle.paddle_a_bottom_stop"] = False 
        

    if collision_type == "paddle.paddle_b_top":
        data["paddle.paddle_b_top_stop"] = False  
        

    if collision_type == "paddle.paddle_b_bottom":
        data["paddle.paddle_b_bottom_stop"] = False   

    if collision_type == "ball_and_a":
        ball_body.velocity = ball_body.velocity+(paddle.paddle_a_body.velocity*magnitude_of_paddle_influence_on_ball)
        if streak_count < max_streak_count:
            streak_count += 1
        pygame.mixer.Sound.play(streak_sound_list[streak_count])
        
        
        

    if collision_type == "ball_and_b": 
        ball_body.velocity = ball_body.velocity+(paddle.paddle_b_body.velocity*magnitude_of_paddle_influence_on_ball)
        if streak_count < max_streak_count:
            streak_count += 1
        pygame.mixer.Sound.play(streak_sound_list[streak_count])
        
        
            



collision_handler.begin = begin
collision_handler.pre_solve = pre_solve
collision_handler.post_solve = post_solve
collision_handler.separate = separate

bar_bg_w = 400
bar_midpoint = bar_bg_w/2
half_of_bar = bar_bg_w/2
bar_bg = pygame.Rect(100, 20 , bar_bg_w, 20)
bar_var_w = bar_midpoint
quit_threshold = 0.25 * bar_bg_w
pad_spd_to_bg_w_ratio = (((bar_bg_w-quit_threshold)-half_of_bar)/default_max_pad_spd)

W_press = False
S_press = False
Down_press = False
Up_press = False


running = True
while running:

    
    
    #bar_var = create_score_bar(player_a_score_val, player_b_score_val)
    #create_score_bar()

    player_a_score_val = collision_handler.data["player_a_score"]
    player_b_score_val = collision_handler.data["player_b_score"]
    score_increment = (collision_handler.data["player_a_score"] + collision_handler.data["player_b_score"])/10

    #Score Bar Shift
    if (player_a_score_val >= 1) or (player_b_score_val >= 1):
        bar_var_w = ((bar_bg_w/(player_a_score_val+player_b_score_val))*player_a_score_val)
   
    bar_var = pygame.Rect(100, 20 , bar_var_w, 20)
    
    if (bar_var_w <= (quit_threshold)) or (bar_var_w >= (bar_bg_w-quit_threshold)):
        pygame.quit()
        sys.exit()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            # Controls

            pressed = pygame.key.get_pressed()

            # Player 1 Controls
            
            K_w = pygame.K_w
            K_s = pygame.K_s

            if not pressed[K_w] and not pressed[K_s]:
                W_press = False
                S_press = False

            if pressed[K_w] and (collision_handler.data["paddle.paddle_a_top_stop"] == False):
                W_press = True
                S_press = False
                #space.gravity = (0, -5)


            
            if pressed[K_s] and (collision_handler.data["paddle.paddle_a_bottom_stop"] == False):
                S_press = True
                W_press= False
               # space.gravity = (0, 5)

            


            # Player 2 Controls

            K_UP = pygame.K_UP
            K_DOWN = pygame.K_DOWN

            if not pressed[K_UP] and not pressed[K_DOWN]:
                Up_press = False
                Down_press = False


            if pressed[K_UP] and (collision_handler.data["paddle.paddle_b_top_stop"] == False):
                Up_press = True
                Down_press = False
                #space.gravity = (0, -5)

            if pressed[K_DOWN] and (collision_handler.data["paddle.paddle_b_bottom_stop"] == False):
                Down_press = True
                Up_press = False
                #space.gravity = (0, 5)



    acceleration_spd = 0.06 # (Default = 0.06) The higher the number the faster it accelerates
    deceleration_spd = 0.995 # (Default = 0.995) WILL ONLY DECELERATE IF THE NUMBER IS LOWER THAN 1, the higher the number, the slower it decelerates

    if  W_press == True:
        lvx, lvy=paddle.paddle_a_body.velocity
        paddle.paddle_a_body.velocity = (0, max(-paddle.paddle_a_max_spd, lvy-acceleration_spd))
       # space.gravity = (0, -5)        

    if S_press == True:
        lvx, lvy=paddle.paddle_a_body.velocity
        paddle.paddle_a_body.velocity = (0, min(paddle.paddle_a_max_spd, lvy+acceleration_spd))
       # space.gravity = (0, 5)
    
    if W_press == False and S_press == False:
        lvx, lvy=paddle.paddle_a_body.velocity
        paddle.paddle_a_body.velocity = paddle.paddle_a_body.velocity*deceleration_spd
        if paddle.paddle_a_body.velocity.length < 1:
            paddle.paddle_a_body.velocity = Vec2d(0, 0)
    

    if  Up_press == True:
        rvx, rvy=paddle.paddle_b_body.velocity
        paddle.paddle_b_body.velocity = (0, max(-paddle.paddle_b_max_spd, rvy-acceleration_spd))
        
        #space.gravity = (0, -5)

    if Down_press == True:
        rvx, rvy=paddle.paddle_b_body.velocity
        paddle.paddle_b_body.velocity = (0, min(paddle.paddle_b_max_spd, rvy+acceleration_spd))
        #space.gravity = (0, 5)

    if Up_press == False and Down_press == False:
        rvx, rvy=paddle.paddle_b_body.velocity
        paddle.paddle_b_body.velocity = paddle.paddle_b_body.velocity*deceleration_spd
        if paddle.paddle_b_body.velocity.length < 1:
            paddle.paddle_b_body.velocity = Vec2d(0, 0)

    #Collision Maintainence

    if collision_handler.data["paddle.paddle_a_bottom_stop"] == True:
        paddle.paddle_a_body.velocity = (0, min(0,paddle.paddle_a_body.velocity[1]))

    if collision_handler.data["paddle.paddle_a_top_stop"] == True:
        paddle.paddle_a_body.velocity = (0, max(0,paddle.paddle_a_body.velocity[1]))

    if collision_handler.data["paddle.paddle_b_bottom_stop"] == True:
        paddle.paddle_b_body.velocity = (0, min(0,paddle.paddle_b_body.velocity[1]))

    if collision_handler.data["paddle.paddle_b_top_stop"] == True:
        paddle.paddle_b_body.velocity = (0, max(0,paddle.paddle_b_body.velocity[1]))
    
    #streak
    streak_sound_index = min(streak_count, 5)
    streak_sound_list[streak_sound_index]
        



   
    

    player_a_score_surface = font.render(
        f"Player A: {collision_handler.data["player_a_score"]}", True, turquoise
    )

    player_b_score_surface = font.render(
        f"Player B: {collision_handler.data["player_b_score"]}", True, turquoise
    )
    
    screen.fill(indigo)
    pygame.draw.rect(screen, fuschia, bar_bg)
    pygame.draw.rect(screen, cyan, bar_var)
    """screen.blit(player_a_score_surface, (10, 10))
    screen.blit(player_b_score_surface, (10, 50))"""
    space.debug_draw(draw_options)
    pygame.display.flip()
    space.step(gamespeed)
pygame.quit()
sys.exit()
