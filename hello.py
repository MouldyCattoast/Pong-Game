import pygame
import time

# initialize pygame
pygame.init()

width = 600
height = 600
screen_res = (width, height)

pygame.display.set_caption("ball bounce thing")
screen = pygame.display.set_mode(screen_res)

red = (42, 198, 215)
black = (0, 0, 0)
ball_obj = pygame.draw.circle(
    surface=screen, color=red, center=[100, 100], radius=40)
time.sleep(0.01)
speed = [1,1]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    
    screen.fill(black)
    ball_obj = ball_obj.move(speed)
    
    if ball_obj.left <= 0 or ball_obj.right >= width:
        speed[0] = -speed[0]
    if ball_obj.top <= 0 or ball_obj.bottom >= height:
        speed[1] = -speed[1]
        
    pygame.draw.circle(surface=screen, color=red,
                       center=ball_obj.center, radius=10)
 
   
    pygame.display.flip()
