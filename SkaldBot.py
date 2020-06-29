
import discord
from Classes.storySwitcher import storySwitcher
from Classes.MythSwitcher import mythSwitcher
import os

home = os.getcwd()

client = discord.Client()

@client.event

async def on_ready():

    print('Hello, I am the skald bot! I am logged in as {0.user}'.format(client))

@client.event

async def on_message(message):

    if message.author == client.user:

        return

    if message.content.startswith('$story'):
        story = storySwitcher(home)
        await message.channel.send(str(story))

    if message.content.startswith('$why'):
        await message.channel.send('Isaac lost his ship to the Fer De Lance mentioned in one of the stories so he drank over 6 ounces of rum and wrote a discord bot. \n\nI am a bot if you would like me to say something new please type "$newStory" but without the quotes.')

    if message.content.startswith('$wisdom'):
        await message.channel.send('Shields grow back. \n\nThis has been the wisdom of the gods.')

    if message.content.startswith('$myth'):
        myth = mythSwitcher(home)
        await message.channel.send(str(myth))

client.run('NzI2NjQwNzQ2MzU4MjQzNDA4.XvgPQA.QoyXYwl0fhGr6iVGWZy4ggbwHVw')