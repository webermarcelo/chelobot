import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class Utilidad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="info")
    async def info_servidor(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=guild.name,
            description="Comunidad de nostalgia de los 90s y 2000s",
            color=0x9B59B6
        )
        embed.add_field(name="Miembros", value=str(guild.member_count), inline=True)
        embed.add_field(name="Canales de texto", value=str(len(guild.text_channels)), inline=True)
        embed.add_field(name="Canales de voz", value=str(len(guild.voice_channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Boosts", value=str(guild.premium_subscription_count), inline=True)
        embed.add_field(name="Creado el", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="CheloBot | Tu bot de nostalgia")
        await ctx.send(embed=embed)
    
    @commands.command(name="perfil")
    async def perfil(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"Perfil de {member.name}",
            color=member.color if member.color != discord.Color.default() else 0x9B59B6
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Miembro desde", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "N/A", inline=True)
        embed.add_field(name="Cuenta creada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        if roles:
            embed.add_field(name="Roles", value=", ".join(roles[:10]), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="encuesta")
    async def encuesta(self, ctx, *, args: str = None):
        if args is None:
            await ctx.send("Uso: `!encuesta Pregunta | Opcion1 | Opcion2 | ...`")
            return
        partes = [p.strip() for p in args.split("|")]
        if len(partes) < 3:
            await ctx.send("Necesitas al menos una pregunta y dos opciones.")
            return
        pregunta = partes[0]
        opciones = partes[1:]
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        embed = discord.Embed(title="Encuesta", description=f"**{pregunta}**", color=0x3498DB)
        texto_opciones = ""
        for i, opcion in enumerate(opciones):
            texto_opciones += f"{emojis[i]} {opcion}\n"
        embed.add_field(name="Opciones", value=texto_opciones, inline=False)
        embed.set_footer(text=f"Encuesta de {ctx.author.name}")
        mensaje_encuesta = await ctx.send(embed=embed)
        for i in range(len(opciones)):
            await mensaje_encuesta.add_reaction(emojis[i])
        await ctx.message.delete()
    
    @commands.command(name="recordatorio")
    async def recordatorio(self, ctx, tiempo: str = None, *, mensaje: str = None):
        if tiempo is None or mensaje is None:
            await ctx.send("Uso: `!recordatorio [tiempo] [mensaje]` (ej: `!recordatorio 1h Stream en 1 hora`)")
            return
        segundos = self.parsear_tiempo(tiempo)
        if segundos is None:
            await ctx.send("Formato de tiempo no valido. Usa: 30s, 5m, 1h, 1d")
            return
        if segundos > 86400:
            await ctx.send("El maximo de tiempo es 24 horas.")
            return
        fecha_objetivo = datetime.utcnow() + timedelta(seconds=segundos)
        embed = discord.Embed(
            title="Recordatorio programado",
            description=f"**Mensaje:** {mensaje}\n**Tiempo:** {tiempo}\n**Te recordare:** <t:{int(fecha_objetivo.timestamp())}:R>",
            color=0x2ECC71
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(segundos)
        embed_recordatorio = discord.Embed(title="RECORDATORIO!", description=f"{ctx.author.mention} - {mensaje}", color=0xF39C12)
        await ctx.send(embed=embed_recordatorio)
    
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
    
    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Avatar de {member.name}", color=member.color if member.color != discord.Color.default() else 0x9B59B6)
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilidad(bot))
