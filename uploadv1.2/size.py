import discord
from discord.ext import commands

# Discord Bot-Token
TOKEN = 'TOKEN'

# Discord-Channel-ID, den du durchsuchen möchtest
TARGET_CHANNEL_ID = 1211228296340049960  # Ersetze dies durch die tatsächliche Channel-ID

# Bot erstellen mit den erforderlichen Intents
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event, das beim Starten des Bots aufgerufen wird
@bot.event
async def on_ready():
    print(f'{bot.user} ist bereit')

    # Überprüfen, ob der Bot im richtigen Kanal ist
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        total_size = 0  # Gesamtgröße aller Anhänge
        async for message in channel.history(limit=None):
            # Überprüfen, ob die Nachricht Anhänge enthält
            if message.attachments:
                for attachment in message.attachments:
                    total_size += attachment.size
        total_size_gb = total_size / (1024 * 1024 * 1024)  # Umrechnung in Gigabytes
        print(f'Die Gesamtgröße aller Anhänge im Kanal beträgt: {total_size_gb:.2f} GB')
    else:
        print("Kanal nicht gefunden!")
    exit(0)
# Bot starten
bot.run(TOKEN)
