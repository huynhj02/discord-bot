import discord
import datetime
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import asyncio
from quote import quote
from random import choice
import pyrebase

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
}

firebase = pyrebase.initialize_app(config)
email = ""
password = ""
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()

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
    box = discord.Embed(title = "Help", description = "Use $help <command> for more details on a command\nExample: $help pomodoro\n\nRemember to stay hydrated!", color = ctx.author.color)

    box.add_field(name = "Scheduling", value = "`pomodoro`\n`add`\n`remove`\n`schedule`")
    box.add_field(name = "Miscellaneous", value = "`motivate`\n`mint`")
    box.add_field(name = "GitHub", value = "**[Link](https://github.com/huynhj02/discord-bot)**")
    box.set_footer(text = "Submission for RU Hacks 2021: Digital")
    box.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed = box)

@help.command()
async def pomodoro(ctx):
    
    box = discord.Embed(title = "Pomodoro", description = "Sets a pomodoro timer", color = ctx.author.color)
    box.add_field(name = "**Usage**", value = "$pomodoro <type> <time>\n<type> - **Work** or **Break**\n<time> - Duration in minutes")
    await ctx.send(embed = box)

@help.command()
async def add(ctx):
    
    box = discord.Embed(title = "Add", description = "Add a task to your schedule", color = ctx.author.color)
    box.add_field(name = "**Usage**", value = "$add <topic> <due date> <time due>\n<due date> - YYYY-MM-DD\n<time due> - Time between **00:00** and **23:59**")
    await ctx.send(embed = box)

@help.command() 
async def remove(ctx):

    box = discord.Embed(title = "Remove", description = "Remove a task from your schedule", color = ctx.author.color)
    box.add_field(name = "**Usage**", value = "$remove <topic>")
    await ctx.send(embed = box)

@help.command()
async def schedule(ctx):

    box = discord.Embed(title = "Schedule", description = "View your current schedule and upcoming events", color = ctx.author.color)
    await ctx.send(embed = box)

@help.command()
async def motivate(ctx):
    
    box = discord.Embed(title = "Motivate", description = "Inspirational quotes to keep you working", color = ctx.author.color)
    await ctx.send(embed = box)

@help.command()
async def mint(ctx):

    box = discord.Embed(title = "Mint", description = "Sends a picture of encouragemint!", color = ctx.author.color)
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
        await message.add_reaction('🥬')
        await message.channel.send('https://external-preview.redd.it/kbRX84LNE0yam1EgdkegfxCBJDWqJNoKzfQysnFGyJ4.jpg?auto=webp&s=5447d91784c1bd9c5bc7f492f838718906915a40')

    if len(message.content.split()) == 4 and message.content.split()[0] == ('$add'):
        try:
            date_given = datetime.datetime.strptime(f'{message.content.split()[2]} {message.content.split()[3]}', '%Y-%m-%d %H:%M')
            db.child("users").child(message.author.id).child(message.content.split()[1]).child(message.content.split()[2]).child(message.content.split()[3]).set("Active")
            await message.channel.send(f'Adding {message.content.split()[1]}')
        except:
            await message.channel.send('incorrect input : Insert as $add Topic YYYY-MM-DD 00:00')

        
    if message.content.split()[0] == ('$remove'):
        if (len(message.content.split()) == 1):
            db.child("users").child(message.author.id).remove()
        elif (len(message.content.split()) == 2):
            db.child("users").child(message.author.id).child(message.content.split()[1]).remove()
        elif (len(message.content.split()) == 3):
            db.child("users").child(message.author.id).child(message.content.split()[1]).child(message.content.split()[2]).remove()
        elif (len(message.content.split()) == 4):
            db.child("users").child(message.author.id).child(message.content.split()[1]).child(message.content.split()[2]).child(message.content.split()[3]).remove()

        await message.channel.send(f'Removed')

    if len(message.content.split()) == 1 and message.content.split()[0] == ('$schedule'):
        courses = db.child("users").child(message.author.id).get()
        for course in courses.each():
            await message.channel.send(f'Subject: {course.key()}')
            for day in course.val():
                await message.channel.send(f'Day: {day}')
                for times in (db.child("users").child(message.author.id).child(course.key()).child(day).get()).each():
                    await message.channel.send(f'Time: {times.key()}')


client.run("")