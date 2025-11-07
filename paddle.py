import pygame
import pymunk
from pymunk.vec2d import Vec2d
import math
import random
import itertools
import os
import sys
import pymunk.pygame_util

# screen
hztl_size = 600
vtcl_size = 600

# speed
FPS = 60
gamespeed = 1/FPS
default_max_pad_spd = 22
paddle_a_max_spd = default_max_pad_spd
paddle_b_max_spd = default_max_pad_spd


# colours
indigo = (32, 11, 105, 1)
blue = (111, 35, 255, 1)
turquoise = (3, 255, 190, 1)
fuschia = (255, 0, 245, 1)
cyan = (0, 209, 255, 1)

# boundaries
left_wall = 0
right_wall = hztl_size
top_wall = 0
bottom_wall = vtcl_size

# paddle
default_paddle_l_scalefactor = 30
paddle_size_variation_percent = 50
max_paddle_l_scalefactor = default_paddle_l_scalefactor * (1+(paddle_size_variation_percent/100))
min_paddle_l_scalefactor = default_paddle_l_scalefactor * (1-(paddle_size_variation_percent/100))
paddle_l_scalefactor_a = default_paddle_l_scalefactor
paddle_l_scalefactor_b = default_paddle_l_scalefactor
paddle_w_scalefactor = 5

paddle_a = [
        Vec2d(left_wall, 0),  # topleft
        Vec2d(left_wall + paddle_w_scalefactor * 3, 0),  # topright
        Vec2d(left_wall, bottom_wall * 0.01 * paddle_l_scalefactor_a),  # bottomleft
        Vec2d(
            left_wall + paddle_w_scalefactor * 3,
            bottom_wall * 0.01 * paddle_l_scalefactor_a,
        ),  # bottomright
]


paddle_b = [
    Vec2d(right_wall - paddle_w_scalefactor * 3, 0),  # topleft
    Vec2d(right_wall, 0),  # topright
    Vec2d(
        right_wall - paddle_w_scalefactor * 3,
        bottom_wall * 0.01 * paddle_l_scalefactor_b,
    ),  # bottomleft
    Vec2d(right_wall, bottom_wall * 0.01 * paddle_l_scalefactor_b),  # bottomright
]

def create_paddle(paddle: list):
    paddle_body = pymunk.Body(1, 1, body_type=pymunk.Body.KINEMATIC)
    paddle_shape = pymunk.Poly(paddle_body, paddle, None, 0)
    paddle_shape.elasticity = 1.06
    paddle_shape.color = blue
    #space.add(paddle_body, paddle_shape)

    return paddle_body, paddle_shape

paddle_shapes = {}


paddle_a_body, paddle_shapes["a"] = create_paddle(paddle_a)
paddle_b_body, paddle_shapes["b"] = create_paddle(paddle_b)

def add_paddle_to_space(space):
    space.add(paddle_a_body, paddle_b_body, paddle_shapes["a"], paddle_shapes["b"])



def player_a_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold):
    
    global paddle_b_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b
    
    paddle_b_max_spd = default_max_pad_spd - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
    paddle_l_scalefactor_a = min(max_paddle_l_scalefactor, default_paddle_l_scalefactor+((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_l_scalefactor_b = max(min_paddle_l_scalefactor, default_paddle_l_scalefactor-((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = blue
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = blue
    
def player_a_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold):
    
    global paddle_a_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b
    
    paddle_a_max_spd = default_max_pad_spd - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
    paddle_l_scalefactor_b = min(max_paddle_l_scalefactor, default_paddle_l_scalefactor+((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_l_scalefactor_a = max(min_paddle_l_scalefactor, default_paddle_l_scalefactor-((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = blue
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = blue

def player_b_score_winning(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, quit_threshold):
    
    global paddle_a_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b

    paddle_a_max_spd = default_max_pad_spd - ((bar_midpoint - bar_var_w)/pad_spd_to_bg_w_ratio)
    paddle_l_scalefactor_b = min(max_paddle_l_scalefactor, default_paddle_l_scalefactor+((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_l_scalefactor_a = max(min_paddle_l_scalefactor, default_paddle_l_scalefactor-((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_midpoint-bar_var_w)/(bar_midpoint-quit_threshold))))
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = blue
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = blue

def player_b_score_losing(bar_var_w, bar_midpoint, pad_spd_to_bg_w_ratio, bar_bg_w, quit_threshold):
    
    global paddle_b_max_spd, paddle_l_scalefactor_a, paddle_l_scalefactor_b

   
    paddle_b_max_spd = default_max_pad_spd - ((bar_var_w - bar_midpoint)/pad_spd_to_bg_w_ratio)
    paddle_l_scalefactor_a = min(max_paddle_l_scalefactor, default_paddle_l_scalefactor+((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_l_scalefactor_b = max(min_paddle_l_scalefactor, default_paddle_l_scalefactor-((max_paddle_l_scalefactor-default_paddle_l_scalefactor)*((bar_var_w - bar_midpoint)/((bar_bg_w-quit_threshold)-bar_midpoint))))
    paddle_shapes["a"] = pymunk.Poly(paddle_a_body, paddle_a, None, 0)
    paddle_shapes["b"] = pymunk.Poly(paddle_b_body, paddle_b, None, 0)
    paddle_shapes["a"].elasticity = 1.06
    paddle_shapes["a"].color = blue
    paddle_shapes["b"].elasticity = 1.06
    paddle_shapes["b"].color = blue
   