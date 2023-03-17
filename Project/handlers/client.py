from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, cancel_buton, for_delete_button, yes_or_no_keyboard
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
import random
from handlers.other import get_cat, get_dog, get_fox
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

class FSMdeal(StatesGroup):
    #user_id = State()
    action = State()
    date = State()
    time = State()

class FSMdelete(StatesGroup):
    num_task = State()

class FSMchange(StatesGroup):
    id_text = State()
    #answer = State()
    text_busines = State()
    date = State()
    time = State()

#@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply("\t\t🐱🦊🐶\nДобро пожаловать в телеграм-бот Cute do list! \n\nВ нём Вы можете:\n\n 📃 Просмотреть свой список дел\n\n ✏ Добавить задачу в To do list\n\n 🗑 Удалить дело из расписания\n\n 📝 Изменить любую ранее созданную вами задачу\n\n 🖼 Получить картинку собаки/кошки/лисы\n", reply_markup=kb_client)



async def Print_list(message: types.Message):
    if sqlite_db.GetIDText(message.from_user.id) > 1:
        answ = parser(sqlite_db.SelectTasks(message.from_user.id),message)
    else:
        answ = ("Дел нет, но есть картинка 😊")
    #mes_copy = message
    number_animal = random.randint(1,3)
    if number_animal == 1:
        await get_dog(message)
    elif number_animal == 2:
        await get_cat(message)
    else:
        await get_fox(message)
    await message.answer(answ)



#Добавление занятия в список дел 
#__________________________________________________________________



async def Add_list(message: types.Message):
    await FSMdeal.action.set()
    await message.reply("Какое занятие добавим?",reply_markup=cancel_buton)

