import pygame
import pymunk
from pymunk.vec2d import Vec2d

# screen
HZTL_SIZE = 600 
VTCL_SIZE = 600 

# speed
FPS = 60 
GAMESPEED = 1/FPS
DEFAULT_MAX_PAD_SPD = 22 
paddle_a_max_spd = DEFAULT_MAX_PAD_SPD
paddle_b_max_spd = DEFAULT_MAX_PAD_SPD


# colours
INDIGO = (32, 11, 105, 1) 
BLUE = (111, 35, 255, 1) 
TURQUOISE = (3, 255, 190, 1) 
FUSCIA = (255, 0, 245, 1) 
CYAN = (0, 209, 255, 1) 

# boundaries
LEFT_WALL = 0 #
RIGHT_WALL = HZTL_SIZE
TOP_WALL = 0
BOTTOM_WALL = VTCL_SIZE

# paddle
DEFAULT_PADDLE_L_SCALEFACTOR = 30
PADDLE_SIZE_VARIATION_PERCENT = 50
MAX_PADDLE_L_SCALEFACTOR = DEFAULT_PADDLE_L_SCALEFACTOR * (1+(PADDLE_SIZE_VARIATION_PERCENT/100))
MIN_PADDLE_L_SCALEFACTOR = DEFAULT_PADDLE_L_SCALEFACTOR * (1-(PADDLE_SIZE_VARIATION_PERCENT/100))
PADDLE_W_SCALEFACTOR = 5
paddle_l_scalefactor_a = DEFAULT_PADDLE_L_SCALEFACTOR
paddle_l_scalefactor_b = DEFAULT_PADDLE_L_SCALEFACTOR


ACCELERATION_SPD = 0.06 # (Default = 0.06) The higher the number the faster it accelerates
DECELERATION_SPD = 0.995 # (Default = 0.995) WILL ONLY DECELERATE IF THE NUMBER IS LOWER THAN 1, the higher the number, the slower it decelerates


def def_paddle_a_dimensions(paddle_l_scalefactor_a):
    paddle_a_dimensions = [
        Vec2d(LEFT_WALL, 0),  # topleft
        Vec2d(LEFT_WALL + PADDLE_W_SCALEFACTOR * 3, 0),  # topright
        Vec2d(LEFT_WALL, BOTTOM_WALL * 0.01 * paddle_l_scalefactor_a),  # bottomleft
        Vec2d(
            LEFT_WALL + PADDLE_W_SCALEFACTOR * 3,
            BOTTOM_WALL * 0.01 * paddle_l_scalefactor_a,
        ),  # bottomright
    ]
    return paddle_a_dimensions

def def_paddle_b_dimensions(paddle_l_scalefactor_b):
    paddle_b_dimensions = [
        Vec2d(RIGHT_WALL - PADDLE_W_SCALEFACTOR * 3, 0),  # topleft
        Vec2d(RIGHT_WALL, 0),  # topright
        Vec2d(
        RIGHT_WALL - PADDLE_W_SCALEFACTOR * 3,
        BOTTOM_WALL * 0.01 * paddle_l_scalefactor_b,
        ),  # bottomleft
        Vec2d(RIGHT_WALL, BOTTOM_WALL * 0.01 * paddle_l_scalefactor_b),  # bottomright
    ]
    return paddle_b_dimensions

def create_paddle(paddle_dimensions: list):
    paddle_body = pymunk.Body(1, 1, body_type=pymunk.Body.KINEMATIC)
    paddle_shape = pymunk.Poly(paddle_body, paddle_dimensions, None, 0)
    paddle_shape.elasticity = 1.06
    paddle_shape.color = BLUE
    #space.add(paddle_body, paddle_shape)

    return paddle_body, paddle_shape

paddle_shapes = {}


paddle_a_dimensions = def_paddle_a_dimensions(paddle_l_scalefactor_a)
paddle_b_dimensions = def_paddle_b_dimensions(paddle_l_scalefactor_b)
paddle_a_body, paddle_shapes["a"] = create_paddle(paddle_a_dimensions)
paddle_b_body, paddle_shapes["b"] = create_paddle(paddle_b_dimensions)

def add_paddle_to_space(space):
    space.add(paddle_a_body, paddle_b_body, paddle_shapes["a"], paddle_shapes["b"])



