import discord
from discord.ext import commands
import asyncio

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="limpiar")
    @commands.has_permissions(manage_messages=True)
    async def limpiar(self, ctx, cantidad: int = 10):
        if cantidad < 1 or cantidad > 100:
            await ctx.send("Cantidad no valida. Usa un numero entre 1 y 100.")
            return
        deleted = await ctx.channel.purge(limit=cantidad + 1)
        msg = await ctx.send(f"Se eliminaron {len(deleted) - 1} mensajes.")
        await asyncio.sleep(3)
        await msg.delete()
    
    @commands.command(name="silenciar")
    @commands.has_permissions(moderate_members=True)
    async def silenciar(self, ctx, member: discord.Member = None, tiempo: str = "10m"):
        if member is None:
            await ctx.send("Uso: `!silenciar @usuario [tiempo]`")
            return
        if member == ctx.author:
            await ctx.send("No puedes silenciarte a ti mismo.")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("No puedes silenciar a alguien con igual o mayor rol.")
            return
        segundos = self.parsear_tiempo(tiempo)
        if segundos is None:
            segundos = 600
        if segundos > 2419200:
            await ctx.send("El maximo de tiempo es 28 dias.")
            return
        try:
            await member.timeout(discord.utils.utcnow() + asyncio.timedelta(seconds=segundos))
            embed = discord.Embed(
                title="Miembro silenciado",
                description=f"**Miembro:** {member.mention}\n**Tiempo:** {self.formatear_tiempo(segundos)}\n**Moderador:** {ctx.author.mention}",
                color=0xF39C12
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error al silenciar: {str(e)}")
    
    @commands.command(name="desilenciar")
    @commands.has_permissions(moderate_members=True)
    async def desilenciar(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Uso: `!desilenciar @usuario`")
            return
        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="Silencio quitado",
                description=f"**Miembro:** {member.mention}\n**Moderador:** {ctx.author.mention}",
                color=0x2ECC71
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
    
    @commands.command(name="expulsar")
    @commands.has_permissions(kick_members=True)
    async def expulsar(self, ctx, member: discord.Member = None, *, razon: str = "No especificada"):
        if member is None:
            await ctx.send("Uso: `!expulsar @usuario [razon]`")
            return
        if member == ctx.author:
            await ctx.send("No puedes expulsarte a ti mismo.")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("No puedes expulsar a alguien con igual o mayor rol.")
            return
        try:
            embed_dm = discord.Embed(
                title="Has sido expulsado",
                description=f"**Servidor:** {ctx.guild.name}\n**Razon:** {razon}\n**Moderador:** {ctx.author.name}",
                color=0xE74C3C
            )
            try:
                await member.send(embed=embed_dm)
            except:
                pass
            await member.kick(reason=razon)
            embed = discord.Embed(
                title="Miembro expulsado",
                description=f"**Miembro:** {member.name}\n**Razon:** {razon}\n**Moderador:** {ctx.author.mention}",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error al expulsar: {str(e)}")
    
    @commands.command(name="info_usuario")
    @commands.has_permissions(view_channel=True)
    async def info_usuario(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Info de {member.name}", color=member.color if member.color != discord.Color.default() else 0x9B59B6)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Cuenta creada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Se unio", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "N/A", inline=True)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        if roles:
            embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles[:10]), inline=False)
        await ctx.send(embed=embed)
    
    def parsear_tiempo(self, tiempo: str) -> int:
        segundos = 0
        unidades = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        actual = ""
        for char in tiempo.lower():
            if char.isdigit():
                actual += char
            elif char in unidades:
                if actual:
                    segundos += int(actual) * unidades[char]
                    actual = ""
        return segundos if segundos > 0 else None
    
    def formatear_tiempo(self, segundos: int) -> str:
        if segundos < 60:
            return f"{segundos} segundos"
        elif segundos < 3600:
            return f"{segundos // 60} minutos"
        elif segundos < 86400:
            return f"{segundos // 3600}h {(segundos % 3600) // 60}m"
        else:
            return f"{segundos // 86400}d {(segundos % 86400) // 3600}h"

async def setup(bot):
    await bot.add_cog(Moderacion(bot))
