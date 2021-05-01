import discord
from time import sleep

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
        sleep(int(message.content.split()[2]) * 60)
        await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')

client.run(token)