import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# ----------------------------
# New Bot Token
BOT_TOKEN = "7760499282:AAE3SSZBfrc87dDsP05wq202HqEoBOOft2U"
CHANNEL_ID = "@TechnophileMrJeph"  # Your channel username
# ----------------------------

def get_link_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        return og_image["content"] if og_image else None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text and "http" in text:
        for word in text.split():
            if word.startswith("http"):
                img = get_link_image(word)
                if img:
                    try:
                        context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=text)
                    except Exception as e:
                        print(f"Error sending photo: {e}")
                        context.bot.send_message(chat_id=CHANNEL_ID, text=text)
                else:
                    context.bot.send_message(chat_id=CHANNEL_ID, text=text)
                break

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
