# Импортируем нужные модули
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters
import random, os

# Читаем токен из переменной окружения (настраивается в Render)
TOKEN = os.getenv("TOKEN")  # Пример: читает токен, например, "1234567890:NEW_TOKEN_HERE" из Render

# Матерные фразы для ответа
ROASTS = [
    "Блять, ты чё, внатуре охуел?",
    "Похер, твой текст — полная хуйня!",
    "Ебать, это что за пиздец ты написал?",
    "Сука, да ты заебал уже!",
    "Похуй, твой месседж — говно!",
    "Чё за херня, бери и вали нахуй!",
    "Пиздец, ты реально ебанулся?",
    "Блять, это ж надо так обосраться!",
    "Хули ты трындишь, дебил?",
    "Ебаный в рот, завали ебало!"
]

# Слова, на которые бот реагирует
TRIGGER_WORDS = [
    "привет", "похер", "бля", "хуй", "пиздец",
    "ебать", "сука", "охуеть", "ебаный", "нахуй",
    "хули", "ебало", "говно", "похуй", "заебал"
]

# Команда /start
async def start(update, context):
    await update.message.reply_text(f"Привет! Добавь меня в группу, будет весело! и упомяни @{context.bot.username}")
# Реакция на слова или упоминания в группах
async def roast(update, context):
    if update.message.chat.type in ["group", "supergroup"]:
        text = update.message.text.lower()
        if any(word in text for word in TRIGGER_WORDS) or f"@{context.bot.username}".lower() in text:
            await update.message.reply_text(random.choice(ROASTS))

# Приветствие новичков и реакция на выход из группы
async def handle_chat_member(update, context):
    status = update.chat_member.difference().get("status")
    new_member = update.chat_member.new_chat_member
    old_member = update.chat_member.old_chat_member

    if status == "status":
        # Проверяем, стал ли пользователь участником (member) или администратором
        if new_member.status in ["member", "administrator", "creator"]:
            await update.effective_chat.send_message(
                f"Добро пожаловать пидор в наш гей-клуб, {new_member.user.first_name}!"
            )
        # Проверяем, покинул ли пользователь группу
        elif old_member.status in ["member", "administrator", "creator"] and new_member.status == "left":
            await update.effective_chat.send_message(
                f"Пошёл нахуй, ебанный натурал, {old_member.user.first_name}!"
            )

# Запуск бота
def main():
    # Создаём бота с токеном
    app = Application.builder().token(TOKEN).build()  # Использует токен из переменной TOKEN
    
    # Добавляем команды
    app.add_handler(CommandHandler("start", start))  # Для /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roast))  # Для слов и упоминаний
    app.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))  # Для новичков и ухода
    
    # Запускаем бота
    app.run_polling()

# Старт программы
if __name__ == "__main__":
    main()
