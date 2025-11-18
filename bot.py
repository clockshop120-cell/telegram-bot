import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8474841559:AAGGrioNVB-MisETulnxOFIOGfzB4ytdPcE")
dp = Dispatcher(bot)

# ======= СПИСОК КАНАЛОВ ДЛЯ ПРОВЕРКИ ==========
CHANNELS = [
    {"name": "Канал №1", "url": "https://t.me/yourchannel1"},
    {"name": "Канал №2", "url": "https://t.me/yourchannel2"},
    {"name": "Канал №3", "url": "https://t.me/yourchannel3"},
    {"name": "Канал №4", "url": "https://t.me/yourchannel4"},
    {"name": "Канал №5", "url": "https://t.me/yourchannel5"},
]


# ==========  КНОПКИ ДЛЯ ПРОВЕРКИ  ==========
def get_check_keyboard():
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Проверить подписку 🔄", callback_data="check")
    kb.add(btn)
    return kb


# ==========  КНОПКИ С КАНАЛАМИ  ==========
def get_channels_keyboard():
    kb = InlineKeyboardMarkup()
    for i, ch in enumerate(CHANNELS):
        kb.add(
            InlineKeyboardButton(
                f"{i+1}) {ch['name']}", url=ch["url"]
            )
        )
    kb.add(InlineKeyboardButton("Проверить подписку 🔄", callback_data="check"))
    return kb


# ==================================================
#          / start
# ==================================================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = (
        "Чтобы получить доступ в канал, тебе нужно подписаться на каналы ниже ✨📌\n\n"
        "Подайте заявки во все каналы снизу!\n\n"
    )

    for i, ch in enumerate(CHANNELS):
        text += f"№{i+1} 🔗 {ch['name']} ({ch['url']})\n"

    text += "\nПосле подписки на каждый канал бот примет вас автоматически 😊"

    await message.answer(text, reply_markup=get_channels_keyboard())


# ==================================================
#      Проверка подписки
# ==================================================
async def check_sub(user_id):
    results = []
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch["url"], user_id=user_id)
            results.append(member.status in ["member", "administrator", "creator"])
        except:
            results.append(False)
    return results


# ==================================================
#   Кнопка "Проверить подписку"
# ==================================================
@dp.callback_query_handler(lambda c: c.data == "check")
async def check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    statuses = await check_sub(user_id)

    if all(statuses):
        # === Все подписки выполнены ===
        msg = (
            "🎉 *ПОЗДРАВЛЯЮ!*\n"
            "Ты выполнил все условия и получаешь доступ! 🔥"
        )
        await callback.message.answer(msg, parse_mode="Markdown")
    else:
        # === НЕ ВСЕ КАНАЛЫ ПОДПИСАНЫ ===
        text = "❌ *ПОХОЖЕ ВЫ НЕ ВЫПОЛНИЛИ ВСЕ УСЛОВИЯ* ❌\n\n"
        text += "Подайте заявки во все каналы снизу!\n\n"

        for i, ch in enumerate(CHANNELS):
            text += f"№{i+1} 🔗 {ch['name']} ({ch['url']})\n"

        await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_channels_keyboard())

    await callback.answer()


# ==================================================
#   Запуск бота
# ==================================================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
