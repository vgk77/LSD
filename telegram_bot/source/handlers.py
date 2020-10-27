from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from .messages import Messages
from .keyboards import MAIN_MENU_KEYBOARD, BACK_TO_MAIN_MENU_KEYBOARD, YES_NO_KEYBOARD
from .services import create_new_user, create_ticket, get_tickets, is_message_valid


class States:
    MAIN_MENU = 'Main menu'
    BACK_TO_MAIN_MENU = 'Back to main menu'
    WRITE_ISSUE = 'Create a new issue'
    APPLY_ISSUE = 'Apply issue'
    ATTACH_FILE = 'Attach file'


def start(update: Update, context: CallbackContext):
    update.message.reply_html(Messages.START, reply_markup=MAIN_MENU_KEYBOARD)
    create_new_user(update.effective_user.username, update.effective_user.id)
    return States.MAIN_MENU


def write_issue(update: Update, context: CallbackContext):
    if 'photo' in update.message.to_dict() and update.message.to_dict()['photo']:
        context.user_data['file_path'] = context.bot.get_file(update.message.photo[::-1][0]['file_id'])['file_path']
    elif 'document' in update.message.to_dict():
        context.user_data['file_path'] = context.bot.get_file(update.message.document['file_id'])['file_path']
    elif 'video' in update.message.to_dict():
        context.user_data['file_path'] = context.bot.get_file(update.message.video['file_id'])['file_path']
    if 'file_path' in context.user_data:
        update.message.reply_html('<i>Your file is in memory of the bot, it will be sent with your message</i>')
    markup = ReplyKeyboardMarkup([[KeyboardButton('Back to main menu'), KeyboardButton('I want to attach a file')]],
                                 resize_keyboard=True)
    update.message.reply_html(Messages.WRITE_COMPLAINT, reply_markup=markup)
    return States.WRITE_ISSUE


def apply_issue(update: Update, context: CallbackContext):
    if not is_message_valid(update.message.text):
        update.message.reply_html('Your message is not in a valid format.', reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
        return States.WRITE_ISSUE
    context.user_data['user_issue'] = update.message.text  # saving the value that user wrote in previous message
    update.message.reply_html(Messages.APPLY_COMPLAINT.format(update.message.text), reply_markup=YES_NO_KEYBOARD)
    return States.APPLY_ISSUE


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
    update.message.reply_html('Your issue was successfully sent.', reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
    return ConversationHandler.END


def issue_not_sent(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_html('You\'ve cancelled sending an issue.', reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
    return ConversationHandler.END


def show_issues(update: Update, context: CallbackContext):
    content = get_tickets(update.effective_user.id)
    for ticket in content:
        update.message.reply_html(Messages.get_message_from_tickets_info(**ticket))
    update.message.reply_html(Messages.MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)
    return States.MAIN_MENU


def main_menu(update: Update, context: CallbackContext):
    context.user_data.clear()
    update.message.reply_html(Messages.MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)
    return States.MAIN_MENU


def attach_file(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup([[KeyboardButton('Back to main menu'),
                                   KeyboardButton('I do not want to attach a file')]], resize_keyboard=True)
    update.message.reply_html('Now you can send a file.', reply_markup=markup)
    return States.ATTACH_FILE
