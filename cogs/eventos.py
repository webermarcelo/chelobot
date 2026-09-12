import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archivo_eventos = "data/eventos.json"
        self.eventos = self.cargar_eventos()
    
    def cargar_eventos(self):
        if os.path.exists(self.archivo_eventos):
            with open(self.archivo_eventos, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"proximos": [], "historial": []}
    
    def guardar_eventos(self):
        with open(self.archivo_eventos, "w", encoding="utf-8") as f:
            json.dump(self.eventos, f, indent=2, ensure_ascii=False)
    
    @commands.command(name="crear_evento")
    @commands.has_permissions(manage_events=True)
    async def crear_evento(self, ctx, fecha: str = None, *, descripcion: str = None):
        """Crear un evento. Formato: !crear_evento 25/12 21:00 Nombre del evento"""
        if fecha is None or descripcion is None:
            await ctx.send(
                "Uso: `!crear_evento [dia/mes] [hora] [descripcion]`\n"
                "Ejemplo: `!crear_evento 25/12 21:00 Watch Party Titanic`"
            )
            return
        
        try:
            partes = descripcion.split(" ", 1)
            hora = partes[0]
            nombre = partes[1] if len(partes) > 1 else "Evento especial"
            
            dia, mes = fecha.split("/")
            anio = datetime.now().year
            
            fecha_evento = datetime(anio, int(mes), int(dia), 
                                   int(hora.split(":")[0]), 
                                   int(hora.split(":")[1]))
            
            evento = {
                "fecha": fecha_evento.strftime("%Y-%m-%d %H:%M"),
                "nombre": nombre,
                "creador": ctx.author.name,
                "canal": ctx.channel.name
            }
            
            self.eventos["proximos"].append(evento)
            self.guardar_eventos()
            
            embed = discord.Embed(
                title="Evento creado!",
                description=f"**{nombre}**\nFecha: {fecha_evento.strftime('%d/%m/%Y %H:%M')}",
                color=0x2ECC71
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error al crear evento: {str(e)}")
    
    @commands.command(name="eventos")
    async def ver_eventos(self, ctx):
        """Ver proximos eventos"""
        if not self.eventos["proximos"]:
            await ctx.send("No hay eventos programados.")
            return
        
        embed = discord.Embed(
            title="Proximos eventos",
            description="Eventos programados del servidor:",
            color=0x9B59B6
        )
        
        for evento in self.eventos["proximos"][:5]:
            fecha = datetime.strptime(evento["fecha"], "%Y-%m-%d %H:%M")
            embed.add_field(
                name=evento["nombre"],
                value=f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}\nCreador: {evento['creador']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="recordar_evento")
    @commands.has_permissions(manage_events=True)
    async def recordar_evento(self, ctx, indice: int = None):
        """Enviar recordatorio de un evento"""
        if indice is None:
            await ctx.send("Uso: `!recordar_evento [numero]`")
            return
        
        if indice < 1 or indice > len(self.eventos["proximos"]):
            await ctx.send("Numero de evento no valido.")
            return
        
        evento = self.eventos["proximos"][indice - 1]
        
        embed = discord.Embed(
            title="Recordatorio de evento!",
            description=(
                f"**{evento['nombre']}**\n"
                f"Fecha: {evento['fecha']}\n"
                f"Creador: {evento['creador']}"
            ),
            color=0xF39C12
        )
        
        canal = ctx.guild.get_channel(ctx.channel.id)
        await canal.send("@everyone", embed=embed)

async def setup(bot):
    await bot.add_cog(Eventos(bot))
