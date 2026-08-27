import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class Streams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.salas_temporales = {}
    
    @commands.command(name="crear_stream")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def crear_stream(self, ctx, *, nombre: str = None):
        if nombre is None:
            await ctx.send("Uso: `!crear_stream [nombre del stream]`")
            return
        if ctx.author.voice is None:
            await ctx.send("Debes estar en un canal de voz para crear una sala de stream.")
            return
        guild_id = str(ctx.guild.id)
        user_id = ctx.author.id
        if guild_id in self.salas_temporales and user_id in self.salas_temporales[guild_id]:
            await ctx.send("Ya tienes una sala de stream activa. Usa `!cerrar_stream` para cerrarla.")
            return
        if guild_id not in self.salas_temporales:
            self.salas_temporales[guild_id] = {}
        if len(self.salas_temporales[guild_id]) >= 5:
            await ctx.send("Se alcanzo el limite de 5 salas de stream temporales.")
            return
        categoria = None
        for cat in ctx.guild.categories:
            if "stream" in cat.name.lower():
                categoria = cat
                break
        if not categoria:
            categoria = await ctx.guild.create_category("STREAMS")
        canal = await ctx.guild.create_voice_channel(
            name=nombre,
            category=categoria,
            overwrites={
                ctx.guild.default_role: discord.PermissionOverwrite(connect=True),
                ctx.author: discord.PermissionOverwrite(manage_channels=True, move_members=True)
            }
        )
        await ctx.author.move_to(canal)
        self.salas_temporales[guild_id][user_id] = {
            "canal": canal,
            "nombre": nombre,
            "fecha_creacion": datetime.utcnow()
        }
        embed = discord.Embed(
            title="Sala de stream creada",
            description=f"**Nombre:** {nombre}\n**Canal:** {canal.mention}\n**Creador:** {ctx.author.mention}\n\nLa sala se cerrara automaticamente en 1 hora o cuando uses `!cerrar_stream`.",
            color=0xE74C3C
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(3600)
        if guild_id in self.salas_temporales and user_id in self.salas_temporales[guild_id]:
            await self.cerrar_stream_logic(ctx, user_id)
    
    @commands.command(name="cerrar_stream")
    async def cerrar_stream(self, ctx):
        await self.cerrar_stream_logic(ctx, ctx.author.id)
    
    async def cerrar_stream_logic(self, ctx, user_id):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.salas_temporales or user_id not in self.salas_temporales[guild_id]:
            await ctx.send("No tienes una sala de stream activa.")
            return
        canal_info = self.salas_temporales[guild_id][user_id]
        canal = canal_info["canal"]
        nombre = canal_info["nombre"]
        for member in canal.members:
            general = next((ch for ch in ctx.guild.voice_channels if "general" in ch.name.lower()), None)
            if general:
                await member.move_to(general)
            else:
                await member.disconnect()
        await canal.delete()
        del self.salas_temporales[guild_id][user_id]
        embed = discord.Embed(
            title="Sala de stream cerrada",
            description=f"**Sala:** {nombre}\n**Creador:** {ctx.author.mention}",
            color=0x2ECC71
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="stream_info")
    async def stream_info(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.salas_temporales or not self.salas_temporales[guild_id]:
            await ctx.send("No hay salas de stream activas en este momento.")
            return
        embed = discord.Embed(title="Salas de stream activas", color=0xE74C3C)
        for user_id, info in self.salas_temporales[guild_id].items():
            member = ctx.guild.get_member(user_id)
            if member:
                embed.add_field(
                    name=info['nombre'],
                    value=f"**Creador:** {member.mention}\n**Canal:** {info['canal'].mention}\n**Usuarios:** {len(info['canal'].members)}",
                    inline=False
                )
        embed.set_footer(text=f"Total: {len(self.salas_temporales[guild_id])} salas activas")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Streams(bot))
