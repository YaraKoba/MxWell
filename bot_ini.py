import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
remove_buttons = types.ReplyKeyboardRemove()
