import os
import discord
import sys
import threading
from tqdm import tqdm
import time
import asyncio
import psutil

# Discord Bot-Token
TOKEN = 'TOKEN'

# Ordnerpfad, aus dem die Dateien hochgeladen werden sollen
ORDNER_PFAD = 'files'

# Discord-Channel-ID, in den die Dateien hochgeladen werden sollen
CHANNEL_ID = 1211228296340049960  # Ersetze dies durch die tatsächliche Channel-ID

intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

async def upload_file(channel, filename, progress_bar):
    file_path = os.path.join(ORDNER_PFAD, filename)
    try:
        start_time = time.time()
        bytes_uploaded = 0
        with open(file_path, 'rb') as file:
            message = await channel.send(file=discord.File(file))
            while not message.attachments:
                await asyncio.sleep(0.1)  # Wait for the message to be processed
            attachment = message.attachments[0]
            bytes_uploaded = attachment.size
        end_time = time.time()
        elapsed_time = end_time - start_time
        file_size = os.path.getsize(file_path)
        upload_speed = bytes_uploaded / elapsed_time / (1024 * 1024)  # Convert to MB/s
        progress_bar.set_postfix({"Speed": f"{upload_speed:.2f} MB/s"})
        os.remove(file_path)  # Lösche die Datei nach dem Hochladen
    except Exception as e:
        print(f'Fehler beim Hochladen der Datei {filename}: {e}')

async def update_upload_speed(progress_bar):
    while True:
        current_bytes_sent = psutil.net_io_counters().bytes_sent
        await asyncio.sleep(0.5)
        new_bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_uploaded = new_bytes_sent - current_bytes_sent
        upload_speed = bytes_uploaded / 0.5 / (1024 * 1024)  # Convert to MB/s
        progress_bar.set_postfix({"Speed": f"{upload_speed:.2f} MB/s"})

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    if channel is not None:
        files = os.listdir(ORDNER_PFAD)
        total_files = len(files)
        with tqdm(total=total_files, desc="Dateien hochladen") as progress_bar:
            for filename in files:
                asyncio.create_task(update_upload_speed(progress_bar))
                await upload_file(channel, filename, progress_bar)
                progress_bar.update(1)  # Update the progress bar after each file
        print("Alle Dateien wurden hochgeladen und gelöscht. Das Programm wird beendet.")
        await client.close()  # Beende den Discord-Client
        sys.exit()  # Beende das Programm

client.run(TOKEN)
