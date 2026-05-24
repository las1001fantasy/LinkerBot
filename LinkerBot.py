import re
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# CONFIGURACIÓ INICIAL

import os

BOT_TOKEN = os.getenv("8769269108:AAFxzAEi2qQurtsR_lqzzDAq54qCRCkgBjg")

# ID DEL GRUP
GROUP_ID = -1001497506939

# ID DE LLIGUES
TARGET_THREAD_ID = 42705

# FILTRATGE
FANTASY_PATTERNS = [
    r"www.fleaflicker.com/nfl",
    r"www.fleaflicker.com/mlb",
    r"www.fleaflicker.com/nba",
    r"sleeper.com/i",
]

# LOGS A LA TERMINAL
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# TASCA BOT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.effective_message

    if not message:
        return

    chat_id = update.effective_chat.id
    thread_id = getattr(message, "message_thread_id", None)

    print("CHAT:", chat_id)
    print("THREAD:", thread_id)

    # CONTROL DE GRUP
    if chat_id != GROUP_ID:
        return

    # CONTROL DE TEMA
    if thread_id is not None:
        return

    text = message.text or message.caption or ""

    # DETECTAR
    if not any(re.search(p, text, re.IGNORECASE) for p in FANTASY_PATTERNS):
        return

    try:
        # COPIAR A LLIGUES
        await context.bot.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.message_id,
            message_thread_id=TARGET_THREAD_ID,
        )

        # ESBORRAR ORIGINAL
        await context.bot.delete_message(
            chat_id=GROUP_ID,
            message_id=message.message_id,
        )

        # AVIS ALS MANAGERS
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text="⚠️ Recuerda: @chuck_villa es imbécil integral y los enlaces de ligas fantasy deben publicarse en el topic 'Ligas', no en General, ¡gracias!"
     )
        print("Missatge mogut a lligues")

    except Exception as e:
        print("ERROR:", e)


# ARRANCADA BOT

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.ALL, handle_message)
    )

    print("BOT FUNCIONANT...")

    app.run_polling()

# START

if __name__ == "__main__":
    main()