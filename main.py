import logging
import re

from amazonify import amazonify
from telegram import Update
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

REGEX_KEY = r'(?:http://|https://| )(?:amazon\.it|amzn\.to)(?:[a-zA-Z0-9./:?=\-]*)'
TELEGRAM_TOKEN = "YOUR KEY"
AMAZON_AFFILIATE_TAG = "acuf59280d-21"


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.username

    try:
        reply = update.message.reply_to_message.message_id
    except:
        reply = None

    chat_id = update.message.chat_id

    message = update.message.text
    old_links = re.findall(REGEX_KEY, message, flags=re.IGNORECASE)
    new_links = [amazonify(u, AMAZON_AFFILIATE_TAG) for u in old_links]

    string_index = 0
    for index in range(0, len(old_links)):
        message = message[:string_index] + message[string_index:].replace(old_links[index], " " + new_links[index], 1)
        string_index = message[string_index:].index(new_links[index]) + len(new_links[index])

    if reply is None:
        context.bot.send_message(chat_id=chat_id, text="Inviato originariamente da: @" + str(user) + "\n\n" + str(message))
    else:
        context.bot.send_message(chat_id=chat_id, reply_to_message_id=reply, text="Inviato originariamente da: @" + str(user) + "\n\n" + str(message))

    update.message.delete()

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(re.compile(REGEX_KEY, re.IGNORECASE)), start)],
        states={},
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
