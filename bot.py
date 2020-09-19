import logging
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('token.json') as f:
	TOKEN = json.load(f)["TOKEN"]

class Fbot:

	def __init__(self):
		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

		self.logger = logging.getLogger(__name__)
		self.updater = Updater(TOKEN, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_handler(CommandHandler('start', self.start))
		self.dispatcher.add_handler(CommandHandler('help', self.help))
		self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
		self.dispatcher.add_handler(MessageHandler(Filters.photo, self.photo))
		self.states = {"content_photo" : 0, "style_photo": 0}
		self.updater.start_polling()
		self.updater.idle()

	@staticmethod
	def start(update, context):
		update.message.reply_text('Hi!')

	@staticmethod
	def help(update, context):
		update.message.reply_text('Help message')

	@staticmethod
	def echo(update, context):
		update.message.reply_text(update.message.text)

	@staticmethod
	def photo(update, context):
		user = update.message.from_user
		photo_file = update.message.photo[-1].get_file()
		array = photo_file.download_as_bytearray()
		print(np.array(array)[0])
		self.logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
		update.message.reply_text('got it')
