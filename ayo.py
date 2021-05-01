import discord
from datetime import datetime, timedelta
import asyncio
from quote import quote
from random import choice

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$add'):
        await message.channel.send('add')

    if len(message.content.split()) == 3 and message.content.split()[0] == ('$pomodoro'):
        await message.channel.send(f'Starting timer for {message.content.split()[2]} minutes now')
        await asyncio.sleep(timedelta(minutes=int(message.content.split()[2])).total_seconds())
        await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')

    if message.content == '$motivate':
        motivate = quote('Motivational Quotes', limit=100)
        await message.channel.send(choice(motivate)['quote'])

client.run('ODM4MDczMjQyMTc0NDg4NjI2.YI1yhw.sdFMhWmwc8OJ0tLjk-l8puO9nRo')