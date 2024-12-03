"""functions."""
import requests
import datetime as dt

from telebot import TeleBot

import helpers.constants as cons
import helpers.endpoints as endp
import helpers.hyperlinks as link
import core.logging as log
import core.keyboards as kb
import helpers.messages as msg
import api_source.meteo_api as mt
import core.permissions as perm

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


class BaseObject:
    """Base object."""


# FIXME:
class Initializator(BaseObject):
    """Base initializator class."""

    def __init__(self, keyboard, log=True):
        """pass."""
        self.keyboard = keyboard
        self.log = log

    def direct(self, id_data: list):
        """pass."""
        chat_id, *_ = id_data

        if self.log:
            log.logging.info(f'sended to: {chat_id}')
        bot_v1.send_message(
            chat_id=chat_id,
            text=msg.direct_messages['TEST'],
            reply_markup=kb.menu_set['init_cmd'],
        )


# TODO: rebuild with OOP
class Menu(BaseObject):
    """Base menu class."""

    def __init__(self, keyboard, text, log=True) -> None:
        """pass."""
        self.keyboard = keyboard
        self.text = text
        self.log = log

    def menu(self, call):
        """pass."""
        chat = call.message.chat
        if self.log:
            log.logging.info(
                f'{call.data}/'
                f'{call.from_user.first_name}/'
                f'{chat.id}/'
            )
        bot_v1.send_message(
            chat_id=chat.id,
            text=self.text,
            reply_markup=self.keyboard,
        )


# TODO:
class React(BaseObject):
    """Base react class."""


# TODO:
def direct_initializator(chat_id) -> bool:
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


start = Menu(
    kb.menu_set['start_menu'],
    msg.TO_MAIN
)
pics = Menu(
    kb.menu_set['pics_menu'],
    msg.menu_brief['PICS']
)
afisha = Menu(
    kb.menu_set['afisha_menu'],
    msg.menu_brief['AFISHA']
)
weather = Menu(
    kb.menu_set['weather_menu'],
    msg.menu_brief['WEATHER']
)
info = Menu(
    kb.menu_set['info_menu'],
    msg.menu_brief['INFO']
)


# TODO: rebuid reacts with oop
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


# FIXME: current temperature data
def weather_react(call):
    """pass."""
    chat = call.message.chat
    keyboard = kb.react_set['weather_react']
    # today_precip = mt.meteo_data_td['precip_prob']

    weather_data = {
        'today': get_weather(mt.get_data()),
        'tomorrow': get_weather(
            mt.get_data(today=False),
            today=False
        ),
    }
    # if ((today_precip <= ALLOW_PRECIP)
    #         and call.data == 'today'):
    #     report += f'\nКуда можно сходить сегодня:\n{mos_afisha}'

    bot_v1.send_message(
        chat.id,
        text=weather_data[call.data],
        reply_markup=keyboard,
    )


# TODO: what about response[0].get('url')
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
        f'{min_temp} - {max_temp} '
        f'{msg.min_max_temp}\n'
        f'{msg.weather['WIND']} {data['wind_direct']}, '
        f'{int(data['wind'])} {msg.weather['W_SPEED']}\n'
        f'{data['precip_prob']}{msg.weather['RAIN']}\n'
    )
    if not today:
        return report

    report += (
        f'\nСечас:\n{int(data['cur_temp'])} °C\n'
        f':updated: {data['time']}\n'
        f'{msg.weather['WIND']} {data["wind_direct"]}, '
        f'{int(data['wind'])} {msg.weather['W_SPEED']}\n'
        f'{msg.weather['HUMID']} {int(data['humid'])} %\n'
    )
    return report
