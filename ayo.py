import discord
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import asyncio
from quote import quote
from random import choice

client = discord.Client()

# overwrite the default help command to look more visually appealing
client = commands.Bot(command_prefix = '$')
client.remove_command("help")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity = discord.Game('RU Hacks 2021: Digital'))

# just run this regardless
@client.group(invoke_without_command = True)
async def help(ctx):
    box = discord.Embed(title = "Help", description = "Use $help <command> for more details on a command\nExample: $help pomodoro", color = ctx.author.color)

    box.add_field(name = "Scheduling", value = "pomodoro\nadd")
    await ctx.send(embed = box)

@help.command()
async def pomodoro(ctx):
    
    box = discord.Embed(title = "Pomodoro", description = "Sets a pomodoro timer", color = ctx.author.color)
    box.add_field(name = "**Usage**", value = "$pomodoro <type> <time>\n<type> - **Work** or **Break**\n<time> - Duration in minutes")
    await ctx.send(embed = box)

@help.command()
async def add(ctx):
    
    box = discord.Embed(title = "Add", description = "In progress", color = ctx.author.color)
    await ctx.send(embed = box)

# since $help <command> exists, CommandNotFound will happen when calling a command normally
# all commands will be executed through the on_message() event
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    if message.content.startswith('$add'):
        await message.channel.send('add')

    if len(message.content.split()) == 3 and message.content.split()[0] == ('$pomodoro'):
        await message.channel.send(f'Starting timer for {message.content.split()[2]} minutes now')
        try: 
            await asyncio.sleep(timedelta(minutes=int(message.content.split()[2])).total_seconds())
            await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')
        except ValueError:
            await asyncio.sleep(timedelta(minutes=float(message.content.split()[2])).total_seconds())
            await message.channel.send(f'{message.author.mention} {message.content.split()[1]} time is done')

    if message.content == '$motivate':
        motivate = quote('Motivational Quotes', limit=100)
        await message.channel.send(choice(motivate)['quote'])

    if message.content == '$mint':
        await message.channel.send('https://external-preview.redd.it/kbRX84LNE0yam1EgdkegfxCBJDWqJNoKzfQysnFGyJ4.jpg?auto=webp&s=5447d91784c1bd9c5bc7f492f838718906915a40')

client.run('')