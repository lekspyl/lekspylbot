import logging
import os
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

updater = Updater(token=os.environ['TG_TOKEN'])
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def calculate_fee(bot, update, args):
    amount = float(' '.join(args))
    result = amount + (amount + amount * 0.0035) * 0.0035
    bot.send_message(chat_id=update.message.chat_id, text=result)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a bot, please talk to me!")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
fee_handler = CommandHandler('fee', calculate_fee, pass_args=True)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(fee_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
