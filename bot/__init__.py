from telegram.ext import Updater

from config import config
from .database import Database

updater = Updater(token=config.telegram.token)
jobs = updater.job_queue
dispatcher = updater.dispatcher

db = Database(config.sqlite.filename)
