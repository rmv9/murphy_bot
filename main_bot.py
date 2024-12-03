"""test mode."""
import sys

import core.functions as func
import core.logging as log
import core.permissions as perm
import helpers.messages as msg

weather_list = ['today', 'tomorrow']
pic_list = ['cat', 'dog']
info_list = ['functions', 'params', 'author']
afisha_list = ['mos_afisha', 'cinema_balt', 'cinema_otrada']


def check_tokens():
    """pass."""
    log.logging.info(msg.sys_info['CHECKING_TOKENS'])
    if perm.check_tokens():
        log.logging.critical(
            f'Corrupted tokens: {perm.check_tokens()}'
        )
        sys.exit()
    log.logging.info(msg.sys_info['END_CHECK'])


def main():
    """pass."""
    check_tokens()
    # func.direct_initializator(CHAT_ID_***)

    func.bot_v1.message_handler(commands=['start'])(func.init_cmd)
    func.bot_v1.callback_query_handler(
        lambda call: call.data == 'start')(func.start.menu)
    func.bot_v1.callback_query_handler(
        lambda call: call.data == 'pictures')(func.pics.menu)
    func.bot_v1.callback_query_handler(
        lambda call: call.data == 'afisha')(func.afisha.menu)
    func.bot_v1.callback_query_handler(
        lambda call: call.data == 'weather')(func.weather.menu)
    func.bot_v1.callback_query_handler(
        lambda call: call.data == 'info')(func.info.menu)
    func.bot_v1.callback_query_handler(
        lambda call: call.data in weather_list)(func.weather_react)
    func.bot_v1.callback_query_handler(
        lambda call: call.data in pic_list)(func.picture_react)
    func.bot_v1.callback_query_handler(
        lambda call: call.data in info_list)(func.info_react)
    func.bot_v1.callback_query_handler(
        lambda call: call.data in afisha_list)(func.afisha_react)


if __name__ == '__main__':
    main()
    func.bot_v1.polling()
