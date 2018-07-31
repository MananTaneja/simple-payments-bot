from config import config


def backup_db_callback(bot, job):

    with open(config.sqlite.filename, 'rb') as f:
        bot.send_document(config.telegram.owner_id, f, caption='#paymentsbot_db')


SCHEDULES = (  # will run daily at 4 AM
    # backup_db_callback,
)
