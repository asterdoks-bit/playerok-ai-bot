import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.reply_to(message, "⏳ Сүрөттөр иштетилип жатат...")

    prompt = """
Сен Playerok үчүн сатуучу жардамчысың.

Колдонуучу жиберген сүрөттөрдүн негизинде:
1. Кооз жана сатылуучу аталыш жаз.
2. Толук сүрөттөмө жаз.
3. Эмодзилерди колдон.
4. Текст орус тилинде болсун.
"""

    photos = []

    for p in message.photo:
        file_info = bot.get_file(p.file_id)
        downloaded = bot.download_file(file_info.file_path)
        photos.append({
            "mime_type": "image/jpeg",
            "data": downloaded
        })

    response = model.generate_content([prompt] + photos)

    bot.send_message(message.chat.id, response.text)

bot.infinity_polling()
