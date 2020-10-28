from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler,\
    CallbackQueryHandler

from source.handlers import States, start, main_menu, issue_sent, add_ticket, issue_not_sent, show_tickets,\
    wait_for_ticket_message
from config.settings import TELEGRAM_BOT_TOKEN


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    conversation_menu_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            States.MAIN_MENU: [
                CommandHandler('add_ticket', add_ticket),
                CommandHandler('show_tickets', show_tickets),
                CallbackQueryHandler(add_ticket, pattern='^add_ticket$'),
                CallbackQueryHandler(show_tickets, pattern='^show_tickets$'),
                MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document, wait_for_ticket_message)
            ],
            States.APPLY_TICKET: [
                CallbackQueryHandler(main_menu, pattern='^menu$'),
                CallbackQueryHandler(issue_sent, pattern='^yes$'),
                CallbackQueryHandler(issue_not_sent, pattern='^no$')
            ],
            States.ADD_TICKET: [
                CommandHandler('add_ticket', add_ticket),
                CommandHandler('show_tickets', show_tickets),
                CallbackQueryHandler(main_menu, pattern='^menu$'),
                MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document, wait_for_ticket_message)
            ],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(conversation_menu_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
