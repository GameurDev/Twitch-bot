class Config:
    # Identifiants Twitch
    BOT_TOKEN = "oauth:Ton_token" # obtenable via twitchtokebgenerator.com
    BOT_PREFIX = "!"
    CHANNEL_NAME = "neyticom"

    # Paramètres Bingo
    BINGO_MIN = 1
    BINGO_MAX = 200

    # Liens externes
    DISCORD_URL = "https://discord.gg/R9WbRP6yFk"
    ALTASIS_DISCORD = "https://discord.gg/5GpBezbBnT"
    MINECRAFT_IP = "play.altasis.fr"
    WEBSITE_URL = "https://altasis.fr"

    # Configuration PC
    PC_CONFIG = ("💻 Configuration Ultra Gaming :\n"
                "• CPU: i9-14900K | GPU: RTX4090 ROG STRIX\n"
                "• RAM: 96GB DDR5 TridentZ5 RGB\n"
                "• MB: ROG Z790-E | Cooling: Ryujin III 360mm\n"
                "• SSD: 4TB 990 Pro | Boitier: NZXT H9 Elite")

    HELP = (" LISTE DES COMMANDES : !bingo (mods) - !stopbingo (mods) - "
           "!discord - !altasis - !ip - !site - !config")

    STATUS = ("Le bot est en ligne ") # message d'envoie au demarrage'
    # Cooldowns (en secondes)
    COOLDOWN_REGULAR = 30
    COOLDOWN_LONG = 60