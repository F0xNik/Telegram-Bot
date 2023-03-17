#from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup#ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1 = KeyboardButton('Список дел')
b2 = KeyboardButton('Добавить задачу')
b3 = KeyboardButton('Удалить задачу')
b4 = KeyboardButton('Изменить задачу')

cancel = KeyboardButton('Отмена')

all_variant = KeyboardButton('Все')

yes = KeyboardButton('Да')
no = KeyboardButton('Нет')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_buton = ReplyKeyboardMarkup(resize_keyboard=True)
for_delete_button = ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).insert(b2).add(b3).insert(b4)
cancel_buton.add(cancel)
for_delete_button.add(cancel).insert(all_variant)
yes_or_no_keyboard.add(yes).insert(no).add(cancel)