from aiogram import types, Dispatcher
from create_bot import dp
from create_bot import bot
#import requests
import requests
import random

class CuteAnimal:
    number_animal = 0
    def RandomAnimal(self):
        number_animal = random.randint(1,3)
        return number_animal
    def GetURL(self,number_animal):
        if (number_animal == 1):
            url = 'https://aws.random.cat/meow'
        elif (number_animal == 2):
            url = 'https://random.dog/woof.json'
        elif (number_animal == 3):
            url = 'https://randomfox.ca/floof/'
        else: 
            url = 'Not correct parameter - not correct url'
        return url
    def GetJSONPicture(self,url):
        response = requests.request("GET", url)
        if  response.status_code==200:
            responses_json = response.json()
        else:
            responses_json = "Not correct"
        return responses_json
    def FindPicture(self, responses_json, number_animal):
        if (responses_json == 'Not correct'):
            find_picture = 'Not correct'
        elif (number_animal == 1): 
            find_picture = responses_json["file"]
        elif (number_animal==2):
            find_picture = responses_json["url"]
        elif (number_animal==3):
            find_picture = responses_json["image"]
        return find_picture





# @dp.message_handler()
# async def repeat(message: types.Message):
#    await message.answer("Балдеж, Насть, но давай юзать кнопки")

async def get_dog(message: types.Message):
    cute_animal = CuteAnimal()
    URL = cute_animal.GetURL(2)
    response_json = cute_animal.GetJSONPicture(URL)
    find_picture = cute_animal.FindPicture(response_json, 2)
    await bot.send_photo(message.from_user.id, find_picture)
    #await message.answer()


async def get_cat(message: types.Message):
    cute_animal = CuteAnimal()
    URL = cute_animal.GetURL(1)
    response_json = cute_animal.GetJSONPicture(URL)
    find_picture = cute_animal.FindPicture(response_json, 1)
    await bot.send_photo(message.from_user.id, find_picture)
    #await message.answer()


async def get_fox(message: types.Message):
    cute_animal = CuteAnimal()
    URL = cute_animal.GetURL(3)
    response_json = cute_animal.GetJSONPicture(URL)
    find_picture = cute_animal.FindPicture(response_json, 3)
    await bot.send_photo(message.from_user.id, find_picture)
    #await message.answer()



def handlers_other(dp : Dispatcher):
    dp.register_message_handler(get_dog,commands=['dog'])
    dp.register_message_handler(get_cat,commands=['cat'])
    dp.register_message_handler(get_fox,commands=['fox'])
    # dp.register_message_handler(repeat)


# #@dp.message_handler()
# async def repeat(message: types.Message):
#    await message.answer("Балдеж, Насть, но давай юзать кнопки")
