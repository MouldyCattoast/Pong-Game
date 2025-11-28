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
import ball
import audio




pygame.init()
pygame.font.init()
pygame.mixer.init()

# colours
INDIGO = (32, 11, 105, 1)
BLUE = (111, 35, 255, 1)
TURQUOISE = (3, 255, 190, 1)
FUSCHIA = (255, 0, 245, 1)
CYAN = (0, 209, 255, 1)


# SCREEN
HZTL_SIZE = 600
VTCL_SIZE = 600
SCREENSIZE = (HZTL_SIZE, VTCL_SIZE)
SCREEN = pygame.display.set_mode(SCREENSIZE)
FONT_PATH = pygame.font.match_font("Times")
font = pygame.font.Font(FONT_PATH, 24)


# speed
FPS = 60
GAMESPEED = 1/FPS
DEFAULT_MAX_PAD_SPD = 22
# boundaries
LEFT_WALL = 0
RIGHT_WALL = HZTL_SIZE
TOP_WALL = 0
BOTTOM_WALL = VTCL_SIZE

# corners
TOPLEFT = (LEFT_WALL, TOP_WALL)
TOPRIGHT = (RIGHT_WALL, TOP_WALL)
BOTTOMLEFT = (LEFT_WALL, BOTTOM_WALL)
BOTTOMRIGHT = (RIGHT_WALL, BOTTOM_WALL)



#Game Space


space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(SCREEN)
paddle.add_paddle_to_space(space)

# walls
WALL_ELASTICITY = 0.96
bottom = pymunk.Segment(space.static_body, BOTTOMLEFT, BOTTOMRIGHT, WALL_ELASTICITY)
right = pymunk.Segment(space.static_body, TOPRIGHT, BOTTOMRIGHT, WALL_ELASTICITY)
top = pymunk.Segment(space.static_body, TOPLEFT, TOPRIGHT, WALL_ELASTICITY)
left = pymunk.Segment(space.static_body, TOPLEFT, BOTTOMLEFT, WALL_ELASTICITY)
walls = [
    bottom,
    right,
    top,
    left,
]

for wall in walls:
    wall.elasticity = WALL_ELASTICITY
space.add(*walls)


# Objects
ball.add_ball_to_space(space)
ball_move_x = ball.ball_body.velocity[0]
ball_move_y = ball.ball_body.velocity[1]






# Collisons+Scoring

collision_handler = space.add_default_collision_handler()
collision_handler.data["player_a_score"] = 10
collision_handler.data["player_b_score"] = 10

collision_handler.data["paddle_a_top_stop"] = False
collision_handler.data["paddle_a_bottom_stop"] = False
collision_handler.data["paddle_b_top_stop"] = False
collision_handler.data["paddle_b_bottom_stop"] = False





def detect_collision(a):
    LEFT_WALL_COLLISION = left in a.shapes
    RIGHT_WALL_COLLISION = right in a.shapes
    TOP_WALL_COLLISION = top in a.shapes
    BOTTOM_WALL_COLLISION = bottom in a.shapes

    paddle.paddle_a_collision = paddle.paddle_shapes["a"] in a.shapes
    paddle.paddle_b_collision = paddle.paddle_shapes["b"] in a.shapes

    BALL_COLLISION = ball.ball in a.shapes

    if (paddle.paddle_a_collision and TOP_WALL_COLLISION) :
        return "paddle_a_top"

    if(paddle.paddle_a_collision and BOTTOM_WALL_COLLISION):
        return "paddle_a_bottom"

    if (paddle.paddle_b_collision and TOP_WALL_COLLISION):
        return "paddle_b_top"
    
    if(paddle.paddle_b_collision and BOTTOM_WALL_COLLISION):
        return "paddle_b_bottom"
    
    if(LEFT_WALL_COLLISION and BALL_COLLISION):
        return "l_wall"
    
    if(RIGHT_WALL_COLLISION and BALL_COLLISION):
        return "r_wall"
    
    if(paddle.paddle_a_collision and BALL_COLLISION):
        return "ball_and_a"
    
    if(paddle.paddle_b_collision and BALL_COLLISION):
        return "ball_and_b"
    


