#Sources: https://docs.pycord.dev/en/stable/ext/commands/api.html#discord.ext.commands.Bot.command_prefix

#Application command - /slash command (from discord import Bot)
# PRefixed command (Application Command) - from discord.ext.commands
# BRidge commands - from discord.ext.bridge Cogs
from discord.ext import commands
from discord.ext.bridge import Bot, BridgeContext, has_permissions
import discord
from settings import TOKEN

#Creating bot object and assigning it to a variable, passing my command prefix and permissions as parameters
my_bot = Bot(command_prefix = "!", intents = discord.Intents.all())

#Will print bot's username
@my_bot.event
async def on_ready():
    print(f'{my_bot.user.name}')
    
#bridge command will await message with prefix or /
@my_bot.bridge_command()
async def ping(ctx: BridgeContext):
    #waiting for the user to respond with !ping or /ping to respond with Pong
    await ctx.respond("Pong")

@my_bot.bridge_command(description="A command to ban users")
#Checking attributes permissions to make sure that the user who is operating this command has admin
@has_permissions(administrator=True)
async def ban(ctx: BridgeContext, user: discord.Member):
    await ctx.guild.ban(user)
    await ctx.respond(f'{user.mention} has been banned!')

@ban.error
async def ban_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("Please properly use the command.")
    print(error)

my_bot.run(TOKEN)
