import logging
from datetime import datetime

import simplesqlitewrap as ssw

from bot import sql
from config import config

logger = logging.getLogger(__name__)


class Database(ssw.Database):
    def __init__(self, filename):
        logger.info('initing Database module')

        ssw.Database.__init__(self, filename)

        self._init_db()

    def _init_db(self):
        logger.info('creating tables')

        self._execute(sql.CREATE_TABLE_USERS)
        self._execute(sql.CREATE_TABLE_PAYMENTS)

    def insert_user(self, user):
        logger.info('adding user %d (%s)', user.id, user.first_name)

        return self._execute(sql.INSERT_OR_REPLACE_USER, (
            user.id,
            user.username,
            user.first_name,
            user.last_name
        ), rowcount=True)

    def insert_invoice(self, unique_id, user_id, price, invoice_date=datetime.now()):
        logger.info('inserting invoice: %s', unique_id)

        # test if we're using the test token for this invoice:
        is_test = True if config.stripe.selected == config.stripe.test else False
        return self._execute(sql.INSERT_PAYMENT_INVOICE, (unique_id, user_id, price, invoice_date, is_test),
                             rowcount=True)

    def update_payment_successfull(self, unique_id, telegram_payment_id,
                                   provider_payment_id, successful_payment_date=datetime.now()):
        logger.info('update payment successfull: %s', unique_id)

        self._execute(sql.UPDATE_PAYMENT_SUCCESSFULL, (telegram_payment_id, provider_payment_id,
                                                       successful_payment_date, unique_id), rowcount=True)

    def get_tables(self):
        logger.info("getting db tables")

        return self._execute(sql.SELECT_TABLES, fetchall=True, as_dict=True)
