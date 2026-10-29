import random
import discord
import asyncio
import subprocess
from discord.ext import commands
from .config import bot

# Mensaje de bot encendido
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Lector de mensajes y manda respuesta segun el mensaje
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'puta':
        await message.channel.send("Puta tú")
    elif message.content == '99!':
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            'Cool. Cool cool cool cool cool cool cool, no doubt no doubt no doubt no doubt.',
        ]
        await message.channel.send(random.choice(brooklyn_99_quotes))
    

    # --- ESTO es lo que hace funcionar @bot.command ---
    # Como tal esta por si acaso se cambia de logica
    await bot.process_commands(message)

# Log de errores
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            f.write(f'Unhandled event {event}: {args}\n')

@bot.event
async def on_command_error(ctx, error):
    # Registramos el error en el mismo archivo de log
    with open('err.log', 'a') as f:
        f.write(f'Error en comando {ctx.command}: {error}\n')

    if isinstance(error, commands.NotOwner):
        await ctx.send("🤓 Este comando es solo para el dueño del bot.")
        return
    
    # Aavisar al usuario en el chat
    await ctx.send(f"Ocurrió un error: {error}")

# Comandos con !, ctx es Context
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

    
@bot.command(name='prender_server')
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



@bot.command(name='apagar_server')
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