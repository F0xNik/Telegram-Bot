Добро пожаловать в телеграм-бот "Cute do list" с классом  взаимодействия с API!

1. Наше приложение использует бесплатные API в сети для загрузки рандомных фотографий котиков, собачек и лисичек: https://aws.random.cat/meow, https://random.dog/woof.json, https://randomfox.ca/floof/, делая, тем самым, работу со списком задач приятнее для пользователя. 
2. Класс взаимодействия с АPI и методы этого класса описаны в файле other.py. Класс -  AnimalCute().
3. В результате, после реализации и проверки функциональности, был написан телеграм-бот "Cute do list".

Описание работы
Для запуска бота необходимо запустить Bash script командой sh bot_run.sh
В работе используется база данных SQL которая создается когда первый пользователь вводит свое дело. Дальше она удаляется если пользователь решит "Удалить задачу"
При вводе параметров ДАТА, ВРЕМЯ присутствует проверка на корректный ввод.
Также при "Удалении задачи" выводится список задач конкретного пользователя (по ip user) при попытке ввести не валидный номер задачи бот среагирует корректно и попросит ввести валидный номер задачи для удаления.  

Инструкция

Необходимо зайти в Telegram и найти в строке "Поиск" телеграм-бот "Сute do list". В начале взаимодействия с телеграм-ботом пользователю требуется нажать команду "/start".

После получения ответа от бота пользователь может обратиться к выпадающему меню со следующими функциями:

- Кнопка "Список дел". При нажатии пользователем данной опции в качестве ответа поступит рандомно сгенерированная картинка - котика, собачки или лисички, и сам список дел. Он будет пуст, если ранее в него не было записано никаких дел или если все дела были удалены ранее.  

- Кнопка "Добавить задачу". При выборе пользователем этой опции необходимо указать дату, время и саму задачу. 

- Кнопка "Удалить задачу". При выборе данной опции и указании номера задачи пользователем, она будет удалена из списка дел.

- Кнопка "Измененить задачу". При выборе пользователем данной опции, указания номера задачи и написания желаемых изменений в задачу - она будет изменена.

Также в дополнительном меню можно выбрать опцию и получить фотографию котика (/cat), собачки (/dog) или лисички (/fox).

В будущем планируется реализация:
1) отправка сообщения пользователю о запланированном деле в назначенную дату и время
2) самоочищение базы данных при преодолении отметки времени данного задания
3) добавление кнопок при выборе удаления или изменения задачи
4) возможность изменить определенные параметры задачи, а не все сразу
