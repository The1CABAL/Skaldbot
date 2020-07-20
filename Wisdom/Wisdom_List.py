
import random

wisdom_list=[
    'Shields grow back.',
    'Gravity is heavy.',
    'If you want to get out of going on a date, pull a spark plug out of your car and send a snap of the car not starting.',
    'Space is hard.',
    'You need to prospect to see things.',
    'We are all egg.',
    'Jormungandr in English is Jormungandr.',
    'A jumo is approximately 6 jumps. Only a Diamondback Explorer is capable of a jumo.',
    'Everything is either a banana or not a banana.',
    'Driving is just reall slow teleportation.'
    ]

def random_wisdom():
    max_int=len(wisdom_list)
    
    choice = random.randint(0, (max_int - 1))

    return wisdom_list[choice]
