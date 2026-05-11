import os
import telebot
import google.generativeai as genai
from PIL import Image
import io

# Эти строки сами заберут ключи из настроек Render
CHROME_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# Проверка, что ключи вообще есть
if not CHROME_TOKEN or not GOOGLE_API_KEY:
    print("ОШИБКА: Токены не найдены в Environment Variables!")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    bot = telebot.TeleBot(CHROME_TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Денчик, AscendLab в строю! Кидай фотку, гляну, что там по лукмаксу.")

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        try:
            bot.reply_to(message, "Так, смотрю... Секунду.")
            
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            image = Image.open(io.BytesIO(downloaded_file))
            
            prompt = "Ты эксперт по мужской эстетике и лукмаксингу. Проанализируй фото: оцени линию челюсти, симметрию, наклон глаз и кожу. Дай конкретные советы, что улучшить (softmaxxing)."
            
            response = model.generate_content([prompt, image])
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, f"Блин, ошибка: {str(e)}")

    if __name__ == "__main__":
        print("Бот запущен и готов к работе!")
        bot.infinity_polling()
