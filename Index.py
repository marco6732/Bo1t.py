import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

# Token va kanal ID'larining ro'yxati
BOT_TOKEN = '7781232918:AAGBgKvCCRko3Dsrv-6zplaBQIX407OG2Fg'

# Tekshiriladigan kanallar ro'yxati
CHANNEL_IDS = [
    {"id": "-1002364818027", "url": "https://t.me/lerza1", "name": "Kanal 1"},  # Kanal 1
    {"id": "-1002364818027", "url": "https://instagram.com/marco1off", "name": "insta"},  # Kanal 3
    {"id": "-1002280395833", "url": "https://t.me/lerza4", "name": "Kanal 4"}   # Kanal 4
]

# Tekshirilmaydigan kanallar ro'yxati
EXCLUDED_CHANNELS = [
    {"id": "-1001234567890", "url": "https://instagram.com/marco1off", "name": "Instagram"}   # Instagram kanal (faqat ko'rinadi, lekin 2-chi o'rinda bo'lishi kerak)
]

# Video File ID
VIDEO_FILE_ID = "BAACAgQAAxkBAAMYZF..."  # O'zingizning video ID'nizni qo'ying

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratamiz
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchi obuna holatini tekshiruvchi funksiya
async def check_subscription(user_id):
    not_subscribed_channels = []  # Foydalanuvchi obuna bo'lmagan kanallar ro'yxati
    for channel in CHANNEL_IDS:  # Faqat tekshiriladigan kanallarni ko'rib chiqamiz
        check_sub_channel = await bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
        if check_sub_channel.status == "left":
            not_subscribed_channels.append(channel)
    return not_subscribed_channels

# /start komanda uchun handler
@dp.message_handler(Command("start"))
async def send_welcome(message: Message):
    not_subscribed_channels = await check_subscription(message.from_user.id)
    if not not_subscribed_channels:
        await message.answer("✅ Botdan foydalanish mumkin!")
    else:
        # Instagram kanalini 2-chi o'rinda qo'shish
        all_channels = CHANNEL_IDS + [EXCLUDED_CHANNELS[0]]  # Instagram kanalini 2-chi o'ringa qo'shamiz
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{channel['name']}", url=channel["url"]) for channel in all_channels],
                [InlineKeyboardButton(text="✅ A'zo bo'ldim ✅", callback_data="azo")]
            ],
            row_width=1
        )
        await message.answer(
            "⬇️ <b>Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling</b> ⬇️",
            reply_markup=keyboard,
            parse_mode='HTML'
        )

# Callback query uchun handler
@dp.callback_query_handler(Text(equals="azo"))
async def callback_subscribe(callback_query: CallbackQuery):
    not_subscribed_channels = await check_subscription(callback_query.from_user.id)
    if not not_subscribed_channels:
        await callback_query.message.answer("✅ Botdan foydalanish mumkin!")
    else:
        # Instagram kanalini 2-chi o'rinda ko'rsatish
        all_channels = CHANNEL_IDS + [EXCLUDED_CHANNELS[0]]  # Instagramni 2-chi o'rinda ko'rsatish
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{channel['name']}❓", url=channel["url"]) for channel in all_channels],
                [InlineKeyboardButton(text="✅ A'zo bo'ldim ✅", callback_data="azo")]
            ],
            row_width=1
        )
        await callback_query.message.reply(
            "❌ A'zo bo'lmadingiz, qayta urinib ko'ring! ❌",
            reply_markup=keyboard
        )

# Har qanday xabar uchun handler
@dp.message_handler()
async def handle_message(message: Message):
    # Foydalanuvchi kanalga a'zo bo'lmasa
    not_subscribed_channels = await check_subscription(message.from_user.id)
    if not not_subscribed_channels:
        # Kanalga a'zo bo'lgan bo'lsa, buyruqlarni qabul qilish
        if message.text == "34":
            await message.answer("segt")
        elif message.text == "39": 
            await message.answer("se55gt")
        elif message.text == "35":
            await message.answer("solom")
        elif message.text == "36":
            await message.answer("senmi")
        elif message.text == "23":
            await message.answer_video(
                video="BAACAgIAAxkBAANuZ2Ltl02bqIVVAhl9aQvEFxDy7NgAApppAALH4dhKU0O1_wFg8-c2BA",
                caption="Mana sizga video!"
            )
        elif message.text == "24":
            await message.answer_video(
                video="BAACAgQAAxkBAAIBDWdi_czxs-BTPOaxSSN2i1KpfGedAAI1EgACfeQYU8W4lFJ3y7rcNgQ",
                caption="Mana sizga video!"
            )
        else:
            await message.answer("⚠️ Bu buyruq noto'g'ri yoki mavjud emas!")
    else:
        # Kanalga a'zo bo'lmagan bo'lsa, kanalga a'zo bo'lish uchun oyna yuboriladi
        all_channels = not_subscribed_channels + EXCLUDED_CHANNELS
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{channel['name']}❓ Kanalga a'zo bo'lish", url=channel["url"]) for channel in all_channels],
                [InlineKeyboardButton(text="✅ A'zo bo'ldim ✅", callback_data="azo")]
            ],
            row_width=1
        )
        await message.answer(
            "⬇️ <b>Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling</b> ⬇️",
            reply_markup=keyboard,
            parse_mode='HTML'
        )


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_video_id(message: Message):
    video_id = message.video.file_id
    await message.answer(f"Video File ID: {video_id}")
    
# Asosiy funksiya
async def main():
    print("Bot ishga tushmoqda.mardon..")
    await dp.start_polling()

# Botni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
