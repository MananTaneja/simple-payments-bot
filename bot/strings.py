WELCOME_TEXT = """Hello there,

with this bot you can send money to {name}. You just have to write the amount of money you want to pay!

> [info about bots payments](https://core.telegram.org/bots/payments#introducing-payments)
> [info about the service that will handle the transaction](https://stripe.com)"""

PAYMENT_DESCRIPTION = """In order to pay, you need a pre-paid/debt card

Neither Telegram nor the bot (or its owner) have access to your payments info"""

INVALID_INPUT = """*Invalid input*
Send me the price you want to pay in one of the following formats:
*>* `1,34`
*>* `12`
*>* `15.45`"""

INVALID_AMOUNT = """*Invalid amount*
Min amount: 0,82 €
Max amount: 8123,04 €"""

INVOICE_TITLE = "Send {amount} € to {name}"

PRICE_LABEL = "money transfer"

INVOICE_ERROR = "I'm sorry, something went wrong during the invoice delivery (`{error_string}`)"

SUCCESSFULL_PAYMENT = "Payment of {amount} € completed sucessfully, thanks a lot!"
