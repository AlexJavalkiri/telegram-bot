# Импортируем нужные модули
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters
import random, os

# Читаем токен из переменной окружения Render
TOKEN = os.getenv("TOKEN")
# Матерные фразы для ответа
ROASTS = [
    "Пиздец, ты чё, из морга сбежал?",
    "Блять, это как так жить умудрился?",
    "Похер, твой текст — пиздец!"
]

# Слова, на которые бот реагирует
TRIGGER_WORDS = ["привет", "похер", "бля"]

# Команда /start
async def start(update, context):
    await update.message.reply_text(f"Бот с матом! Пиши слова ({', '.join(TRIGGER_WORDS)}) или @YourBotName")

# Реакция на слова или упоминания в группах
async def roast(update, context):
    if update.message.chat.type in ["group", "supergroup"]:
        text = update.message.text.lower()
        if any(word in text for word in TRIGGER_WORDS) or f"@{context.bot.username}".lower() in text:
            await update.message.reply_text(random.choice(ROASTS))

# Приветствие новичков
async def welcome(update, context):
    for member in update.chat_member.new_chat_members:
        await update.message.reply_text(f"Здаров, {member.first_name}! С кладбища сбежал?")

# Запуск бота
def main():
    # Создаём бота
    app = Application.builder().token(TOKEN).build().
    # Добавляем команды
    app.add_handler(CommandHandler("start", start))  # Для /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roast))  # Для слов и упоминаний
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))  # Для новичков
    
    # Запускаем бота
    app.run_polling()

# Старт программы
if __name__ == "__main__":
    main()
