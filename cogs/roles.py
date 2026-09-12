import discord
from discord.ext import commands

ROLES_INTERES = {
    "🎮": "Retro Gamer",
    "🎬": "Cinefilo 90s",
    "📺": "Fan de la TV",
    "🎵": "Melomano Retro",
    "📚": "Fan del Comic",
    "🗾": "Otaku 90s",
}

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="roles")
    async def ver_roles(self, ctx):
        embed = discord.Embed(
            title="Roles disponibles",
            description="Reacciona con el emoji para obtener el rol:",
            color=0x9B59B6
        )
        
        texto = ""
        for emoji, rol in ROLES_INTERES.items():
            texto += f"{emoji} - {rol}\n"
        
        embed.add_field(name="Elige tu rol", value=texto, inline=False)
        embed.set_footer(text="Tambien puedes usar !rol [emoji] para obtener un rol")
        
        mensaje = await ctx.send(embed=embed)
        
        for emoji in ROLES_INTERES.keys():
            await mensaje.add_reaction(emoji)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        
        canal = self.bot.get_channel(payload.channel_id)
        mensaje = await canal.fetch_message(payload.message_id)
        
        if mensaje.author != self.bot.user:
            return
        
        emoji = str(payload.emoji)
        if emoji in ROLES_INTERES:
            rol_nombre = ROLES_INTERES[emoji]
            rol = discord.utils.get(payload.member.guild.roles, name=rol_nombre)
            
            if rol:
                await payload.member.add_roles(rol)
                embed = discord.Embed(
                    title="Rol asignado!",
                    description=f"Ahora tienes el rol **{rol_nombre}**",
                    color=0x2ECC71
                )
                embed.set_footer(text="Quita la reaccion para eliminar el rol")
                await canal.send(embed=embed, delete_after=5)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        canal = self.bot.get_channel(payload.channel_id)
        mensaje = await canal.fetch_message(payload.message_id)
        
        if mensaje.author != self.bot.user:
            return
        
        emoji = str(payload.emoji)
        if emoji in ROLES_INTERES:
            rol_nombre = ROLES_INTERES[emoji]
            rol = discord.utils.get(payload.member.guild.roles, name=rol_nombre)
            
            if rol:
                await payload.member.remove_roles(rol)

async def setup(bot):
    await bot.add_cog(Roles(bot))
