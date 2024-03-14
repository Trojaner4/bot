import os
import discord
from discord.ext import commands

TOKEN = 'MTIwOTQ0MDczNTY4NzA5MDI0Ng.GNcvNs.JfeXYOuFKnW2I3GgZaNIUWJVAFh26bRUhM3isg'
CHANNEL_ID = 1211228296340049960  # ID des Discord-Kanals, aus dem die Dateien heruntergeladen werden sollen
SPLIT_PREFIX = 'split_'  # Prefix für die gesplitteten Dateien
MERGED_DIRECTORY = 'merged'  # Verzeichnis zum Speichern der zusammengefügten Dateien

intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

async def download_and_join():
    downloaded_dir = os.path.join(os.getcwd(), 'downloaded')
    if not os.path.exists(downloaded_dir):
        os.makedirs(downloaded_dir)

    merged_file_path = os.path.join(downloaded_dir, ORIGINAL_FILE)
    if os.path.exists(merged_file_path):
        print(f'Die Datei "{ORIGINAL_FILE}" wurde bereits heruntergeladen und zusammengefügt.')
        return

    print(f'Suche nach Teilen für die Datei "{ORIGINAL_FILE}"...')
    channel = client.get_channel(CHANNEL_ID)
    parts = []
    async for message in channel.history(limit=None):
        for attachment in message.attachments:
            if ORIGINAL_FILE in attachment.filename:
                parts.append(attachment)
    if len(parts) == 0:
        print(f'Keine Teile für die Datei "{ORIGINAL_FILE}" gefunden.')
        return

    print(f'Gefundene Teile für die Datei "{ORIGINAL_FILE}":')
    for part in parts:
        print(part.filename)

    parts.sort(key=lambda x: int(x.filename.split('_')[-1].split('.')[0][4:]))
    with open(merged_file_path, 'wb') as merged_file:
        for part in parts:
            print(f'Herunterladen und Hinzufügen von Teil "{part.filename}"...')
            file_path = os.path.join(downloaded_dir, part.filename)
            await part.save(file_path)
            with open(file_path, 'rb') as part_file:
                merged_file.write(part_file.read())
            print(f'Teil "{part.filename}" erfolgreich heruntergeladen und hinzugefügt.')

    print(f'Alle Teile für die Datei "{ORIGINAL_FILE}" heruntergeladen und zusammengefügt.')
    exit(0)
@client.event
async def on_ready():
    print('Bot ist bereit!')
    await download_and_join()

# Öffne die Textdatei und zeige ihren Inhalt an
with open('original_file_names.txt', 'r') as f:
    available_files_content = f.read()

print("Verfügbare Dateien:")
print(available_files_content)
print()

# Fordere den Benutzer auf, den gewünschten Dateinamen einzugeben
ORIGINAL_FILE = input("Welche Datei möchten Sie herunterladen? ")

client.run(TOKEN)
