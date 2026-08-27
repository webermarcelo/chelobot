import discord
from discord.ext import commands
from discord.utils import get
import json
import os

class Bienvenida(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archivo_config = "data/config_servidor.json"
        self.config = self.cargar_config()
    
    def cargar_config(self):
        """Cargar configuración del servidor"""
        if os.path.exists(self.archivo_config):
            with open(self.archivo_config, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def guardar_config(self):
        """Guardar configuración del servidor"""
        with open(self.archivo_config, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Evento cuando un miembro se une al servidor"""
        guild = member.guild
        
        # Buscar canal de bienvenida
        canal_bienvenida = None
        for channel in guild.text_channels:
            if "bienvenida" in channel.name.lower():
                canal_bienvenida = channel
                break
        
        if canal_bienvenida:
            # Crear embed de bienvenida
            embed = discord.Embed(
                title=f"¡Bienvenido/a {member.name}! 🎉",
                description=(
                    f"¡Hola {member.mention}! Bienvenido/a a **{guild.name}**.\n\n"
                    f"Somos una comunidad de nostalgia de los 90s y 2000s.\n"
                    f"📺 Películas, series, videojuegos, música y mucho más.\n\n"
                    f"Revisa los canales de información y usa `!ayuda` para ver los comandos disponibles."
                ),
                color=0x9B59B6
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Miembros totales: {guild.member_count}")
            
            await canal_bienvenida.send(embed=embed)
        
        # Asignar rol automático
        await self.asignar_rol_automatico(member)
    
    async def asignar_rol_automatico(self, member):
        """Asignar rol automático a nuevos miembros"""
        guild = member.guild
        
        # Buscar rol "Miembro" o "Nuevo Retro"
        rol_auto = None
        for role in guild.roles:
            if role.name.lower() in ["miembro", "nuevo retro"]:
                rol_auto = role
                break
        
        if rol_auto:
            try:
                await member.add_roles(rol_auto)
                print(f"  ✓ Rol '{rol_auto.name}' asignado a {member.name}")
            except Exception as e:
                print(f"  ✗ Error asignando rol: {e}")
    
    @commands.command(name="configurar_bienvenida")
    @commands.has_permissions(administrator=True)
    async def configurar_bienvenida(self, ctx, canal: discord.TextChannel):
        """Configurar canal de bienvenida"""
        if "bienvenida" in canal.name.lower():
            self.config[str(ctx.guild.id)] = {
                "canal_bienvenida": canal.id
            }
            self.guardar_config()
            await ctx.send(f"✅ Canal de bienvenida configurado en {canal.mention}")
        else:
            await ctx.send("❌ El canal debe llamarse 'bienvenida' o contener esa palabra.")
    
    @commands.command(name="preview_bienvenida")
    @commands.has_permissions(administrator=True)
    async def preview_bienvenida(self, ctx):
        """Vista previa del mensaje de bienvenida"""
        embed = discord.Embed(
            title=f"¡Bienvenido/a [Nombre]! 🎉",
            description=(
                f"¡Hola [Usuario]! Bienvenido/a a **{ctx.guild.name}**.\n\n"
                f"Somos una comunidad de nostalgia de los 90s y 2000s.\n"
                f"📺 Películas, series, videojuegos, música y mucho más.\n\n"
                f"Revisa los canales de información y usa `!ayuda` para ver los comandos disponibles."
            ),
            color=0x9B59B6
        )
        embed.set_footer(text="Miembros totales: X")
        
        await ctx.send(embed=embed)
        await ctx.send("^( Esta es la vista previa del mensaje de bienvenida )")

async def setup(bot):
    await bot.add_cog(Bienvenida(bot))
