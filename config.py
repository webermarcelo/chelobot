import os

# Token del bot - se carga desde variable de entorno
TOKEN = os.getenv("CHELOBOT_TOKEN", "")

# ID del servidor (se obtiene automáticamente, pero puedes configurarlo aquí)
GUILD_ID = None  # Si lo dejas en None, el bot funcionará en todos los servidores donde esté

# Configuración de canales (se configuran por nombre)
CANALES = {
    "bienvenida": "bienvenida",
    "anuncios": "anuncios",
    "reglas": "reglas",
    "charla": "charla-general",
    "logs": "logs",
    "roles": "roles-y-canales",
    "stream_anuncios": "anuncios-de-streams",
}

# Configuración de roles
ROLES = {
    "miembro": "Miembro",
    "nuevo": "Nuevo Retro",
    "retro_gamer": "Retro Gamer",
    "cinefilo": "Cinefilo 90s",
    "musico": "Melómano Retro",
    "comic": "Fan del Cómic",
    "tv": "Fan de la TV",
}

# Embed colors (hex)
COLORES = {
    "principal": 0x9B59B6,    # Morado retro
    "exito": 0x2ECC71,        # Verde
    "error": 0xE74C3C,        # Rojo
    "info": 0x3498DB,         # Azul
    "advertencia": 0xF39C12,  # Amarillo
}

# Configuración de moderacion
MODERACION = {
    "max_mensajes_limpiar": 100,
    "duracion_silencio_default": 600,  # 10 minutos en segundos
}

# Configuración de streams
STREAMS = {
    "duracion_sala_temporal": 3600,  # 1 hora en segundos
    "max_salas_temporales": 5,
}
