from discord.ext import commands 
from .config import bot
import traceback

# Log de erroes
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        f.write(f'--- Error en {event} ---\n')
        f.write(traceback.format_exc())
        f.write('\n')

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