import argparse
import datetime
import importlib
import logging
import logging.config
import os

from telegram.ext.dispatcher import run_async
from yaml import safe_load

from bot import updater, dispatcher, jobs
from config import config


parser = argparse.ArgumentParser()


def load_logging_config(file_path='logging.yaml'):
    with open(file_path, 'rt') as f:
        logging_config = safe_load(f.read())
        logging_config['handlers']['file']['filename'] = config.log.filename
    logging.config.dictConfig(logging_config)


logger = logging.getLogger(__name__)
load_logging_config()


@run_async
def error_callback(bot, update, error):
    logger.info('Update: %s\nerror: %s', update, error, exc_info=True)


def main(args):
    if args.test:
        config.stripe.selected = config.stripe.test
        logger.info('Stripe payments token: TEST %s%s', config.stripe.test[:9], '*' * len(config.stripe.test[11:]))
    else:
        config.stripe.selected = config.stripe.live
        logger.info('Stripe payments token: LIVE %s%s', config.stripe.live[:9], '*' * len(config.stripe.live[11:]))

    for modname in [f.rstrip('.py') for f in os.listdir('bot/handlers') if f.endswith('.py')]:
        handlers = getattr(importlib.import_module('bot.handlers.{}'.format(modname)), 'HANDLERS')
        logger.info('Importing module: %s (handlers: %d)', modname, len(handlers))
        for handler in handlers:
            dispatcher.add_handler(handler)

    dispatcher.add_error_handler(error_callback)

    callbacks = getattr(importlib.import_module('bot.schedules.schedules'), 'SCHEDULES')
    logger.info('Importing schedules (%d callbacks)', len(callbacks))
    for cb in callbacks:
        jobs.run_daily(cb, time=datetime.time(hour=4, minute=00))

    try:
        # try to notify the owner
        updater.bot.send_message(config.telegram.owner_id,
                                '#paymentsbot_running ({})'.format('TEST token' if args.test else 'LIVE token'))
    except:
        pass
    
    logger.info('starting polling loop...')
    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    parser.add_argument('-t', '--test', action='store_true', help="Use Stripe's TEST token instead of the LIVE one")
    args = parser.parse_args()

    main(args)
