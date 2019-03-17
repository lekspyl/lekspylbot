import logging
import os
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from prometheus_client import start_http_server, Counter

FEE_FUNC_CALLS_TOTAL = Counter('fee_func_calls_total', 'Amount of fee function calls')
UNKNOWN_COMMANDS_TOTAL = Counter('unknown_command_total', 'Unknows commands entered')


updater = Updater(token=os.environ['TG_TOKEN'])
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def calculate_fee(bot, update, args):
    FEE_FUNC_CALLS_TOTAL.inc()
    amount = float(' '.join(args))
    result = round((amount + (amount + amount * 0.0035) * 0.0035), 2)
    bot.send_message(chat_id=update.message.chat_id,
                     text="{0} UAH".format(result))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello.")


def unknown(bot, update):
    UNKNOWN_COMMANDS_TOTAL.inc()
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
fee_handler = CommandHandler('fee', calculate_fee, pass_args=True)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(fee_handler)
dispatcher.add_handler(unknown_handler)

start_http_server(8000)
updater.start_polling()
