import discord
from discord.ext import commands
import json
import os
import random

class Niveles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archivo_niveles = "data/niveles.json"
        self.niveles = self.cargar_niveles()
    
    def cargar_niveles(self):
        if os.path.exists(self.archivo_niveles):
            with open(self.archivo_niveles, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def guardar_niveles(self):
        with open(self.archivo_niveles, "w", encoding="utf-8") as f:
            json.dump(self.niveles, f, indent=2, ensure_ascii=False)
    
    @commands.command(name="nivel")
    async def ver_nivel(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        user_id = str(member.id)
        if user_id in self.niveles:
            data = self.niveles[user_id]
            nivel = data.get("nivel", 0)
            xp = data.get("xp", 0)
            mensajes = data.get("mensajes", 0)
            xp_siguiente = ((nivel + 1) ** 2) * 100
            
            embed = discord.Embed(
                title=f"Nivel de {member.name}",
                color=0x9B59B6
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="Nivel", value=str(nivel), inline=True)
            embed.add_field(name="XP", value=f"{xp}/{xp_siguiente}", inline=True)
            embed.add_field(name="Mensajes", value=str(mensajes), inline=True)
            
            porcentaje = (xp / xp_siguiente) * 100 if xp_siguiente > 0 else 0
            barra = "█" * int(porcentaje / 10) + "░" * (10 - int(porcentaje / 10))
            embed.add_field(name="Progreso", value=f"`{barra}` {porcentaje:.1f}%", inline=False)
            
            # Roles de nivel
            if nivel >= 10:
                embed.add_field(name="Rango", value="Leyenda Retro", inline=False)
            elif nivel >= 5:
                embed.add_field(name="Rango", value="Veterano 90s", inline=False)
            elif nivel >= 1:
                embed.add_field(name="Rango", value="Miembro Activo", inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aun no tienes datos. Escribe mensajes para ganar XP!")
    
    @commands.command(name="top")
    async def top_niveles(self, ctx):
        if not self.niveles:
            await ctx.send("No hay datos de niveles aun.")
            return
        
        # Ordenar por XP
        top = sorted(self.niveles.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
        
        embed = discord.Embed(
            title="Top 10 Miembros",
            description="Los miembros con mas experiencia:",
            color=0x9B59B6
        )
        
        texto = ""
        for i, (user_id, data) in enumerate(top, 1):
            member = ctx.guild.get_member(int(user_id))
            if member:
                nivel = data.get("nivel", 0)
                xp = data.get("xp", 0)
                texto += f"{i}. **{member.name}** - Nivel {nivel} ({xp} XP)\n"
        
        embed.add_field(name="Ranking", value=texto or "Sin datos", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Niveles(bot))
