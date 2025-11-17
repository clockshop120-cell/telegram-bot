from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor

TOKEN = "8474841559:AAGGrioNVB-MisETulnxOFIOGfzB4ytdPcE"

REQUIRED_CHANNELS = [
    "@rps1weryy",
]

PRIVATE_LINK = "testprivate_link"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def check_subscriptions(user_id: int) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    text = "Чтобы получить доступ, подпишись на каналы:\n\n"

    for ch in REQUIRED_CHANNELS:
        text += f"{ch}\n"

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Я подписался", callback_data="check"))

    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "check")
async def check(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if await check_subscriptions(user_id):
        await callback.message.answer(f"Ты подписался! Вот ссылка:\n{PRIVATE_LINK}")
    else:
        await callback.answer("Ты не подписался на все каналы!", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
