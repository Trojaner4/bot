import discord
from discord.ext import commands
import asyncio
# Discord Bot-TOKEN
TOKEN = 'TOKEN'

# Discord-Channel-ID, in dem die Anhänge überprüft werden sollen
TARGET_CHANNEL_ID = 1211228296340049960  # Ersetze dies durch die tatsächliche Channel-ID

# Bot erstellen mit den erforderlichen Intents
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Liste für die gesendeten Dateinamen
sent_filenames = set()

# Event, das beim Starten des Bots aufgerufen wird
@bot.event
async def on_ready():
    print(f'{bot.user} ist bereit')

    # Überprüfen, ob der Bot im richtigen Kanal ist
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        # Durchlaufen der Nachrichten im Kanalverlauf
        async for message in channel.history(limit=None):
            # Überprüfen, ob die Nachricht Anhänge enthält
            if message.attachments:
                for attachment in message.attachments:
                    # Überprüfen, ob die Datei bereits in der Liste der gesendeten Dateinamen vorhanden ist
                    if attachment.filename in sent_filenames:
                        # Nachricht löschen, wenn die Datei bereits gesendet wurde
                        await message.delete()
                        print(f'Nachricht von {message.author} gelöscht, da die Datei "{attachment.filename}" bereits gesendet wurde.')
                        await asyncio.sleep(1)  # Pause von 1 Sekunde
                    else:
                        # Dateinamen zur Liste der gesendeten Dateinamen hinzufügen
                        sent_filenames.add(attachment.filename)
    else:
        print("Kanal nicht gefunden!")

# Bot starten
bot.run(TOKEN)
