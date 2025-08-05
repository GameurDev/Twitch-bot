import twitchio
from twitchio.ext import commands
from config import Config
from commandes.bingo import BingoCommands
from commandes.info import InfoCommands
from commandes.utils import UtilsCommands
import asyncio
import threading
import sys
import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Configuration du système de logging
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        filename='logs/neyticom_bot.log',
        when='midnight',
        backupCount=7
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    twitchio_logger = logging.getLogger('twitchio')
    twitchio_logger.setLevel(logging.WARNING)

    return logger

logger = setup_logging()

class NeyticomBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=Config.BOT_TOKEN,
            prefix=Config.BOT_PREFIX,
            initial_channels=[Config.CHANNEL_NAME]
        )
        self.load_commands()
        logger.info("Initialisation du bot Neyticom")

    def load_commands(self):
        try:
            self.add_cog(BingoCommands(self))
            self.add_cog(InfoCommands(self))
            self.add_cog(UtilsCommands(self))
            logger.info("Commandes chargées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des commandes: {str(e)}")
            raise

    async def event_ready(self):
        logger.info(f"Connecté en tant que {self.nick}")
        logger.info(f"Rejoint le canal: {Config.CHANNEL_NAME}")
        
        try:
            channel = self.get_channel(Config.CHANNEL_NAME)
            if channel:
                await channel.send(Config.STATUS + Config.HELP)
                logger.info("Message de bienvenue envoyé")
        except Exception as e:
            logger.error(f"Erreur initialisation: {str(e)}")

    def is_moderator(self, ctx):
        try:
            return ctx.author.is_mod or ctx.author.name.lower() == Config.CHANNEL_NAME.lower()
        except Exception as e:
            logger.error(f"Erreur is_moderator: {str(e)}")
            return False

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f"Erreur commande {ctx.command.name}: {str(error)}")
        await ctx.send(f"❌ Une erreur est survenue avec la commande {ctx.command.name}")

def get_system_status():
    """Récupère les informations système en utilisant psutil avec gestion des erreurs"""
    try:
        import psutil
        
        status = {}
        
        # CPU - peut échouer sur Termux
        try:
            status['cpu'] = {
                'percent': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count()
            }
        except Exception as e:
            logger.warning(f"Impossible de récupérer les infos CPU: {str(e)}")
            status['cpu'] = {'error': 'Données non disponibles'}
        
        # Mémoire - peut échouer sur Termux
        try:
            mem = psutil.virtual_memory()
            status['memory'] = {
                'total': round(mem.total / (1024**3), 2),
                'used': round(mem.used / (1024**3), 2),
                'percent': mem.percent
            }
        except Exception as e:
            logger.warning(f"Impossible de récupérer les infos mémoire: {str(e)}")
            status['memory'] = {'error': 'Données non disponibles'}
        
        # Processus - devrait fonctionner
        try:
            process = psutil.Process(os.getpid())
            status['process'] = {
                'memory': round(process.memory_info().rss / (1024**2), 2),
                'cpu': process.cpu_percent(interval=0.1)
            }
        except Exception as e:
            logger.warning(f"Impossible de récupérer les infos processus: {str(e)}")
            status['process'] = {'error': 'Données non disponibles'}
        
        # Temps de fonctionnement
        try:
            status['uptime'] = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
        except:
            status['uptime'] = 'Inconnu'
        
        return status
        
    except ImportError:
        logger.warning("psutil non disponible - fonctionnalité limitée")
        return {'error': 'psutil non disponible'}
    except Exception as e:
        logger.error(f"Erreur inattendue dans get_system_status: {str(e)}")
        return {'error': 'Erreur inconnue'}

def run_bot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot = NeyticomBot()
        logger.info("Démarrage du bot...")
        loop.run_until_complete(bot.start())
    except Exception as e:
        logger.critical(f"Erreur critique dans run_bot: {str(e)}")
        os._exit(1)

def start_bot():
    try:
        bot_thread = threading.Thread(target=run_bot, name="BotThread")
        bot_thread.daemon = True
        bot_thread.start()
        logger.info("Thread du bot démarré")
        return bot_thread
    except Exception as e:
        logger.critical(f"Erreur lors du démarrage du thread: {str(e)}")
        raise

def console_listener():
    logger.info("Console listener prêt. Commandes: 'restart', 'exit', 'status'")
    while True:
        try:
            command = input().strip().lower()
            if command == 'restart':
                logger.info("Commande de redémarrage reçue")
                print("🔄 Redémarrage du bot en cours...")
                python = sys.executable
                os.execl(python, python, *sys.argv)
            elif command == 'exit':
                logger.info("Commande d'arrêt reçue")
                print("🛑 Arrêt du bot...")
                os._exit(0)
            elif command == 'status':
                logger.info("Statut du bot demandé")
                status = get_system_status()
                
                print("\n=== STATUT DU BOT ===")
                
                # Afficher les informations disponibles
                if 'error' in status:
                    print("❌ Impossible de récupérer les informations système")
                else:
                    # CPU
                    if 'error' in status['cpu']:
                        print("🖥️ CPU: Données non disponibles")
                    else:
                        print(f"🖥️ CPU: {status['cpu']['percent']}% (Cores: {status['cpu']['cores']})")
                    
                    # Mémoire
                    if 'error' in status['memory']:
                        print("💾 Mémoire: Données non disponibles")
                    else:
                        print(f"💾 Mémoire: {status['memory']['used']}GB / {status['memory']['total']}GB ({status['memory']['percent']}%)")
                    
                    # Processus
                    if 'error' in status['process']:
                        print("🤖 Processus: Données non disponibles")
                    else:
                        print(f"🤖 Processus: CPU={status['process']['cpu']}% MEM={status['process']['memory']}MB")
                
                # Uptime (toujours disponible)
                print(f"⏱️ Uptime: {status.get('uptime', 'Inconnu')}\n")
                
            else:
                logger.warning(f"Commande inconnue reçue: {command}")
                print("Commande inconnue. Options: restart, exit, status")
        except Exception as e:
            logger.error(f"Erreur dans console_listener: {str(e)}")

if __name__ == "__main__":
    try:
        print("🔄 Démarrage du bot Neyticom...")
        print("Commandes console: 'restart', 'exit', 'status'")
        
        bot_thread = start_bot()
        
        console_thread = threading.Thread(target=console_listener, name="ConsoleThread")
        console_thread.daemon = True
        console_thread.start()
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Arrêt du bot via Ctrl+C")
        print("\n🛑 Arrêt du bot...")
        os._exit(0)
    except Exception as e:
        logger.critical(f"Erreur critique dans main: {str(e)}")
        print(f"❌ Erreur critique: {str(e)}")
        os._exit(1)