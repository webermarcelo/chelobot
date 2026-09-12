import sys
sys.stdout.reconfigure(encoding='utf-8')
import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import os
from datetime import datetime, timedelta

TOKEN = os.getenv("CHELOBOT_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Descripciones de canales
DESCRIPCIONES = {
    'bienvenida': 'Canal automatico de bienvenida para nuevos miembros',
    'reglas': 'Lee las reglas del servidor antes de escribir',
    'anuncios': 'Anuncios oficiales del servidor',
    'roles-y-canales': 'Elige tus roles para acceder a canales exclusivos',
    'guia-del-servidor': 'Guia completa del servidor y comandos de CheloBot',
    'programas-de-tv': 'Friends, Los Simpson, Seinfeld, Buffy... Hablamos de todas las series de los 90s',
    'peliculas-90s': 'Titanic, Matrix, Jurassic Park... Comparte tus peliculas favoritas',
    'retro-gaming': 'NES, SNES, Game Boy, PS1... La epoca dorada de los videojuegos',
    'comics-y-manga': 'Marvel, DC, Dragon Ball, Sailor Moon... Comics y manga clasico',
    'musica-retro': 'Nirvana, Spice Girls, Backstreet Boys... La musica que definio una generacion',
    'recuerdos-y-nostalgia': 'Comparte tus recuerdos de la epoca: que jugabas, que mirabas, que escuchabas',
    'fotos-de-la-epoca': 'Comparte fotos vintage, captures de TV, portadas de juegos',
    'charla-general': 'Habla de lo que quieras con la comunidad',
    'presentaciones': 'Presentate cuando entres al servidor',
    'encuestas': 'Participa de las encuestas y votaciones',
    'off-topic': 'Habla de cualquier cosa que no sea nostalgia',
    'anuncios-de-streams': 'Proximos streams y eventos en vivo',
    'calendario': 'Calendario de eventos y actividades',
    'clips-y-highlights': 'Comparte los mejores momentos de los streams',
    'staff-chat': 'Canal privado del equipo de moderacion',
    'logs': 'Registro de actividad del servidor (solo administradores)',
    'sugerencias': 'Propone mejoras para el servidor',
}

# Roles por interes
ROLES_INTERES = {
    "🎮": "Retro Gamer",
    "🎬": "Cinefilo 90s",
    "📺": "Fan de la TV",
    "🎵": "Melomano Retro",
    "📚": "Fan del Comic",
    "🗾": "Otaku 90s",
}

# Datos de nivel
nivel_data = {}

def cargar_niveles():
    global nivel_data
    if os.path.exists("data/niveles.json"):
        with open("data/niveles.json", "r", encoding="utf-8") as f:
            nivel_data = json.load(f)
    else:
        nivel_data = {}

def guardar_niveles():
    with open("data/niveles.json", "w", encoding="utf-8") as f:
        json.dump(nivel_data, f, indent=2, ensure_ascii=False)

def calcular_nivel(xp):
    return int((xp / 100) ** 0.5)

@bot.event
async def on_ready():
    print(f"=========================================")
    print(f"  CheloBot conectado como {bot.user}")
    print(f"  Servidores: {len(bot.guilds)}")
    print(f"=========================================")
    
    cargar_niveles()
    
    # Configurar descripciones
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name in DESCRIPCIONES:
                try:
                    if channel.topic != DESCRIPCIONES[channel.name]:
                        await channel.edit(topic=DESCRIPCIONES[channel.name])
                        print(f"  [OK] Descripcion: {channel.name}")
                except:
                    pass
    
    # Cargar cogs
    cogs_list = [
        "cogs.bienvenida",
        "cogs.nostalgia",
        "cogs.utilidad",
        "cogs.moderacion",
        "cogs.streams",
        "cogs.roles",
        "cogs.niveles",
        "cogs.contenido_automatico",
        "cogs.eventos",
        "cogs.verificacion",
    ]
    
    for cog in cogs_list:
        try:
            await bot.load_extension(cog)
            print(f"  [OK] Cargado: {cog}")
        except Exception as e:
            print(f"  [ERROR] {cog}: {e}")
    
    print(f"=========================================")
    print(f"  CheloBot listo para usar!")
    print(f"=========================================")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="la nostalgia de los 90s | !ayuda"
        )
    )
    
    # Iniciar tarea de contenido automatico
    if not contenido_diario.is_running():
        contenido_diario.start()

