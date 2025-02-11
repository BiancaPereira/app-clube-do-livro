import logging
import os

from telegram.ext import Application, CommandHandler

from dotenv import load_dotenv

from commands import start, promo, gratis

# Carrega variáveis de ambiente
load_dotenv()

logging.basicConfig(
    format='ℹ️ %(asctime)s - %(name)s - %(levelname)s - %(message)s\n',
    level=logging.INFO
)

def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()
    
    # Comando start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Comando promo
    promo_handler = CommandHandler('promo', promo)
    application.add_handler(promo_handler)

    # Comando gratis
    gratis_handler = CommandHandler('gratis', gratis)
    application.add_handler(gratis_handler)
    
    application.run_polling()

if __name__ == '__main__':
   main()
