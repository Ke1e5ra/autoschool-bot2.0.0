import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    name = State()
    phone = State()
    city = State()
    category = State()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Как вас зовут?")
    await Form.name.set()

@dp.message_handler(state=Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Отправить номер", request_contact=True))
    await message.answer("Пожалуйста, отправьте ваш номер телефона, нажав кнопку ниже, или введите его вручную:", reply_markup=kb)
    await Form.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Укажите ваш город:", reply_markup=ReplyKeyboardRemove())
    await Form.city.set()

@dp.message_handler(state=Form.phone)
async def get_phone_text(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    if len(phone) < 10 or not any(char.isdigit() for char in phone):
        await message.answer("Пожалуйста, введите корректный номер телефона.")
        return
    await state.update_data(phone=phone)
    await message.answer("Укажите ваш город:", reply_markup=ReplyKeyboardRemove())
    await Form.city.set()

@dp.message_handler(state=Form.city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("На какую категорию вы хотите обучаться? (A, B, C и т.д.)")
    await Form.category.set()

@dp.message_handler(state=Form.category)
async def get_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    text = (
        f"Новая заявка на автошколу:\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Город: {data['city']}\n"
        f"Категория: {data['category']}"
    )
    await bot.send_message(chat_id=MANAGER_CHAT_ID, text=text)
    await message.answer("Спасибо! Мы скоро свяжемся с вами.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
