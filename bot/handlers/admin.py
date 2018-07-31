import logging
import os
import sys
from functools import wraps

from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from config import config

logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != int(config.telegram.owner_id):
            logger.warning('unauthorized access denied: %d', user_id)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


@restricted
@run_async
def restart_bot(bot, update, args):
    logger.info('restarting bot...')
    update.message.reply_text('restarting {}'.format(*args if len(args) > 0 else '(no args)'))

    # updater.stop()  # this will just make the script hang
    script_args = [sys.argv[0]]  # keep just the first element of sys.argv
    script_args.extend(args)
    os.execl(sys.executable, sys.executable, *script_args)


@restricted
@run_async
def send_db(bot, update):
    logger.info('sending db file')

    with open(config.sqlite.filename, 'rb') as f:
        update.message.reply_document(f)


@restricted
@run_async
def send_log(bot, update):
    logger.info('sending log file')

    with open(config.log.filename, 'rb') as f:
        update.message.reply_document(f)


HANDLERS = (
    CommandHandler('restart', restart_bot, pass_args=True),
    CommandHandler('db', send_db),
    CommandHandler('log', send_log)
)
