from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import get_data
import json
import os
import time

# bot = Bot(token='')
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Ножи", 'Перчатки', 'Снайперские винтовки']
    keyword = types.ReplyKeyboarsMarkup(resize_keyboard=True)
    keyword.add(*start_buttons)

    await message.answer("Выберите категорию", reply_markup=keyword)


@dp.message_handler(Text(equals="Ножи"))
async def get_shoes(message: types.Message):
    await message.answer("Please waiting...")

    get_data()

    with open('data.json', 'r') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("title"), item.get("link_3d"))}\n' \
               f"{hlink(hbold(item.get('Цена: ')))} {hlink(item.get('price'))}\n" \
               f"{hlink(hbold(item.get('Скидка: ')))} {hlink(item.get('discount'))}\n"

        if index % 20 == 0:
            time.sleep(3)

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
