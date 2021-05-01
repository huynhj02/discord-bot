import discord
from datetime import datetime, timedelta
import asyncio

client = discord.Client()
times = {datetime.min : 'Ayo'}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    while True:
        await asyncio.sleep(60)
        now = datetime.now() - timedelta(seconds=datetime.now().second, microseconds=datetime.now().microsecond)
        if now in times:
            await message.channel.send(f'{times[now]} time is done')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$add'):
        await message.channel.send('add')

    if len(message.content.split()) == 3 and message.content.split()[0] == ('$pomodoro'):
        await message.channel.send(f'Starting timer for {message.content.split()[2]} minutes now')
        current = datetime.now() - timedelta(seconds=datetime.now().second, microseconds=datetime.now().microsecond)
        '''alarmTime = datetime.now() + timedelta(minutes=int(message.content.split()[2]))
        print(datetime.now())
        print(alarmTime)
        while datetime.now() <= alarmTime:
            continue
        await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')'''
        times.popitem()
        times[current] = message.author.mention + message.content.split()[1]

client.run('ODM4MDczMjQyMTc0NDg4NjI2.YI1yhw.c1jyAR00tSen2WdSWf4KwuGCLMs')