# Comando de ayuda
@bot.command(name="ayuda")
async def ayuda(ctx):
    embed = discord.Embed(
        title="CheloBot - Comandos Disponibles",
        description="Tu bot de nostalgia de los 90s y 2000s",
        color=0x9B59B6
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
            "`!encuesta` - Crear encuesta\n"
            "`!recordatorio` - Programar recordatorio\n"
            "`!perfil` - Tu perfil de nostalgia\n"
            "`!nivel` - Ver tu nivel"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Roles",
        value=(
            "`!roles` - Ver roles disponibles\n"
            "`!rol [emoji]` - Obtener un rol"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Eventos",
        value=(
            "`!crear_evento` - Crear un evento\n"
            "`!eventos` - Ver proximos eventos\n"
            "`!recordar_evento` - Enviar recordatorio"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Verificacion",
        value=(
            "`!verificar` - Verificarse para acceder\n"
            "`!setup_verificacion` - Configurar verificacion (admin)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Moderacion (Solo Admin)",
        value=(
            "`!limpiar` - Limpiar mensajes\n"
            "`!silenciar` - Silenciar miembro\n"
            "`!expulsar` - Expulsar miembro"
        ),
        inline=False
    )
    
    embed.set_footer(text="CheloBot v1.1 | Hecho con amor por los 90s")
    await ctx.send(embed=embed)

# Sistema de niveles por mensajes
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Actualizar XP
    user_id = str(message.author.id)
    if user_id not in nivel_data:
        nivel_data[user_id] = {"xp": 0, "nivel": 0, "mensajes": 0}
    
    nivel_data[user_id]["xp"] += random.randint(5, 15)
    nivel_data[user_id]["mensajes"] += 1
    
    nivel_actual = calcular_nivel(nivel_data[user_id]["xp"])
    nivel_anterior = nivel_data[user_id]["nivel"]
    
    if nivel_actual > nivel_anterior:
        nivel_data[user_id]["nivel"] = nivel_actual
        embed = discord.Embed(
            title=f"Subiste de nivel!",
            description=f"{message.author.mention} ahora eres **Nivel {nivel_actual}**!",
            color=0x9B59B6
        )
        await message.channel.send(embed=embed)
    
    guardar_niveles()
    await bot.process_commands(message)

# Contenido automatico diario
@tasks.loop(hours=24)
async def contenido_diario():
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        # Buscar canal de memes o contenido
        canal = None
        for ch in guild.text_channels:
            if "recuerdos" in ch.name or "contenidoretro" in ch.name:
                canal = ch
                break
        
        if canal:
            # Seleccionar contenido aleatorio
            tipo = random.choice(["pelicula", "serie", "juego", "cancion", "dato"])
            
            if tipo == "pelicula":
                with open("data/peliculas.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                item = random.choice(datos)
                embed = discord.Embed(
                    title=f"Pelicula del dia: {item['titulo']}",
                    description=item.get("sinopsis", ""),
                    color=0xE74C3C
                )
                embed.add_field(name="Ano", value=str(item.get("anio", "N/A")), inline=True)
                embed.add_field(name="Genero", value=item.get("genero", "N/A"), inline=True)
            elif tipo == "serie":
                with open("data/series.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                item = random.choice(datos)
                embed = discord.Embed(
                    title=f"Serie del dia: {item['titulo']}",
                    description=item.get("sinopsis", ""),
                    color=0x3498DB
                )
                embed.add_field(name="Temporadas", value=str(item.get("temporadas", "N/A")), inline=True)
            elif tipo == "juego":
                with open("data/juegos.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                item = random.choice(datos)
                embed = discord.Embed(
                    title=f"Juego del dia: {item['titulo']}",
                    description=item.get("descripcion", ""),
                    color=0x2ECC71
                )
                embed.add_field(name="Plataforma", value=item.get("plataforma", "N/A"), inline=True)
            elif tipo == "cancion":
                with open("data/canciones.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                item = random.choice(datos)
                embed = discord.Embed(
                    title=f"Cancion del dia: {item['titulo']}",
                    description=f"**Artista:** {item.get('artista', 'N/A')}",
                    color=0xF39C12
                )
            else:
                with open("data/datos_curiosos.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                item = random.choice(datos)
                embed = discord.Embed(
                    title="Dato curioso del dia",
                    description=item.get("texto", ""),
                    color=0x9B59B6
                )
            
            embed.set_footer(text="CheloBot | Contenido automatico diario")
            await canal.send(embed=embed)

# Comando para ver nivel
@bot.command(name="nivel")
async def ver_nivel(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    user_id = str(member.id)
    if user_id in nivel_data:
        data = nivel_data[user_id]
        nivel = data["nivel"]
        xp = data["xp"]
        mensajes = data["mensajes"]
        xp_siguiente = ((nivel + 1) ** 2) * 100
        
        embed = discord.Embed(
            title=f"Nivel de {member.name}",
            color=0x9B59B6
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Nivel", value=str(nivel), inline=True)
        embed.add_field(name="XP", value=f"{xp}/{xp_siguiente}", inline=True)
        embed.add_field(name="Mensajes", value=str(mensajes), inline=True)
        
        # Barra de progreso
        porcentaje = (xp / xp_siguiente) * 100
        barra = "█" * int(porcentaje / 10) + "░" * (10 - int(porcentaje / 10))
        embed.add_field(name="Progreso", value=f"`{barra}` {porcentaje:.1f}%", inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Aun no tienes datos. Escribe mensajes para ganar XP!")

bot.run(TOKEN)
