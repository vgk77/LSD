from telegram import InlineKeyboardButton, InlineKeyboardMarkup


MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Add new ticket', callback_data='add_ticket'),
     InlineKeyboardButton('Show my tickets', callback_data='show_tickets')]
])


YES_NO_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Yes', callback_data='yes'), InlineKeyboardButton('No', callback_data='no')],
    [InlineKeyboardButton('Back to main menu', callback_data='menu')]
])


BACK_TO_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Back to main menu', callback_data='menu')]
])


def get_keyboard_from_tickets(tickets):
    keyboard = []
    for ticket in tickets:
        keyboard.append([InlineKeyboardButton(ticket['topic'], callback_data=f'ticket#{ticket["number"]}')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup
