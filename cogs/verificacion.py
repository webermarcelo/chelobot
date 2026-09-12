import discord
from discord.ext import commands
import asyncio

class Verificacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.usuarios_verificados = set()
    
    @commands.command(name="verificar")
    async def verificar(self, ctx):
        """Verificarse para acceder al servidor"""
        # Verificar si ya está verificado
        if ctx.author.id in self.usuarios_verificados:
            await ctx.send("Ya estás verificado!")
            return
        
        # Verificar si tiene el rol de verificado
        rol_verificado = discord.utils.get(ctx.guild.roles, name="Verificado")
        if rol_verificado in ctx.author.roles:
            await ctx.send("Ya estás verificado!")
            return
        
        # Crear embed de verificación
        embed = discord.Embed(
            title="Verificación de cuenta",
            description=(
                "Para acceder a todos los canales, react con ✅ abajo.\n"
                "Esto confirma que no eres un bot."
            ),
            color=0x3498DB
        )
        embed.set_footer(text="Tienes 60 segundos para verificarte")
        
        mensaje = await ctx.send(embed=embed)
        await mensaje.add_reaction("✅")
        
        # Esperar reacción
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅"
        
        try:
            await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            
            # Asignar rol de verificado
            rol_verificado = discord.utils.get(ctx.guild.roles, name="Verificado")
            if rol_verificado:
                await ctx.author.add_roles(rol_verificado)
                self.usuarios_verificados.add(ctx.author.id)
                
                embed_exito = discord.Embed(
                    title="Verificación completada!",
                    description=f"Ahora tienes acceso a todos los canales, {ctx.author.mention}!",
                    color=0x2ECC71
                )
                await ctx.send(embed=embed_exito, delete_after=10)
                await ctx.message.delete()
            else:
                await ctx.send("Error: No se encontró el rol 'Verificado'. Crea el rol en la configuración del servidor.")
        
        except asyncio.TimeoutError:
            embed_timeout = discord.Embed(
                title="Verificación expirada",
                description="No te verificaste a tiempo. Usa `!verificar` de nuevo.",
                color=0xE74C3C
            )
            await ctx.send(embed=embed_timeout, delete_after=10)
            await ctx.message.delete()
    
    @commands.command(name="setup_verificacion")
    @commands.has_permissions(administrator=True)
    async def setup_verificacion(self, ctx):
        """Configurar sistema de verificación"""
        # Crear rol "Verificado"
        rol_verificado = discord.utils.get(ctx.guild.roles, name="Verificado")
        if not rol_verificado:
            rol_verificado = await ctx.guild.create_role(
                name="Verificado",
                color=0x2ECC71,
                reason="Rol de verificación para nuevos miembros"
            )
        
        # Configurar permisos del rol en todos los canales
        for channel in ctx.guild.text_channels:
            try:
                await channel.set_permissions(
                    rol_verificado,
                    read_messages=True,
                    send_messages=True
                )
            except:
                pass
        
        # Configurar permisos para @everyone (no ver canales sin verificar)
        everyone = ctx.guild.default_role
        for channel in ctx.guild.text_channels:
            if channel.name not in ["bienvenida", "verificacion"]:
                try:
                    await channel.set_permissions(
                        everyone,
                        read_messages=False
                    )
                except:
                    pass
        
        embed = discord.Embed(
            title="Sistema de verificación configurado",
            description=(
                "1. Se creó el rol **Verificado**\n"
                "2. Los canales están ocultos hasta que se verifiquen\n"
                "3. Usa `!verificar` en #bienvenida para probar"
            ),
            color=0x2ECC71
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Verificacion(bot))
