import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def download_instagram_content(insta_url):
    api = f"https://api.sssgram.com/api/download?url={insta_url}"
    res = requests.get(api).json()
    try:
        media_url = res["data"]["media"][0]["url"]
        return media_url
    except:
        return None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Salom! Menga Instagram havolasini yuboring.")

@dp.message_handler()
async def handle_instagram_link(message: types.Message):
    url = message.text.strip()
    if "instagram.com" in url:
        await message.reply("⏳ Yuklanmoqda, kuting...")
        media_url = download_instagram_content(url)
        if media_url:
            await message.reply_document(media_url)
        else:
            await message.reply("❌ Yuklab bo‘lmadi. Linkni tekshiring yoki boshqa postni sinab ko‘ring.")
    else:
        await message.reply("📎 Iltimos, faqat Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
