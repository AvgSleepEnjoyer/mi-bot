import discord
from discord.utils import get
import asyncio
# import subprocess
from discord.ext import commands 
from .config import bot

intents = discord.Intents.default()
intents.message_content = True

@bot.hybrid_command(name='prender_mcserver')
@commands.is_owner()

async def prender_server(ctx):
    # Usamos asyncio.create_subprocess_exec para que sea asíncrono
    # https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.subprocess.PIPE
    proceso = await asyncio.create_subprocess_exec(
        './start_mc.sh',
        cwd='/home/guillo/mcserver/',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Esperamos a que el script termine (solo tarda en crear el tmux, no en arrancar Java)
    stdout, stderr = await proceso.communicate()
    
    if proceso.returncode == 0:
        await ctx.send("✅ Servidor de Minecraft iniciado. Espera unos segundos a que cargue el mundo.")
    else:
        await ctx.send(f"❌ Error al iniciar: {stderr.decode()}")



@bot.hybrid_command(name='apagar_mcserver')
@commands.is_owner()

async def apagar_server(ctx):
    # Usamos asyncio.create_subprocess_exec para que sea asíncrono
    # https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.subprocess.PIPE
    proceso = await asyncio.create_subprocess_exec(
        './close_mc.sh',
        cwd='/home/guillo/mcserver/',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Esperamos a que el script termine (cerrará la instancia del server de minecraft)
    stdout, stderr = await proceso.communicate()

    salida = stdout.decode().strip()
    error = stderr.decode().strip()

    if proceso.returncode != 0:
        # El script falló 
        await ctx.send(f"❌ Error al apagar: {error or 'sin detalles'}")

    elif salida: # Imprime lo mismo que la terminal
        await ctx.send(f"✅ {salida}")
    else:
        # Caso raro: terminó bien pero no imprimió nada 
        await ctx.send("❓ El script terminó sin devolver mensaje.")