import pymunk
import math
import random
import itertools

# screen
HZTL_SIZE = 600
VTCL_SIZE = 600

# colours
INDIGO = (32, 11, 105, 1)
BLUE = (111, 35, 255, 1)
TURQUOISE = (3, 255, 190, 1)
FUSCHIA = (255, 0, 245, 1)
CYAN = (0, 209, 255, 1)

# boundaries
LEFT_WALL = 0
RIGHT_WALL = HZTL_SIZE
TOP_WALL = 0
BOTTOM_WALL = VTCL_SIZE

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
    ball.color = TURQUOISE
    ball.elasticity = bounciness
    return ball_body, ball

ball_body, ball = create_ball(20, 1, 1, 10)
def add_ball_to_space(space):
    space.add(ball_body, ball)