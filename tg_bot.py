from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import sigmalib

tty_port = "/dev/ttyUSB0"

async def gen(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    #check if is a response
    if update.message.reply_to_message:
        #get the text
        text = update.message.reply_to_message.text
        #send the text
        sigmalib.send_line(text, tty_port = "/dev/ttyUSB0")
    else:
        #get the text
        text = update.message.text[4:]
        #send the text
        sigmalib.send_line(text, tty_port = "/dev/ttyUSB0")
    
async def display(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    #check if is a response
    if update.message.reply_to_message is not None:
        #get the text and user
        username = update.message.reply_to_message.from_user.username
        text = "[" + username + "] " + update.message.reply_to_message.text

        #escape < and >
        text = text.replace("<", "\<")

        #send the text
        sigmalib.send_line("<?xml version=\"1.0\"?><composition><left>" + text + "</left></composition>", tty_port = "/dev/ttyUSB0")
    else:
        #error
        await update.message.reply_text("Error, debes responder a un mensaje")


app = Application.builder().token("").build()
app.add_handler(CommandHandler("gen", gen))
app.add_handler(CommandHandler("display", display))
app.run_polling()