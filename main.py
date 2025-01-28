import plistlib
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from funct import parse_plist, handle_response

TOKEN: Final = "YOUR_TOKEN"
BOT_USERNAME: Final = "@YOUR_BOT_USERNAME"


    
# HELP TEXT / DOCUMENTATION:
help_text = """Hi, I'm HakckintoshBot, my purpose is to help you with your hackintosh journey with some easy commands. Every type of command with more than one option has a special help session, so to get help on '/link', you will need to type '/link help'. These are the commands you can use to interact with me:
	/link (name of product)
	/creator
	/plist

/link: Gives out the link of a product/package/software
/creator: Gives credit to developer
/plist: When in response of a config.plist file, it allows to have an overview of its elements without having to do absolutely nothing.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text("Hello, International Hackintosh bot here! ")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(help_text)
	await update.message.reply_text("Please send any further help request to @Helemen7")
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await handle_response(update, context)

if __name__ == "__main__":
	print("[DEBUG]: Starting...")
	app = Application.builder().token(TOKEN).build()
	app.add_handler(CommandHandler("start", start))
	app.add_handler(CommandHandler("help", help))
	app.add_handler(CommandHandler("plist", parse_plist))
	app.add_handler(MessageHandler(filters.COMMAND, commands))
	print("[DEBUG]: Polling...")
	app.run_polling(poll_interval=3)
