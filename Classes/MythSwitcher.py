
import random
import os

def mythSwitcher(home):
    path = home + '//Myths'
    os.chdir(path)
    directory = os.fsencode(path)
    files = os.listdir(directory)
    max_files = len(files)
    max_int = max_files-1

    choice = random.randint(0,max_int)

    file = files[choice]

    with open(file, 'r') as openedfile:
        storylist = openedfile.readlines()
        separator = ', '
        story = separator.join(storylist)

        story = story.replace(', ', '')

    return story