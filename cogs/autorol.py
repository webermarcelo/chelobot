import discord
from discord.ext import commands
from discord import app_commands
import json
import os

# Mapeo de emojis a roles
ROLES_CONFIG = {
    "\U0001f3ae": {"nombre": "Retro Gamer", "descripcion": "Amante de los videojuegos retro"},
    "\U0001f3ac": {"nombre": "Cinefilo 90s", "descripcion": "Fan del cine de los 90s"},
    "\U0001f3b5": {"nombre": "Melomano Retro", "descripcion": "Amante de la musica retro"},
    "\U0001f4da": {"nombre": "Fan del Comic", "descripcion": "Coleccionista de comics y manga"},
    "\U0001f4fa": {"nombre": "Fan de la TV", "descripcion": "Fan de las series de television"},
    "\U0001f916": {"nombre": "Retro Gamer Avanzado", "descripcion": "Gamer experto en retrogaming"},
    "\u2764\ufe0f": {"nombre": "Miembro", "descripcion": "Miembro de la comunidad"},
}

class Autorol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.archivo_config = "autorol_config.json"
        self.config = self.cargar_config()
    
    def cargar_config(self):
        if os.path.exists(self.archivo_config):
            with open(self.archivo_config, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def guardar_config(self):
        with open(self.archivo_config, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    @commands.command(name="setup_autorol")
    @commands.has_permissions(administrator=True)
    async def setup_autorol(self, ctx):
        """Envia el mensaje de autorol al canal actual"""
        embed = discord.Embed(
            title="ELIGE TUS ROLES",
            description=(
                "Reacciona con los emojis para obtener el rol que mas te guste.\n"
                "Puedes elegir varios roles.\n\n"
                "Si quieres quitar un rol, simplemente quita tu reaccion.\n\n"
                "**Roles disponibles:**"
            ),
            color=0x9B59B6
        )
        
        texto_roles = ""
        for emoji, info in ROLES_CONFIG.items():
            texto_roles += f"{emoji} **{info['nombre']}** - {info['descripcion']}\n"
        
        embed.add_field(name="Elige tus roles:", value=texto_roles, inline=False)
        embed.set_footer(text="Reacciona para obtener/quitar roles | Tu servidor Millennials")
        
        mensaje = await ctx.send(embed=embed)
        
        for emoji in ROLES_CONFIG.keys():
            await mensaje.add_reaction(emoji)
        
        self.config[str(ctx.guild.id)] = {
            "canal_id": ctx.channel.id,
            "mensaje_id": mensaje.id
        }
        self.guardar_config()
        
        await ctx.send("Mensaje de autorol configurado.", delete_after=5)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Manejar reacciones para asignar roles"""
        if payload.user_id == self.bot.user.id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        config_guild = self.config.get(str(payload.guild_id))
        if not config_guild:
            return
        
        if payload.message_id != config_guild.get("mensaje_id"):
            return
        
        emoji_str = str(payload.emoji)
        
        if emoji_str in ROLES_CONFIG:
            rol_nombre = ROLES_CONFIG[emoji_str]["nombre"]
            rol = discord.utils.get(guild.roles, name=rol_nombre)
            
            if rol:
                member = guild.get_member(payload.user_id)
                if member:
                    try:
                        await member.add_roles(rol)
                        print(f"  [AUTOROL] Rol '{rol_nombre}' asignado a {member.name}")
                    except Exception as e:
                        print(f"  [ERROR] Error asignando rol: {e}")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Manejar reacciones para quitar roles"""
        if payload.user_id == self.bot.user.id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        config_guild = self.config.get(str(payload.guild_id))
        if not config_guild:
            return
        
        if payload.message_id != config_guild.get("mensaje_id"):
            return
        
        emoji_str = str(payload.emoji)
        
        if emoji_str in ROLES_CONFIG:
            rol_nombre = ROLES_CONFIG[emoji_str]["nombre"]
            rol = discord.utils.get(guild.roles, name=rol_nombre)
            
            if rol:
                member = guild.get_member(payload.user_id)
                if member:
                    try:
                        await member.remove_roles(rol)
                        print(f"  [AUTOROL] Rol '{rol_nombre}' removido de {member.name}")
                    except Exception as e:
                        print(f"  [ERROR] Error removiendo rol: {e}")
    
    @app_commands.command(name="roles", description="Ver y gestionar tus roles disponibles")
    async def roles_slash(self, interaction: discord.Interaction):
        """Comando slash para ver roles"""
        embed = discord.Embed(
            title="TUS ROLES ACTUALES",
            description="Estos son los roles que tienes actualmente:",
            color=0x9B59B6
        )
        
        roles_usuario = [role.name for role in interaction.user.roles if role.name != "@everyone"]
        if roles_usuario:
            embed.add_field(name="Roles actuales:", value=", ".join(roles_usuario), inline=False)
        else:
            embed.add_field(name="Roles actuales:", value="No tienes roles especiales", inline=False)
        
        embed.add_field(
            name="Como obtener mas roles:",
            value="Ve al canal <#autorol-miembro> y reacciona con los emojis para elegir tus roles.",
            inline=False
        )
        
        embed.set_footer(text="Millennials Server | Tu bot de nostalgia")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @roles_slash.error
    async def roles_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(
            "Ocurrio un error al ejecutar el comando.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Autorol(bot))
