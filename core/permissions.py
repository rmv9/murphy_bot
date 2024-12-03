"""Access and tokens."""
import os

import dotenv
from dotenv import load_dotenv

dotenv_path = dotenv.find_dotenv()
load_dotenv(dotenv_path, override=True)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID_MAX = os.getenv('CHAT_ID_MAX')


def check_tokens() -> None | list:
    """Check that all necessary envs are present."""
    tokens = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'CHAT_ID_MAX': CHAT_ID_MAX,
    }

    report_list = []

    for name, token in tokens.items():
        if not token:
            report_list.append(name)
    if report_list:
        return report_list
