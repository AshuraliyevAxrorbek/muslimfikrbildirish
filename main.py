import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import ChatNotFound, BotBlocked, TelegramAPIError
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import asyncio

# logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# O'zgaruvchilar
API_TOKEN = "8382580096:AAHlyf3qGsvEtRUmpYzX_NjABTSpf5R59Ik"  # Bot tokeningizni yozing
ADMIN_CHAT_ID = -1002944106693  # Admin kanal ID'si

# WebApp URL manzilini kiriting
WEB_APP_URL_MUSLIM = "https://ashuraliyevaxrorbek.github.io/muslimshirinliklari/" # Sizning WebApp manzilingiz

# Bosh menyu klaviaturasi
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📝 Fikr qoldirish",
                web_app=WebAppInfo(url=WEB_APP_URL_MUSLIM)
            )
        ]
    ],
    resize_keyboard=True
)

# /start buyrug'ini qabul qilish
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Fikr-mulohazalaringizni qoldiring.", reply_markup=main_menu)

# WebAppdan kelgan ma'lumotni qabul qilish
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    print("--- WebApp'dan yangi ma'lumot keldi ---")

    try:
        data = json.loads(message.web_app_data.data)
        print("✅ Ma'lumot muvaffaqiyatli tahlil qilindi:", data)
    except Exception as e:
        logger.exception("WebApp data parsing error")
        await message.answer(f"❌ JSON xato: {e}")
        return

    rating = data.get("rating", "—")
    name = data.get("name", "—")
    comment = data.get("comment", "—")

    caption = (
        "<b>Yangi fikr!</b>\n\n"
        f"⭐ <b>Yulduz:</b> {rating}\n"
        f"👤 <b>Ism:</b> {name}\n"
        f"💬 <b>Fikr:</b> {comment}\n\n"
        "--- Ma'lumotlar ---\n"
        f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
        f"👤 <b>Foydalanuvchi:</b> {message.from_user.full_name}"
    )

    try:
        await bot.send_message(ADMIN_CHAT_ID, caption, parse_mode='HTML')
        await message.answer("✅ Fikringiz qabul qilindi, rahmat!")
        print("✅ Ma'lumot admin kanalga yuborildi.")
    except Exception as e:
        print(f"❌ Xabar yuborishda xato: {e}")
        await message.answer("❌ Fikringizni qabul qilishda xato yuz berdi.")

# Botni ishga tushirish
if __name__ == '__main__':
    from aiogram import executor
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True)
