from telegram import Update
from telegram.ext import CallbackContext

from .messages import Messages
from .keyboards import MENU_INLINE_KEYBOARD, YES_NO_INLINE_KEYBOARD, BACK_TO_MENU_INLINE_KEYBOARD,\
    get_keyboard_from_tickets
from .services import create_new_user, create_ticket, get_tickets, get_ticket_by_number,\
    get_beautiful_time


class States:
    MAIN_MENU = 'Main menu'
    APPLY_TICKET = 'Apply ticket'
    ADD_TICKET = 'Add ticket'
    SHOW_TICKETS = 'Show tickets'


def start(update: Update, context: CallbackContext):
    update.message.reply_html(Messages.START)
    create_new_user(update.effective_user.username, update.effective_user.id)
    context.bot.send_message(update.effective_chat.id, text=Messages.MAIN_MENU, parse_mode='HTML',
                             reply_markup=MENU_INLINE_KEYBOARD)
    return States.MAIN_MENU


def add_ticket(update: Update, context: CallbackContext):
    context.bot.send_message(update.effective_chat.id, text=Messages.WRITE_COMPLAINT, parse_mode='HTML',
                             reply_markup=BACK_TO_MENU_INLINE_KEYBOARD)
    return States.ADD_TICKET


def show_tickets(update: Update, context: CallbackContext):
    content = get_tickets(update.effective_user.id)
    keyboard = get_keyboard_from_tickets(content)
    keyboard.inline_keyboard.append(BACK_TO_MENU_INLINE_KEYBOARD.inline_keyboard[0])
    context.bot.send_message(update.effective_chat.id, text=Messages.SHOW_TICKETS, parse_mode='HTML',
                             reply_markup=keyboard)
    return States.SHOW_TICKETS


def show_chosen_ticket(update: Update, context: CallbackContext):
    data = update.callback_query.data
    ticket_id = data.split('#')[1]
    ticket = get_ticket_by_number(ticket_id)
    text = F' <b>{ticket["topic"]}</b>\n' \
           F'{ticket["message"]}\n\n' \
           F'Status: {ticket["status"]}\n' \
           F'Date of creation: {get_beautiful_time(ticket["created_at"])}'
    context.bot.send_message(update.effective_chat.id, text=text, parse_mode='HTML',
                             reply_markup=BACK_TO_MENU_INLINE_KEYBOARD)
    return States.SHOW_TICKETS


def wait_for_ticket_message(update: Update, context: CallbackContext):
    context.user_data['user_issue'] = update.message.text
    if 'photo' in update.message.to_dict() and update.message.to_dict()['photo']:
        context.user_data['file_path'] = context.bot.get_file(update.message.photo[::-1][0]['file_id'])['file_path']
    elif 'document' in update.message.to_dict():
        context.user_data['file_path'] = context.bot.get_file(update.message.document['file_id'])['file_path']
    elif 'video' in update.message.to_dict():
        context.user_data['file_path'] = context.bot.get_file(update.message.video['file_id'])['file_path']
    if 'file_path' in context.user_data:
        context.bot.send_message(update.effective_chat.id,
                                 text='<i>Your file is in memory of the bot, it will be sent with your message</i>',
                                 parse_mode='HTML')
        context.user_data['user_issue'] = update.message.caption
    context.bot.send_message(update.effective_chat.id,
                             Messages.APPLY_COMPLAINT.format(context.user_data['user_issue']), parse_mode='HTML',
                             reply_markup=YES_NO_INLINE_KEYBOARD)
    return States.APPLY_TICKET


def issue_sent(update: Update, context: CallbackContext):
    attachment = None
    if 'file_path' in context.user_data:
        attachment = context.user_data['file_path']
    if 'user_issue' in context.user_data:
        create_ticket(
            update.effective_user.username,
            update.effective_user.id,
            context.user_data['user_issue'],
            attachment=attachment,
        )
    context.user_data.clear()
    context.bot.send_message(update.effective_chat.id, text='Your issue was successfully sent.', parse_mode='HTML')
    context.bot.send_message(update.effective_chat.id, text=Messages.MAIN_MENU, parse_mode='HTML',
                             reply_markup=MENU_INLINE_KEYBOARD)
    return States.MAIN_MENU


def issue_not_sent(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.bot.send_message(update.effective_chat.id, text='You\'ve cancelled sending an issue.', parse_mode='HTML')
    context.bot.send_message(update.effective_chat.id, text=Messages.MAIN_MENU, parse_mode='HTML',
                             reply_markup=MENU_INLINE_KEYBOARD)
    return States.MAIN_MENU


def main_menu(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.bot.send_message(update.effective_chat.id, text=Messages.MAIN_MENU, parse_mode='HTML',
                             reply_markup=MENU_INLINE_KEYBOARD)
    return States.MAIN_MENU
