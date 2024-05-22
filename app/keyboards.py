from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить гайд')]],
    resize_keyboard=True,
    input_field_placeholder= 'Выберите действие'
)


create_yourself = main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать себя')]],
    resize_keyboard=True
)


request = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Я хочу узнать кто Я'), KeyboardButton(text='Я хочу узнать свою истинную цель')],
    [KeyboardButton(text='Я хочу понять, как уменьшить тревогу и избавиться от стресса')],[KeyboardButton(text='Как мыслить позитивно каждый день и жить свою лучшую жизнь')],
    [KeyboardButton(text='Как начать проявляться и зарабатывать на любимом деле')]],
    resize_keyboard=True,
    input_field_placeholder= 'Свой вариант...')

download_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Скачать гайд', 
                                           callback_data='download_guide')]])