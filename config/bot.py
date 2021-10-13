import telebot
from config.db import config

config.read('konfig.ini')

TOKEN = config.get('BotKu', 'API_TELEGRAM')
bot = telebot.TeleBot(config.get('BotKu', 'API_TELEGRAM'))