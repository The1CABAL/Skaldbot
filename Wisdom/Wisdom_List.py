
import random

wisdom_list=[
    'Shields grow back.',
    'Gravity is heavy.'
    ]

def random_wisdom():
    max_int=len(wisdom_list)
    
    choice = random.randint(0,max_int)

    return wisdom_list[choice]