from aiogram import executor
from create_bot import dp
from data_base import sqlite_db

async def on_startup(_):
    print('Bot online')
    sqlite_db.CreateBD()

from handlers import client, other

client.handlers_client(dp)
other.handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True, on_startup=on_startup)