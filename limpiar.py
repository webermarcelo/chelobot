import sys
sys.stdout.reconfigure(encoding='utf-8')
import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Canales que queremos conservar (parte del nombre)
CANALES_VALIDOS = [
    "bienvenida", "reglas", "anuncios", "roles-y-canales", "guia-del-servidor",
    "programas-de-tv", "peliculas-90s", "retro-gaming", "comics-y-manga", 
    "musica-retro", "recuerdos-y-nostalgia", "fotos-de-la-epoca",
    "charla-general", "presentaciones", "encuestas", "off-topic",
    "anuncios-de-streams", "calendario", "clips-y-highlights", 
    "sala-de-stream", "general-stream",
    "staff-chat", "logs", "sugerencias",
    "general", "gaming", "musica"
]

@bot.event
async def on_ready():
    print(f"Bot conectado: {bot.user}")
    
    for guild in bot.guilds:
        print(f"\nLimpiando servidor: {guild.name}")
        
        eliminados = 0
        
        # Revisar canales de texto
        for channel in guild.text_channels:
            nombre_lower = channel.name.lower().replace("-", "").replace("_", "")
            es_valido = any(v.replace("-", "").replace("_", "") in nombre_lower for v in CANALES_VALIDOS)
            
            if not es_valido:
                try:
                    await channel.delete()
                    print(f"  [DELETE] Texto: {channel.name}")
                    eliminados += 1
                except Exception as e:
                    print(f"  [ERROR] {channel.name}: {e}")
        
        # Revisar canales de voz
        for channel in guild.voice_channels:
            nombre_lower = channel.name.lower().replace("-", "").replace("_", "")
            es_valido = any(v.replace("-", "").replace("_", "") in nombre_lower for v in CANALES_VALIDOS)
            
            if not es_valido:
                try:
                    await channel.delete()
                    print(f"  [DELETE] Voz: {channel.name}")
                    eliminados += 1
                except Exception as e:
                    print(f"  [ERROR] {channel.name}: {e}")
        
        print(f"\n  Total eliminados: {eliminados}")
        print(f"  Canales restantes:")
        
        for cat in guild.categories:
            print(f"\n  {cat.name}:")
            for ch in cat.channels:
                print(f"    - {ch.name}")
    
    await bot.close()

bot.run(TOKEN)
