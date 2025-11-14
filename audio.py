import pygame

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