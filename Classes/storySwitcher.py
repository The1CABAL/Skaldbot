
import random
import os

def storySwitcher(home, folder):
    path = home + '//' + folder
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

def storyFinder(home, folder, iteration = ''):
    path = home + '//' + folder
    os.chdir(path)
    directory = os.fsencode(path)
    foundfiles = os.listdir(directory)
    cleaned_files = {}

    count = 1
    for i in foundfiles:
        i = str(i).replace('.txt''', '')
        i = str(i).replace('b''', '')
        cleaned_files.update({count:i})

        count += 1

    if iteration == '':
        return cleaned_files
    else:
        file = foundfiles[iteration-1]

        with open(file, 'r') as openedfile:
            storylist = openedfile.readlines()
            separator = ', '
            story = separator.join(storylist)

            story = story.replace(', ', '')

        return story
