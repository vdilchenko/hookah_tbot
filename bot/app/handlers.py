from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters
import aiohttp
from app.config import Config
from loguru import logger

API_URL = f"http://localhost"


async def send_table(update: Update, data: list, is_brands: bool):
    """Отправка данных в виде таблицы."""
    if not data:
        await update.message.reply_text("❌ Ничего не найдено")
        return

    header = "🏆 ТОП БРЕНДОВ 🏆" if is_brands else "🍏 ТОП ВКУСОВ 🍏"
    rows = []
    for i, item in enumerate(data, 1):
        if is_brands:
            row = f"{i}. *{item['Бренд']}* \n Название вкуса: `{item['Название_вкуса']}` \n  Рейтинг: `{item['Рейтинг']}`"
        else:
            row = f"{i}. *{item['Вкус']}* \n   Бренд: `{item['Бренд']}` \n Название вкуса: `{item['Название_вкуса']}` \n  Рейтинг: `{item['Рейтинг']}`"
        rows.append(row)
    
    await update.message.reply_text(
        f"{header}\n" + "\n".join(rows),
        parse_mode="Markdown"
    )


async def handle_query(update: Update, _):
    query = update.message.text.strip()
    logger.info(f"Запрос: {query}")
    
    async with aiohttp.ClientSession(trust_env=True) as session:
        try:
            # Пробуем как вкус
            async with session.get(f"{API_URL}/brands/{query}", ssl=False) as resp:
                if resp.status == 200:
                    await send_table(update, await resp.json(), is_brands=True)
                    return
            
            # Пробуем как бренд
            async with session.get(f"{API_URL}/flavors/{query}") as resp:
                if resp.status == 200:
                    await send_table(update, await resp.json(), is_brands=False)
                    return
            
            await update.message.reply_text("🔍 Не найдено ни брендов, ни вкусов")
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await update.message.reply_text("⚠️ Ошибка сервера")


def setup_handlers(app):
    app.add_handler(CommandHandler("start", lambda u, _: u.message.reply_text("Введите бренд или вкус")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))