def begin(a, s, data):
    collision_type = detect_collision(a)

    if collision_type == "l_wall":
        if audio.streak_count >= audio.VALUE_CONSIDERED_STREAK:
            audio.streak_count = 0
            pygame.mixer.Sound.play(audio.streak_broken_sound)
        else:
            pygame.mixer.Sound.play(audio.miss_sound)
        
    
    if collision_type == "r_wall":
        if audio.streak_count >= audio.VALUE_CONSIDERED_STREAK :
            audio.streak_count = 0
            pygame.mixer.Sound.play(audio.streak_broken_sound)
        else:
            pygame.mixer.Sound.play(audio.miss_sound)

    
        
         
    if collision_type == "l_wall":
        

        data["player_b_score"] += score_increment
        if bar_var_w>bar_midpoint: #if bar above 50%(player a winning)
            paddle.player_b_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])

        if  bar_var_w<bar_midpoint: #if bar below 50%(player b winning)
            paddle.player_b_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
        print("a = ", paddle.paddle_l_scalefactor_a)
        print("b = ", paddle.paddle_l_scalefactor_b)
            

    if collision_type == "r_wall":

        data["player_a_score"] += score_increment

        if (bar_var_w>bar_midpoint): #if bar above 50%(player a winning)
            paddle.player_a_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])


        if (bar_var_w<bar_midpoint): #if bar below 50%(player b winning)
            paddle.player_a_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold)
            space.remove(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])
            space.add(paddle.paddle_shapes["a"], paddle.paddle_shapes["b"])

        print("a =", paddle.paddle_l_scalefactor_a)
        print("b =", paddle.paddle_l_scalefactor_b)

    if collision_type == "paddle_a_top":
        data["paddle_a_top_stop"] = True
        
    if collision_type == "paddle_a_bottom":
        data["paddle_a_bottom_stop"] = True

    if collision_type == "paddle_b_top":
        data["paddle_b_top_stop"] = True

    if collision_type == "paddle_b_bottom":
        data["paddle_b_bottom_stop"] = True

    return True


def pre_solve(a, s, d):
    return True


def post_solve(a, s, d):

    pass


def separate(a, s, data):
    collision_type = detect_collision(a)
    magnitude_of_paddle_influence_on_ball  = 0.5 #Anything above 1 is very very obvious

    

    if collision_type == "paddle_a_top":
        data["paddle_a_top_stop"] = False
        
    
    if collision_type == "paddle_a_bottom":
        data["paddle_a_bottom_stop"] = False 
        

    if collision_type == "paddle_b_top":
        data["paddle_b_top_stop"] = False  
        

    if collision_type == "paddle_b_bottom":
        data["paddle_b_bottom_stop"] = False   

    if collision_type == "ball_and_a":
        ball.ball_body.velocity = ball.ball_body.velocity+(paddle.paddle_a_body.velocity*magnitude_of_paddle_influence_on_ball)
        if audio.streak_count < audio.MAX_STREAK_COUNT:
            audio.streak_count += 1
        pygame.mixer.Sound.play(audio.STREAK_SOUND_LIST[audio.streak_count])
        
        
        

    if collision_type == "ball_and_b": 
        ball.ball_body.velocity = ball.ball_body.velocity+(paddle.paddle_b_body.velocity*magnitude_of_paddle_influence_on_ball)
        if audio.streak_count < audio.MAX_STREAK_COUNT:
            audio.streak_count += 1
        pygame.mixer.Sound.play(audio.STREAK_SOUND_LIST[audio.streak_count])
        
        
            



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
pad_spd_to_bg_w_ratio = (((bar_bg_w-quit_threshold)-half_of_bar)/DEFAULT_MAX_PAD_SPD)

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

            if pressed[K_w] and (collision_handler.data["paddle_a_top_stop"] == False):
                W_press = True
                S_press = False
                #space.gravity = (0, -5)

            if pressed[K_s] and (collision_handler.data["paddle_a_bottom_stop"] == False):
                S_press = True
                W_press= False
               # space.gravity = (0, 5)

            # Player 2 Controls

            K_UP = pygame.K_UP
            K_DOWN = pygame.K_DOWN

            if not pressed[K_UP] and not pressed[K_DOWN]:
                Up_press = False
                Down_press = False

            if pressed[K_UP] and (collision_handler.data["paddle_b_top_stop"] == False):
                Up_press = True
                Down_press = False
                #space.gravity = (0, -5)

            if pressed[K_DOWN] and (collision_handler.data["paddle_b_bottom_stop"] == False):
                Down_press = True
                Up_press = False
                #space.gravity = (0, 5)

    paddle.assign_controls(W_press, S_press, Up_press, Down_press)

    paddle.limit_paddle(collision_handler)
        
    #streak
    streak_sound_index = min(audio.streak_count, 5)
    audio.STREAK_SOUND_LIST[streak_sound_index]
        
    player_a_score_surface = font.render(
        f"Player A: {collision_handler.data["player_a_score"]}", True, TURQUOISE
    )

    player_b_score_surface = font.render(
        f"Player B: {collision_handler.data["player_b_score"]}", True, TURQUOISE
    )
    
    SCREEN.fill(INDIGO)
    pygame.draw.rect(SCREEN, FUSCHIA, bar_bg)
    pygame.draw.rect(SCREEN, CYAN, bar_var)
    """SCREEN.blit(player_a_score_surface, (10, 10))
    SCREEN.blit(player_b_score_surface, (10, 50))"""
    space.debug_draw(draw_options)
    pygame.display.flip()
    space.step(GAMESPEED)
pygame.quit()
sys.exit()
