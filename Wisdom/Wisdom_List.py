
import random

wisdom_list=[
    'Shields grow back.',
    'Gravity is heavy.',
    'If you want to get out of going on a date, pull a spark plug out of your car and send a snap of the car not starting.',
    'Space is hard.',
    'You need to prospect to see things.'
    ]

def random_wisdom():
    max_int=len(wisdom_list)
    
    choice = random.randint(0,max_int)

    return wisdom_list[choice]
