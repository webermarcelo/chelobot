import discord
from discord.ext import commands
import os
import json
from config import TOKEN, CANALES, ROLES, COLORES

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Crear el bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento: Bot listo
@bot.event
async def on_ready():
    print(f"=========================================")
    print(f"  CheloBot conectado como {bot.user}")
    print(f"  Servidores: {len(bot.guilds)}")
    print(f"=========================================")
    
    # Cargar todos los cogs (modulos)
    cogs_list = [
        "cogs.bienvenida",
        "cogs.nostalgia",
        "cogs.utilidad",
        "cogs.moderacion",
        "cogs.streams",
    ]
    
    for cog in cogs_list:
        try:
            await bot.load_extension(cog)
            print(f"  [OK] Cargado: {cog}")
        except Exception as e:
            print(f"  [ERROR] Error cargando {cog}: {e}")
    
    print(f"=========================================")
    print(f"  CheloBot listo para usar!")
    print(f"  Prefijo: !")
    print(f"=========================================")
    
    # Establecer activity (estado del bot)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="la nostalgia de los 90s | !ayuda"
        )
    )

# Comando de ayuda personalizado
@bot.command(name="ayuda")
async def ayuda(ctx):
    embed = discord.Embed(
        title="CheloBot - Comandos Disponibles",
        description="Tu bot de nostalgia de los 90s y 2000s",
        color=COLORES["principal"]
    )
    
    embed.add_field(
        name="Nostalgia",
        value=(
            "`!pelicula90` - Pelicula aleatoria de los 90s\n"
            "`!serie90` - Serie aleatoria de los 90s\n"
            "`!juego8bit` - Juego retro aleatorio\n"
            "`!musica90` - Cancion de los 90s\n"
            "`!dime90` - Dato curioso de la epoca\n"
            "`!anime90` - Anime clasico"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Utilidad",
        value=(
            "`!info` - Info del servidor\n"
            "`!encuesta [pregunta] | [opcion1] | [opcion2]` - Crear encuesta\n"
            "`!recordatorio [tiempo] [mensaje]` - Programar recordatorio\n"
            "`!perfil` - Tu perfil de nostalgia"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Moderacion (Solo Admin)",
        value=(
            "`!limpiar [cantidad]` - Limpiar mensajes\n"
            "`!silenciar @usuario [tiempo]` - Silenciar miembro\n"
            "`!desilenciar @usuario` - Quitar silencio\n"
            "`!expulsar @usuario [razon]` - Expulsar miembro"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Streams",
        value=(
            "`!crear_stream [nombre]` - Crear sala temporal\n"
            "`!cerrar_stream` - Cerrar sala temporal\n"
            "`!stream_info` - Info del stream actual"
        ),
        inline=False
    )
    
    embed.set_footer(text="CheloBot v1.0 | Hecho con amor por los 90s")
    await ctx.send(embed=embed)

# Ejecutar el bot
if __name__ == "__main__":
    bot.run(TOKEN)
