from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from .messages import Messages
from .keyboards import MAIN_MENU_KEYBOARD, BACK_TO_MAIN_MENU_KEYBOARD, YES_NO_KEYBOARD
from .services import create_new_user, create_ticket, get_tickets


class States:
    MAIN_MENU = 'Main menu'
    BACK_TO_MAIN_MENU = 'Back to main menu'
    WRITE_ISSUE = 'Create a new issue'
    APPLY_ISSUE = 'Apply issue'


def start(update: Update, context: CallbackContext):
    update.message.reply_html(Messages.START, reply_markup=MAIN_MENU_KEYBOARD)
    create_new_user(update.effective_user.username, update.effective_user.id)
    return States.MAIN_MENU


def write_issue(update: Update, context: CallbackContext):
    update.message.reply_html(Messages.WRITE_COMPLAINT, reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
    return States.WRITE_ISSUE


def apply_issue(update: Update, context: CallbackContext):
    context.user_data['user_issue'] = update.message.text  # saving the value that user wrote in previous message
    update.message.reply_html(Messages.APPLY_COMPLAINT.format(update.message.text), reply_markup=YES_NO_KEYBOARD)
    return States.APPLY_ISSUE


def issue_sent(update: Update, context: CallbackContext):
    if 'user_issue' in context.user_data:
        create_ticket(
            update.effective_user.username,
            update.effective_user.id,
            context.user_data['user_issue'],
        )
    update.message.reply_html('Your issue was successfully sent.', reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
    return ConversationHandler.END


def issue_not_sent(update: Update, context: CallbackContext):
    update.message.reply_html('You\'ve cancelled sending an issue.', reply_markup=BACK_TO_MAIN_MENU_KEYBOARD)
    return ConversationHandler.END


def show_issues(update: Update, context: CallbackContext):
    content = get_tickets(update.effective_user.id)
    update.message.reply_html(Messages.MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)
    return States.MAIN_MENU


def main_menu(update: Update, context: CallbackContext):
    update.message.reply_html(Messages.MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)
    return States.MAIN_MENU
