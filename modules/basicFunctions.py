import random
import discord
from discord.utils import get
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

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(1323481864501203015)
    if canal is None:
        return

    embed = discord.Embed(
        title="Den la bienvenida a un nuevo papu a nuestro papuservidor!",
        description=f"{member.mention} acaba de entrar al servidor.",
        color=discord.Color.blue()
    )
    embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnlydWo5OGh0cHJ3NDd0ano2Z2N1ZnA1OGNjNmV1ZzRhMjV6OW43cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HhtwEsgx7cgkeVybfN/giphy.gif")
    embed.set_thumbnail(url=member.display_avatar.url)

    await canal.send(embed=embed)


# Comandos con (, ctx es Context
@bot.hybrid_command(name='roll_dice', help='Simulates rolling dice.')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


# Repite lo que el usuario pida
@bot.command(name='di', help='Repite lo que pidas.')
async def repite(ctx, *, oracion : str):
    await ctx.message.delete()
    await ctx.send(oracion)


@bot.hybrid_command(name='soymod') # Otorgarme rol de moderador en un server con amigos
@commands.is_owner()

async def darme_rol(ctx):
    rol = discord.utils.get(ctx.guild.roles, name="Moderadores")
    
    if rol is None:
        await ctx.send("❌ No existe el rol.")
        return
    
    if rol in ctx.author.roles:
        await ctx.send(f"Ya tienes el rol **{rol.name}**.")
        return
    
    await ctx.author.add_roles(rol)
    await ctx.send(f"✅ Se te otorgó el rol **{rol.name}**, {ctx.author.mention}.")


@bot.hybrid_command(name='join') # Hacer que se una a vc (nomas pq si)
async def join(ctx):
    # Verificar que el usuario esté en un canal de voz
    if ctx.author.voice is None:
        await ctx.send("Primero entra a un canal de voz.")
        return

    # Obtener el canal y conectar
    channel = ctx.author.voice.channel
    await channel.connect(self_deaf=True, self_mute=True)

