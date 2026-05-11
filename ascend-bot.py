import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

# Твои ключи
TELEGRAM_TOKEN = '8374574297:AAHBE4MvKwRqkkDwITgG84XG1N8xj1nkqVM'
GEMINI_KEY = 'AIzaSyB_xif6893H-KbYQq7e1XJM1wcSbDQcAfI'

genai.configure(api_key=GEMINI_KEY)
# Вместо старой строки с моделью вставь это:
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
)

# Увеличиваем таймаут, чтобы "семафор" не вылетал
bot = Bot(token=TELEGRAM_TOKEN, timeout=60)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🦾 AscendLab в строю! Кидай селфи, Денчик.")

@dp.message_handler(content_types=['photo'])
async def handle_analysis(message: types.Message):
    status = await message.answer("🧪 Анализирую...")
    photo = message.photo[-1]
    path = f"scan_{message.from_user.id}.jpg"
    await photo.download(destination_file=path)
    
    try:
        with open(path, 'rb') as f:
            img_data = f.read()
        
        prompt = "Ты эксперт по мужской эстетике. Проанализируй лицо на фото. Оцени глаза, челюсть, кожу и волосы. Дай советы по улучшению. Будь краток."
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
        
        await message.answer(f"📋 **ОТЧЕТ:**\n\n{response.text}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        if os.path.exists(path): os.remove(path)

if __name__ == '__main__':
    print("ЗАПУСКАЮ БОТА...")
    executor.start_polling(dp, skip_updates=True)
