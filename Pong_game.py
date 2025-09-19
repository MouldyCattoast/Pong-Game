import pygame
import pymunk
from pymunk.vec2d import Vec2d
import math
import os
import pymunk.pygame_util

pygame.init()
pygame.font.init()

# colours
navy = (32, 11, 105, 1)
blurple = (111, 35, 255, 1)
teal = (3, 255, 190, 1)

# screen
hztl_size = 600
vtcl_size = 600
screensize = (hztl_size, vtcl_size)
screen = pygame.display.set_mode(screensize)

# speed
gamespeed = 0.01
paddle_spd = 20


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

# score


space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# walls
wall_elasticity = 1
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
    wall.elasticity = 1
space.add(*walls)

# paddles
paddle_l_scalefactor = 30
paddle_w_scalefactor = 5

paddle_a = [
    Vec2d(left_wall, 0),  # topleft
    Vec2d(left_wall + paddle_w_scalefactor * 3, 0),  # topright
    Vec2d(left_wall, bottom_wall * 0.01 * paddle_l_scalefactor),  # bottomleft
    Vec2d(
        left_wall + paddle_w_scalefactor * 3,
        bottom_wall * 0.01 * paddle_l_scalefactor,
    ),  # bottomright
]

paddle_b = [
    Vec2d(right_wall - paddle_w_scalefactor * 3, 0),  # topleft
    Vec2d(right_wall, 0),  # topright
    Vec2d(
        right_wall - paddle_w_scalefactor * 3,
        bottom_wall * 0.01 * paddle_l_scalefactor,
    ),  # bottomleft
    Vec2d(right_wall, bottom_wall * 0.01 * paddle_l_scalefactor),  # bottomright
]


def create_ball(radius, bounciness, mass, moment):
    ball_body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    ball_body.position = (300, 300)
    ball_body.velocity = (20, 20)
    ball_body.damping = 0.5
    ball = pymunk.Circle(ball_body, radius)
    ball.color = teal
    ball.elasticity = bounciness
    space.add(ball_body, ball)
    return ball


def create_paddle(paddle: list):
    paddle_body = pymunk.Body(1, 1, body_type=pymunk.Body.KINEMATIC)
    paddle = pymunk.Poly(paddle_body, paddle, None, 0)
    paddle.elasticity = 0.8
    paddle.color = blurple
    space.add(paddle_body, paddle)

    return paddle_body


# Objects
ball = create_ball(20, 1, 1, 10)
paddle_a_body = create_paddle(paddle_a)
paddle_b_body = create_paddle(paddle_b)

# Collisons
collision_handler = space.add_default_collision_handler()
collision_handler.data["player_a_score"] = 0
collision_handler.data["player_b_score"] = 0
score_increment = 1


def begin(a, s, data):

    ball_collision = ball
    left_wall_collision = left in a.shapes
    right_wall_collision = right in a.shapes

    if left_wall_collision == True:
        data["player_b_score"] += score_increment
        print("Player B score = " + str(data["player_b_score"]))

    if right_wall_collision == True:
        data["player_a_score"] += score_increment
        print("Player A score = " + str(data["player_a_score"]))

    print(ball_collision)

    return True


def pre_solve(a, s, d):
    return True


def post_solve(a, s, d):
    pass


def separate(a, s, d):
    pass


collision_handler.begin = begin
collision_handler.pre_solve = pre_solve
collision_handler.post_solve = post_solve
collision_handler.separate = separate
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print(
                    "No modifier keys were in a pressed state when this "
                    "event occurred."
                )

            # Controls

            pressed = pygame.key.get_pressed()

            # Player 1 Controls
            K_w = pygame.K_w
            K_s = pygame.K_s

            if not pressed[K_w] and not pressed[K_s]:
                paddle_a_body.velocity = (0, 0)

            if pressed[K_w]:
                print("W KEY PRESSED")
                paddle_a_body.velocity = (0, -paddle_spd)

            if pressed[K_s]:
                print("S KEY PRESSED")
                paddle_a_body.velocity = (0, paddle_spd)
            # Player 2 Controls

            K_UP = pygame.K_UP
            K_DOWN = pygame.K_DOWN

            if not pressed[K_UP] and not pressed[K_DOWN]:
                paddle_b_body.velocity = (0, 0)

            if pressed[K_UP]:
                print("UP ARROW PRESSED")
                paddle_b_body.velocity = (0, -paddle_spd)

            if pressed[K_DOWN]:
                print("DOWN ARROW PRESSED")
                paddle_b_body.velocity = (0, paddle_spd)

    screen.fill(navy)
    space.debug_draw(draw_options)
    pygame.display.flip()
    space.step(gamespeed)
pygame.quit()
