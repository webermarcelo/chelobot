import discord
from discord.ext import commands, tasks
import random
import json

class ContenidoAutomatico(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datos = self.cargar_datos()
    
    def cargar_datos(self):
        datos = {}
        archivos = {
            "peliculas": "data/peliculas.json",
            "series": "data/series.json",
            "juegos": "data/juegos.json",
            "canciones": "data/canciones.json",
            "datos_curiosos": "data/datos_curiosos.json",
        }
        for nombre, archivo in archivos.items():
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    datos[nombre] = json.load(f)
            except:
                datos[nombre] = []
        return datos
    
    @tasks.loop(hours=24)
    async def contenido_diario(self):
        await self.bot.wait_until_ready()
        
        for guild in self.bot.guilds:
            canal = None
            for ch in guild.text_channels:
                if "recuerdos" in ch.name or "contenido" in ch.name:
                    canal = ch
                    break
            
            if canal:
                tipo = random.choice(["pelicula", "serie", "juego", "cancion", "dato"])
                embed = self.crear_contenido(tipo)
                if embed:
                    await canal.send(embed=embed)
    
    def crear_contenido(self, tipo):
        if tipo == "pelicula" and self.datos["peliculas"]:
            item = random.choice(self.datos["peliculas"])
            embed = discord.Embed(
                title=f"Pelicula del dia: {item['titulo']}",
                description=item.get("sinopsis", ""),
                color=0xE74C3C
            )
            embed.add_field(name="Ano", value=str(item.get("anio", "N/A")), inline=True)
            embed.add_field(name="Genero", value=item.get("genero", "N/A"), inline=True)
            if item.get("dato_curioso"):
                embed.add_field(name="Dato curioso", value=item["dato_curioso"], inline=False)
            return embed
        
        elif tipo == "serie" and self.datos["series"]:
            item = random.choice(self.datos["series"])
            embed = discord.Embed(
                title=f"Serie del dia: {item['titulo']}",
                description=item.get("sinopsis", ""),
                color=0x3498DB
            )
            embed.add_field(name="Temporadas", value=str(item.get("temporadas", "N/A")), inline=True)
            return embed
        
        elif tipo == "juego" and self.datos["juegos"]:
            item = random.choice(self.datos["juegos"])
            embed = discord.Embed(
                title=f"Juego del dia: {item['titulo']}",
                description=item.get("descripcion", ""),
                color=0x2ECC71
            )
            embed.add_field(name="Plataforma", value=item.get("plataforma", "N/A"), inline=True)
            return embed
        
        elif tipo == "cancion" and self.datos["canciones"]:
            item = random.choice(self.datos["canciones"])
            embed = discord.Embed(
                title=f"Cancion del dia: {item['titulo']}",
                description=f"**Artista:** {item.get('artista', 'N/A')}",
                color=0xF39C12
            )
            embed.add_field(name="Album", value=item.get("album", "N/A"), inline=True)
            return embed
        
        elif tipo == "dato" and self.datos["datos_curiosos"]:
            item = random.choice(self.datos["datos_curiosos"])
            embed = discord.Embed(
                title="Dato curioso del dia",
                description=item.get("texto", ""),
                color=0x9B59B6
            )
            if item.get("categoria"):
                embed.add_field(name="Categoria", value=item["categoria"], inline=True)
            return embed
        
        return None

async def setup(bot):
    await bot.add_cog(ContenidoAutomatico(bot))
