# Импортируем нужные модули
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters
import random, os

# Читаем токен из переменной окружения (настраивается в Render)
TOKEN = os.getenv("TOKEN")  # Пример: читает токен, например, "1234567890:NEW_TOKEN_HERE" из Render

# Слова, на которые бот реагирует
TRIGGER_WORDS = [
    "Привет", "Да", "Бля", "Хуй", "Похуй",
    "Первый", "Циркулярная", "Хахаха", "Хпхпхп",
    "Матроскин", "Туплю", "Приказ", "Командир", "Постираться",
    "Хуйня", "Похуй", "Каракоба", "Ваня", "Игла2", "Старшина", "Дембель",
    "Виноват", "Баня", "Власов сказал", "БПлА"
]

# Специфические ответы на слова
SPECIFIC_RESPONSES = {
"Да": "Пизда",
"Первый": "Пидорас",
"Привет": "Здарова, заебал! ~(˘▾˘~)",
"Циркулярная": "О, пиздец ヽ(∀° )人( °∀)ノ",
"Хахаха": "Не смешно (╯°□°)╯",
"Хпхпхп": "Дохуя смешно тебе (o_O)?",
"Матроскин": "Ты тоже такой медленный)?",
"Туплю": "Ты чё ебало в блиндаже топил, когда мозги всем раздавали?",
"Приказ": "Приказ на бумаге",
"Командир": "Слюнявого не называй, толчок наш больше командир чем он)",
"Постираться": "Ага, размечтался, в вонючем ходи",
"Хуйня": "Хуйня в строевой или, за белой дверью в роте, а это не хуйня",
"Похуй": "3 дня до дома будет, будет похуй, а сейчас ебошка",
"Каракоба": "Долина в Крыму в окрестностях Севастополя, вливается в Инкерманскую с востока у пос. Сахарная головка. Пространственно сопряжена с одноименной 280 м горой",
"Ваня": "Его пердеж настолько громкий, что ИГЛА-2 путает его с детонацией ᕦ(ò_óˇ)ᕤ",
"Игла2": "Медведь и стая пидорасов",
"Старшина": "Начало мне уже не нравится!",
"Морсков": "После многих и многих научных исследований,учеными было решено, что это самый медленный человек не то что в России, даже не в мире, в целом, нет существ более медленных чем он",
"Дембель": "Не существует его",
"Виноват": "Виноват военкомат, что призвал тебя",
"Баня": "Не называй горячий душ баней, это же просто горячая вода",
"Власов сказал": "Ебать, боец , ты чё приказы из жопы выдумал?",
"БПлА": "Беспилотный летательный аппарат, если что!)"
    
}

# Команда /start
async def start(update, context):
    await update.message.reply_text(
        f"Привет! Добавь меня в группу, будет весело! и упомяни @{context.bot.username}"
    )

# Команда /who (Кто сегодня пиздализ?)
async def who(update, context):
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Эта команда работает только в группах!")
        return

    # Проверяем, была ли команда уже вызвана в этой группе
    if context.chat_data.get("pizdaliz_called"):
        await update.message.reply_text("я же блять сказал, кто сегодня пиздализ :)")
        return

    try:
        # Получаем список участников группы
        members = await context.bot.get_chat_members(update.effective_chat.id)
        # Фильтруем только пользователей (не ботов)
        users = [member.user for member in members if not member.user.is_bot]
        
        if len(users) < 2:
            await update.message.reply_text("В группе слишком мало людей, чтобы выбрать пиздализов!")
            return

        # Выбираем двух случайных участников
        pizdalizs = random.sample(users, 2)
        pizdaliz1 = pizdalizs[0]
        pizdaliz2 = pizdalizs[1]

        # Формируем ссылки на пользователей
        pizdaliz1_link = f"@{pizdaliz1.username}" if pizdaliz1.username else pizdaliz1.first_name
        pizdaliz2_link = f"@{pizdaliz2.username}" if pizdaliz2.username else pizdaliz2.first_name

        # Отправляем ответ
        await update.message.reply_text(
            f"Сегодня пиздализы: {pizdaliz1_link} и {pizdaliz2_link}!"
        )

        # Помечаем, что команда была вызвана
        context.chat_data["pizdaliz_called"] = True

    except Exception as e:
        await update.message.reply_text(f"Ошибка, блять: {str(e)}")

# Реакция на слова или упоминания в группах
async def roast(update, context):
    if update.message.chat.type in ["group", "supergroup"]:
        text = update.message.text.lower()
        # Проверяем, есть ли триггерное слово или упоминание бота
        for word in TRIGGER_WORDS:
            if word in text:
                # Если есть специфический ответ, используем его
                response = SPECIFIC_RESPONSES.get(word, random.choice(ROASTS))
                await update.message.reply_text(response)
                return
        if f"@{context.bot.username}".lower() in text:
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
                f"Добро пожаловать, пидор, в наш гей-клуб, {new_member.user.first_name}!"
            )
        # Проверяем, покинул ли пользователь группу
        elif old_member.status in ["member", "administrator", "creator"] and new_member.status == "left":
            await update.effective_chat.send_message(
                f"Пошёл нахуй, ебанный натурал, {old_member.user.first_name}!"
            )

# Запуск бота
def main():
    # Создаём бота с токеном
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем команды
    app.add_handler(CommandHandler("start", start))  # Для /start
    app.add_handler(CommandHandler("who", who))  # Для /who
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roast))  # Для слов и упоминаний
    app.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))  # Для новичков и ухода
    
    # Запускаем бота
    app.run_polling()

# Старт программы
if __name__ == "__main__":
    main()
