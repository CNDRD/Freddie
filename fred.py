from discord.ext import commands
from datetime import datetime
import yaml
import os

################################# Config Load #################################
config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
token = config.get('token')
prefix = str(config.get('prefix'))

################################## Functions ##################################
def cogs(cc):
    if cc == 1:
        return f"With 1 cog"
    return f"With {cc} cogs"

################################## Bot Setup ##################################
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

################################### Cog Load ##################################
cog_count = 0
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cog_count += 1

################################### Commands ##################################
@client.event
async def on_ready():
    tn = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Here comes Fred! [{cogs(cog_count)}] [{tn}]")


@client.command(aliases=['r'])
async def reload_cogs(ctx):
    y = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
            y += 1
    print(f"\nSuccesfully reloaded {y}/{cog_count} cogs!\n")
    await ctx.message.add_reaction('✅')

client.run(token)
