import logging
import re

from telegram import LabeledPrice
from telegram.error import BadRequest
from telegram.ext import Filters
from telegram.ext import MessageHandler
# from telegram.ext.dispatcher import run_async

from config import config
from bot import db
import bot.strings as s

logger = logging.getLogger(__name__)

payment_amount_regex = re.compile(r'(\d+(?:[.,]\d{1,2})?)', re.IGNORECASE)


# @run_async
def on_text_message(bot, update):
    chat_id = update.message.chat_id
    logger.info('[%d] new message', chat_id)

    match = payment_amount_regex.search(update.message.text)
    if not match:
        logger.info('[%d] payment amount: no match', chat_id)
        update.message.reply_markdown(s.INVALID_INPUT)
    else:
        price_string = match.group(1).replace(',', '.')
        price = int(float(price_string) * 100)  # must be an integer of cents
        logger.info('[%d] payment amount: %d', chat_id, price)

        if price <= 81 or price >= 812304:
            logger.info('[%d] invalid payment amount: %d', chat_id, price)
            update.message.reply_markdown(s.INVALID_AMOUNT)
        else:
            invoice_title = s.INVOICE_TITLE.format(amount=price_string, name=config.telegram.owner_name)

            # unique payload to recognize the invoice
            payload = '{}_{}'.format(chat_id, update.message.message_id)
            provider_token = config.stripe.selected

            prices = [LabeledPrice(s.PRICE_LABEL, price)]

            try:
                sent_invoice_message = bot.send_invoice(
                    chat_id=chat_id,
                    title=invoice_title,
                    description=s.PAYMENT_DESCRIPTION,
                    payload=payload,
                    provider_token=provider_token,
                    start_parameter=payload,
                    currency=config.general.currency,
                    prices=prices
                )
            except BadRequest as e:
                error_string = str(e)
                logger.info('[%d] sendInvoice exception: %s', chat_id, error_string, exc_info=True)
                update.message.reply_markdown(s.INVOICE_ERROR.format(error_string=error_string))
                return

            # on sendInvoice success: insert in db
            db.insert_invoice(
                unique_id=payload,
                user_id=update.effective_user.id,
                price=price,
                invoice_date=sent_invoice_message.date
            )


# @run_async
def successful_payment_callback(bot, update):
    chat_id = update.message.chat_id
    logger.info('[%d] successful payment', chat_id)

    # https://core.telegram.org/bots/api#successfulpayment
    amount = update.message.successful_payment.total_amount
    invoice_payload = update.message.successful_payment.invoice_payload
    telegram_payment_charge_id = update.message.successful_payment.telegram_payment_charge_id
    provider_payment_charge_id = update.message.successful_payment.provider_payment_charge_id

    db.update_payment_successfull(
        unique_id=invoice_payload,
        telegram_payment_charge_id=telegram_payment_charge_id,
        provider_payment_charge_id=provider_payment_charge_id,
        successful_payment_date=update.message.date
    )

    bot.send_message(chat_id, s.SUCCESSFULL_PAYMENT.format(amount=amount / 100))


HANDLERS = (
    MessageHandler(Filters.text, on_text_message),
    MessageHandler(Filters.successful_payment, successful_payment_callback)
)
