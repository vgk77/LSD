from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton(text='Create a new issue'), KeyboardButton('Show my issues')]
], resize_keyboard=True)


BACK_TO_MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton('Back to main menu')]
], resize_keyboard=True)


YES_NO_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton('Yes'), KeyboardButton('No')]
], resize_keyboard=True)
