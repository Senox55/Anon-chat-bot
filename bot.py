from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from database import Database

BOT_TOKEN = '6783993214:AAEo0dxpvyjQy4ifGUabn23rDnT0j7EmtF8'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = Database('my_db.mwb')

button_start_search = KeyboardButton(text='😎 Поиск собеседника')
button_stop_search = KeyboardButton(text='❌ Остановить поиск собеседника')

keyboard_before_start_search = ReplyKeyboardMarkup(keyboard=[[button_start_search]], resize_keyboard=True)
keyboard_after_start_research = ReplyKeyboardMarkup(keyboard=[[button_stop_search]], resize_keyboard=True)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Добро пожаловать в анонимный чат бот!\n'
        'Чтобы начать общение нажмите кнопку '
        '"Поиск собеседника"',
        reply_markup=keyboard_before_start_search
    )


@dp.message(F.text == '😎 Поиск собеседника')
async def process_start_search_command(message: Message):
    await message.answer(
        'Ищем собеседника...',
        reply_markup=keyboard_after_start_research
    )
    db.add_queue(message.chat.id)


if __name__ == '__main__':
    dp.run_polling(bot)
