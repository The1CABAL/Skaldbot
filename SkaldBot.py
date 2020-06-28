
import discord

client = discord.Client()

@client.event

async def on_ready():

    print('Hello, I am the skald bot! I am logged in as {0.user}'.format(client))

@client.event

async def on_message(message):

    if message.author == client.user:

        return

    if message.content.startswith('$story'):
        await message.channel.send('This is the story of the brave I.N.S. Gungnir. It is not a story you will hear often, but the Gungnir died for this squadron. The Gungnir selfishly launched to earn several million credits for the poor unfortunate souls who are too weak to earn credits for themselves in any way other than mining. Yet despite the numerous foes who fell at the hands of her brave captain, the Gungnir fell to a simple Fer De Lance who shall not be named. Though resurrected, the Gungnir will be forever immortalized in the memories of the Jotun''s Angels. Gods speed to the Gungnir and her captain. o7 \n\nI am a bot. If you want to know why I exist type "$why" but without the quote symbols')

    if message.content.startswith('$why'):
        await message.channel.send('Isaac lost his ship to the Fer De Lance mentioned in the story so he drank over 6 ounces of rum and wrote a discord bot. \n\nI am a bot if you would like me to say something new please type "$newStory" but without the quotes.')

    if message.content.startswith('$newStory'):
        await message.channel.send('I am sorry but I cannot bring myself to tell any other story for no story is as tragic as thr story you will hear from typing "$story" without the quotes..."')

client.run('NzI2NjQwNzQ2MzU4MjQzNDA4.XvgPQA.QoyXYwl0fhGr6iVGWZy4ggbwHVw')