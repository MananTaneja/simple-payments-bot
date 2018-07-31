import logging

from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

import bot.strings as s
from bot import db
from config import config

logger = logging.getLogger(__name__)


@run_async
def welcome_user(bot, update):
    logger.info('[%d] welcoming user', update.effective_chat.id)

    db.insert_user(update.effective_user)

    update.message.reply_markdown(s.WELCOME_TEXT.format(name=config.telegram.owner_name), disable_web_page_preview=True)


HANDLERS = (
    CommandHandler(['start', 'help'], welcome_user),
)
