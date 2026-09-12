import sys
sys.stdout.reconfigure(encoding='utf-8')
import discord
from discord.ext import commands
import asyncio
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Estructura deseada del servidor
ESTRUCTURA = {
    "INFORMACION": {
        "canales_texto": ["👋-bienvenida", "📜-reglas", "📢-anuncios", "🎭-roles-y-canales", "ℹ️-guia-del-servidor"],
        "canales_voz": []
    },
    "CONTENIDO RETRO": {
        "canales_texto": ["📺-programas-de-tv", "🎬-peliculas-90s", "🎮-retro-gaming", "📚-comics-y-manga", "🎵-musica-retro", "💭-recuerdos-y-nostalgia", "📸-fotos-de-la-epoca"],
        "canales_voz": []
    },
    "COMUNIDAD": {
        "canales_texto": ["💬-charla-general", "👋-presentaciones", "📊-encuestas", "🎲-off-topic"],
        "canales_voz": []
    },
    "STREAMS": {
        "canales_texto": ["📢-anuncios-de-streams", "📅-calendario", "🎥-clips-y-highlights"],
        "canales_voz": ["🔊-sala-de-stream", "🔊-general-stream"]
    },
    "ADMINISTRACION": {
        "canales_texto": ["🔒-staff-chat", "📝-logs", "💡-sugerencias"],
        "canales_voz": []
    },
    "ZONA AUDIO": {
        "canales_texto": [],
        "canales_voz": ["🔊-general", "🔊-gaming", "🔊-musica"]
    }
}

@bot.event
async def on_ready():
    print(f"Bot conectado: {bot.user}")
    
    for guild in bot.guilds:
        print(f"\nReestructurando servidor: {guild.name}")
        
        # 1. Eliminar canales existentes (excepto los que queremos conservar)
        canales_a_conservar = ["bienvenida", "reglas", "anuncios", "charla-general"]
        
        for channel in guild.channels:
            nombre_limpio = channel.name.replace("-", "").replace("_", "").lower()
            conservar = any(c.replace("-", "").replace("_", "").lower() in nombre_limpio for c in canales_a_conservar)
            
            if not conservar:
                try:
                    await channel.delete()
                    print(f"  [DELETE] {channel.name}")
                except Exception as e:
                    print(f"  [ERROR] No se pudo eliminar {channel.name}: {e}")
        
        # 2. Eliminar categorias existentes
        for category in guild.categories:
            try:
                await category.delete()
                print(f"  [DELETE] Categoria: {category.name}")
            except Exception as e:
                print(f"  [ERROR] No se pudo eliminar categoria {category.name}: {e}")
        
        await asyncio.sleep(1)
        
        # 3. Crear nueva estructura
        for nombre_cat, canales in ESTRUCTURA.items():
            try:
                categoria = await guild.create_category(nombre_cat)
                print(f"  [CREATE] Categoria: {nombre_cat}")
                
                # Crear canales de texto
                for nombre_canal in canales["canales_texto"]:
                    try:
                        await guild.create_text_channel(nombre_canal, category=categoria)
                        print(f"    [CREATE] Texto: {nombre_canal}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"    [ERROR] No se pudo crear {nombre_canal}: {e}")
                
                # Crear canales de voz
                for nombre_canal in canales["canales_voz"]:
                    try:
                        await guild.create_voice_channel(nombre_canal, category=categoria)
                        print(f"    [CREATE] Voz: {nombre_canal}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"    [ERROR] No se pudo crear {nombre_canal}: {e}")
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"  [ERROR] No se pudo crear categoria {nombre_cat}: {e}")
        
        # 4. Configurar rol @everyone
        try:
            everyone = guild.default_role
            await everyone.edit(permissions=discord.Permissions(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                connect=True,
                speak=True,
                add_reactions=True,
                use_external_emojis=True,
            ))
            print("\n  [OK] Permisos de @everyone configurados")
        except Exception as e:
            print(f"\n  [ERROR] No se pudieron configurar permisos: {e}")
        
        print(f"\n=========================================")
        print(f"  SERVIDOR REESTRUCTURADO!")
        print(f"=========================================")
    
    await bot.close()

bot.run(TOKEN)
