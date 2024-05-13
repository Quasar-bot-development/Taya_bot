from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from time import sleep
from aiogram.types import FSInputFile
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import os
import re
import asyncio
from datetime import datetime
import sqlite3 as sql
import app.keyboards as kb
import pandas as pd 


ADMIN_ID = []
TIME_SLEEP = 2
with open('admin_id.txt', 'r') as f:
    ADMIN_ID = f.readlines()


with open('./setting.txt','r') as f:
    SETTING_FILE = f.readlines()


SEND_TIME_1 = "10:00:00"
SEND_TIME_2 = "10:00:01"
SETTING_FILE = SETTING_FILE[1].split('/')
CURRENT_TIME = datetime.now() #По возможности убрать в БД, глобалить это нельзя
IS_HOMEWORK_DONE = False #Нужно подтягивать из БД и убрать из глобала


#Проверка на валидацию номера телефона
def is_phone_number(input):
    pattern = re.compile(r'^(\+7|7|8)\d{10}$')
    if pattern.match(input):
        return True
    else:
        return False


h_w_flag = False #Флаг домашнего задания false -не выполнено, true - выполнено
router = Router()


class User_info(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    telegram_name = State()
    instagramm_name = State()
    request = State()


async def send_news(message: Message, bot: Bot, data):
    connection = sql.connect('./User_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT IS_HOMEWORK_DONE, user_step FROM User WHERE name = ? AND phone_number = ? AND telegram_name = ?',(data['name'],data['phone_number'],data['telegram_name']))
    arr = cursor.fetchall()
    user_step = int(arr[0][1])
    IS_HOMEWORK_DONE = arr[0][0]   #Нужно будет перепроверить
    connection.close()

    if user_step==1:
        await message.answer('Отлично❤️ Я вижу, ты уже скачал мой гайд, и я надеюсь уже выполнил все мои задания, а значит уже на шаг приблизился к своему новому состоянию и новой жизни 🕊️')
    
    elif user_step==2:
        await message.answer('А ты знал, что с помощью арт-терапии …')
        await asyncio.sleep(TIME_SLEEP)
        await message.answer_photo(caption='<i>«вы получаете то, что повторяете»</i>', photo=FSInputFile("./img/photo_4.jpg"))

    elif user_step==3:
        await message.answer('Доброе утро 🤍 \nКак ты? Хочу поделиться с тобой отзывами моих учеников 🥰')
        await message.answer('Посмотри, сколько людей мне пишут о своих изменениях и какое воздействие наша работа через арт-терапию оказала на их состояние и жизнь в целом:')

    elif user_step==4:
        await message.answer('Начни свой путь к лучшей жизни уже сейчас 🫶🏻 и не забудь получить свой подарок в конце видео ❗️')

    elif user_step==5:
        await message.answer_photo(caption='<i>«Знать и не делать – все равно что не знать»</i>', photo=FSInputFile("./img/photo_5.jpg"))
    
    elif user_step==6:
        await message.answer_photo(caption='<i>«Не самосовершенствование – а самооткрытие»</i>', photo=FSInputFile("./img/photo_6.jpg"))

    elif user_step==7:
        if IS_HOMEWORK_DONE == False: #Нужно подтягивать из БД
            video_note = FSInputFile('./video/video_2.mp4')
            await message.answer_video_note(video_note=video_note)
        else:
            user_step-=1

    elif user_step==8:
        await message.answer_photo(caption='<i>«Хорошие привычки делают время союзников. Плохие – врагом»</i>', photo=FSInputFile("./img/photo_7.jpg"))

    connection = sql.connect('./User_db.db')
    cursor = connection.cursor()
    cursor.execute('Update User set user_step = ? WHERE name = ? AND phone_number = ? AND telegram_name = ?',(int(user_step)+1,data['name'],data['phone_number'],data['telegram_name']))
    connection.commit()
    connection.close()


@router.message(F.text, Command("start"))
async def start_loop(message: Message, bot: Bot, state = FSMContext):
    await start_message(message, bot, state)
    await asyncio.sleep(10)
    while True:
        await asyncio.sleep(TIME_SLEEP)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        data = await state.get_data()
        if current_time == SEND_TIME_1 or current_time == SEND_TIME_2: 
            await send_news(message, bot, data)
            break


async def start_message(message: Message, bot: Bot, state = FSMContext):
    data = await state.get_data()
    caption =  "Привет, " + message.from_user.full_name + '''! Рада тебе🩷\n
    Я очень ценю то, что ты доверяешь мне изменение своей жизни в лучшую сторону.\n 
    Меня зовут Тая. Я арт-коуч, бизнес-наставник, музыкант и художница с собственным бизнесом, построенном на любимом творческом деле 🎨\n
    К своим результатам я пришла сама и буду рада поделиться своими секретами, которые успешно работаю в моей жизни и жизни моих учеников.\n
    Я помогу тебе стать лучшей версией себя 🕊️'''

    await asyncio.sleep(TIME_SLEEP)
    await message.answer_photo(caption=caption, photo=FSInputFile("./img/photo_8.jpg"))
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('Чтобы познакомиться со мной поближе я записала для тебя кружочек ⬇️😻')
    await asyncio.sleep(TIME_SLEEP)
    video_note = FSInputFile('./video/video_1.mp4')
    await message.answer_video_note(video_note=video_note)
    await asyncio.sleep(TIME_SLEEP)
    await message.answer_photo(caption='<i>«Себя не находят – себя создают»</i>', photo=FSInputFile("./img/photo_1.jpg"))
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('Отлично! Теперь ты знаешь меня чуть лучше😻')
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('Я тоже хочу познакомиться с тобой и сразу после пришлю тебе файл, который поможет изменить твою жизнь к лучшему\nЯ тоже хочу познакомиться с тобой поближе и сразу после этого пришлю тебе файл, который поможет изменить твою жизнь к лучшему 🫶🏻')
    await asyncio.sleep(TIME_SLEEP)
    await state.set_state(User_info.name)
    await message.answer('Как тебя зовут?')


@router.message(User_info.name)
async def get_name(message: Message,state = FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(User_info.age)
    await message.answer('Сколько тебе лет?')
 

@router.message(User_info.age)
async def get_age(message: Message,state = FSMContext):
    if message.text.isdigit():
        await state.update_data(age = message.text)
        await state.set_state(User_info.phone_number)
        await message.answer('Напиши свой номер телефона')
    else:
        await state.set_state(User_info.age)
        await message.answer('Запиши возраст цифрами')
        await message.answer('Сколько тебе лет?')
    
    
@router.message(User_info.phone_number)
async def get_age(message: Message,state = FSMContext):
    try:
        if is_phone_number(message.text):
            await state.update_data(phone_number = message.text)
            await state.set_state(User_info.telegram_name)
            await message.answer('Напиши свой ник в телеграм')
        else:
            await state.set_state(User_info.phone_number)
            await message.answer('Номер телефона введён некорректно')
            await message.answer('Напиши свой номер телефона')
    except:
        await state.set_state(User_info.phone_number)
        await message.answer('Номер телефона введён некорректно')
        await message.answer('Напиши свой номер телефона')
    
    
@router.message(User_info.telegram_name)
async def get_tg(message: Message,state = FSMContext):
    await state.update_data(telegram_name = message.text)
    await state.set_state(User_info.instagramm_name)
    await message.answer('Напиши свой ник в Инстаграм')
    

@router.message(User_info.instagramm_name)
async def get_insta(message: Message,state = FSMContext):
    await state.update_data(instagramm_name = message.text)
    await state.set_state(User_info.request)
    await message.answer("Выбери свой запрос/цель из предложенных или напиши свой вариант:\n"
                        "• Я хочу узнать, кто я\n"
                        "• Я хочу узнать свою истинную цель\n"
                        "• Я хочу узнать, как уменьшить тревогу и избавиться от стресса\n"
                        "• Я хочу узнать, как мыслить позитивно каждый день и жить свою лучшую жизнь\n"
                        "• Я хочу узнать, как начать проявляться и зарабатывать на любимом деле\n"
                        "• Напишу свой вариант", reply_markup=kb.request)
    

@router.message(User_info.request)
async def get_request(message: Message,bot: Bot, state = FSMContext):
    await state.update_data(request = message.text)
    await message.answer('Спасибо за твои ответы 🤍\nНиже ты можешь скачать свой гайд 🫶🏻 ', reply_markup=kb.download_inline_keyboard)
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('В нем ты узнаешь:\nКак убрать тревогу\nКак поменять мышление с негативного на позитивное\nКак понять свои точки А и B и как прийти к точке B\n', reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(TIME_SLEEP)
    await message.answer_photo(caption='<i>«Единственные ограничения – те, что живут в нашем разуме»</i>', photo=FSInputFile("./img/photo_2.jpg"))
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('''К своим результатам по работе над мышлением (а все начинается именно с него!) я пришла благодаря разным техникам и практикам. В гайде не получится уместить все, но я выбрала <b>САМЫЕ ПРОСТЫЕ И ДЕЙСТВЕННЫЕ</b>.Эти практики я и мои ученики используем регулярно, и они действительно работают! 🔥\nНО! для того чтобы в твоей жизни начались позитивные изменения, необходимо следовать «<b>всем моим инструкциям</b>» из гайда.\nДля дополнительной мотивации в конце гайда тебя ждет <b>подарок</b> 🎁 <i>p.s. торопись, подарок смогут забрать только первые 20 человек 🫶🏻</i>''')
    await asyncio.sleep(TIME_SLEEP)
    await message.answer_photo(caption='<i>«Все создается дважды. Мы можем переложить ответственность за свою жизнь на наш прошлый опыт, детство, других людей – а можем быть творцами своей жизни взяв за нее ответственность.»</i>', photo=FSInputFile("./img/photo_3.jpg"))
    await asyncio.sleep(TIME_SLEEP)
    await message.answer('Твоим домашним заданием будет выполнить арт-терапию, которую ты найдешь в конце этого гайда и прислать её результаты (фото) мне в директ (или сюда в бота)😻')

    data = await state.get_data()
    connection = sql.connect('./User_db.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO User (name,age,phone_number, telegram_name,instagramm_name,request, CURRENT_TIME, IS_HOMEWORK_DONE, user_step) VALUES (?,?,?,?,?,?,?,?,?)', (data['name'], data['age'], data['phone_number'],data['telegram_name'], data['instagramm_name'],data['request'], CURRENT_TIME, False, 1))
    connection.commit()
    connection.close()
    

@router.message(F.photo)
async def home_work(message: Message, bot: Bot, state = FSMContext):
    await message.answer('Молодец😻')
    #Отправка сообщения всем админам
    for current_id in ADMIN_ID:
        await bot.forward_message(chat_id=current_id, from_chat_id=message.chat.id, message_id=message.message_id)
    data = await state.get_data()
    connection = sql.connect('./User_db.db')
    cursor = connection.cursor()
    cursor.execute('Update User set IS_HOMEWORK_DONE = True WHERE name = ? AND phone_number = ? AND telegram_name = ?',(data['name'],data['phone_number'],data['telegram_name']))
    connection.commit()
    connection.close()
    
@router.message(F.text == "/users") 
async def start_loop(message: Message, bot: Bot): 
    if str(message.from_user.id) in ADMIN_ID: 
        conn = sql.connect('User_db.db')
        df = pd.read_sql_query('SELECT * FROM User', conn) 
        df.to_excel("data.xlsx", index=False) 
        conn.close()
        await message.answer_document(document=FSInputFile("data.xlsx"))
        os.remove(f"data.xlsx")
        
        
@router.callback_query(lambda c: c.data == "download_guide")
async def handle_download_button(callback_query: CallbackQuery):
    await callback_query.message.answer_document(document=FSInputFile("./doc/Taya_guide.pdf"))