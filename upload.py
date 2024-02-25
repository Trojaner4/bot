import os
import discord
import sys
import threading

# Discord Bot-Token
TOKEN = 'YOUR_BOT_TOKEN'

# Ordnerpfad, aus dem die Dateien hochgeladen werden sollen
ORDNER_PFAD = 'files'

# Discord-Channel-ID, in den die Dateien hochgeladen werden sollen
CHANNEL_ID = YOUR_CHANNEL_ID  # Ersetze dies durch die tatsächliche Channel-ID

intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    if channel is not None:
        for filename in os.listdir(ORDNER_PFAD):
            file_path = os.path.join(ORDNER_PFAD, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        await channel.send(file=discord.File(file))
                    print(f'Datei hochgeladen: {filename}')
                    os.remove(file_path)  # Lösche die Datei nach dem Hochladen
                    print(f'Datei gelöscht: {filename}')
                except Exception as e:
                    print(f'Fehler beim Hochladen der Datei {filename}: {e}')
        print("Alle Dateien wurden hochgeladen und gelöscht. Das Programm wird beendet.")
        await client.close()  # Beende den Discord-Client
        sys.exit()  # Beende das Programm

client.run(TOKEN)