def player_a_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold, space):
    
    global paddle_b_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b
    
    paddle_b_max_spd = DEFAULT_MAX_PAD_SPD - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
    space.remove(paddle_shapes["a"], paddle_shapes["b"])

    paddle_l_scalefactor_a = min(MAX_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR+((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_l_scalefactor_b = max(MIN_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR-((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_a_dimensions = def_paddle_a_dimensions(paddle_l_scalefactor_a)
    paddle_b_dimensions = def_paddle_b_dimensions(paddle_l_scalefactor_b)
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a_dimensions, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b_dimensions, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = BLUE
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = BLUE
    space.add(paddle_shapes["a"], paddle_shapes["b"])

    
def player_a_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold, space):
    
    global paddle_a_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b
    
    paddle_a_max_spd = DEFAULT_MAX_PAD_SPD - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
    space.remove(paddle_shapes["a"], paddle_shapes["b"])
    paddle_l_scalefactor_b = min(MAX_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR+((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_l_scalefactor_a = max(MIN_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR-((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_a_dimensions = def_paddle_a_dimensions(paddle_l_scalefactor_a)
    paddle_b_dimensions = def_paddle_b_dimensions(paddle_l_scalefactor_b)
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a_dimensions, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b_dimensions, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = BLUE
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = BLUE
    space.add(paddle_shapes["a"], paddle_shapes["b"])


def player_b_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold, space):
    
    global paddle_a_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b
    paddle_a_max_spd = DEFAULT_MAX_PAD_SPD - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
    space.remove(paddle_shapes["a"], paddle_shapes["b"])

    paddle_l_scalefactor_b = min(MAX_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR+((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_l_scalefactor_a = max(MIN_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR-((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_a_dimensions = def_paddle_a_dimensions(paddle_l_scalefactor_a)
    paddle_b_dimensions = def_paddle_b_dimensions(paddle_l_scalefactor_b)
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a_dimensions, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b_dimensions, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = BLUE
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = BLUE
    space.add(paddle_shapes["a"], paddle_shapes["b"])


def player_b_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold, space):
    
    global paddle_b_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b

   
    paddle_b_max_spd = DEFAULT_MAX_PAD_SPD - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
    space.remove(paddle_shapes["a"], paddle_shapes["b"])

    paddle_l_scalefactor_a = min(MAX_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR+((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_l_scalefactor_b = max(MIN_PADDLE_L_SCALEFACTOR, DEFAULT_PADDLE_L_SCALEFACTOR-((MAX_PADDLE_L_SCALEFACTOR-DEFAULT_PADDLE_L_SCALEFACTOR)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_a_dimensions = def_paddle_a_dimensions(paddle_l_scalefactor_a)
    paddle_b_dimensions = def_paddle_b_dimensions(paddle_l_scalefactor_b)
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a_dimensions, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b_dimensions, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = BLUE
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = BLUE
    space.add(paddle_shapes["a"], paddle_shapes["b"])


   
def assign_controls(W_press, S_press, Up_press, Down_press):
    global ACCELERATION_SPD, DECELERATION_SPD, paddle_a_body, paddle_b_body

    if  W_press == True:
        lvx, lvy=paddle_a_body.velocity
        paddle_a_body.velocity = (0, max(-paddle_a_max_spd, lvy-ACCELERATION_SPD))
       # space.gravity = (0, -5)        

    if S_press == True:
        lvx, lvy=paddle_a_body.velocity
        paddle_a_body.velocity = (0, min(paddle_a_max_spd, lvy+ACCELERATION_SPD))
       # space.gravity = (0, 5)
    
    if W_press == False and S_press == False:
        lvx, lvy=paddle_a_body.velocity
        paddle_a_body.velocity = paddle_a_body.velocity*DECELERATION_SPD
        if paddle_a_body.velocity.length < 1:
            paddle_a_body.velocity = Vec2d(0, 0)
    

    if  Up_press == True:
        rvx, rvy=paddle_b_body.velocity
        paddle_b_body.velocity = (0, max(-paddle_b_max_spd, rvy-ACCELERATION_SPD))
        
        #space.gravity = (0, -5)

    if Down_press == True:
        rvx, rvy=paddle_b_body.velocity
        paddle_b_body.velocity = (0, min(paddle_b_max_spd, rvy+ACCELERATION_SPD))
        #space.gravity = (0, 5)

    if Up_press == False and Down_press == False:
        rvx, rvy=paddle_b_body.velocity
        paddle_b_body.velocity = paddle_b_body.velocity*DECELERATION_SPD
        if paddle_b_body.velocity.length < 1:
            paddle_b_body.velocity = Vec2d(0, 0)

def limit_paddle(collision_handler):
    if collision_handler.data["paddle_a_bottom_stop"] == True:
        paddle_a_body.velocity = (0, min(0,paddle_a_body.velocity[1]))

    if collision_handler.data["paddle_a_top_stop"] == True:
        paddle_a_body.velocity = (0, max(0,paddle_a_body.velocity[1]))

    if collision_handler.data["paddle_b_bottom_stop"] == True:
        paddle_b_body.velocity = (0, min(0,paddle_b_body.velocity[1]))

    if collision_handler.data["paddle_b_top_stop"] == True:
        paddle_b_body.velocity = (0, max(0,paddle_b_body.velocity[1]))
    
   