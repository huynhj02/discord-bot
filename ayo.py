import discord
from datetime import datetime, timedelta
import asyncio

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
        alarmTime = datetime.now() + timedelta(minutes=int(message.content.split()[2]))
        while datetime.now() <= alarmTime:
            continue
        await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')

client.run(token)