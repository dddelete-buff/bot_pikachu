import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

TOKEN = '8650180210:AAGxAQOHwA-_KGoaapKpiif9Vr4dJhO8JEw'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

PIKACHU_IMAGES = {
    'happy': ['pikachu_happy1.jpg', 'pikachu_happy2.jpg', 'pikachu_happy3.jpg'],
    'angry': ['pikachu_angry1.jpg', 'pikachu_angry2.jpg'],
    'sleepy': ['pikachu_sleepy1.jpg', 'pikachu_sleepy2.jpg'],
    'cute': ['pikachu_cute1.jpg', 'pikachu_cute2.jpg', 'pikachu_cute3.jpg']
}

os.makedirs('image/pikachu', exist_ok=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="😊 Счастливый")],
            [types.KeyboardButton(text="😠 Сердитый")],
            [types.KeyboardButton(text="😴 Сонный")],
            [types.KeyboardButton(text="🥰 Милый")],
            [types.KeyboardButton(text="🎲 Случайный")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Я бот с картинками Пикачу!\n"
        "Выбери настроение Пикачу:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text in ["😊 Счастливый", "😠 Сердитый", "😴 Сонный", "🥰 Милый"])
async def send_category_pikachu(message: types.Message):
    category_map = {
        "😊 Счастливый": "happy",
        "😠 Сердитый": "angry",
        "😴 Сонный": "sleepy",
        "🥰 Милый": "cute"
    }
    category = category_map.get(message.text)
    if category and category in PIKACHU_IMAGES:
        image_name = random.choice(PIKACHU_IMAGES[category])
        image_path = f"image/pikachu/{image_name}"
        try:
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo, caption=f"Вот {message.text.lower()} Пикачу! 🎉")
        except FileNotFoundError:
            await message.answer("❌ Картинка не найдена. Добавь её в папку images/pikachu/")

@dp.message(lambda message: message.text == "🎲 Случайный")
async def send_random_pikachu(message: types.Message):
    all_images = []
    for images in PIKACHU_IMAGES.values():
        all_images.extend(images)
    if all_images:
        image_name = random.choice(all_images)
        image_path = f"image/pikachu/{image_name}"
        try:
            photo = FSInputFile(image_path)
            await message.answer_photo(photo=photo, caption="🐭 Случайный Пикачу!")
        except FileNotFoundError:
            await message.answer("❌ Картинка не найдена")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🎮 Как пользоваться ботом:\n"
        "• Нажми на кнопку с настроением\n"
        "• Получи картинку Пикачу\n"
        "• Или используй команды:\n"
        "  /start - начать заново\n"
        "  /help - эта справка\n"
        "  /random - случайный Пикачу"
    )

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    await send_random_pikachu(message)

async def main():
    print("🤖 Бот с Пикачу запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())