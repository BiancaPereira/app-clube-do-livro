from telegram import Update
from telegram.ext import ContextTypes
from book_info import generate_affiliate_link, scrap_book_info
from ai import generate_ai_summary

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start para dar boas-vindas ao bot."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Boas vindas ao nosso bot!")

async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /promo para gerar link de afiliado de um livro em promoção."""
    if update.message and update.message.text:
        promo_link = update.message.text.replace('/promo ', '', 1)
        try:
            affiliate_link = generate_affiliate_link(promo_link)
            info = scrap_book_info(promo_link)
            summary = generate_ai_summary(info['title'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                parse_mode='Markdown',
                text=f"`#promo 🔻 | **{info['title']}**\n💵 R${info['price']}\n\n📖 {summary}\n\n👉 {affiliate_link}`"
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Erro ao processar o link: {e}"
            )

async def gratis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /gratis para divulgar um livro grátis."""
    if update.message and update.message.text:
        promo_link = update.message.text.replace('/gratis ', '', 1)
        try:
            affiliate_link = generate_affiliate_link(promo_link)
            info = scrap_book_info(promo_link)
            summary = generate_ai_summary(info['title'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                parse_mode='Markdown',
                text=f"`#gratis 🆓 | **{info['title']}**\n\n📖 {summary}\n\n👉 {affiliate_link}`"
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Erro ao processar o link: {e}"
            )