async def get_act(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['action'] = message.text
    await FSMdeal.next()
    await message.reply("Дата?")

async def get_date(message: types.Message, state: FSMContext):
    if len(message.text) == 10:
        check = 1
        for i in range(0, 9):
            if message.text[i].isdigit():
                if i == 0 and int(message.text[i]) > 3:
                    check = 0
                elif i == 3 and int(message.text[i]) > 1:
                    check = 0
                elif i == 6 and int(message.text[i]) != 2:
                    check = 0
                elif i == 7 and int(message.text[i]) != 0:
                    check = 0
                elif i == 8 and int(message.text[i]) != 2:
                    check = 0
                elif i == 9 and int(message.text[i]) > 2:
                    check = 0
            elif i == 2 or i == 5:
                if message.text[i]!='.':
                    check = 0
        if check == 1:
            async with state.proxy() as data:
                data['date'] = message.text
            await FSMdeal.next()
            await message.reply("Время?")
        else:
            await message.reply("Некорректный формат даты! Пожалуйста, введите дату правильного формата:\n\tdd.mm.yyyy")
    else:
        await message.reply("Некорректный формат даты! Пожалуйста, введите дату правильного формата:\n\tdd.mm.yyyy")


async def get_time(message: types.Message, state: FSMContext):
    if len(message.text) == 5:
        check = 1
        for i in range(0,4):
            if message.text[i].isdigit():
                if i == 0 and int(message.text[i]) > 2:
                    check = 0
                elif i == 1 and int(message.text[i-1]) == 2 and int(message.text[i]) > 3:
                    check = 0
                elif i == 3 and int(message.text[i]) > 5:
                    check = 0
            elif message.text[i]!=':':
                check = 0
        if check == 1:
            async with state.proxy() as data:
                data['time'] = message.text
            async with state.proxy() as data:
                sqlite_db.FillDB(sqlite_db.GetIDBusiness(),data['date'],data['time'],sqlite_db.GetIDText(message.from_user.id),data['action'], message.from_user.id)
            await message.answer("Запись успешно добавлена!", reply_markup=kb_client)
            await state.finish()
        else: 
            await message.reply("Некорректный формат времени! Пожалуйста, введите время правильного формата: \n\thh:mm")
    else:
        await message.reply("Некорректный формат времени! Пожалуйста, введите время правильного формата:\n\thh:mm")



#__________________________________________________________________



async def delete_list(message: types.Message):
    await Print_list(message)
    await FSMdelete.num_task.set()
    await message.reply("Какую задачу вы хотите удалить?\nВведите номер задачи:", reply_markup=for_delete_button)

async def delete_list_2(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if (int(message.text)in range (0, sqlite_db.GetIDText(message.from_user.id))):
            async with state.proxy() as data_del:
                data_del['num_task'] = message.text
                sqlite_db.DeleteTheTask(message.from_user.id, int(data_del['num_task']))
                await message.answer("Задание успешно удалено из списка дел",reply_markup=kb_client)
                await state.finish()
        else:
            await message.reply("Ошибка.\nВведите номер задачи или воспользуйтесь кнопкой <<Все>> для удаления всех задач")
    elif message.text == "Все":
        for i in range(sqlite_db.GetIDText(message.from_user.id),0,-1):
            num = i
            sqlite_db.DeleteTheTask(message.from_user.id, num)
        await message.answer("Все задания успешно удалены из списка дел",reply_markup=kb_client)
        await state.finish()
    else:
        await message.reply("Ошибка.\nВведите номер задачи или воспользуйтесь кнопкой <<Все>> для удаления всех задач")
        await Print_list(message)


#____________________________________________________________________________________________________




async def change_list(message: types.Message):
    await Print_list(message)
    await FSMchange.id_text.set()
    await message.reply("Какую задачу вы хотите изменить?\nВведите номер задачи:",reply_markup=cancel_buton)

async def change_list_id_text(message: types.Message, state=FSMchange.id_text):
    if not message.text.isdigit() or (int(message.text) not in range (0, sqlite_db.GetIDText(message.from_user.id))):
        await message.answer("Неверный номер задачи")
        await Print_list(message)
    else:
        async with state.proxy() as data_change:
            data_change['id_text'] = message.text
        #await FSMchange.next()
        #await message.answer("Uзменить текст задачи?")#, reply_markup=yes_or_no_keyboard)
        await FSMchange.next()
        await message.answer("Введите новый текст задачи:")
        #await change_list_helper(message, FSMchange.answer)

# async def change_list_helper(message: types.Message, state=FSMchange.answer):
#     if yes_or_no(message,FSMchange.answer):
#         #
#         #МЕНЯЕМ ТЕКСТ
#         #
#         await FSMchange.id_text.set()
#         await message.answer("Введите новый текст")
#         await change_list_text_busines(message,FSMchange.text_busines)
#     else:
#         await message.answer("Хотите изменить дату?", reply_markup=yes_or_no_keyboard)
#         FSMchange.ans.set()
#         if yes_or_no(message):
#             #
#             #Меняем дату
#             #
#             await FSMchange.date.set()
#             await message.answer("Введите новую дату")
#             await change_list_date(message,FSMchange.date)
#         else:
#             await message.answer("Хотите изменить время?", reply_markup=yes_or_no_keyboard)
#             FSMchange.ans.set()
#             if yes_or_no(message):
#                 #
#                 #Меняем время
#                 #
#                 await FSMchange.time.set()
#                 await message.answer("Введите новое время")
#                 await change_list_time(message, FSMchange.time)
#             else:
#                 await message.answer("Что ж, значит ничего не меняем)", reply_markup=kb_client)

# async def yes_or_no(message: types.Message, state = FSMchange.answer):
#     if message.text == "Да":
#         return 1
#     elif message.text == "Нет":
#         return 0
#     else:
#         await message.reply("Непонял")




async def change_list_text_busines(message: types.Message, state=FSMchange.text_busines):
    async with state.proxy() as data_change:
        data_change['text_busines'] = message.text
    sqlite_db.UpdateTaskText(message.from_user.id, int(data_change['id_text']), data_change['text_busines'])
    await FSMchange.next()
    await message.answer("Введите дату задачи:")
    
async def change_list_date(message: types.Message, state=FSMchange.date):
    if len(message.text) == 10:
        check = 1
        for i in range(0, 9):
            if message.text[i].isdigit():
                if i == 0 and int(message.text[i]) > 3:
                    check = 0
                elif i == 3 and int(message.text[i]) > 1:
                    check = 0
                elif i == 6 and int(message.text[i]) != 2:
                    check = 0
                elif i == 7 and int(message.text[i]) != 0:
                    check = 0
                elif i == 8 and int(message.text[i]) != 2:
                    check = 0
                elif i == 9 and int(message.text[i]) > 2:
                    check = 0
            elif i == 2 or i == 5:
                if message.text[i]!='.':
                    check = 0
        if check == 1:
            async with state.proxy() as data_change:
                data_change['date'] = message.text
            sqlite_db.UpdateTaskDate(message.from_user.id, int(data_change['id_text']),data_change['date'])
            #await message.answer("time",reply_markup=kb_client)
            await FSMchange.next()
            await message.answer("Введите время задачи:")
        else:
            await message.reply("Некорректный формат даты! Пожалуйста, введите дату правильного формата:\n\tdd.mm.yyyy")
    else:
        await message.reply("Некорректный формат даты! Пожалуйста, введите дату правильного формата:\n\tdd.mm.yyyy")


async def change_list_time(message: types.Message, state=FSMchange.time):
    if len(message.text) == 5:
        check = 1
        for i in range(0,4):
            if message.text[i].isdigit():
                if i == 0 and int(message.text[i]) > 2:
                    check = 0
                elif i == 1 and int(message.text[i-1]) == 2 and int(message.text[i]) > 3:
                    check = 0
                elif i == 3 and int(message.text[i]) > 5:
                    check = 0
            elif message.text[i]!=':':
                check = 0
        if check == 1:
            async with state.proxy() as data_change:
                data_change['time'] = message.text
            sqlite_db.UpdateTaskTime(message.from_user.id, int(data_change['id_text']),data_change['time'])
            await message.answer("Задача успешно изменена!", reply_markup=kb_client)
            await state.finish()
        else: 
            await message.reply("Некорректный формат времени! Пожалуйста, введите время правильного формата:\n\thh:mm")
    else:
        await message.reply("Некорректный формат времени! Пожалуйста, введите время правильного формата:\n\thh:mm")
    





def parser(list_info, message: types.Message):
    our_str = ""
    for i in range(0,sqlite_db.GetIDText(message.from_user.id)-1):
        our_str = our_str + str(list_info[i][2]) +". "+ list_info[i][3] +": "+ list_info[i][0] +", "+ list_info[i][1] + "\n\n"
    return our_str


@dp.message_handler(Text("Отмена"), state='*')
async def cancel_func(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is not None:
        await state.finish()
        await message.answer("Действие успешно отменено!", reply_markup=kb_client)


def handlers_client(dp : Dispatcher):
    dp.register_message_handler(send_welcome,commands=['start'])
    dp.register_message_handler(Print_list,Text('Список дел'))
    #_____________________________________________________________________
    dp.register_message_handler(Add_list,Text('Добавить задачу'),state=None)
    dp.register_message_handler(get_act,state=FSMdeal.action)
    dp.register_message_handler(get_date,state=FSMdeal.date)
    dp.register_message_handler(get_time,state=FSMdeal.time)
    #_____________________________________________________________________
    dp.register_message_handler(delete_list,Text('Удалить задачу'), state=None)
    dp.register_message_handler(delete_list_2, state=FSMdelete.num_task)
    #_____________________________________________________________________
    #dp.register_message_handler(change_list,Text('Изменить задачу'))
    dp.register_message_handler(change_list,Text('Изменить задачу'), state=None)
    #dp.register_message_handler(change_list_helper)
    dp.register_message_handler(change_list_id_text, state=FSMchange.id_text)
    dp.register_message_handler(change_list_text_busines, state=FSMchange.text_busines)
    dp.register_message_handler(change_list_date, state=FSMchange.date)
    dp.register_message_handler(change_list_time, state=FSMchange.time)