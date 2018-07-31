### Simple payments bot

This bot is a simple working implementation of the payments methods of [Telegram's bot API](https://core.telegram.org/bots), and allows users to send you money.

It uses [Stripe](https://stripe.com/) as payment provider and requires minimal setup.

### Running the bot

1. install the requirements with `pip install -r requirements.txt`
2. rename `config.example.ini` to `config.ini`, open it, and edit the following sections of the file:
  - `[telegram]`:
    - `token`: bot token (get it from [@botfather](https://t.me/botfather))
    - `owner_id`: your Telegram user id
    - `owner_name`: your name (will be included in some messages)
  - `[stripe]` (please follow [these](https://core.telegram.org/bots/payments#getting-a-token) instructions to get your Stripe tokens):
    - `live`: your LIVE Stripe token
    - `test`: your TEST Stripe token
  - `[general]` (optional):
    - `currency`: currency to use (full list [here](https://core.telegram.org/bots/payments#supported-currencies)), change it if not `EUR`
    - `sourcecode`: sourcecode link
  - `[sqlite]` (optional):
    - `filename`: name of the sqlite database
  - `[log]` (optional):
    - `filename`: name of the log file

Now the bot can be started: `python3 main.py`. To use Stripe's TEST token, run it with the `-t` flag: `python3 main.py -t`

### Bot replies

All the strings used by the bot are placed under `bot/strings.py`, you can edit them from this file.

### Restarting the bot

You can restart the bot directly from Telegram with `/restart`. Restarting it with `/restart -t` will force it to use Stripe's TEST token

### Receiving your money

Stripe will transfer received money in your bank account every few days, and [charges a small commission](https://stripe.com/pricing)