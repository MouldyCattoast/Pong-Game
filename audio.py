import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

# colours
INDIGO = (32, 11, 105, 1)
BLUE = (111, 35, 255, 1)
TURQUOISE = (3, 255, 190, 1)
FUSCHIA = (255, 0, 245, 1)
CYAN = (0, 209, 255, 1)


# screen
HZTL_SIZE = 600
VTCL_SIZE = 600
SCREENSIZE = (HZTL_SIZE, VTCL_SIZE)
screen = pygame.display.set_mode(SCREENSIZE)
font_path = pygame.font.match_font("Times")
font = pygame.font.Font(font_path, 24)

# Audio
miss_sound = pygame.mixer.Sound("Miss.wav")
miss_sound.set_volume(0.2)
streak_broken_sound = pygame.mixer.Sound("Streak Broken.wav")
streak_broken_sound.set_volume(0.2)
VALUE_CONSIDERED_STREAK = 2
MAX_STREAK_COUNT = 5
streak_count = 0
STREAK_SOUND_LIST = ["placeholder",
                     pygame.mixer.Sound("Hit 1.wav"),
                     pygame.mixer.Sound("Hit 2.wav"), 
                     pygame.mixer.Sound("Hit 3.wav"), 
                     pygame.mixer.Sound("Hit 4.wav"), 
                     pygame.mixer.Sound("Hit 5.wav") ]