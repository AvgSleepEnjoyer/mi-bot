import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='(', intents=intents)

@bot.command()
@commands.is_owner()
async def sync(ctx):
    # Sincroniza los comandos hybrid para usar con "/" igual que con comando, usar cada que se añada un comando
    bot.tree.copy_global_to(guild=ctx.guild)
    synced = await bot.tree.sync(guild=ctx.guild)
    await ctx.send(f"Sincronicé {len(synced)} comandos en este servidor.")
