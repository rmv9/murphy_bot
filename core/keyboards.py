"""keyboards."""

from telebot import types

import helpers.messages as msg

# initial command
init_cmd_keyboard = types.InlineKeyboardMarkup()
init_cmd_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start',
    ),
)

# start menu and other
start_menu_keyboard = types.InlineKeyboardMarkup()
start_menu_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.main_btns['PICS'],
        callback_data='pictures',
    ),
    types.InlineKeyboardButton(
        text=msg.main_btns['WEATH'],
        callback_data='weather',
    ),
),
start_menu_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.main_btns['INFO'],
        callback_data='info',
    ),
    types.InlineKeyboardButton(
        text=msg.main_btns['AFISHA'],
        callback_data='afisha',
    ),
)

# pictures menu
picture_keyboard = types.InlineKeyboardMarkup()
picture_keyboard.row(
    types.InlineKeyboardButton(
        text='котик',
        callback_data='cat',
    ),
    types.InlineKeyboardButton(
        text='пёсель',
        callback_data='dog',
    ),
)
picture_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start',
    )
)

# weather menu
weather_keyboard = types.InlineKeyboardMarkup()
weather_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.weather_btns['TODAY'],
        callback_data='today'
    ),
    types.InlineKeyboardButton(
        text=msg.weather_btns['TOMORROW'],
        callback_data='tomorrow'
    ),
)
weather_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.weather_btns['WEEK'],
        callback_data='week'
    ),
)
weather_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start',
    )
)

# info menu
info_keyboard = types.InlineKeyboardMarkup()
info_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.info_menu['GUIDE'],
        callback_data='functions'
    ),
    types.InlineKeyboardButton(
        text=msg.info_menu['PARAMS'],
        callback_data='params'
    ),
)
info_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.info_menu['AUTHOR'],
        callback_data='author'
    ),
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start'
    ),
)

# afisha menu
afisha_keyboard = types.InlineKeyboardMarkup()
afisha_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.afisha_btns['BALT'],
        callback_data='cinema_balt',
    ),
    types.InlineKeyboardButton(
        text=msg.afisha_btns['OTRADA'],
        callback_data='cinema_otrada',
    ),
)
afisha_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.afisha_btns['EVENTS'],
        callback_data='mos_afisha',
    ),
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start',
    ),
)


# afisha react
afisha_react_keyboard = types.InlineKeyboardMarkup()
afisha_react_keyboard.row(
    types.InlineKeyboardButton(
        text=msg.TO_MAIN,
        callback_data='start',
    ),
    types.InlineKeyboardButton(
        text=msg.afisha_btns['BACK'],
        callback_data='afisha',
    ),
)


# info react
info_react_keyboard = types.InlineKeyboardMarkup()
info_react_keyboard.row(
    types.InlineKeyboardButton(
        text='На главную',
        callback_data='start',
    ),
    types.InlineKeyboardButton(
        text='Другую инфу',
        callback_data='info',
    ),
)

# weather react
weather_react_keyboard = types.InlineKeyboardMarkup()
weather_react_keyboard.row(
    types.InlineKeyboardButton(
        text='На главную',
        callback_data='start',
    ),
    types.InlineKeyboardButton(
        text='Другой прогноз',
        callback_data='weather',
    ),
)

# picture react
picture_react_keyboard = types.InlineKeyboardMarkup()
picture_react_keyboard.row(
    types.InlineKeyboardButton(
        text='Еще котейку',
        callback_data='cat',
    ),
    types.InlineKeyboardButton(
        text='Собачку',
        callback_data='dog',
    )
),
picture_react_keyboard.row(
    types.InlineKeyboardButton(
        text='На главную',
        callback_data='start',
    )
)

menu_set = {
    'init_cmd': init_cmd_keyboard,
    'start_menu': start_menu_keyboard,
    'pics_menu': picture_keyboard,
    'weather_menu': weather_keyboard,
    'info_menu': info_keyboard,
    'afisha_menu': afisha_keyboard,
}
react_set = {
    'info_react': info_react_keyboard,
    'afisha_react': afisha_react_keyboard,
    'weather_react': weather_react_keyboard,
    'picture_react': picture_react_keyboard,
}
