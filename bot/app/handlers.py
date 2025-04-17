from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import aiohttp
from app.config import Config
from loguru import logger

API_URL = f"http://localhost"

# Состояния диалога
SELECTING_CATEGORY, ENTERING_QUERY = range(2)

# Клавиатура для главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    [["Бренды", "Вкусы"]],
    resize_keyboard=True,
    one_time_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите категорию:",
        reply_markup=main_menu_keyboard
    )
    return SELECTING_CATEGORY


async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора категории"""
    user_choice = update.message.text.lower()
    context.user_data['category'] = user_choice

    await update.message.reply_text(
        f"Вы выбрали: {user_choice}. Теперь введите поисковый запрос:",
        reply_markup=ReplyKeyboardRemove()
    )
    return ENTERING_QUERY


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


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    logger.info(f"Запрос: {query}")

    user_choice = context.user_data['category'].lower()
    print(user_choice)
    print(query)
    try:
        async with aiohttp.ClientSession() as session:
            if user_choice == "бренды":
                async with session.get(f"{API_URL}/brands/{query}") as resp:
                    if resp.status == 200:
                        await send_table(update, await resp.json(), is_brands=True)
                    else:
                        await update.message.reply_text(
                            f"⚠️ API вернул ошибку: {resp.status}"
                        )
            elif user_choice == "вкусы":
                async with session.get(f"{API_URL}/flavors/{query}") as resp:
                    if resp.status == 200:
                        await send_table(update, await resp.json(), is_brands=False)
                    else:
                        await update.message.reply_text(
                            f"⚠️ API вернул ошибку: {resp.status}"
                        )
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Ошибка при запросе к API: {str(e)}"
        )

    # async with aiohttp.ClientSession(trust_env=True) as session:
    #     if user_choice == "бренды":
    #         # Здесь может быть API-запрос или выбор из базы данных
    #         await update.message.reply_text(
    #             "Запрос по брендам отправлен. Вот список...",
    #             reply_markup=ReplyKeyboardRemove()
    #         )
    #         # Дополнительная логика для брендов
    #         async with session.get(f"{API_URL}/flavors/{query}") as resp:
    #         # if resp.status == 200:
    #             await send_table(update, await resp.json(), is_brands=False)
    #             return
    #     elif user_choice == "вкусы":
    #         await update.message.reply_text(
    #             "Запрос по вкусам отправлен. Вот список...",
    #             reply_markup=ReplyKeyboardRemove()
    #         )
    #         async with session.get(f"{API_URL}/brands/{query}") as resp:
    #             # if resp.status == 200:
    #             await send_table(update, await resp.json(), is_brands=True)
    #             return
    #         # Дополнительная логика для вкусов
    #     else:
    #         await update.message.reply_text(
    #         "Пожалуйста, выберите вариант из меню.",
    #         reply_markup=main_menu_keyboard
    #         )
    return ConversationHandler.END

        # try:
        #     # Пробуем как вкус
        #     async with session.get(f"{API_URL}/brands/{query}") as resp:
        #         if resp.status == 200:
        #             await send_table(update, await resp.json(), is_brands=True)
        #             return
        #
        #     # Пробуем как бренд
        #     async with session.get(f"{API_URL}/flavors/{query}") as resp:
        #         if resp.status == 200:
        #             await send_table(update, await resp.json(), is_brands=False)
        #             return
        #
        #     await update.message.reply_text("🔍 Не найдено ни брендов, ни вкусов")
        # except Exception as e:
        #     logger.error(f"Ошибка: {e}")
        #     await update.message.reply_text("⚠️ Ошибка сервера")
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога"""
    await update.message.reply_text(
        "Поиск отменен. Нажмите /start для нового поиска.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def setup_handlers(app):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_category)
            ],
            ENTERING_QUERY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))