from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from source.handlers import States, start, apply_issue, write_issue, main_menu, show_issues, issue_sent,\
    issue_not_sent, attach_file
from config.settings import TELEGRAM_BOT_TOKEN


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    back_to_main_menu_handler = MessageHandler(Filters.regex('Back to main menu'), main_menu)

    conversation_menu_handler = ConversationHandler(
        entry_points=[start_handler, back_to_main_menu_handler],
        states={
            States.MAIN_MENU: [MessageHandler(Filters.regex('Create a new issue'), write_issue),
                               MessageHandler(Filters.regex('Show my issues'), show_issues)],
            States.WRITE_ISSUE: [MessageHandler(Filters.regex('Back to main menu'), main_menu),
                                 MessageHandler(Filters.regex('I want to attach a file'), attach_file),
                                 MessageHandler(Filters.text, apply_issue)],
            States.ATTACH_FILE: [MessageHandler(Filters.regex('Back to main menu'), main_menu),
                                 MessageHandler(Filters.regex('I do not want to attach a file'), write_issue),
                                 MessageHandler(Filters.video |
                                                Filters.photo |
                                                Filters.document.video |
                                                Filters.document.image, write_issue)],
            States.APPLY_ISSUE: [MessageHandler(Filters.regex('Yes'), issue_sent),
                                 MessageHandler(Filters.regex('No'), issue_not_sent)],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(conversation_menu_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
