import math
import random

wire_length = 80
target_area_sum = 300
square_1_area=1
square_2_area=1

while square_1_area+square_2_area != target_area_sum:
    cut_1 = random.randint(0, wire_length-1)
    cut_2 = wire_length - cut_1
    square_1_area = (cut_1/4)*(cut_1/4)
    square_2_area = (cut_2/4)*(cut_2/4)
    area_sum = square_1_area+square_2_area
print(cut_1, cut_2)
        

