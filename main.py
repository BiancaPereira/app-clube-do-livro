import logging
import os
from urllib.parse import urlparse

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

# Carrega variáveis de ambiente
load_dotenv()

logging.basicConfig(
    format='ℹ️ %(asctime)s - %(name)s - %(levelname)s - %(message)s\n',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Boas vindas ao nosso bot!")

def scrap_info(url: str) -> dict:
    info = get_book_metadata(url)
    clean_url = f"https://www.amazon.com.br/dp/{info['asin']}?tag=biancaperei0d-20"
    return {'clean_url': clean_url, 'title': info['title'], 'price': info['price']}

async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        promo_link = update.message.text.replace('/promo ', '', 1)
        info = scrap_info(promo_link)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode='Markdown',
            text=f"`#promo 🔻 | **{info['title']}**\n💵 R${info['price']}\n\n👉 {info['clean_url']}`")
        
async def gratis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        promo_link = update.message.text.replace('/gratis ', '', 1)
        info = scrap_info(promo_link)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode='Markdown',
            text=f"`#gratis 😍 | **{info['title']}** \n\n👉 {info['clean_url']}`")

def get_book_metadata(url: str) -> dict:
    driver = webdriver.Chrome()  # or use the appropriate WebDriver for your browser

    driver.get(url)

    title_element = driver.find_element(By.ID, 'productTitle')
    title = title_element.text if title_element else 'Erro título'

    price_whole_element = driver.find_element(By.CLASS_NAME, 'a-price-whole')
    price_fraction_element = driver.find_element(By.CLASS_NAME, 'a-price-fraction')
    price_whole = price_whole_element.text if price_whole_element else 'Erro preço'
    price_fraction = price_fraction_element.text if price_fraction_element else '00'
    price = f"{price_whole},{price_fraction}"

    try:
        asin_element = driver.find_element(By.XPATH, "//span[@class='a-list-item' and contains (.,'ASIN')]//span[2]")
        asin = asin_element.text if asin_element else ''
    except:
        asin = ''

    if not asin:
        try:
            isbn_element = driver.find_element(By.XPATH, "//span[@class='a-list-item' and contains (.,'ISBN-10')]//span[2]")
            asin = isbn_element.text if isbn_element else 'Erro ASIN/ISBN-10'
        except:
            asin = 'Erro ASIN/ISBN-10'

    driver.quit()

    return {'asin': asin, 'title': title, 'price': price}

def main() -> None:
    token = os.getenv('TOKEN')
    application = ApplicationBuilder().token(token).build()
    
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
