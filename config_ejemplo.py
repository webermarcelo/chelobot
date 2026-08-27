import os

# Token del bot - se carga desde variable de entorno
TOKEN = os.getenv("CHELOBOT_TOKEN", "")

# Configuracion de canales (se configuran por nombre)
CANALES = {
    "bienvenida": "bienvenida",
    "anuncios": "anuncios",
    "reglas": "reglas",
    "charla": "charla-general",
    "logs": "logs",
    "roles": "roles-y-canales",
    "stream_anuncios": "anuncios-de-streams",
}

# Configuracion de roles
ROLES = {
    "miembro": "Miembro",
    "nuevo": "Nuevo Retro",
    "retro_gamer": "Retro Gamer",
    "cinefilo": "Cinefilo 90s",
    "musico": "Melomano Retro",
    "comic": "Fan del Comic",
    "tv": "Fan de la TV",
}

# Embed colors (hex)
COLORES = {
    "principal": 0x9B59B6,
    "exito": 0x2ECC71,
    "error": 0xE74C3C,
    "info": 0x3498DB,
    "advertencia": 0xF39C12,
}

# Configuracion de moderacion
MODERACION = {
    "max_mensajes_limpiar": 100,
    "duracion_silencio_default": 600,
}

# Configuracion de streams
STREAMS = {
    "duracion_sala_temporal": 3600,
    "max_salas_temporales": 5,
}
