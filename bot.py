import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# ----------------------------
# PASTE YOUR BOT TOKEN AND CHANNEL ID HERE
BOT_TOKEN = "8475795056:AAE0EdaDnk8aD8lx71z4yAnggri7Bz1jC3U"
CHANNEL_ID = "@TechnophileMrJeph"  # Use channel username with @ or channel ID as integer
# ----------------------------

def get_link_image(url):
    """
    Get og:image from a webpage if exists
    """
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
    """
    Handle messages: if message contains a link, try to fetch og:image and send it
    """
    text = update.message.text
    if text and "http" in text:  # detect link
        for word in text.split():
            if word.startswith("http"):
                img = get_link_image(word)
                if img:
                    caption = text
                    try:
                        context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption)
                        update.message.delete()  # delete original message
                    except Exception as e:
                        print(f"Error sending photo: {e}")
                        context.bot.send_message(chat_id=CHANNEL_ID, text=text)
                else:
                    # No image found, send text only
                    context.bot.send_message(chat_id=CHANNEL_ID, text=text)
                break

def main():
    """
    Start the bot
    """
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
