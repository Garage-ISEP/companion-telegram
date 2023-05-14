import os
import openai
import logging
from flask import Flask, request

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler, Dispatcher, Updater

load_dotenv()


app = Flask(__name__)


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your Telegram bot token
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")





def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("📚 Labs", callback_data="labs"),
            InlineKeyboardButton("🛠️ Projects", url="https://garageisep.notion.site/1ed2ab87215348009f4bf7bd59db1bd7"),


        ],
        [
            InlineKeyboardButton("📩 Contact", callback_data="contact"),
            InlineKeyboardButton("🤝 Join",
                                 url="https://docs.google.com/forms/d/e/1FAIpQLSfDbNnXzS5LsS7_mFqPnrLvL8GM6aCIVGurFac5RK_1r3Mqpw/viewform"),
        ],
        [
            InlineKeyboardButton("💬 Garage GPT", callback_data="garage_gpt"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Bonjour je suis Garage Companion, que souhaites tu faire ?", reply_markup=reply_markup)



def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "garage_gpt":
        query.edit_message_text("Bonjour je suis Garage GPT ! Comment puis-je t'aider aujourd'hui ?")
    elif query.data == "labs":
        labs_keyboard = [
            [
                InlineKeyboardButton("🕶️ Meta Lab",
                                     url="https://www.notion.so/VR-AR-Metaverse-Lab-6840f36ee0ff4849b371fd659ba4bf64"),
                InlineKeyboardButton("🧠 IA Lab", url="https://www.notion.so/IA-Lab-82d18f66b5214389b954f50abc316e30"),

            ],
            [
                InlineKeyboardButton("🛡️ Cyber Lab",
                                     url="https://www.notion.so/Cyber-Lab-74ea963739584267a09432348acc9fcd"),
                InlineKeyboardButton("⛓️ Blockchain Lab",
                                     url="https://www.notion.so/Blockchain-Lab-8d9128d5c13f4a449a12061669443dfc"),
            ],
            [
                InlineKeyboardButton("💻 Coder Lab",
                                     url="https://www.notion.so/Coder-Lab-059bdcca13db4e529d5b6c884ae9968e"),
                InlineKeyboardButton("🔧 Maker Lab",
                                     url="https://www.notion.so/Maker-Lab-9ec19272af7c4c0387fe1a571ad71f6a"),
            ],
        ]

        labs_markup = InlineKeyboardMarkup(labs_keyboard)
        query.edit_message_text("Choose a lab to explore:", reply_markup=labs_markup)
    elif query.data == "contact":
        query.edit_message_text("To contact us, please send an email to: [Bureau@garageisep.com ](mailto:Bureau@garageisep.com )", parse_mode="Markdown")



def handle_message(update: Update, context: CallbackContext):
    message = update.message.text
    gpt_response = generate_gpt_response(message)
    update.message.reply_text(gpt_response)

def generate_gpt_response(message):
    prompt = (
        "Garage ISEP is the student innovation hub at ISEP, dedicated to fostering innovation and new technologies among its members. "
        "Established in 2017, our mission is to bring students together around emerging technologies and empower them to take an active role in their own learning. "
        "Our members are organized into specialized labs where they work on innovative projects, organize conferences and workshops, and participate in hackathons. "
        "Our labs include the Artificial Intelligence Lab (IA Lab), Blockchain Lab (Blockchain Lab), Virtual and Augmented Reality and Metaverse Lab (Meta Lab), "
        "Programming Lab (Coder Lab), Cybersecurity Lab (Cyber Lab), and Electronics, Drones, and Robotics Lab (Maker Lab). "
        f"Please answer the following user's question in French: {message}\n\nAnswer: "
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def main():
    updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(handle_button_click))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

