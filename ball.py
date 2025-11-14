import pymunk
import math
import random
import itertools

# screen
hztl_size = 600
vtcl_size = 600

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
    return ball_body, ball

ball_body, ball = create_ball(20, 1, 1, 10)
def add_ball_to_space(space):
    space.add(ball_body, ball)