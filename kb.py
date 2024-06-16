from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


start_kb = ReplyKeyboardMarkup( #кнопка начинающая тестирования
    keyboard=[
    [KeyboardButton(text="начать тестирование")]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?')

started_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Да👍"),
        KeyboardButton(text="Нет👎")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Нравится?')


fiztech_url = InlineKeyboardButton( #инлайн кнопка с ссылкой на сайт колледжа 
    text= "Наш сайт",
    url="https://phystech.pro")

fiztech_tg = InlineKeyboardButton( #инлайн кнопка с ссылкой на ткг коллджа
    text="Наш телеграмм-канал",
    url="https://web.telegram.org/a/#-1001612689610")
        

end_kb = InlineKeyboardMarkup(inline_keyboard=[[fiztech_tg],[fiztech_url]]) #форма инлайн кнопки в маркап


    




