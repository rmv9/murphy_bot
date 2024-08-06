"""functions."""
import requests
import datetime as dt

from dotenv import load_dotenv
from telebot import TeleBot

import helpers.constants as cons
import helpers.endpoints as endp
import helpers.hyperlinks as link
import core.keyboards as kb
import helpers.messages as msg
import api.meteo_api as mt
import core.permissions as perm

load_dotenv()

bot_v1 = TeleBot(token=perm.TELEGRAM_BOT_TOKEN)

now = dt.datetime.now()
current_hour = now.time().hour
contact_info = 'rmv.msk@mail.ru'

ALLOW_PRECIP = 45

mos_afisha = link.events['today']['mos_afisha']
cinema_balt = link.cinema['today']['baltic']
cinema_otrada = link.cinema['today']['otrada']

param_text = (
    'TEST mode. v1\n'
    f'retry period: {cons.RETRY_PERIOD} sec.\n'
    f'meteo_api: available\n'
    f'retry mode: {cons.RETRY_MODE}\n\n'
    f'owner id: {perm.CHAT_ID_MAX}\n'
    f'contact mail: {contact_info}'
)


# FIXME:
def direct_initialization(chat_id):
    """pass."""
    keyboard = kb.menu_set['init_cmd']

    bot_v1.send_message(
        chat_id=chat_id,
        text=msg.direct_messages['TEST'],
        reply_markup=keyboard,
    )


def init_cmd(message):
    """pass."""
    name = message.from_user.first_name
    keyboard = kb.menu_set['init_cmd']

    bot_v1.send_message(
        chat_id=message.chat.id,
        text=(
            f'Привет {name}!\n{msg.HELLO_SPEECH}'
        ),
        reply_markup=keyboard,
    )


def start_menu(call):
    """Say hello to user."""
    chat = call.message.chat
    keyboard = kb.menu_set['start_menu']

    bot_v1.send_message(
        chat_id=chat.id,
        text=msg.START_GUIDE,
        reply_markup=keyboard,
    )


def pics_menu(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.menu_set['pics_menu']

    bot_v1.send_message(
        chat_id=chat.id,
        text='1000 картинок котов или собак, к твоим услугам)',
        reply_markup=keyboard,
    )


def afisha_menu(call):
    """pass."""
    message = call.message
    chat = message.chat
    keyboard = kb.menu_set['afisha_menu']
    bot_v1.send_message(
        chat_id=chat.id,
        text=('интересует афиша?'),
        reply_markup=keyboard,
    )


def weather_menu(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.menu_set['weather_menu']

    bot_v1.send_message(
        chat_id=chat.id,
        text=('Погода на какое время интересует?'),
        reply_markup=keyboard,
    )


def info_menu(call):
    """pass."""
    message = call.message
    chat = message.chat
    keyboard = kb.menu_set['info_menu']

    bot_v1.send_message(
        chat_id=chat.id,
        text=msg.INFO_SPEECH,
        reply_markup=keyboard,
    )


def info_react(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.react_set['info_react']
    data_dict = {
        'author': msg.author,
        'functions': msg.functions,
        'params': param_text,
    }
    bot_v1.send_message(
        chat_id=chat.id,
        text=data_dict[call.data],
        reply_markup=keyboard,
    )


# TODO:
def weather_react(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.react_set['weather_react']
    # today_precip = mt.meteo_data_td['precip_prob']

    weather_data = {
        'today': get_weather(mt.meteo_data_td),
        'tomorrow': get_weather(mt.meteo_data_tm, today=False),
    }
    report = weather_data[call.data]
    # if ((today_precip <= ALLOW_PRECIP)
    #         and call.data == 'today'):
    #     report += f'\nКуда можно сходить сегодня:\n{mos_afisha}'

    bot_v1.send_message(
        chat.id,
        text=report,
        reply_markup=keyboard,
    )


# TODO: think about response[0].get('url')
# now we have json collection as dict. whith key-'url'
# maybe better use url with picture directly
def picture_react(call):
    """Get cat pic from external API."""
    chat = call.message.chat
    keyboard = kb.react_set['picture_react']

    picture_data = {
        'cat': endp.CAT_PIC_ENDPOINT,
        'dog': endp.DOG_PIC_ENDPOINT,
    }
    response = requests.get(picture_data[call.data]).json()
    pic_url = response[0].get('url')

    bot_v1.send_photo(
        chat_id=chat.id,
        photo=pic_url,
        reply_markup=keyboard,
    )


def afisha_react(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.react_set['afisha_react']
    cinema_data = {
        'mos_afisha': mos_afisha,
        'cinema_balt': cinema_balt,
        'cinema_otrada': cinema_otrada,
    }

    bot_v1.send_message(
        chat_id=chat.id,
        text=cinema_data[call.data],
        reply_markup=keyboard,
    )


def get_weather(data: dict, today=True) -> str:
    """Get meteo data from external API."""
    min_temp, max_temp = (
        data['min_temp'], data['max_temp']
    )
    report = (
        f'{min_temp}-{max_temp} '
        f'{msg.min_max_temp} '
        f'{data['precip_prob']}{msg.optional_reacts['RAIN']}'
    )
    if not today:
        return report
    report += (
        f'Сечас {int(data['cur_temp'])} °C\n'
        f'Ветер {int(data['wind'])} м/с\n'
        f'Влажность {int(data['humid'])} %\n'
        )

    return report
