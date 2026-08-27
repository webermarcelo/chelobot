import discord
from discord.ext import commands
import random
import json
import os

class Nostalgia(commands.Cog):
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
            "animes": "data/animes.json",
        }
        for nombre, archivo in archivos.items():
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    datos[nombre] = json.load(f)
            else:
                datos[nombre] = []
        return datos
    
    def elegir_aleatorio(self, lista):
        if not lista:
            return None
        return random.choice(lista)
    
    @commands.command(name="pelicula90")
    async def pelicula90(self, ctx):
        pelicula = self.elegir_aleatorio(self.datos.get("peliculas", []))
        if not pelicula:
            await ctx.send("No hay peliculas en la base de datos.")
            return
        embed = discord.Embed(
            title=pelicula['titulo'],
            description=pelicula.get("sinopsis", "Sin sinopsis disponible."),
            color=0xE74C3C
        )
        embed.add_field(name="Ano", value=str(pelicula.get("anio", "N/A")), inline=True)
        embed.add_field(name="Genero", value=pelicula.get("genero", "N/A"), inline=True)
        if pelicula.get("dato_curioso"):
            embed.add_field(name="Dato curioso", value=pelicula["dato_curioso"], inline=False)
        embed.set_footer(text="CheloBot | Peliculas de los 90s")
        await ctx.send(embed=embed)
    
    @commands.command(name="serie90")
    async def serie90(self, ctx):
        serie = self.elegir_aleatorio(self.datos.get("series", []))
        if not serie:
            await ctx.send("No hay series en la base de datos.")
            return
        embed = discord.Embed(
            title=serie['titulo'],
            description=serie.get("sinopsis", "Sin sinopsis disponible."),
            color=0x3498DB
        )
        embed.add_field(name="Temporadas", value=str(serie.get("temporadas", "N/A")), inline=True)
        embed.add_field(name="Genero", value=serie.get("genero", "N/A"), inline=True)
        if serie.get("dato_curioso"):
            embed.add_field(name="Dato curioso", value=serie["dato_curioso"], inline=False)
        embed.set_footer(text="CheloBot | Series de los 90s")
        await ctx.send(embed=embed)
    
    @commands.command(name="juego8bit")
    async def juego8bit(self, ctx):
        juego = self.elegir_aleatorio(self.datos.get("juegos", []))
        if not juego:
            await ctx.send("No hay juegos en la base de datos.")
            return
        embed = discord.Embed(
            title=juego['titulo'],
            description=juego.get("descripcion", "Sin descripcion disponible."),
            color=0x2ECC71
        )
        embed.add_field(name="Plataforma", value=juego.get("plataforma", "N/A"), inline=True)
        embed.add_field(name="Ano", value=str(juego.get("anio", "N/A")), inline=True)
        if juego.get("dato_curioso"):
            embed.add_field(name="Dato curioso", value=juego["dato_curioso"], inline=False)
        embed.set_footer(text="CheloBot | Juegos retro")
        await ctx.send(embed=embed)
    
    @commands.command(name="musica90")
    async def musica90(self, ctx):
        cancion = self.elegir_aleatorio(self.datos.get("canciones", []))
        if not cancion:
            await ctx.send("No hay canciones en la base de datos.")
            return
        embed = discord.Embed(
            title=cancion['titulo'],
            description=f"**Artista:** {cancion.get('artista', 'N/A')}",
            color=0xF39C12
        )
        embed.add_field(name="Album", value=cancion.get("album", "N/A"), inline=True)
        embed.add_field(name="Ano", value=str(cancion.get("anio", "N/A")), inline=True)
        if cancion.get("dato_curioso"):
            embed.add_field(name="Dato curioso", value=cancion["dato_curioso"], inline=False)
        embed.set_footer(text="CheloBot | Musica de los 90s")
        await ctx.send(embed=embed)
    
    @commands.command(name="anime90")
    async def anime90(self, ctx):
        anime = self.elegir_aleatorio(self.datos.get("animes", []))
        if not anime:
            await ctx.send("No hay animes en la base de datos.")
            return
        embed = discord.Embed(
            title=anime['titulo'],
            description=anime.get("sinopsis", "Sin sinopsis disponible."),
            color=0x9B59B6
        )
        embed.add_field(name="Episodios", value=str(anime.get("episodios", "N/A")), inline=True)
        embed.add_field(name="Genero", value=anime.get("genero", "N/A"), inline=True)
        if anime.get("dato_curioso"):
            embed.add_field(name="Dato curioso", value=anime["dato_curioso"], inline=False)
        embed.set_footer(text="Clasicos del anime 90s")
        await ctx.send(embed=embed)
    
    @commands.command(name="dime90")
    async def dime90(self, ctx):
        dato = self.elegir_aleatorio(self.datos.get("datos_curiosos", []))
        if not dato:
            await ctx.send("No hay datos curiosos en la base de datos.")
            return
        embed = discord.Embed(
            title="Sabias que...?",
            description=dato.get("texto", "No hay dato disponible."),
            color=0x9B59B6
        )
        if dato.get("categoria"):
            embed.add_field(name="Categoria", value=dato["categoria"], inline=True)
        embed.set_footer(text="CheloBot | Datos curiosos de los 90s/2000s")
        await ctx.send(embed=embed)
    
    @commands.command(name="lista90")
    async def lista90(self, ctx, tipo: str = None):
        if tipo is None:
            embed = discord.Embed(
                title="Listas disponibles",
                description="Usa `!lista90 [tipo]` para ver el contenido.",
                color=0x9B59B6
            )
            embed.add_field(
                name="Tipos disponibles",
                value=(
                    "`!lista90 peliculas` - Peliculas de los 90s\n"
                    "`!lista90 series` - Series de los 90s\n"
                    "`!lista90 juegos` - Juegos retro\n"
                    "`!lista90 musica` - Musica de los 90s\n"
                    "`!lista90 animes` - Animes clasico"
                ),
                inline=False
            )
            await ctx.send(embed=embed)
            return
        
        tipo = tipo.lower()
        mapeo = {
            "peliculas": "peliculas", "pelicula": "peliculas",
            "series": "series", "serie": "series",
            "juegos": "juegos", "juego": "juegos",
            "musica": "canciones", "canciones": "canciones",
            "animes": "animes", "anime": "animes",
        }
        clave = mapeo.get(tipo)
        if not clave or clave not in self.datos:
            await ctx.send("Tipo no valido. Usa: peliculas, series, juegos, musica, animes")
            return
        lista = self.datos[clave]
        if not lista:
            await ctx.send(f"No hay {tipo} en la base de datos.")
            return
        texto = f"**{tipo.upper()} DISPONIBLES:**\n\n"
        for i, item in enumerate(lista[:20], 1):
            titulo = item.get("titulo", "Sin titulo")
            anio = item.get("anio", "")
            texto += f"{i}. {titulo} ({anio})\n"
        if len(lista) > 20:
            texto += f"\n*... y {len(lista) - 20} mas*"
        embed = discord.Embed(title=f"{tipo.title()} de los 90s", description=texto, color=0x9B59B6)
        embed.set_footer(text=f"Total: {len(lista)} elementos")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Nostalgia(bot))
